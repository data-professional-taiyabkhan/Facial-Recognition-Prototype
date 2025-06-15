import base64
import sqlite3
from io import BytesIO
from datetime import datetime

from flask import Flask, request, jsonify
import face_recognition
import numpy as np
from PIL import Image

DB_PATH = "attendance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    # create tables…
    conn.commit()
    conn.close()

app = Flask(__name__)
init_db()   # ← ensure DB exists before any requests

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    image_b64 = data.get("image")
    name = data.get("name", "")
    if not image_b64:
        return jsonify(status="error", message="No image provided"), 400

    img_data = base64.b64decode(image_b64)
    img = np.array(Image.open(BytesIO(img_data)))
    locations = face_recognition.face_locations(img)
    if len(locations) != 1:
        return jsonify(status="error",
                       message=f"Expected 1 face, found {len(locations)}"), 400

    encoding = face_recognition.face_encodings(img, locations)[0]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
      "INSERT INTO users (name, encoding) VALUES (?, ?)",
      (name, encoding.tobytes())
    )
    conn.commit()
    conn.close()
    return jsonify(status="ok", message="User registered")

@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    image_b64 = data.get("image")
    if not image_b64:
        return jsonify(status="error", message="No image provided"), 400

    img_data = base64.b64decode(image_b64)
    img = np.array(Image.open(BytesIO(img_data)))
    locations = face_recognition.face_locations(img)
    if len(locations) != 1:
        return jsonify(status="error",
                       message=f"Expected 1 face, found {len(locations)}"), 400

    encoding = face_recognition.face_encodings(img, locations)[0]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, encoding FROM users")
    users = c.fetchall()
    conn.close()

    for user_id, enc_blob in users:
        known = np.frombuffer(enc_blob, dtype=np.float64)
        if face_recognition.compare_faces([known], encoding)[0]:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
              "INSERT INTO attendance (user_id, timestamp) VALUES (?, ?)",
              (user_id, datetime.utcnow().isoformat())
            )
            conn.commit()
            conn.close()
            return jsonify(status="ok", message="Present", user_id=user_id)

    return jsonify(status="ok", message="Unknown user")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
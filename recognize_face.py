import face_recognition
import cv2
import pickle

# Load known face encoding
with open("my_face.pkl", "rb") as f:
    known_face_encoding = pickle.load(f)

video_capture = cv2.VideoCapture(0)
print("Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to read from webcam.")
        break

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)

    # Safely compute face encodings
    face_encodings = []
    for face_location in face_locations:
        try:
            encodings = face_recognition.face_encodings(rgb_frame, [face_location])
            if encodings:
                face_encodings.append(encodings[0])
        except Exception as e:
            print("⚠️ Encoding error:", e)

    # Compare and display
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
        name = "Unknown"
        if matches[0]:
            name = "YOU ✅"

        # Draw box and label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('Recognize Face', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
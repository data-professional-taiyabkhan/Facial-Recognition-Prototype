import face_recognition
import cv2
import pickle

video_capture = cv2.VideoCapture(0)
print("Press 's' to save your face or 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    cv2.imshow('Register Face', frame)
    key = cv2.waitKey(1)

    if key & 0xFF == ord('s'):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        print("Captured frame for face recognition.")

        ret, frame = video_capture.read()
        if not ret or frame is None:
            print("Failed to capture image from webcam.")
            continue

        # Convert BGR (OpenCV default) to RGB for face_recognition
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print("Error converting frame to RGB:", e)
            continue

        # Ensure it's 8-bit
        if rgb_frame.dtype != 'uint8':
            print("Image is not 8-bit. Found dtype:", rgb_frame.dtype)
            continue

        face_locations = face_recognition.face_locations(rgb_frame)

        
        print("Frame shape:", rgb_frame.shape, "Dtype:", rgb_frame.dtype)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            with open("my_face.pkl", "wb") as f:
                pickle.dump(face_encodings[0], f)
            print("Face saved.")
        else:
            print("No face detected.")
        break
    elif key & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
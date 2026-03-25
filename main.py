import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions, RunningMode
from mediapipe.tasks.python.core import base_options as base_options_module
import pygame
import os

# --- 1. FINDING THE MUSIC ---
folder_path = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(folder_path, "rock.mp3")
pygame.mixer.init()
try:
    pygame.mixer.music.load(audio_file)
    print("✅ Music loaded! Ready to rock.")
except:
    print(f"❌ Error: Put 'rock.mp3' in this folder: {folder_path}")

# --- 2. SETUP NEW MEDIAPIPE API ---
model_path = os.path.join(folder_path, "face_landmarker.task")
options = FaceLandmarkerOptions(
    base_options=base_options_module.BaseOptions(model_asset_path=model_path),
    running_mode=RunningMode.IMAGE,
    num_faces=1
)
face_landmarker = FaceLandmarker.create_from_options(options)

# --- 3. STARTING THE CAMERA ---
cap = cv2.VideoCapture(0)
playing = False
print("System Active! Press 'q' to quit.")

# --- 4. THE LOOP ---
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    results = face_landmarker.detect(mp_image)

    if results.face_landmarks:
        face = results.face_landmarks[0]
        nose_y = face[1].y  # Nose tip landmark

        threshold = 0.6
        if nose_y > threshold:
            if not playing:
                pygame.mixer.music.play(-1)
                playing = True
            cv2.putText(frame, "STATUS: ROCKING OUT", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if playing:
                pygame.mixer.music.pause()
                playing = False
            cv2.putText(frame, "STATUS: Looking up...", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(frame, f"Nose Level: {round(nose_y, 2)}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    cv2.imshow('RockLook Project', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
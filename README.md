# RockLook 🤘

## What it does
Detects when you look down via webcam and plays rock music. Looking up pauses it.

## Tech Stack
- OpenCV — webcam feed
- MediaPipe FaceLandmarker — face/nose tracking
- pygame mixer — audio playback

## How it works
Uses MediaPipe to track nose tip position (landmark #1). 
When nose_y > 0.6 (looking down), music plays. Looking up pauses it.
Threshold value is displayed live on screen.

## How to run
1. Install dependencies: `pip install mediapipe opencv-python pygame`
2. Download `face_landmarker.task` model into the project folder
3. Add a `rock.mp3` file to the project folder
4. Run: `python main.py`

## Hardware concept learned
Sensor (webcam) → threshold (nose_y > 0.6) → actuator (music on/off)
This mirrors a tilt sensor triggering a relay.

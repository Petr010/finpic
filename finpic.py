import cv2
import mediapipe as mp


# Function to check if peace sign gesture is detected
def is_peace_sign(landmarks):
    # Logic to determine if the gesture resembles a peace sign
    # For example, you might check the positions of specific landmarks
    
    # Example: Check if index and middle finger tips are raised while other fingers are closed
    if (
        landmarks[8][1] < landmarks[6][1] and
        landmarks[12][1] < landmarks[10][1] and
        landmarks[16][1] > landmarks[14][1] and
        landmarks[20][1] > landmarks[18][1]
    ):
        return True
    else:
        return False


# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize webcam
external_cam_index = 2  # Change this index accordingly

# Open the webcam (default webcam, can be changed if multiple webcams are connected)
cap = cv2.VideoCapture(external_cam_index, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_SETTINGS, 1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame with MediaPipe
    results = hands.process(frame_rgb)
    
    # Check if hand(s) detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Calculate landmark positions
            landmarks = []
            for landmark in hand_landmarks.landmark:
                x, y, _ = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]), int(landmark.z * frame.shape[1])
                landmarks.append((x, y))
            
            # Check for peace sign gesture
            if is_peace_sign(landmarks):
                # Save a screenshot
                screenshot_filename = "peace_sign_screenshot.jpg"
                cv2.imwrite(screenshot_filename, frame)
                cv2.putText(frame, 'Peace Sign Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display frame
    cv2.imshow('Hand Gestures', frame)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


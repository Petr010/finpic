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

def collage(overlay_image):
    blank_image = cv2.imread("finpic.jpg")
    overlay_image_resized =  cv2.imread(overlay_image)
    # Define the position where you want to overlay the resized image on the blank image
    # Let's place it in the top-left corner for this example
    x_offset = random.randint(0, 1000)  # x-coordinate of the top-left corner of the overlay image on the blank image
    y_offset = random.randint(0, 3000)  # y-coordinate of the top-left corner of the overlay image on the blank image
    # Overlay the resized image onto the blank image
    blank_image[y_offset:y_offset+overlay_image_resized.shape[0], 
                x_offset:x_offset+overlay_image_resized.shape[1]] = overlay_image_resized

    # Save the resulting image
    cv2.imwrite("finpic.jpg", blank_image)

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize webcam
external_cam_index = 2  # Change this index accordingly

# Open the webcam (default webcam, can be changed if multiple webcams are connected)
cap = cv2.VideoCapture(external_cam_index, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_SETTINGS, 1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

# Flag to indicate if a frame has been captured after detecting the gesture
frame_captured = False

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
                # Capture frame if not already captured
                if not frame_captured:
                    # Save a screenshot
                    screenshot_filename = "peace_sign_screenshot.jpg"
                    cv2.imwrite(screenshot_filename, frame)
                    frame_captured = True
                    # Uncomment the following line if you want to exit the loop after capturing the frame
                    # break
    
    # Display frame
    cv2.imshow('Hand Gestures', frame)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
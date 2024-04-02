import time
import random
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
    blank_image = cv2.imread("finpic.jpg") # og canvas 4000 x 2250
    y_bi, x_bi, channels = blank_image.shape
    overlay_image_in =  cv2.imread(overlay_image)
    y_oi, x_oi, channels = overlay_image_in.shape
    # Define the position where you want to overlay the resized image on the blank image
    # Let's place it in the top-left corner for this example
    x_offset = random.randint(0, x_bi-1-x_oi)  # x-coordinate of the top-left corner of the overlay image on the blank image
    y_offset = random.randint(0, y_bi-1-y_oi)  # y-coordinate of the top-left corner of the overlay image on the blank image 
    # Overlay the resized image onto the blank image
    print(x_offset, y_offset)
    blank_image[y_offset:y_offset+overlay_image_in.shape[0], 
                x_offset:x_offset+overlay_image_in.shape[1]] = overlay_image_in

    # Save the resulting image
    cv2.imwrite("finpic.jpg", blank_image)
    displayable = cv2.imread("finpic.jpg")
    # Create a window with adjustable size
    cv2.namedWindow('finpic', cv2.WINDOW_NORMAL)
    # Display the image
    cv2.imshow('finpic', displayable)

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize webcam
external_cam_index = 2  # Change this index accordingly

# Open the webcam (default webcam, can be changed if multiple webcams are connected)
cap = cv2.VideoCapture(external_cam_index, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_SETTINGS, 1)

x_pix = 500
y_pix = 285

cap.set(cv2.CAP_PROP_FRAME_WIDTH, x_pix)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y_pix)

# initialies first pic
first_time = 1
# Set the rotation angle for vertical orientation
rotation_angle = -90

while cap.isOpened():
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break
    
    if rotation_angle == -90:
        # rotated
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        temp = x_pix
        x_pix = y_pix
        y_pix = temp

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
                # cv2.putText(frame, 'Peace Sign Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if first_time == 1:
                    collage(screenshot_filename)
                    first_time = 0
            else: first_time = 1
    
    # Display frame
    cv2.imshow('Hand Gestures', frame)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


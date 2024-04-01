import cv2

# Open the webcam (default webcam, can be changed if multiple webcams are connected)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Couldn't open the webcam")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is not read correctly, exit the loop
    if not ret:
        print("Error: Can't receive frame from the webcam")
        break

    # Perform your analysis here
    # Example: Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('Original', frame)
    cv2.imshow('Grayscale', gray_frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
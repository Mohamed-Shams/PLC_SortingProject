import cv2
import numpy as np
from opcua import Client
import sys

# Replace with OPC UA server URL
url = "opc.tcp://Shams:53530/OPCUA/SimulationServer"
try:
    client = Client(url)
    client.connect()
    print("Connected to OPC UA")
except Exception as err:
    print("err", err)
    sys.exit(1)

# Initialize the camera capture object
# 0 represents the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, input_img = cap.read()

    # Check if the frame was successfully read
    if not ret:
        print("Failed to capture frame.")
        break

    # Resize the frame
    img = cv2.resize(input_img, (640, 480))
    # Make a copy to draw contour outline
    input_image_cpy = img.copy()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of red color in HSV
    # lower_red = np.array([0, 50, 50])
    # upper_red = np.array([10, 255, 255])

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([7, 255, 255])

    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # define range of green color in HSV
    lower_green = np.array([40, 20, 50])
    upper_green = np.array([90, 255, 255])

    # create a mask for red color
    # mask_red = cv2.inRange(hsv, lower_red, upper_red)

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine masks for red (due to the range being split)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # create a mask for green color
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # find contours in the red mask
    contours_red, _ = cv2.findContours(
        mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find contours in the green mask
    contours_green, _ = cv2.findContours(
        mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    color = "Undefined"  # Initialize with "Undefined"

    # loop through the red contours and draw a rectangle around them
    for cnt in contours_red:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, 'Red', (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            color = "Red"  # Set the color to "Red" if red is detected

    # loop through the green contours and draw a rectangle around them
    for cnt in contours_green:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, 'Green', (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            color = "Green"  # Set the color to "Green" if green is detected

    print(color)  # Print the detected color
    # Display final output for multiple color detection opencv python
    cv2.imshow('image', img)

    if __name__ == '__main__':
        # To be changed With prosys(OPC UA) Variable
        new_node = client.get_node("ns=3;s=1009")
        client.set_values([new_node], [color])

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

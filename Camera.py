# Import opencv for computer vision stuff
import cv2
# Import matplotlib so we can visualize an image
from matplotlib import pyplot as plt
cam = 2
# Connect to capture device
cap = cv2.VideoCapture(cam)

# Get a frame from the capture device
ret, frame = cap.read()

print(ret)

print(frame)

plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.show()

# Releases capture back into the wild 
cap.release()

def take_photo(): 
    cap = cv2.VideoCapture(cam)
    ret, frame = cap.read(cam)
    cv2.imwrite('webcamphoto.jpg', frame)
    cap.release()


    
    
take_photo()
# Connect to webcam
cap = cv2.VideoCapture(cam)
# Loop through every frame until we close our webcam
while cap.isOpened(): 
    ret, frame = cap.read()
    
    # Show image 
    cv2.imshow('Webcam', frame)
    
    # Checks whether q has been hit and stops the loop
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# Releases the webcam
cap.release()
# Closes the frame
cv2.destroyAllWindows()
import cv2  # Import the OpenCV library for image processing
from picamera2 import Picamera2  # Library for accessing the Raspberry Pi Camera
import numpy as np  # Library for mathematical calculations
from IPython.display import display, Image  # Library for displaying images in Jupyter Notebook
import ipywidgets as widgets  # Library for creating interactive widgets like buttons
import threading  # Library for creating new threads to execute tasks asynchronously

# Load the Haar cascade classifier for face detection
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create a "Stop" button for users to stop the video stream by clicking on it
# ================
stopButton = widgets.ToggleButton(
    value=False,
    description='Stop',
    disabled=False,
    button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='square' # (FontAwesome names without the `fa-` prefix)
)


# Define a display function to process video frames and perform face detection
# ================
def view(button):
    # If you are using a CSI camera, uncomment the picam2 related code below, 
    # and comment out the camera related code.
    # This is because the latest version of OpenCV (4.9.0.80) no longer supports CSI cameras, 
    # and you need to use picamera2 to capture camera images.
    
    # picam2 = Picamera2()  # Create an instance of Picamera2
    # picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))  # Configure camera parameters
    # picam2.start()  # Start the camera

    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW) 
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    display_handle=display(None, display_id=True)  # Create a display handle to update the displayed image
    i = 0
    
    avg = None
    
    while True:
        # frame = picam2.capture_array()
        _, frame = camera.read()
        # frame = cv2.flip(frame, 1) # if your camera reverses your image

        img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert the image from RGB to BGR because OpenCV defaults to BGR
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale because face detection is typically performed on grayscale images

        # Perform face detection using the cascade classifier
        faces = faceCascade.detectMultiScale(
                gray,     
                scaleFactor=1.2,
                minNeighbors=5,     
                minSize=(20, 20)
            )

        if len(faces):
            for (x,y,w,h) in faces: # Loop through all detected faces
                cv2.rectangle(frame,(x,y),(x+w,y+h),(64,128,255),1) # Draw a rectangle around the detected face
        
        _, frame = cv2.imencode('.jpeg', frame) # Encode the frame as JPEG format
        display_handle.update(Image(data=frame.tobytes()))
        if stopButton.value==True:
            # picam2.close()
            cv2.release() # If yes, close the camera
            display_handle.update(None)

            
# Display the "Stop" button and start a thread to execute the display function
# ================
display(stopButton)
thread = threading.Thread(target=view, args=(stopButton,))
thread.start()
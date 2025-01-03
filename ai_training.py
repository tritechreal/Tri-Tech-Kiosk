import tflite_runtime.interpreter as tflite
import cv2
import numpy as np

# Load the TensorFlow Lite model
interpreter = tflite.Interpreter(model_path='path/to/your/model.tflite')
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Initialize the Raspberry Pi AI camera
camera = cv2.VideoCapture(0)

# Capture an image
ret, frame = camera.read()

# Pre-process the image
input_data = cv2.resize(frame, (input_details[0]['shape'][1], input_details[0]['shape'][2]))
input_data = np.expand_dims(input_data, axis=0)
input_data = input_data.astype(np.float32)

# Run inference
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

# Get the output
output_data = interpreter.get_tensor(output_details[0]['index'])

# Calculate the bounding box area for each detected fish
for i in range(len(output_data[0])):
    if output_data[0][i][0] > 0.5:  # Adjust the threshold as needed
        ymin = int(output_data[0][i][1] * frame.shape[0])
        xmin = int(output_data[0][i][2] * frame.shape[1])
        ymax = int(output_data[0][i][3] * frame.shape[0])
        xmax = int(output_data[0][i][4] * frame.shape[1])
        area = (ymax - ymin) * (xmax - xmin)
        print(f"Fish {i+1} bounding box area: {area} pixels")

# Release the camera
camera.release()
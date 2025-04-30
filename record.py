#!/usr/bin/python3

# Capture a PNG image while still running in the preview mode.
# The image release is activated with the button 'p' and with 'q' the script is stopped.

from sys import stdin
from termios import TCIOFLUSH, tcflush
from time import strftime
import time
from keyboard import is_pressed

from picamera2 import Picamera2, Preview
cam = Picamera2()

cam.start
cam.start_preview(Preview.QTGL)
cam.start()


for i in range(200,401):
    num = str(i)
    time.sleep(0.2)
    filename = "data/" + num + "fish" + '.png'
    cam.capture_file(filename, format="png", wait=None)
    print(f"\rCaptured {filename} succesfully")
    



cam.stop_preview()
cam.stop()
cam.close()
tcflush(stdin, TCIOFLUSH)
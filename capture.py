#!/usr/bin/env python
import time
import picamera
import cStringIO
import os
import atexit
from flask import Flask, send_file

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
camera = picamera.PiCamera()
camera.rotation=270
camera.resolution=(2000,2000)

@app.route("/camera/frame.jpg")
def get_frame():
    image = capture_frame()
    image.seek(0)
    return send_file(image, mimetype='image/jpeg')

def capture_frame():
    print "Capture starting..."
    image =  cStringIO.StringIO()
    camera.capture(image, format='jpeg', quality=10)
    image.seek(0, os.SEEK_END)
    print "Capture complete. image is %lu bytes" % image.tell()
    return image

    camera.close()
def cleanup():
    print "cleaned up"

atexit.register(cleanup)

if __name__ == '__main__':
    app.run()


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
camera.resolution=(2592,1944)

@app.route("/camera/frame.jpg")
def get_frame():
    image = capture_frame()
    image.seek(0)
    return send_file(image, mimetype='image/jpeg')

def capture_frame():
    start = time.time()
    image =  cStringIO.StringIO()
    camera.capture(image, format='jpeg', quality=100)
    elapsed = time.time() - start
    image.seek(0, os.SEEK_END)
    print "Capture complete. image is %lu bytes (%0.3f s)" % (image.tell(), elapsed)
    return image

def cleanup():
    camera.close()
    print "cleaned up"

atexit.register(cleanup)

if __name__ == '__main__':
    app.run()


#!/usr/bin/env python
import time
import picamera
import cStringIO
import os
import atexit
from flask import Flask, send_file, request, redirect, url_for

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
camera = picamera.PiCamera()
camera.rotation=270
camera.resolution=(2592,1944)
camera.exposure_mode = 'night'
camera.brightness = 55
camera_format = 'jpeg'
camera_quality = 100
camera_use_video_port = False

@app.route("/camera/frame.jpg")
def get_frame():
    apply_camera_settings(request)
    image = capture_frame()
    image.seek(0)
    return send_file(image, mimetype='image/jpeg')

def capture_frame():
    start = time.time()
    image =  cStringIO.StringIO()
    camera.capture(image, use_video_port = camera_use_video_port, format = camera_format, quality = camera_quality)
    elapsed = time.time() - start
    image.seek(0, os.SEEK_END)
    print "Capture complete. image is %lu bytes (%0.3f s)" % (image.tell(), elapsed)
    return image

def apply_camera_settings(request):
    for key in request.args.keys():
        print "Applying setting ", key, ": ", request.args[key]

def safe_int(val, default):
    try:
        return int(val)
    except ValueError:
        return default

def safe_bool(val):
    return val == "True" or val == 1

def rotation(val):
    pass

def quality(val):
    pass

def format(val):
    pass

def use_video_port(val):
    pass

def exposure_mode(val):
    pass

def awb_mode(val):
    pass

def brightness(val):
    pass

def color_effects(val):
    pass

def contrast(val):
    pass

def crop(val):
    pass

def drc_strength(val):
    pass

def exposure_compensation(val):
    pass

def image_effect(val):
    pass

def led(val):
    pass

def meter_mode(val):
    pass

def resolution(val):
    pass

def saturation(val):
    pass

def sharpness(val):
    pass

def shutter_speed(val):
    pass

def cleanup():
    camera.close()
    print "cleaned up"

atexit.register(cleanup)

if __name__ == '__main__':
    app.run()


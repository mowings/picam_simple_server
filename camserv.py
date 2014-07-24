#!/usr/bin/env python
import time
import picamera
import cStringIO
import os
import atexit
from flask import Flask, send_file, request, redirect, url_for
from ast import literal_eval

ALLOWED_OPERATIONS = "rotation resolution exposure_mode awb_mode brightness format quality use_video_port color_effects contrast crop drc_strength exposure_compensation image_effect led meter_mode saturation sharpness shutter_speed hflip vflip".split()
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
    operations = [op for op in request.args.keys() if op in ALLOWED_OPERATIONS]
    for op in operations:
        print "Applying setting ", op, ": ", request.args[op]
        globals()[op](request.args[op])

def safe_int(val, default):
    try:
        return int(val)
    except ValueError:
        return default

def safe_bool(val):
    return val == "True" or val == "1"

def rotation(val):
    global camera
    camera.rotation = safe_int(val,0)

def quality(val):
    global camera_quality
    camera_quality = safe_int(val, 100)

def format(val):
    global camera_format
    camera_format = val

def use_video_port(val):
    global camera_use_video_port
    print safe_bool(val)
    camera_use_video_port  = safe_bool(val)

def exposure_mode(val):
    global camera
    camera.exposure_mode = val

def awb_mode(val):
    global camera
    camera.awb_mode = val

def brightness(val):
    global camera
    camera.brightness = safe_int(val, 50)

def color_effects(val):
    global camera
    camera.color_effects = literal_eval(val)

def contrast(val):
    global camera
    camera.contrast = safe_int(val,0)

def crop(val):
    global camera
    camera.crop = literal_eval(val)

def drc_strength(val):
    global camera
    camera.drc_strength = val

def exposure_compensation(val):
    global camera
    camera.exposure_compensation = safe_int(val,0)

def image_effect(val):
    global camera
    camera.image_effect = val

def led(val):
    global camera
    camera.led = safe_bool(val)

def vflip(val):
    global camera
    camera.vflip = safe_bool(val)

def hflip(val):
    global camera
    camera.hflip= safe_bool(val)

def meter_mode(val):
    global camera
    camera.meter_mode = val

def resolution(val):
    global camera
    camera.resolution = literal_eval(val)

def saturation(val):
    global camera
    camera.saturation = safe_int(val, 0)

def sharpness(val):
    global camera
    camera.sharpness = safe_int(val, 0)

def shutter_speed(val):
    global camera
    camera.shutter_speed = safe_int(val,0)

def cleanup():
    camera.close()
    print "cleaned up"

atexit.register(cleanup)

if __name__ == '__main__':
    app.run()


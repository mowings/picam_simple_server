#!/usr/bin/env python
import time
import picamera
import cStringIO
import os
import atexit
from flask import Flask, send_file, request, redirect, url_for
from ast import literal_eval

class Webcam:
    ALLOWED_OPERATIONS = "rotation resolution exposure_mode awb_mode brightness format quality use_video_port color_effects contrast crop drc_strength exposure_compensation image_effect led meter_mode saturation sharpness shutter_speed hflip vflip reset".split()

    def __init__(self):
        self.camera = None

    def reset(self, val=None):
        if self.camera: self.camera.close()
        self.camera = picamera.PiCamera()
        self.camera.resolution=(2592,1944)
        self._format = 'jpeg'
        self._quality = 100
        self._use_video_port = False

    def close(self):
        self.camera.close()

    def capture_frame(self):
        start = time.time()
        image =  cStringIO.StringIO()
        self.camera.capture(image, use_video_port = self._use_video_port, format = self._format, quality = self._quality)
        elapsed = time.time() - start
        image.seek(0, os.SEEK_END)
        print "Capture complete. image is %lu bytes (%0.3f s)" % (image.tell(), elapsed)
        return image

    def safe_int(self, val, default):
        try:
            return int(val)
        except ValueError:
            return default

    def safe_bool(self, val):
        return val in ["True", "true", "1", "t", "y", "yes"]

    def rotation(self, val):
        self.camera.rotation = self.safe_int(val,0)

    def quality(self, val):
        self._quality = self.safe_int(val, 100)

    def format(self, val):
        self._format = val

    def use_video_port(self, val):
        self._use_video_port  = self.safe_bool(val)

    def exposure_mode(self, val):
        self.camera.exposure_mode = val

    def awb_mode(self, val):
        self.camera.awb_mode = val

    def brightness(self, val):
        self.camera.brightness = self.safe_int(val, 50)

    def color_effects(self, val):
        self.camera.color_effects = literal_eval(val)

    def contrast(self, val):
        self.camera.contrast = self.safe_int(val,0)

    def crop(self, val):
        self.camera.crop = literal_eval(val)

    def drc_strength(self, val):
        self.camera.drc_strength = val

    def exposure_compensation(self, val):
        self.camera.exposure_compensation = self.safe_int(val,0)

    def image_effect(self, val):
        self.camera.image_effect = val

    def led(self, val):
        self.camera.led = self.safe_bool(val)

    def vflip(self, val):
        self.camera.vflip = self.safe_bool(val)

    def hflip(self, val):
        self.camera.hflip= self.safe_bool(val)

    def meter_mode(self, val):
        self.camera.meter_mode = val

    def resolution(self, val):
        self.camera.resolution = literal_eval(val)

    def saturation(self, val):
        self.camera.saturation = self.safe_int(val, 0)

    def sharpness(self, val):
        self.camera.sharpness = self.safe_int(val, 0)

    def shutter_speed(self, val):
        self.camera.shutter_speed = self.safe_int(val,0)

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
webcam = Webcam()
webcam.reset()

@app.route("/camera/frame.jpg")
def get_frame():
    apply_camera_settings(request)
    image = webcam.capture_frame()
    image.seek(0)
    return send_file(image, mimetype='image/jpeg')

def apply_camera_settings(request):
    operations = [op for op in request.args.keys() if op in Webcam.ALLOWED_OPERATIONS]
    for op in operations:
        print "Applying setting ", op, ": ", request.args[op]
        getattr(webcam, op)(request.args[op])

def cleanup():
    webcam.close()
    print "cleaned up"

atexit.register(cleanup)

if __name__ == '__main__':
    app.run()


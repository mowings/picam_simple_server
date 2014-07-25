Raspberry Pi Camera Simple HTTP Server
===

A couple of demos showing how to pull stills from the pi cam and serve them on a web page, useful if you want to play with the camera, but don't have (or want to use) a monitor. 

Image data is pulled into memory to save wear on the flash. 

camserv.py allows you to play with most camera settings when you snap a picture.

### capture.py

This simple demo uses Flask and the PiCam python API to create a simple on-demand jpeg capture over http. This is
just a demo -- if you need to change any parameters, just change them in the code. Note that I have rotation set to 270; this is just to fit my particular use case. You may wish to remove that setting (unless you need it).

The picam capture is captured into a stringio object whenever we see a GET request to `/camera/frame.jpg`. We then return the contents of the stringio object to the user as a jpeg. This eats some memory, but saves us from writing the SD card.

To run this, you'll need to have the [picam python package](http://picamera.readthedocs.org/en/release-1.5/) installed, as well as [Flask](http://flask.pocoo.org/docs). 

Flask can be installed via pip (`sudo pip install flask`). If you do not have pip installed, install it first (http://pip.readthedocs.org/en/latest/installing.html).

To run the server:

    sudo ./capture.py
    
To fetch a frame, simply point your browser to `http://<hostname>:5000/camera/frame.jpg` 
    
If you want the server to run as a managed service, you can easily create a [simple upstart job](http://stackful-dev.com/what-every-developer-needs-to-know-about-ubuntu-upstart.html).

### camserv.py
camserve is installed and run exactly like capture.py, but you can add parameters to the URL to change the camera settings prior to taking a picture. Most settings from the API are supported. You can also change the image format and quality, as well as switch to and from the video port for capturing. Note that only the most minimal parameter checking is done. The main purpose of camserv is to allow you to play with the picam settings without needing a monitor.

To run the server:

    sudo ./capture.py
    
To fetch a frame, simply point your browser to `http://<hostname>:5000/camera/frame.jpg` and add the settings ypu'd like to change. Some examples:

    http://<hostname>:5000/camera/frame.jpg?resolution=(1900,1900)&exposure_compensation=-5&awb_mode=cloudy&led=0
    http://<hostname>:5000/camera/frame.jpg?quality=10&image_effect=emboss
    http://<hostname>:5000/camera/frame.jpg?resolution=(1900,1080)&use_video_port=1
    # etc...
    
Pass `reset=1` if you want to set the camera beck to the default settings:

    http://<hostname>:5000/camera/frame.jpg?reset=1
    
Note that you can change the output format (`format=png|bmp|gif|...`), but you still fetch the image at the same .jpg url, and the mime type returned by the server is still `image/jpeg`. This wont be an issue for most browsers, but YMMV.  
    

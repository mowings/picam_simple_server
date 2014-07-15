Raspberry Pi Camera Simple HTTP Server
===
This simple demo uses Flask and the PiCam python API to create a simple on-demand jpeg capture over http. This is
just a demo -- if you need to change any parameters, just change them in the code.

The picam capture is captured into a stringio object whenever we see a GET request to `/camera/frame.jpg`. We then return the contents of the stringio object to the user as a jpeg. This eats some memory, but saves us from writing the SD card.

To run this, you'll need to have the [picam python package](http://picamera.readthedocs.org/en/release-1.5/) installed, as well as [Flask](http://flask.pocoo.org/docs). 

Flask can be installed via pip (`sudo pip install flask`). If you do not have pip installed, install it first (http://pip.readthedocs.org/en/latest/installing.html).

To run the server:

    sudo ./capture.py
    
If you want the server to run as a managed service, you can easily create a [simple upstart job](http://stackful-dev.com/what-every-developer-needs-to-know-about-ubuntu-upstart.html).

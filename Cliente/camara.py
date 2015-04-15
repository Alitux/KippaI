# -*- coding: utf-8 -*-
##Este metodo funciona pero desgraciadamente no puedo superponer imagenes. Se podria hacer algo mas chancho con muchas ventanas superpuestas.
#import subprocess
#import os
#import shlex #splits the command
#proceso=subprocess.Popen(["nohup","mplayer","tv://", "-tv", "driver=v4l2:width=640:height=480:device=/dev/video0:norm=NTSC","-fps", "0"])
#print "peronista"

##Método por SimpleCV
from SimpleCV import Camera
# Initialize the camera
cam = Camera(0)
# Loop to continuously get images
while True:
    # Get Image from camera
    img = cam.getImage()
    # Make image black and white
    # Draw the text "Hello World" on image
    img.drawText("Ave Maria purisima")
    # Show the image
    img.show()
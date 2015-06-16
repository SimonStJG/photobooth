#!/usr/bin/env python
# Created by br@re-web.eu, 2015

import subprocess

class CameraException(Exception):
    """Custom exception class to handle camera class errors"""
    pass

class Camera_gPhoto:
    """Camera class providing functionality to take pictures using gPhoto 2"""

    def __init__(self):
        # Print the abilities of the connected camera
        print(self.call_gphoto("-a", "/dev/null"))

    def call_gphoto(self, action, filename):
        # Try to run the command
        try:
            cmd = "gphoto2 --force-overwrite --quiet " + action + " --filename " + filename
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            if "ERROR" in output:
                raise subprocess.CalledProcessError(returncode=0, cmd=cmd, output=output)
        except subprocess.CalledProcessError as e:
            if "Canon EOS Capture failed: 2019" in e.output:
                raise CameraException("Can't focus! Move and try again!")
            elif "No camera found" in e.output:
                raise CameraException("No (supported) camera detected!")
            else:
                raise CameraException("Unknown error!\n" + '\n'.join(e.output.split('\n')[1:3]))
        return output

    def take_picture(self, filename="/tmp/picture.jpg"):
        self.call_gphoto("--capture-image-and-download", filename)
        return filename

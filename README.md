# PiLapse

Raspberry Pi time lapse photography with diurnal light cycles using 12V LED strip lights

There are many different Raspberry Pi time lapse scripts and setups available on the web, but I designed this with a specific purpose in mind. In particular, taking images of developing dung fungi with diurnal light cycling. The user specifies the length of the 'day' period whereby the lights are on. During the night period, the lights turn on for the duration of the image being taken. The user sets the time period between imaging, e.g. 60 seconds. The script runs indefinitely, or until the user interrupts it.

The script produces two image files, the original image and a timestamped image. The timestamped image has a count-up time in the bottom left hand corner in the format T: days:hours:minutes:seconds.

There is some time drift with the script cause by using sleep between images. I don't think this is an issue for time-lapse photography, rather something to be aware of. 

**Hardware setup**

I have used a Raspberry Pi 4 (4 Gb memory), with the HQ camera with the 6 mm, wide angle lens. I also used the standard Raspberry Pi OS, rather than using a headless option. It makes the setting up of the camera much simpler. The camera is mounted on a tripod for adjustment and stability.

The lights are 12V LED strips that are controlled by the Pi via a mosfet connected to pin 17 (GPIO 17).

![alt text](https://github.com/arnilsen/PiLapse/blob/main/files/box_setup.jpg?raw=true)
![alt text](https://github.com/arnilsen/PiLapse/blob/main/files/pilapse_hardware.jpg?raw=true)


**Software requirements**

There were some stability issues with raspistill in some of the Pi OS's. I had to use the dev version '' for it to work. Additionally, since late 2021 raspistill has been replaced with libcamera-still in the later Pi OS releases. This script will not work with libcamera-still.

Timestamp images are created with ImageMagick. ImageMagick can be installed by running

`sudo apt-get install imagemagick`

Timestamped images are saved in the directory 'timestamped' located in the user specified output directory.

Before you can run the script the camera has to be enabled. This only has to be done once. To enable the camera

`sudo raspi-config`

Navigate to *Interfacing Options* then select *Camera* and follow the prompt to enable the camera.

Also, the GPIO pins also need to be accessible. This will have to be done after every reboot. To do this run:

`sudo pigpiod`

**Running the script**

Because the hardware can be a bit fiddly, I would recommend that the pi and camera be setup in a non remote fashion. This allows the user to make adjustments to the camera, lights and specimens.


Run `pilapse.py` to view the script options

I strongly recommend running the light on full (255) and stopping down the aperture on the camera to get the best depth of field.

```
usage: pilapse.py [-h] -t  -o  -l  -p

Takes a timelapse at the user defined intervals. It flicks the LEDs on 1 sec
before imaging.

optional arguments:
  -h, --help            show this help message and exit
  -t , --time_sec       enter the period between images in seconds
  -o , --output         path to output directory, e.g. /home/pi/timelapse/.
                        Important: include the / after the directory name!
  -l , --light_intensity
                        light intensity (int) value must be between 30 and
                        255, the larger the number the brighter the light
  -p , --time_period    Duration of light period, within a 24 hour cycle.
                        Always starts with the light period. Must be specified
                        in hours.

Additional info: The script takes a continuous time lapse, imaging every x
seconds until the user disrupts the script (control + c). The images are saved
to the user specified folder and are numbered incrementally and datetime
stamped, e.g. "img0001_05_03_21-17:39:46". NOTE: before you can use this
script you need to run sudo pigpiod

```

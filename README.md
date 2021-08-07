# PiLapse

Raspberry Pi time lapse photography with diurnal light cycles using 12V LED strip lights

There are many different Raspberry Pi time lapse scripts and setups available on the web, but I designed this with a specific purpose in mind. In particular, taking images of developing dung fungi with diurnal light cycling. The user specifies the length of the 'day' period whereby the lights are on. During the night period, the lights turn on 1 second before an image is taken. The user sets the time period between imaging, e.g. 60 seconds. The script run indefinitely, or until the user interrupts it.

**Hardware setup**

I have used a Raspberry Pi 4 (4 Gb memory), with the HQ camera with the 6 mm, wide angle lens. I also used the standard Raspberry Pi OS, rather than using a headless option. It makes the setting up of the camera much simpler. The camera is mounted on a tripod for adjustment and stability.

The lights are 12V LED strips that are controlled by the pi via a mosfet connected to pin 17.

<img src=https://github.com/arnilsen/PiLapse/tree/main/files/picam.jpg width="400" height="790">

**Running the script**

Because the hardware can be a bit fiddly, I would recommend that the pi and camera be setup in a non remote fashion. This allows the user to make adjustments to the camera, lights and specimens.

Before you can run the script the camera has to be enabled.

To enable the camera

`sudo raspi-config`

Navigate to *Interfacing Options* then select *Camera* and follow the prompt to enable the camera.

Also, the GPIO pins also need to be accessible. To do this run:

`sudo pigpiod`

Run `pilapse.py` to view the script options


```usage: pilapse.py [-h] -t  -o  -l  -p

Takes a timelapse at the user defined intervals. It flicks the LEDs on 1 sec
before imaging

optional arguments:
  -h, --help            show this help message and exit
  -t , --time_sec       enter the period between images in seconds
  -o , --output         path to output directory, e.g. /home/pi/timelapse/.
                        Important: include the / after the directory name!
  -l , --light_intensity
                        light intensity (int) value must be between 30 and
                        255, the larger the numeber the brighter the light
  -p , --time_period    Duration of light period, within a 24 hour cycle.
                        Always starts with the light period. Must be specified
                        in hours.

Additional info: The script takes a continuous time lapse, imaging every x
seconds until the user disrupts the script (control c). The images are saved
to the user specified folder and are numbered incrementally and datetime
stamped, e.g. "img0001_05_03_21-17:39:46". NOTE: before you can use this
script you need to run sudo pigpiod

```

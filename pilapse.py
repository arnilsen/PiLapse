# pilapse.py
#
# This script is designed for timelapse photography with light and dark time periods administered
# by a 12 V LED light strip, controlled by the pi. This was originally designed to be used to
# observe the growth of dung fungi like Coprinopsis species but could be used for any number
# of other purposes.
#
# The script requires that the user enters the light period in hours (-p), time period in
# seconds (-t) and light intensity (-l) within the range of 0-255, 255 being fully on.
# The light period begins with the lights on for the given length of time specified. The
# period is calculated on a 24 hour cycle. If the light period (-p) is set to 10,
# then the dark period will be 14 hours. Images are taken at every -t seconds. When the dark
# period begins the lights are off and will turn on one second before the image is taken, then
# turn off again.
#
# This script runs indefinitely, or until the user use a the keyboard interrupt (CTRL + c).
#
# The script uses the sleep() function between taking images. I realise that this could cause
# time drift, but I don't think this is an issue for timelapse photography. The lights are
# controlled by a mosfet connected to pin 17 on the GPIO.
#
# This script is free to use, modify or distribute and comes with no warranties. If used, it would be
# great it you cite the GitHub page:
#
# NOTE: before you can use this script you need to run 'sudo pigpiod' to enable the GPIO pins



from time import sleep
from datetime import datetime, timedelta
import subprocess
import os
import argparse
import sys
import pigpio


parser = argparse.ArgumentParser(description = 'Takes a timelapse at the user defined intervals. It flicks the LEDs on 1 sec before imaging',\
epilog = 'Additional info: \n \
    The script takes a continuous time lapse, imaging every x seconds until the user disrupts the script (control c).\n \
    The images are saved to the user specified folder and are numbered incrementally and datetime stamped, e.g. "img0001_05_03_21-17:39:46". \n\n \
    NOTE: before you can use this script you need to run sudo pigpiod')


parser.add_argument('-t', '--time_sec', type=int, metavar = '', required = True, help = 'enter the period between images in seconds')
parser.add_argument('-o', '--output', type=str, metavar = '', required = True, help = 'path to output directory, e.g. /home/pi/timelapse/. Important: include the / after the directory name!')
parser.add_argument('-l', '--light_intensity', type=int, metavar = '', required = True, choices = range(30,256), help = 'light intensity (int) value must be between 30 and 255, the larger the number the brighter the light')
parser.add_argument('-p', '--time_period', type=int, metavar = '', required = True, choices = range(0,25), help = 'Duration of light period, within a 24 hour cycle. Always starts with the light period. Must be specified in hours.')
args = parser.parse_args()


WAIT_TIME = args.time_sec
out_dir = args.output
light_int = args.light_intensity
t_period = args.time_period
pi = pigpio.pi()



def check_dir(dname):
    #checks if the directory exists or makes a new one
    path = os.path.join(dname, 'timestamped')
    if os.path.isdir(dname):        
        os.mkdir(path)
        
    else:
        try:
            os.makedirs(path)
        except OSError:
            print('Creation of directory {} failed'.format(dname))
            sys.exit(1)



def tlapse():
    # initialise the times for the first 24 hour time period
    image = 0
    START_TIME = datetime.now()
    current_time = datetime.now()
    hours_added = timedelta(hours = t_period)
    new_time = current_time + hours_added
    new_time_24h = current_time + timedelta(hours = 24)

    print('light period begins ' + str(datetime.now()))

    while True:
        # Set up the infinite loop
        # Start with the light period
        try:
            while datetime.now() < new_time:
                pi.set_PWM_dutycycle(17, light_int)

                try:
                    now_time = datetime.now()
                    pic_time = now_time.strftime("%d_%m_%y-%H_%M_%S")
                    pic_name = 'img{}_'.format(str(image).zfill(4)) + pic_time + '.jpg'
                    time_elaps = now_time - START_TIME
                    cmd = 'raspistill -t 100 -ex night -n -o ' + out_dir + pic_name # command to call from the terminal. -n = no preview, -t time lag in ms
                    t_stamp = "T: %02d:%02d:%02d:%02d" % (time_elaps.days, time_elaps.seconds // 3600, time_elaps.seconds // 60 % 60, time_elaps.seconds % 60)                    
                    print(t_stamp)
                    subprocess.call(cmd, shell = True)
                    #sleep(2) # just incase there was a delay in the time it took to write image
                    stamp_cmd = "convert {}/{} -pointsize 90 -fill white -annotate +3350+2900 '{}' {}/timestamped/{}".format(out_dir, pic_name, t_stamp, out_dir, pic_name)
                    subprocess.call(stamp_cmd, shell = True)
                    image += 1
                    sleep(WAIT_TIME - 4)
                except KeyboardInterrupt:
                    print('\n\nTimelapse has ended. There are {} images in {}\n\
                    If you want to create a movie run "ffmpeg -f image2 -pattern_type glob -r 3 -i img*.jpg  foo.avi"\n'.format(str(image), str(out_dir)))
                    pi.set_PWM_dutycycle(17, 0)
                    pi.stop()
                    sys.exit(1)

            pi.set_PWM_dutycycle(17, 0)

            print('night period begins ' + str(datetime.now()))

            sleep(WAIT_TIME)



            # night period
            while new_time < datetime.now() < new_time_24h:
                try:
                    now_time = datetime.now()
                    pic_time = now_time.strftime("%d_%m_%y-%H_%M_%S")
                    pic_name = 'img{}_'.format(str(image).zfill(4)) + pic_time + '.jpg'
                    time_elaps = now_time - START_TIME
                    pi.set_PWM_dutycycle(17, light_int)
                    cmd = 'raspistill -t 100 -ex night -n -o ' + out_dir + pic_name # command to call from the terminal. -n = no preview, -t time lag in ms
                    t_stamp = "T: %02d:%02d:%02d:%02d" % (time_elaps.days, time_elaps.seconds // 3600, time_elaps.seconds // 60 % 60, time_elaps.seconds % 60)                    
                    print(t_stamp)
                    subprocess.call(cmd, shell = True)
                    #sleep(2) # just incase there was a delay in the time it took to write image
                    pi.set_PWM_dutycycle(17, 0)
                    stamp_cmd = "convert {}/{} -pointsize 90 -fill white -annotate +3350+2900 '{}' {}/timestamped/{}".format(out_dir, pic_name, t_stamp, out_dir, pic_name)
                    subprocess.call(stamp_cmd, shell = True)
                    image += 1
                    sleep(WAIT_TIME - 4)
                                        
                except KeyboardInterrupt:
                    print('\n\nTimelapse has ended. There are {} images in {}\n\
                    If you want to create a movie run "ffmpeg -f image2 -pattern_type glob -r 3 -i img*.jpg  foo.avi"\n'.format(str(image), str(out_dir)))
                    pi.set_PWM_dutycycle(17, 0)
                    pi.stop()
                    sys.exit(1)

            current_time = datetime.now()
            hours_added = timedelta(hours = t_period)
            new_time = current_time + hours_added
            new_time_24h = current_time + timedelta(hours = 24)

            sleep(WAIT_TIME)

            print('light period begins ' + str(datetime.now()))



        except KeyboardInterrupt:
            print('\n\nTimelapse has ended. There are {} images in {}\n\
            If you want to create a movie run "ffmpeg -f image2 -pattern_type glob -r 3 -i img*.jpg  foo.avi"\n'.format(str(image), str(out_dir)))
            pi.set_PWM_dutycycle(17, 0)
            pi.stop()
            sys.exit(1)





if __name__ == '__main__':
    check_dir(out_dir)
    tlapse()
    pi.stop()

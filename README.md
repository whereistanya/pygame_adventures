## moana.py 
moana.py is a small extremely stupid game because I wanted to learn pygame.


![screenshot](/images/screenshot.jpg)

Warning: it makes sounds.

I don't have rights to the moana pictures (obviously) and I forget where I found
the shell, so I should replace them. The mud picture is legit mine at least.

Sounds by Elizabeth :-D

## toddlerclock.py
toddlerclock.is a small extremely stupid colour-coded clock which also uses pygame.

It displays a message based on the time of day and tells Elizabeth whether she can
wake me. It's intended to be run on a raspberry pi with a pitft screen.

## Installing pygame for python3

There are a bunch of libraries pygame needs. Here's what I installed:

sudo apt-get install python-dev
sudo apt-get install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-image1.2-dev libsdl-mixer1.2-dev
sudo apt-get install python-pip3
sudo pip3 install pygame

## Using a raspberry pi display for toddlerclock

The code as-is works with thw [PiTFT capacitive display](https://www.adafruit.com/product/1983). 

For the [7" touchscreen display](https://www.adafruit.com/product/2718), comment out ```os.putenv('SDL_FBDEV', '/dev/fb1')```, and it should use the right display by default. 

You can modify the brightness (at least for the 7" display; I haven't tested the PiTFT) by editing ```/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/brightness```

```
$ echo 255 > brightness   # completely on  
$ echo 0 > brightness     # completely off  
$ echo 120 > brightness   # somewhere in between  

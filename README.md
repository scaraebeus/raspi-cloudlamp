# raspi-cloudlamp
Interactive cloud lamp built around the Raspberry Pi platform.

This was created and tested with Rasberry Pi OS (Dec 2, 2020 - Debian Buster Release) on a Raspberry Pi ZeroW.

Uses an IR Remote (Adafruit Mini Remote) with IR control handled by in-kernel IR.
Configured through ir-keytable and events accessed in python by `python-evdev` library.

RPi hardware and Neopixel control accessed via Circuit Python (adafruit-blinka).
Animations built off of adafruit-led-animations library.


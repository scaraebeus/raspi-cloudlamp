""" cloud_animations v0.2
Main init file for raspi-cloudlamp animations
"""

import board
import neopixel

from adafruit_led_animation.color import WHITE, calculate_intensity

from mylog import get_logger

logger = get_logger(__name__)

# Setup NeoPixels
logger.info("Initializing NeoPixels . . .")
pixel_pin = board.D18
pixel_num = 48
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

# Custom colors
DULL_WHITE = calculate_intensity(WHITE, 0.1)

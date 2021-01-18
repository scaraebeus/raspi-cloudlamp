# The MIT License (MIT)
#
# Copyright (c) 2020 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
""" randcolorcycle v0.2
Modified from:  `adafruit_led_animation.animation.colorcycle`
Modified by: Alex P

Implements selection of random 'num_pixels' pixels and randomizes the timing
between draws by setting speed between lower_speed and upper_speed (rounded
to 2 decimals).
Resets selected pixels at the end of each cycle.

================================================================================
Color cycle animation for CircuitPython helper library for LED animations.
* Author(s): Kattni Rembor
Implementation Notes
--------------------
**Hardware:**
* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

import random
from adafruit_led_animation.animation import Animation
from adafruit_led_animation.color import WHITE
from . import DULL_WHITE


class RandColorCycle(Animation):
    """
    Animate a sequence of one or more colors, cycling at the specified speed.
    :param pixel_object: The initialised LED object.
    :param float lower_speed: Animation speed in seconds (lower bound), e.g. ``0.05``.
    :param float upper_speed: Animation speed in seconds (upper bound), e.g. ``0.1``.
    :param int num_pixels: Number of pixels to randomly select to animate at the beginning
                   of each cycle.
    :param colors: A list of colors to cycle through in ``(r, g, b)`` tuple, or ``0x000000`` hex
                   format. Defaults to a rainbow color cycle.
    """

    def __init__(
        self,
        pixel_object,
        speed=0.05,
        num_pixels=1,
        colors=[WHITE, DULL_WHITE],
        name=None,
    ):
        self.colors = colors
        super().__init__(pixel_object, speed, colors[0], name=name)
        self._generator = self._color_generator()
        next(self._generator)
        self._pixels = []
        self._max_speed = speed
        self._num_pixels = num_pixels
        self._get_pixels(self)
        self.add_cycle_complete_receiver(self._get_pixels)

    on_cycle_complete_supported = True

    def draw(self):
        for pixel in self._pixels:
            self.pixel_object[pixel] = self.color
        next(self._generator)
        for pixel in range(len(self.pixel_object)):
            if pixel not in self._pixels:
                self.pixel_object[pixel] = self.colors[1]
        self.speed = self._max_speed * random.randint(1, 4)

    def _color_generator(self):
        index = 0
        while True:
            self._color = self.colors[index]
            yield
            index = (index + 1) % len(self.colors)
            if index == 0:
                self.cycle_complete = True

    def _get_pixels(self, animation):
        self._pixels = [
            random.randint(0, (len(self.pixel_object) - 1))
            for _ in range(self._num_pixels)
        ]
        animation.notify_cycles = random.randint(1, 5)
        animation.cycle_count = 0

    def reset(self):
        """
        Resets to the first color.
        """
        self._generator = self._color_generator()

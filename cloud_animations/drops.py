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
"""
cloud_animations.drops
Modified from: `adafruit_led_animation.animation.grid_rain`
================================================================================
Rain animations for CircuitPython helper library for LED animations.
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
from adafruit_led_animation.color import calculate_intensity

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation.git"

from adafruit_led_animation.color import BLACK


class Drops(Animation):
    """
    Droplets of rain.
    :param pixel_object: The initialised NeoPixel object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param count: Number of drops to generate per animation cycle.
    :param start_int: Starting intensity (Default 0.1)
    :param max_int: Max intensity before drop (Default 1.0)
    :param step: Steps in intensity (Default 0.1)
    :param background: Background color (Default BLACK).
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixel_object,
        speed,
        color,
        count=1,
        start_int=0.1,
        max_int=1.0,
        step=0.1,
        background=BLACK,
        name=None,
    ):
        self._count = count
        self._start_int = start_int
        self._max_int = max_int
        self._step = step
        self._background = background
        self._drops = []
        super().__init__(pixel_object, speed, color, name=name)

    def draw(self):

        # Increase drop intensity
        keep = []
        for drop in self._drops:
            drop[1] += self._step
            if drop[1] > drop[2]:
                self.pixel_object[drop[0]] = self._background
            else:
                drop[3] = calculate_intensity(self.color, drop[1])
                keep.append(drop)
        self._drops = keep

        # Add a drop
        if len(self._drops) < self._count:
            d = random.randint(0, len(self.pixel_object) - 1)
            self._drops.append(
                [
                    d,
                    self._start_int,
                    self._generate_drop(self._max_int),
                    calculate_intensity(self.color, self._start_int),
                ]
            )

        # Draw raindrops
        for d, n, i, color in self._drops:
            self.pixel_object[d] = color

    def _generate_drop(self, n):
        return round(random.uniform(self._max_int / 2, self._max_int), 1)

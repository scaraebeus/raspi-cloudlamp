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
from adafruit_led_animation import MS_PER_SECOND, monotonic_ms
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
    :param min_period: Minimum period for pulse (Default 1.0)
    :param max_period: Max period for pulse (Default 6.0)
    :param background: Background color (Default BLACK).
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixel_object,
        speed,
        color,
        count=1,
        min_period=1.0,
        max_period=6.0,
        background=BLACK,
        name=None,
    ):
        self._count = count
        self._min_period = min_period
        self._max_period = max_period
        self._background = background
        self._drops = []
        super().__init__(pixel_object, speed, color, name=name)

    def draw(self):

        # Increase drop intensity
        keep = []
        for drop in self._drops:
            color = next(drop["generator"])
            if color is not None:
                drop["color"] = color
                keep.append(drop)
            else:
                self.pixel_object[drop["pixel"]] = self._background
        self._drops = keep

        # Add a drop
        if len(self._drops) < self._count:
            # create list of pixels not in self._drops
            used = [drop["pixel"] for drop in self._drops]
            avail = [n for n in range(len(self.pixel_object)) if n not in used]
            # randomly pick one from that list
            d = random.choice(avail)
            period = random.randint(self._min_period, self._max_period)
            _generator = pulse_generator(period, self.color)
            self._drops.append(
                {
                    "pixel" : d,
                    "color" : self._background,
                    "generator" : _generator,
                }
            )

        # Draw raindrops
        for drop in self._drops:
            self.pixel_object[drop["pixel"]] = drop["color"]


def pulse_generator(period: float, color):
    """
    Generates a sequence of colors for a pulse, based on the time period specified.
    :param period: Pulse duration in seconds.
    :param color: RGB Color
    """
    period = int(period * MS_PER_SECOND)
    half_period = period // 2

    last_update = monotonic_ms()
    cycle_position = 0
    while True:
        now = monotonic_ms()
        time_since_last_draw = now - last_update
        last_update = now
        pos = cycle_position = (cycle_position + time_since_last_draw) % period
        if pos > half_period:
            cycle_position = 0
            yield None
            continue
        intensity = pos / half_period
        yield calculate_intensity(color, intensity)

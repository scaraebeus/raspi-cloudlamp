""" colorhandler v0.2
Color handler for raspi-cloudlamp
"""

from math import floor

from adafruit_led_animation import color

avail_colors = [
    color.RED,
    color.YELLOW,
    color.ORANGE,
    color.GREEN,
    color.TEAL,
    color.CYAN,
    color.BLUE,
    color.PURPLE,
    color.MAGENTA,
    color.JADE,
    color.PINK,
    color.AQUA,
    color.AMBER,
    color.WHITE,
]


class ColorHandler(object):
    """ Class for the ColorHandler object """

    def __init__(self, colors=avail_colors):

        self._intensity = 1.0
        self._colors = colors
        self._current_color = 0
        self._total_colors = len(self._colors) - 1
        self.color = self._current_color

    @property
    def color(self):
        return self._set_intensity(self._color)

    @color.setter
    def color(self, value):
        self._color = self._colors[value]

    # Functions
    def next_color(self):
        if self._current_color == self._total_colors:
            self._current_color = 0
        else:
            self._current_color += 1

        self.color = self._current_color

    def prev_color(self):
        if self._current_color == 0:
            self._current_color = self._total_colors
        else:
            self._current_color -= 1

        self.color = self._current_color

    def inc_intensity(self, step=0.1):
        if self._intensity == 1.0:
            return
        if (self._intensity + step) > 1.0:
            self._intensity = 1.0
        else:
            self._intensity += step

    def dec_intensity(self, step=0.1):
        if self._intensity == 0.1:
            return
        if (self._intensity - step) < 0.1:
            self._intensity = 0.1
        else:
            self._intensity -= step

    def intensity(self, value):
        if value < 0.0 or value > 1.0:
            return
        self._intensity = value

    def _set_intensity(self, color):
        return (
            int(color[0] * self._intensity),
            int(color[1] * self._intensity),
            int(color[2] * self._intensity),
        )


def increase_intensity(rgb, step=0.1):
    """Helper function to increase intensity by modifying the value from hsv"""
    h, s, v = rgb_to_hsv(rgb)
    v = min(v + step, 1)
    return hsv_to_rgb((h, s, v))


def decrease_intensity(rgb, step=0.1):
    """Helper function to decrease intensity by modifying the value from hsv"""
    h, s, v = rgb_to_hsv(rgb)
    v = max(0.1, v - step)
    return hsv_to_rgb((h, s, v))


def rgb_to_hsv(rgb):
    """Convert rgb tuple to hsv equivalent
    Math from http://www.easyrgb.com/en/math.php"""

    r, g, b = rgb
    r = r / 255
    g = g / 255
    b = b / 255

    rgbmin = min(r, g, b)
    rgbmax = max(r, g, b)
    rgbdel = rgbmax - rgbmin

    val = rgbmax

    if rgbdel == 0:
        hue = 0
        sat = 0
    else:
        sat = rgbdel / rgbmax
        del_r = (((rgbmax - r) / 6) + (rgbdel / 2)) / rgbmax
        del_g = (((rgbmax - g) / 6) + (rgbdel / 2)) / rgbmax
        del_b = (((rgbmax - b) / 6) + (rgbdel / 2)) / rgbmax

        if r == rgbmax:
            hue = del_b - del_g
        elif g == rgbmax:
            hue = (1 / 3) + del_r - del_b
        elif b == rgbmax:
            hue = (2 / 3) + del_g - del_r

        if hue < 0:
            hue += 1
        if hue > 1:
            hue -= 1

    return (hue, sat, val)


def hsv_to_rgb(hsv):
    """Convert hsv tuple to rgb equivalent
    Math from http://www.easyrgb.com/en/math.php"""

    h, s, v = hsv

    if s == 0:
        r = int(v * 255)
        g = int(v * 255)
        b = int(v * 255)
    else:
        var_h = h * 6
        if var_h == 6:
            var_h = 0
        var_i = floor(var_h)
        var_1 = v * (1 - s)
        var_2 = v * (1 - s * (var_h - var_i))
        var_3 = v * (1 - s * (1 - (var_h - var_i)))

        if var_i == 0:
            var_r = v
            var_g = var_3
            var_b = var_1
        elif var_i == 1:
            var_r = var_2
            var_g = v
            var_b = var_1
        elif var_i == 2:
            var_r = var_1
            var_g = v
            var_b = var_3
        elif var_i == 3:
            var_r = var_1
            var_g = var_2
            var_b = v
        elif var_i == 4:
            var_r = var_3
            var_g = var_1
            var_b = v
        else:
            var_r = v
            var_g = var_1
            var_b = var_2

        r = int(var_r * 255)
        g = int(var_g * 255)
        b = int(var_b * 255)

    return (r, g, b)

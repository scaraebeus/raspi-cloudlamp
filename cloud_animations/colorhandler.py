""" colorhandler v0.2
Color handler for raspi-cloudlamp
"""

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

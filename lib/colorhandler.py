'''
Color handler for APCloudLight 2020
'''

from adafruit_led_animation.color import RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, JADE, PINK, AQUA, AMBER, WHITE, OLD_LACE

aColors = [
    RED,
    YELLOW,
    ORANGE,
    GREEN,
    TEAL,
    CYAN,
    BLUE,
    PURPLE,
    MAGENTA,
    JADE,
    PINK,
    AQUA,
    AMBER,
    WHITE,
    OLD_LACE,
]
    

class ColorHandler(object):
    ''' Class for the ColorHandler object '''
    
    def __init__(self, colors = aColors):
        
        self._intensity = 1.0
        self._colors = colors
        self._currentColor = 0
        self._totalColors = len(self._colors) - 1
        self.color = self._currentColor
        
    @property
    def color(self):
        return self._setintensity(self._color)
    
    @color.setter
    def color(self, value):
        self._color = self._colors[value]
    
    # Functions
    def nextColor(self):
        if self._currentColor == self._totalColors:
            self._currentColor = 0
        else:
            self._currentColor += 1
    
        self.color = self._currentColor
    
    def prevColor(self):
        if self._currentColor == 0:
            self._currentColor = self._totalColors
        else:
            self._currentColor -= 1
        
        self.color = self._currentColor
    
    def incIntensity(self):
        if self._intensity == 1.0:
            return
        if (self._intensity + 0.2) > 1.0:
            self._intensity = 1.0
        else:
            self._intensity += 0.2
    
    def decIntensity(self):
        if self._intensity == 0.2:
            return
        if (self._intensity - 0.2) < 0.2:
            self._intensity = 0.2
        else:
            self._intensity -= 0.2
    
    def intensity(self, value):
        if value < 0.2 or value > 1.0:
            return
        self._intensity = value
    
    def _setintensity(self, color):
        return (
            int(color[0] * self._intensity),
            int(color[1] * self._intensity),
            int(color[2] * self._intensity),
        )
""" animations v0.2
Contains animations for weather patterns and others
except lightning which is in lightning_animations module. """

from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.color import (
    RED,
    YELLOW,
    BLUE,
    WHITE,
    BLACK,
)
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow

from . import pixels, DULL_WHITE
from .drops import Drops
from .groups import (
    cross_strips,
    hatch_strips,
    sunny25,
    sunny50,
    sunny75,
    cloudy25,
    cloudy50,
    cloudy75,
    top_half,
    rain_pixels,
)
from .lightning_animations import lightning_list
from mylog import get_logger

logger = get_logger(__name__)

# Weather Animations
clearday = Solid(pixels, color=YELLOW)

cloud25 = AnimationGroup(
    Solid(sunny75, color=YELLOW), Solid(cloudy25, color=DULL_WHITE), sync=True
)

cloud50 = AnimationGroup(
    Solid(sunny50, color=YELLOW), Solid(cloudy50, color=DULL_WHITE), sync=True
)

cloud75 = AnimationGroup(
    Solid(sunny25, color=YELLOW), Solid(cloudy75, color=DULL_WHITE), sync=True
)

cloud100 = Solid(pixels, color=DULL_WHITE)

rainlight = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(
        rain_pixels, speed=0.1, min_period=2, color=BLUE, count=4, background=DULL_WHITE
    ),
    sync=False,
)

rainheavy = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(
        rain_pixels,
        speed=0.1,
        color=BLUE,
        max_period=5,
        count=10,
        background=DULL_WHITE,
    ),
    sync=False,
)

rainveryheavy = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(
        rain_pixels,
        speed=0.1,
        color=BLUE,
        max_period=4,
        count=16,
        background=DULL_WHITE,
    ),
    sync=False,
)

snowlight = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(
        rain_pixels,
        speed=0.1,
        color=WHITE,
        min_period=2,
        count=4,
        background=DULL_WHITE,
    ),
    sync=False,
)

snowheavy = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(
        rain_pixels,
        speed=0.1,
        color=WHITE,
        max_period=5,
        count=10,
        background=DULL_WHITE,
    ),
    sync=False,
)

snowveryheavy = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(
        rain_pixels,
        speed=0.1,
        color=WHITE,
        max_period=4,
        count=16,
        background=DULL_WHITE,
    ),
    sync=False,
)

solid = Solid(pixels, color=RED)
rainbow = Rainbow(pixels, speed=0.1, period=2)
pulse = Pulse(pixels, speed=0.1, period=6, color=RED)
sparkle = Sparkle(pixels, speed=0.1, color=RED, num_sparkles=10)
r_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)

c_scan = Comet(
    cross_strips, speed=0.2, color=RED, tail_length=3, bounce=False, ring=True
)

h_scan = Comet(
    hatch_strips, speed=0.2, color=RED, tail_length=4, bounce=False, ring=True
)

reset_strip = Solid(pixels, color=BLACK)

wth_list = [
    clearday,
    cloud25,
    cloud50,
    cloud75,
    cloud100,
    rainlight,
    rainheavy,
    rainveryheavy,
    snowlight,
    snowheavy,
    snowveryheavy,
]

# Sub list [animation_object, can_change_color, can_change_intensity]
mode = [
    [clearday, "n", "n"],  # 0: Place holder for weather mode (default)
    [solid, "y", "y"],  # 1: Solid color mode - Can change color (and ideally intensity)
    [rainbow, "n", "n"],  # 2: Rainbow mode
    [pulse, "y", "y"],  # 3: Pulse/Breath mode - Can change color
    [sparkle, "y", "y"],  # 4: Sparkle mode - Can change color
    # [p_sparkle, 'y', 'n'], # N: Pulse Sparkle mode - Can change color
    [r_sparkle, "n", "n"],  # 5: Rainbow Sparkle mode
    [c_scan, "y", "y"],  # 6: Line Scan mode - Can change color
    [h_scan, "y", "y"],  # 7: Grid Scan mode - Can change color
    [lightning_list[0], "n", "n"],  # 8: Lightning mode - Can change color
    [wth_list[0], "n", "n"],  # 9: Weather demo mode - can cycle between patterns
]

# Map openweathermap condition codes to weather animations.
# List for each dict item is in the form [ day_animation, night_animation ]
weather_anim = {
    "200": [cloud100, cloud100],  # T-Storm - light rain
    "201": [cloud100, cloud100],  # T-Storm - rain
    "202": [cloud100, cloud100],  # T-Storm - heavy rain
    "210": [cloud100, cloud100],  # Light T-Storm
    "211": [cloud100, cloud100],  # T-Storm
    "212": [cloud100, cloud100],  # Heavy T-Storm
    "221": [cloud100, cloud100],  # Ragged T-Storm
    "230": [cloud100, cloud100],  # T-Storm - light drizzle
    "231": [cloud100, cloud100],  # T-Storm - drizzle
    "232": [cloud100, cloud100],  # T-Storm - heavy drizzle
    "300": [rainlight, rainlight],  # Light drizzle
    "301": [rainlight, rainlight],  # Drizzle
    "302": [rainheavy, rainheavy],  # Heavy drizzle
    "310": [rainlight, rainlight],  # Light drizzle rain
    "311": [rainheavy, rainheavy],  # Drizzle rain
    "312": [rainheavy, rainheavy],  # Heavy drizzle rain
    "313": [rainheavy, rainheavy],  # Shower rain and drizzle
    "314": [rainheavy, rainheavy],  # Heavy shower rain and drizzle
    "321": [rainheavy, rainheavy],  # Shower drizzle
    "500": [rainlight, rainlight],  # Light rain
    "501": [rainlight, rainlight],  # Moderate rain
    "502": [rainheavy, rainheavy],  # Heavy rain
    "503": [rainveryheavy, rainveryheavy],  # Very heavy rain
    "504": [rainveryheavy, rainveryheavy],  # Extreme rain
    "511": [rainheavy, rainheavy],  # Freezing rain
    "520": [rainlight, rainlight],  # Light shower rain
    "521": [rainheavy, rainheavy],  # Shower rain
    "522": [rainheavy, rainheavy],  # Heavy shower rain
    "531": [rainveryheavy, rainveryheavy],  # Ragged shower rain
    "600": [snowlight, snowlight],  # Light snow
    "601": [snowheavy, snowheavy],  # Snow
    "602": [snowveryheavy, snowveryheavy],  # Heavy snow
    "611": [rainlight, rainlight],  # Sleet
    "612": [rainlight, rainlight],  # Light shower sleet
    "613": [rainheavy, rainheavy],  # Shower sleet
    "615": [rainlight, rainlight],  # Light rain and snow
    "616": [rainlight, rainlight],  # Rain and snow
    "620": [snowlight, snowlight],  # Light shower snow
    "621": [snowheavy, snowheavy],  # Shower snow
    "622": [snowveryheavy, snowveryheavy],  # Heavy shower snow
    "701": [cloud100, cloud100],  # Mist
    "711": [cloud100, cloud100],  # Smoke
    "721": [cloud100, cloud100],  # Haze
    "731": [cloud100, cloud100],  # Dust whirls
    "741": [cloud100, cloud100],  # Fog
    "751": [cloud100, cloud100],  # Sand
    "761": [cloud100, cloud100],  # Dust
    "762": [cloud100, cloud100],  # Volcanic Ash
    "771": [cloud100, cloud100],  # Squalls
    "781": [cloud100, cloud100],  # Tornado
    "800": [clearday, clearday],  # Clear sky
    "801": [cloud25, cloud25],  # Few clouds
    "802": [cloud50, cloud50],  # Scattered clouds
    "803": [cloud75, cloud75],  # Broken clouds
    "804": [cloud100, cloud100],  # Overcast clouds
    "def": [cloud100, cloud100],  # Default weather
}

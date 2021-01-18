""" animations v0.2
Contains animations for weather patterns and others
except lightning which is in lightning_animations module. """

from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.color import (
    YELLOW,
    BLUE,
    WHITE,
    BLACK,
)

# from adafruit_led_animation.animation.comet import Comet
from .rcl_comet import Comet
from adafruit_led_animation.animation.pulse import Pulse

# from adafruit_led_animation.animation.sparkle import Sparkle
from .rcl_sparkle import Sparkle
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow

from . import pixels, DULL_WHITE
from .drops import Drops
from .groups import (
    cross_strips,
    hatch_strips,
    cloudy25_night,
    cloudy50_night,
    cloudy75_night,
    cloudy100_night,
    top_half,
    rain_pixels,
    clear_night,
    bottom_half,
    top_two,
    bottom_six,
    top_center,
    bottom_heavy,
)
from .lightning_animations import lightningsequencerand
from mylog import get_logger

logger = get_logger(__name__)

# Weather Animations
clearday = Solid(pixels, color=YELLOW)

cloud25 = AnimationGroup(
    Solid(top_half, color=YELLOW), Solid(bottom_half, color=DULL_WHITE), sync=True
)

cloud50 = AnimationGroup(
    Solid(top_two, color=YELLOW), Solid(bottom_six, color=DULL_WHITE), sync=True
)

cloud75 = AnimationGroup(
    Solid(top_center, color=YELLOW), Solid(bottom_heavy, color=DULL_WHITE), sync=True
)

cloud100 = Solid(pixels, color=DULL_WHITE)

clearnight = Solid(clear_night, color=DULL_WHITE)
cloud25night = Solid(cloudy25_night, color=DULL_WHITE)
cloud50night = Solid(cloudy50_night, color=DULL_WHITE)
cloud75night = Solid(cloudy75_night, color=DULL_WHITE)
cloud100night = Solid(cloudy100_night, color=DULL_WHITE)

rainlight = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(
        rain_pixels, speed=0.1, min_period=2, color=BLUE, count=4, background=DULL_WHITE
    ),
    sync=False,
)

rainlightnight = AnimationGroup(
    Solid(cloudy50_night, color=DULL_WHITE),
    Drops(
        rain_pixels, speed=0.1, min_period=2, color=BLUE, count=4, background=DULL_WHITE
    ),
    sync=False,
)

rainlightlightning = AnimationGroup(
    lightningsequencerand,
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

rainheavynight = AnimationGroup(
    Solid(cloudy50_night, color=DULL_WHITE),
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

rainheavylightning = AnimationGroup(
    lightningsequencerand,
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

rainveryheavynight = AnimationGroup(
    Solid(cloudy50_night, color=DULL_WHITE),
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

rainveryheavylightning = AnimationGroup(
    lightningsequencerand,
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

solid = Solid(pixels, color=BLACK)
solid.speed = 0.2
rainbow = Rainbow(pixels, speed=0.1, period=2)
pulse = Pulse(pixels, speed=0.1, period=6, color=BLACK)
sparkle = Sparkle(pixels, speed=0.1, color=BLACK, num_sparkles=10)
r_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)

c_scan = Comet(
    cross_strips, speed=0.2, color=BLACK, tail_length=3, bounce=False, ring=True
)

h_scan = Comet(
    hatch_strips, speed=0.2, color=BLACK, tail_length=4, bounce=False, ring=True
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
    rainlightlightning,
    rainheavylightning,
    rainveryheavylightning,
    clearnight,
    cloud25night,
    cloud50night,
    cloud75night,
    cloud100night,
    rainlightnight,
    rainheavynight,
    rainveryheavynight,
    snowlight,
    snowheavy,
    snowveryheavy,
    lightningsequencerand,
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
    [lightningsequencerand, "n", "n"],  # 8: Lightning mode - Can change color
    [wth_list[0], "n", "n"],  # 9: Weather demo mode - can cycle between patterns
]

# Map openweathermap condition codes to weather animations.
# List for each dict item is in the form [ day_animation, night_animation ]
weather_anim = {
    "200": [rainlightlightning, cloud100night],  # T-Storm - light rain
    "201": [rainheavylightning, cloud100night],  # T-Storm - rain
    "202": [rainveryheavylightning, cloud100night],  # T-Storm - heavy rain
    "210": [lightningsequencerand, cloud100night],  # Light T-Storm
    "211": [lightningsequencerand, cloud100night],  # T-Storm
    "212": [lightningsequencerand, cloud100night],  # Heavy T-Storm
    "221": [lightningsequencerand, cloud100night],  # Ragged T-Storm
    "230": [rainlightlightning, cloud100night],  # T-Storm - light drizzle
    "231": [rainlightlightning, cloud100night],  # T-Storm - drizzle
    "232": [rainheavylightning, cloud100night],  # T-Storm - heavy drizzle
    "300": [rainlight, rainlightnight],  # Light drizzle
    "301": [rainlight, rainlightnight],  # Drizzle
    "302": [rainheavy, rainheavynight],  # Heavy drizzle
    "310": [rainlight, rainlightnight],  # Light drizzle rain
    "311": [rainheavy, rainheavynight],  # Drizzle rain
    "312": [rainheavy, rainheavynight],  # Heavy drizzle rain
    "313": [rainheavy, rainheavynight],  # Shower rain and drizzle
    "314": [rainheavy, rainheavynight],  # Heavy shower rain and drizzle
    "321": [rainheavy, rainheavynight],  # Shower drizzle
    "500": [rainlight, rainlightnight],  # Light rain
    "501": [rainlight, rainlightnight],  # Moderate rain
    "502": [rainheavy, rainheavynight],  # Heavy rain
    "503": [rainveryheavy, rainveryheavynight],  # Very heavy rain
    "504": [rainveryheavy, rainveryheavynight],  # Extreme rain
    "511": [rainheavy, rainheavynight],  # Freezing rain
    "520": [rainlight, rainlightnight],  # Light shower rain
    "521": [rainheavy, rainheavynight],  # Shower rain
    "522": [rainheavy, rainheavynight],  # Heavy shower rain
    "531": [rainveryheavy, rainveryheavynight],  # Ragged shower rain
    "600": [snowlight, snowlight],  # Light snow
    "601": [snowheavy, snowheavy],  # Snow
    "602": [snowveryheavy, snowveryheavy],  # Heavy snow
    "611": [rainlight, rainlightnight],  # Sleet
    "612": [rainlight, rainlightnight],  # Light shower sleet
    "613": [rainheavy, rainheavynight],  # Shower sleet
    "615": [rainlight, rainlightnight],  # Light rain and snow
    "616": [rainlight, rainlightnight],  # Rain and snow
    "620": [snowlight, snowlight],  # Light shower snow
    "621": [snowheavy, snowheavy],  # Shower snow
    "622": [snowveryheavy, snowveryheavy],  # Heavy shower snow
    "701": [cloud100, cloud100night],  # Mist
    "711": [cloud100, cloud100night],  # Smoke
    "721": [cloud100, cloud100night],  # Haze
    "731": [cloud100, cloud100night],  # Dust whirls
    "741": [cloud100, cloud100night],  # Fog
    "751": [cloud100, cloud100night],  # Sand
    "761": [cloud100, cloud100night],  # Dust
    "762": [cloud100, cloud100night],  # Volcanic Ash
    "771": [cloud100, cloud100night],  # Squalls
    "781": [cloud100, cloud100night],  # Tornado
    "800": [clearday, clearnight],  # Clear sky
    "801": [cloud25, cloud25night],  # Few clouds
    "802": [cloud50, cloud50night],  # Scattered clouds
    "803": [cloud75, cloud75night],  # Broken clouds
    "804": [cloud100, cloud100night],  # Overcast clouds
    "def": [cloud100, cloud100night],  # Default weather
}

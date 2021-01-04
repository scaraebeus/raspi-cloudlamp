import board
import neopixel

from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.helper import PixelSubset, PixelMap
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import (
    RED,
    YELLOW,
    PURPLE,
    BLUE,
    WHITE,
    JADE,
    BLACK,
    calculate_intensity,
)
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow

from cloud_animations.lightningflash import LightningFlash
from cloud_animations.drops import Drops

# Setup NeoPixels
pixel_pin = board.D18
pixel_num = 48
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

# Setup Pixel Groups
cross_strips = PixelMap(
    pixels,
    [
        (31, 16, 15, 0),
        (30, 17, 14, 1),
        (29, 18, 13, 2),
        (28, 19, 12, 3),
        (27, 20, 11, 4),
        (26, 21, 10, 5),
        (25, 22, 9, 6),
        (24, 23, 8, 7),
        (35, 36, 43, 44),
        (34, 37, 42, 45),
        (33, 38, 41, 46),
        (32, 39, 40, 47),
    ],
    individual_pixels=True,
)

hatch_strips = PixelMap(
    pixels,
    [(24, 32), (16, 24), (8, 16), (0, 8), (44, 48), (40, 44), (36, 40), (32, 36)],
)

sunny75 = PixelSubset(pixels, 8, 32)
sunny50 = PixelSubset(pixels, 16, 32)
sunny25 = PixelSubset(pixels, 24, 32)
cloudy75 = PixelMap(pixels, [(32, 48), (0, 24)])
cloudy50 = PixelMap(pixels, [(32, 48), (0, 16)])
cloudy25 = PixelMap(pixels, [(32, 48), (0, 8)])
top_half = PixelSubset(pixels, 0, 32)
rain_pixels = PixelSubset(pixels, 32, 48)

# Lightning Animations
# TODO: Move all of the lightning animation stuff to its own module
lightning_path_1 = PixelMap(
    pixels, [26, 28, 30, 19, 11, 2, 46, 42, 38], individual_pixels=True
)

lightning_path_2 = PixelMap(
    pixels, [41, 45, 4, 13, 20, 25, 27, 33], individual_pixels=True
)

lightning_path_3 = PixelMap(
    pixels, [39, 31, 29, 18, 11, 7, 45, 41], individual_pixels=True
)

lightningflash = LightningFlash(
    pixels, lower_speed=0.05, upper_speed=0.1, num_pixels=12, color=WHITE
)

lightningstreak1 = Comet(
    lightning_path_1, speed=0.03, color=WHITE, tail_length=3, bounce=False
)

lightningstreak2 = Comet(
    lightning_path_2, speed=0.03, color=WHITE, tail_length=3, bounce=False
)

lightningstreak3 = Comet(
    lightning_path_3, speed=0.03, color=WHITE, tail_length=3, bounce=False
)

lightningseq1 = AnimationSequence(
    lightningflash,
    lightningstreak2,
    lightningflash,
    auto_clear=True,
    auto_reset=True,
    advance_on_cycle_complete=True,
)

lightningseq2 = AnimationSequence(
    lightningstreak1,
    lightningflash,
    auto_clear=True,
    auto_reset=True,
    advance_on_cycle_complete=True,
)

lightningseq3 = AnimationSequence(
    lightningflash,
    lightningstreak3,
    auto_clear=True,
    auto_reset=True,
    advance_on_cycle_complete=True,
)

lightningseq4 = AnimationSequence(
    lightningstreak2,
    lightningflash,
    lightningstreak1,
    auto_clear=True,
    auto_reset=True,
    advance_on_cycle_complete=True,
)

lightningseq5 = AnimationSequence(
    lightningstreak3,
    lightningflash,
    lightningflash,
    auto_clear=True,
    auto_reset=True,
    advance_on_cycle_complete=True,
)

lightningseq6 = AnimationSequence(
    lightningflash,
    lightningflash,
    auto_clear=True,
    auto_reset=True,
    advance_on_cycle_complete=True,
)

lightning_list = [
    lightningseq1,
    lightningseq6,
    lightningseq2,
    lightningseq6,
    lightningseq3,
    lightningseq6,
    lightningseq4,
    lightningseq6,
    lightningseq5,
    lightningseq6,
]

# Weather Animations
# TODO: Move the weather animations to their own module
DULL_WHITE = calculate_intensity(WHITE, 0.1)
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
    Drops(rain_pixels, speed=0.1, color=BLUE, count=4, background=DULL_WHITE),
    sync=False,
)
rainheavy = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(rain_pixels, speed=0.1, color=BLUE, max_period=5, count=10, background=DULL_WHITE),
    sync=False,
)
rainveryheavy = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(rain_pixels, speed=0.1, color=BLUE, max_period=3, count=16, background=DULL_WHITE),
    sync=False,
)
snowlight = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(rain_pixels, speed=0.1, color=WHITE, count=4, background=DULL_WHITE),
    sync=False,
)
snowheavy = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(rain_pixels, speed=0.1, color=WHITE, max_period=5, count=10, background=DULL_WHITE),
    sync=False,
)
snowveryheavy = AnimationGroup(
    Solid(top_half, color=DULL_WHITE),
    Drops(rain_pixels, speed=0.1, color=WHITE, max_period=3, count=16, background=DULL_WHITE),
    sync=False,
)


solid = Solid(pixels, color=RED)
rainbow = Rainbow(pixels, speed=0.1, period=2)
pulse = Pulse(pixels, speed=0.1, period=6, color=RED)
sparkle = Sparkle(pixels, speed=0.1, color=RED, num_sparkles=10)
r_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
c_scan = Comet(
    cross_strips, speed=0.2, color=PURPLE, tail_length=3, bounce=False, ring=True
)
h_scan = Comet(
    hatch_strips, speed=0.2, color=JADE, tail_length=4, bounce=False, ring=True
)
reset_strip = Solid(pixels, color=BLACK)

wth_list = [clearday, cloud25, cloud50, cloud75, cloud100, rainlight, rainheavy, rainveryheavy, snowlight, snowheavy, snowveryheavy]

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
    [lightning_list[0], "y", "n"],  # 8: Lightning mode - Can change color
    [wth_list[0], "n", "n"],  # 9: Weather demo mode - can cycle between patterns
]

# Map openweathermap condition codes to weather animations
weather_anim = {
    "200": cloud100,        # T-Storm - light rain
    "201": cloud100,        # T-Storm - rain
    "202": cloud100,        # T-Storm - heavy rain
    "210": cloud100,        # Light T-Storm
    "211": cloud100,        # T-Storm
    "212": cloud100,        # Heavy T-Storm
    "221": cloud100,        # Ragged T-Storm
    "230": cloud100,        # T-Storm - light drizzle
    "231": cloud100,        # T-Storm - drizzle
    "232": cloud100,        # T-Storm - heavy drizzle
    "300": rainlight,       # Light drizzle
    "301": rainlight,       # Drizzle
    "302": rainheavy,       # Heavy drizzle
    "310": rainlight,       # Light drizzle rain
    "311": rainheavy,       # Drizzle rain
    "312": rainheavy,       # Heavy drizzle rain
    "313": rainheavy,       # Shower rain and drizzle
    "314": rainheavy,       # Heavy shower rain and drizzle
    "321": rainheavy,       # Shower drizzle
    "500": rainlight,       # Light rain
    "501": rainlight,       # Moderate rain
    "502": rainheavy,       # Heavy rain
    "503": rainveryheavy,   # Very heavy rain
    "504": rainveryheavy,   # Extreme rain
    "511": rainheavy,       # Freezing rain
    "520": rainlight,       # Light shower rain
    "521": rainheavy,       # Shower rain
    "522": rainheavy,       # Heavy shower rain
    "531": rainveryheavy,   # Ragged shower rain
    "600": snowlight,       # Light snow
    "601": snowheavy,       # Snow
    "602": snowveryheavy,   # Heavy snow
    "611": rainlight,       # Sleet
    "612": rainlight,       # Light shower sleet
    "613": rainheavy,       # Shower sleet
    "615": rainlight,       # Light rain and snow
    "616": rainlight,       # Rain and snow
    "620": snowlight,       # Light shower snow
    "621": snowheavy,       # Shower snow
    "622": snowveryheavy,   # Heavy shower snow
    "701": cloud100,        # Mist
    "711": cloud100,        # Smoke
    "721": cloud100,        # Haze
    "731": cloud100,        # Dust whirls
    "741": cloud100,        # Fog
    "751": cloud100,        # Sand
    "761": cloud100,        # Dust
    "762": cloud100,        # Volcanic Ash
    "771": cloud100,        # Squalls
    "781": cloud100,        # Tornado
    "800": clearday,        # Clear sky
    "801": cloud25,         # Few clouds
    "802": cloud50,         # Scattered clouds
    "803": cloud75,         # Broken clouds
    "804": cloud100,        # Overcast clouds
}

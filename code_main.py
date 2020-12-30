import sys
import signal
sys.path.append(r'/home/pi/cloud/lib')

from time import monotonic, sleep
from random import randint
import board
import neopixel
import remote_v0_2 as remote
import weather
import adafruit_logging as logging
#from adafruit_remote_mapping import mapping
from adafruit_remote_mapping import mapping2 as mapping
from mysecrets import secrets
import colorhandler

from adafruit_led_animation.helper import PixelSubset, PixelMap
from cloud_animations.lightningflash import LightningFlash
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.sequence import AnimationSequence, AnimateOnce
from adafruit_led_animation.color import RED, YELLOW, PURPLE, BLUE, WHITE, AMBER, JADE, MAGENTA, ORANGE, BLACK, calculate_intensity


from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import RED, PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE, BLACK

# Create and setup logger
logger = logging.getLogger('cloud')
logger.setLevel(logging.INFO)

# Setup Weather class
logger.info('Initiating myWeather . . .')
myWeather = weather.Weather()
logger.info('myWeather initiated.')

# Setup IR remote
myRemote = remote.IRRemote(mapping)

# Setup neopixels
pixel_pin = board.D18
pixel_num = 48
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

# Setup ColorHandler
myColor = colorhandler.ColorHandler()

# Setup Pixel Groups
rain_pixel_start = 32
rain_pixel_end = 48
rain_pixels = PixelSubset(pixels, rain_pixel_start, rain_pixel_end)
cross_strips = PixelMap(pixels, [
    (31, 16, 15, 0),
    (30, 17, 14, 1),
    (29, 18, 13, 2),
    (28, 19, 12, 3),
    (27, 20, 11, 4),
    (26, 21, 10, 5),
    (25, 22,  9, 6),
    (24, 23,  8, 7),
    (35, 36, 43, 44),
    (34, 37, 42, 45),
    (33, 38, 41, 46),
    (32, 39, 40, 47)],
    individual_pixels=True)
hatch_strips = PixelMap(pixels, [
    (24,32),
    (16,24),
    (8,16),
    (0,8),
    (44,48),
    (40,44),
    (36,40),
    (32,36)])
sunny75 = PixelSubset(pixels, 8, 32)
sunny50 = PixelSubset(pixels, 16, 32)
sunny25 = PixelSubset(pixels, 24, 32)
cloudy75 = PixelMap(pixels, [(32,48),(0,24)])
cloudy50 = PixelMap(pixels, [(32,48),(0,16)])
cloudy25 = PixelMap(pixels, [(32,48),(0,8)])
top_half = PixelSubset(pixels, 0, 32)
lightning_path_1 = PixelMap(pixels, [26, 28, 30, 19, 11, 2, 46, 42, 38], individual_pixels=True)
lightning_path_2 = PixelMap(pixels, [41, 45, 4, 13, 20, 25, 27, 33], individual_pixels=True)
lightning_path_3 = PixelMap(pixels, [39, 31, 29, 18, 11, 7, 45, 41], individual_pixels=True)

# Lightning Animations
lightningflash = LightningFlash(pixels, lower_speed=0.05, upper_speed=0.1, num_pixels=12, color=WHITE)
lightningstreak1 = Comet(lightning_path_1, speed=0.03, color=WHITE, tail_length=3, bounce=False)
lightningstreak2 = Comet(lightning_path_2, speed=0.03, color=WHITE, tail_length=3, bounce=False)
lightningstreak3 = Comet(lightning_path_3, speed=0.03, color=WHITE, tail_length=3, bounce=False)

lightningseq1 = AnimationSequence(lightningflash, lightningstreak2, lightningflash, auto_clear=True, auto_reset=True, advance_on_cycle_complete=True)
lightningseq2 = AnimationSequence(lightningstreak1, lightningflash, auto_clear=True, auto_reset=True, advance_on_cycle_complete=True)
lightningseq3 = AnimationSequence(lightningflash, lightningstreak3, auto_clear=True, auto_reset=True, advance_on_cycle_complete=True)
lightningseq4 = AnimationSequence(lightningstreak2, lightningflash, lightningstreak1, auto_clear=True, auto_reset=True, advance_on_cycle_complete=True)
lightningseq5 = AnimationSequence(lightningstreak3, lightningflash, lightningflash, auto_clear=True, auto_reset=True, advance_on_cycle_complete=True)
lightningseq6 = AnimationSequence(lightningflash, lightningflash, auto_clear=True, auto_reset=True, advance_on_cycle_complete=True)

#lightningseq1.add_cycle_complete_receiver(anim_pauser)
#lightningseq2.add_cycle_complete_receiver(anim_pauser)
#lightningseq3.add_cycle_complete_receiver(anim_pauser)
#lightningseq4.add_cycle_complete_receiver(anim_pauser)
#lightningseq5.add_cycle_complete_receiver(anim_pauser)

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
    lightningseq6
]

# Weather Animations
DULL_WHITE = calculate_intensity(WHITE, 0.1)
clearday = Solid(pixels, color=YELLOW)
cloud25 = AnimationGroup(Solid(sunny75, color=YELLOW), Solid(cloudy25, color=DULL_WHITE), sync=True)
cloud50 = AnimationGroup(Solid(sunny50, color=YELLOW), Solid(cloudy50, color=DULL_WHITE), sync=True)
cloud75 = AnimationGroup(Solid(sunny25, color=YELLOW), Solid(cloudy75, color=DULL_WHITE), sync=True)
cloud100 = Solid(pixels, color=DULL_WHITE)
rain = AnimationGroup(Solid(top_half, color=DULL_WHITE), SparklePulse(rain_pixels, speed=0.1, period=2, color=BLUE), sync=False)
snow = AnimationGroup(Solid(top_half, color=DULL_WHITE), SparklePulse(rain_pixels, speed=0.1, period=2, color=WHITE), sync=False)

solid = Solid(pixels, color=RED)
rainbow = Rainbow(pixels, speed=0.1, period=2)
pulse = Pulse(pixels, speed=0.1, period=3, color=RED)
sparkle = Sparkle(pixels, speed=0.1, color=RED, num_sparkles=10)
r_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
c_scan = Comet(cross_strips, speed=0.2, color=PURPLE, tail_length=3, bounce=False, ring=True)
h_scan = Comet(hatch_strips, speed=0.2, color=JADE, tail_length=4, bounce=False, ring=True)
reset_strip = Solid(pixels, color=BLACK)

wth_demo = AnimationSequence(clearday, cloud25, cloud50, cloud75, cloud100, rain, snow, lightningseq1, reset_strip, lightningseq2, reset_strip, lightningseq3, reset_strip, lightningseq4, reset_strip, lightningseq5, auto_clear=True, auto_reset=True, advance_interval=5)

wth_list = [
    clearday,
    cloud25,
    cloud50,
    cloud75,
    cloud100,
    rain,
    snow
]
w_index = 0

# Setup modes and weather_anim
weather_anim = {
    '200' : cloud100,
    '300' : rain,
    '500' : rain,
    '600' : snow,
    '700' : cloud100,
    '800' : clearday,
    '801' : cloud25,
    '802' : cloud50,
    '803' : cloud75,
    '804' : cloud100
}

# Sub list [animation_object, can_change_color, can_change_intensity]
mode = [
    [rain, 'n', 'n'],   # 0: Place holder for weather mode (default)
    [solid, 'y', 'y'],     # 1: Solid color mode - Can change color (and ideally intensity)
    [rainbow, 'n', 'n'],   # 2: Rainbow mode
    [pulse, 'y', 'n'],     # 3: Pulse/Breath mode - Can change color
    [sparkle, 'y', 'n'],   # 4: Sparkle mode - Can change color
    # [p_sparkle, 'y', 'n'], # 5: Pulse Sparkle mode - Can change color
    [r_sparkle, 'n', 'n'], # 6: Rainbow Sparkle mode
    [c_scan, 'y', 'n'],    # 7: Line Scan mode - Can change color
    [h_scan, 'y', 'n'],    # 8: Grid Scan mode - Can change color
    [lightning_list[0], 'y', 'n'],  # 9: Lightning mode - Can change color
    [wth_list[w_index], 'n', 'n']
]

# Helper functions
def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

# Some basic initializing
is_enabled = True
reset_strip.animate()
curr_mode = 0
max_mode = len(mode) - 1
last_mode = curr_mode
next_update = monotonic()
if myWeather.current != 'Clouds':
    mode[0][0] = weather_anim[str(myWeather.id)[0] + '00']
else:
    mode[0][0] = weather_anim[str(myWeather.id)]

logger.info('Starting main loop')
try:
    while True:
        while (not myRemote.received()):
            if not is_enabled:
                sleep(1)
                continue
            if curr_mode == 0:
                logger.debug('Current mode is weather')
                if myWeather.update():
                    logger.info(f'Changing animation due to new weather: {myWeather.current}')
                    if myWeather.current != 'Clouds':
                        mode[0][0] = weather_anim[str(myWeather.id)[0] + '00']
                    else:
                        mode[0][0] = weather_anim[str(myWeather.id)]

            if curr_mode != last_mode:
                reset_strip.animate()
                mode[last_mode][0].reset()
                last_mode = curr_mode

            if curr_mode == 8 or (curr_mode == 0 and str(myWeather.id)[0] == '2'):
                now = monotonic()
                if now >= next_update:
                    mode[8][0].cycle_count = 0
                    mode[8][0] = lightning_list[randint(0,(len(lightning_list)-1))]
                    next_update = now + randint(1,5)
                if mode[8][0].cycle_count >= 3:
                    reset_strip.animate()
                    continue
                mode[8][0].animate()
                continue

            mode[curr_mode][0].animate()

        logger.info(f'myRemote.received() returned True.  Key: {myRemote.pressed}')
        pressed = myRemote.pressed
        if pressed == 'Mode':
            last_mode = curr_mode
            if curr_mode == max_mode:
                curr_mode = 0
            else:
                curr_mode += 1
        elif pressed in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            curr_mode = int(pressed)
        elif pressed == 'Right':
            if curr_mode != 9:
                if mode[curr_mode][1] == 'y':
                    myColor.nextColor()
                    mode[curr_mode][0].color = myColor.color
            else:
                new_idx = w_index + 1
                if new_idx > (len(wth_list) - 1):
                   new_idx = 0
                mode[curr_mode][0] = wth_list[new_idx]
        elif pressed == 'Left':
            if curr_mode != 9:
                if mode[curr_mode][1] == 'y':
                    myColor.prevColor()
                    mode[curr_mode][0].color = myColor.color
            else:
                new_idx = w_index - 1
                if new_idx < 0:
                   new_idx = (len(wth_list) - 1)
                mode[curr_mode][0] = wth_list[new_idx]
        elif pressed == 'Up':
            if mode[curr_mode][2] == 'y':
                myColor.incIntensity()
                mode[curr_mode][0].color = myColor.color
        elif pressed == 'Down':
            if mode[curr_mode][2] == 'y':
                myColor.decIntensity()
                mode[curr_mode][0].color = myColor.color
        elif pressed == 'Play':
            if is_enabled:
                reset_strip.animate()
                is_enabled = False
            else:
                is_enabled = True

finally:
    pixels.fill(0)
    pixels.show()
    myRemote.close()
    board.pin.GPIO.cleanup()
    print('Exiting Cloud App.')

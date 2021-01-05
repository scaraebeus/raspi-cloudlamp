"""
raspi-cloudlamp v0.1
By Scaraebeus (Alex P)

Interactive cloud lamp built on the Raspberry PI platform.

TODO:
* Add license info - ensure all 3rd party code/licenses are
  appropriately credited

"""

# Standard library imports
import board
from random import randint
import sys
import signal
from time import monotonic, sleep

# Application library imports
from mylog import get_logger
import remote.remote as remote
import weather.weather as weather
from remote.adafruit_remote_mapping import mapping
from secrets import secrets
import cloud_animations.colorhandler as colorhandler
from cloud_animations import pixels
from cloud_animations.animations import (
    wth_list,
    mode,
    reset_strip,
    weather_anim,
)
from cloud_animations.lightning_animations import lightning_list

# Create and setup logger
logger = get_logger(__name__)

# Setup Weather class
logger.info("Initiating Weather . . .")
try:
    myWeather = weather.Weather(appid=secrets["ow_appid"])
except KeyError:
    logger.warning("ow_appid not set in secrets file - No API Key specified")
    myWeather = weather.Weather()

# Setup IR remote
logger.info("Initiating IRRemote . . .")
myRemote = remote.IRRemote(mapping)

# Setup ColorHandler
logger.info("Initiating ColorHandler . . .")
myColor = colorhandler.ColorHandler()


def main():
    # Some basic initializing
    is_enabled = True
    reset_strip.animate()
    curr_mode = 0
    max_mode = len(mode) - 1
    last_mode = curr_mode
    next_update = monotonic()
    w_index = 0
    mode[0][0] = weather_anim[str(myWeather.id)]

    logger.info("Main loop started.")
    try:
        while True:
            while not myRemote.received():
                if not is_enabled:
                    sleep(1)
                    continue

                weather_check(curr_mode, myWeather, mode, weather_anim)

                if curr_mode != last_mode:
                    logger.debug(f"Mode changed. prev: {last_mode} new: {curr_mode}")
                    reset_strip.animate()
                    mode[last_mode][0].reset()
                    last_mode = curr_mode

                next_update = cycle_lightning(
                    curr_mode, myWeather.id, mode, lightning_list, next_update
                )

                mode[curr_mode][0].animate()

            logger.debug(f"myRemote.received() returned True.  Key: {myRemote.pressed}")
            pressed = myRemote.pressed
            if pressed == "Mode":
                last_mode = curr_mode
                if curr_mode == max_mode:
                    curr_mode = 0
                else:
                    curr_mode += 1
            elif pressed in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                curr_mode = int(pressed)
            elif pressed == "Right":
                if curr_mode != 9:
                    if mode[curr_mode][1] == "y":
                        myColor.next_color()
                        mode[curr_mode][0].color = myColor.color
                else:
                    new_idx = w_index + 1
                    if new_idx > (len(wth_list) - 1):
                        new_idx = 0
                    mode[curr_mode][0] = wth_list[new_idx]
                    w_index = new_idx
            elif pressed == "Left":
                if curr_mode != 9:
                    if mode[curr_mode][1] == "y":
                        myColor.prev_color()
                        mode[curr_mode][0].color = myColor.color
                else:
                    new_idx = w_index - 1
                    if new_idx < 0:
                        new_idx = len(wth_list) - 1
                    mode[curr_mode][0] = wth_list[new_idx]
                    w_index = new_idx
            elif pressed == "Up":
                if mode[curr_mode][2] == "y":
                    myColor.inc_intensity()
                    mode[curr_mode][0].color = myColor.color
            elif pressed == "Down":
                if mode[curr_mode][2] == "y":
                    myColor.dec_intensity()
                    mode[curr_mode][0].color = myColor.color
            elif pressed == "Play":
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
        logger.info("Exiting raspi-cloudlamp.")


# Helper functions
def sigterm_handler(_signo, _stack_frame):
    logger.info("SIGTERM received.")
    sys.exit(0)


def weather_check(c_mode, wth_cls, mode_list, anim_list):
    """If c_mode is 0 (weather mode), check to see if weather has changed.  If so, update mode_list with matching weather animation from anim_list."""
    if c_mode != 0:
        return
    if wth_cls.update():
        logger.debug(f"Changing whether animation: {wth_cls.current}")
        try:
            mode_list[c_mode][0] = anim_list[str(wth_cls.id)]
        except KeyError:
            logger.warning(f"KeyError in anim_list: {wth_cls.id} does not exist")
            mode_list[c_mode][0] = anim_list["def"]


def cycle_lightning(c_mode, wth_id, mode_list, anim_list, next_update):
    """If c_mode is 8 (lightning mode) or c_mode is 0 (weather mode) and current weather is T-Storms, cycle lightning animations."""
    if (c_mode == 8) or (c_mode == 0 and str(wth_id)[0] == "2"):
        now = monotonic()
        if now >= next_update:
            mode_list[c_mode][0] = anim_list[randint(0, (len(anim_list) - 1))]
            next_update = now + randint(1, 5)
        if mode_list[c_mode][0].cycle_count >= 3:
            mode_list[c_mode][0].cycle_count = 0
            mode_list[c_mode][0] = reset_strip
    return next_update


signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    logger.info("Starting main loop . . .")
    main()

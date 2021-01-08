""" raspi-cloudlamp v0.2
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
    next_update = monotonic()
    mode[0][0] = weather_anim[str(myWeather.id)]

    logger.info("Main loop started.")
    try:
        while True:
            while not myRemote.received():
                if not is_enabled:
                    sleep(1)
                    continue

                weather_check(curr_mode, myWeather, mode, weather_anim)

                next_update = cycle_lightning(
                    curr_mode, myWeather.id, mode, lightning_list, next_update
                )

                mode[curr_mode][0].animate()

            logger.debug(f"myRemote.received() returned True.  Key: {myRemote.pressed}")
            pressed = myRemote.pressed
            curr_mode = process_mode_change(curr_mode, pressed, mode)
            process_color_change(curr_mode, pressed, mode)
            process_intensity_change(curr_mode, pressed, mode)

            if curr_mode == 9:
                process_pattern_change(curr_mode, pressed, mode, wth_list)

            if pressed == "Play":
                is_enabled = process_startstop(is_enabled)

    finally:
        cleanup_on_exit()


# Helper functions
def sigterm_handler(_signo, _stack_frame):
    logger.info("SIGTERM received.")
    sys.exit(0)


def cleanup_on_exit():
    pixels.fill(0)
    pixels.show()
    myRemote.close()
    board.pin.GPIO.cleanup()
    logger.info("Exiting raspi-cloudlamp.")


def weather_check(c_mode, wth_cls, mode_list, anim_list, force_update=False):
    """If c_mode is 0 (weather mode), check to see if weather has changed.  If so, update mode_list with matching weather animation from anim_list."""
    if c_mode != 0:
        return
    if wth_cls.update(force_update):
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


def process_mode_change(c_mode, pressed, mode_list):
    """If Mode or Numeric keys are pressed, this function processes that request and returns the new mode state and last mode state (or current if unchanged)"""
    if pressed not in ["Mode", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        return c_mode
    if pressed == "Mode":
        if c_mode == (len(mode_list) - 1):
            new_mode = 0
        else:
            new_mode = c_mode + 1
    if pressed in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        new_mode = int(pressed)
    if pressed == "0" and c_mode == 0:
        logger.info("Forcing weather check . . .")
        weather_check(c_mode, myWeather, mode_list, weather_anim, True)
    if new_mode != c_mode:
        logger.debug(f"Mode changed. prev {c_mode} new: {new_mode}")
        reset_strip.animate()
        mode_list[c_mode][0].reset()
        return new_mode
    else:
        logger.debug("Mode unchanged.")
        return c_mode


def process_color_change(c_mode, pressed, mode_list):
    """If Right or Left keys are pressed and current mode is not weather demo, process color change."""
    if (c_mode == 9) or not (
        (mode_list[c_mode][1] == "y") and (pressed in ["Right", "Left"])
    ):
        return
    if pressed == "Right":
        myColor.next_color()
        mode_list[c_mode][0].color = myColor.color
        return
    elif pressed == "Left":
        myColor.prev_color()
        mode_list[c_mode][0].color = myColor.color
        return
    else:
        logger.warning(
            "In process_color_change - did not process color change correctly"
        )
        return


def process_intensity_change(c_mode, pressed, mode_list):
    if not ((mode_list[c_mode][2] == "y") and (pressed in ["Up", "Down"])):
        return
    if pressed == "Up":
        # myColor.inc_intensity()
        # mode_list[c_mode][0].color = myColor.color
        mode_list[c_mode][0].color = colorhandler.increase_intensity(mode_list[c_mode][0].color)
        return
    elif pressed == "Down":
        # myColor.dec_intensity()
        # mode_list[c_mode][0].color = myColor.color
        mode_list[c_mode][0].color = colorhandler.decrease_intensity(mode_list[c_mode][0].color)
        return
    else:
        logger.warning(
            "In process_intensity_change - did not process intensity change correctly."
        )
        return


def process_pattern_change(c_mode, pressed, mode_list, weather_list):
    if not ((c_mode == 9) and (pressed in ["Left", "Right"])):
        return
    cur_idx = weather_list.index(mode_list[c_mode][0])
    if pressed == "Right":
        new_idx = cur_idx + 1
        if new_idx > (len(weather_list) - 1):
            new_idx = 0
        mode_list[c_mode][0] = weather_list[new_idx]
        return
    elif pressed == "Left":
        new_idx = cur_idx - 1
        if new_idx < 0:
            new_idx = len(weather_list) - 1
        mode_list[c_mode][0] = weather_list[new_idx]
        return
    else:
        logger.warning(
            "In process_pattern_change - did not process pattern change correctly."
        )
        return


def process_startstop(enabled):
    if enabled:
        reset_strip.animate()
        return False
    elif not enabled:
        return True
    else:
        logger.warning(
            f"Recevied invalid enabled state.  Expected True/False, got: {enabled}."
        )
        return True


signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    logger.info("Starting main loop . . .")
    main()

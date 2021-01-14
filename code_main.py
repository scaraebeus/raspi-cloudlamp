""" raspi-cloudlamp v0.2
By Scaraebeus (Alex P)

Interactive cloud lamp built on the Raspberry PI platform.

TODO:
* Add license info - ensure all 3rd party code/licenses are
  appropriately credited

"""

# Standard library imports
from random import randint
import sys
import signal
from time import monotonic, sleep

# Application library imports
from mylog import get_logger
from myconfig import load_configuration, store_configuration
import remote.remote as remote
from weather.weather import Weather
from remote.adafruit_remote_mapping import mapping
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

# Load config file info
parameters = load_configuration()

# Setup Weather class
logger.info("Initiating Weather . . .")
try:
    myWeather = Weather(
        zipcode=parameters["zipcode"],
        country=parameters["country"],
        appid=parameters["ow_appid"],
    )
except KeyError:
    logger.warning("ow_appid not set in secrets file - No API Key specified")
    myWeather = Weather()

# Setup IR remote
logger.info("Initiating IRRemote . . .")
myRemote = remote.IRRemote(mapping)


def main():
    # Some basic initializing
    reset_strip.animate()
    curr_mode = parameters["current_mode"]
    day_night = myWeather.day_or_night()
    mode[0][0] = weather_anim[str(myWeather.id)][day_night]
    mode[1][0].color = parameters["mode1_color"]
    mode[3][0].color = parameters["mode3_color"]
    mode[4][0].color = parameters["mode4_color"]
    mode[6][0].color = parameters["mode6_color"]
    mode[7][0].color = parameters["mode7_color"]
    mode[9][0] = wth_list[parameters["mode9_index"]]

    weather_check_interval = 3600
    daynight_check_interval = 21600
    save_interval = 900
    next_update = monotonic()
    next_weather_check = next_update + weather_check_interval
    next_daynight_check = next_update + daynight_check_interval
    next_save_check = next_update + save_interval

    is_enabled = parameters["is_enabled"]

    logger.info("Main loop started.")
    try:
        while True:
            while not myRemote.received():
                if not is_enabled:
                    sleep(1)
                    continue

                now = monotonic()
                if now > next_weather_check:
                    weather_check(curr_mode, myWeather, mode, weather_anim)
                    next_weather_check = now + weather_check_interval

                if now > next_daynight_check:
                    day_night = process_daynight(
                        curr_mode, myWeather, mode, weather_anim, day_night
                    )
                    next_daynight_check = now + daynight_check_interval

                next_update = cycle_lightning(
                    curr_mode, myWeather.id, mode, lightning_list, next_update
                )

                if now > next_save_check:
                    save_state(parameters)
                    next_save_check = now + save_interval

                mode[curr_mode][0].animate()
                sleep(0.03)

            logger.debug(f"myRemote.received() returned True.  Key: {myRemote.pressed}")
            pressed = myRemote.pressed
            curr_mode = process_mode_change(curr_mode, pressed, mode)
            process_color_change(curr_mode, pressed, mode)
            process_intensity_change(curr_mode, pressed, mode)

            if curr_mode == 9:
                process_pattern_change(curr_mode, pressed, mode, wth_list)

            if pressed == "Play":
                is_enabled = process_startstop(is_enabled)

            if pressed == "Enter":
                save_state(parameters)
                logger.info("Current configuration saved.")

    finally:
        cleanup_on_exit()


# Helper functions
def sigterm_handler(_signo, _stack_frame):
    logger.info("SIGTERM received.")
    sys.exit(0)


def cleanup_on_exit():
    save_state(parameters)
    myRemote.close()
    pixels.deinit()
    logger.info("Exiting raspi-cloudlamp.")


def weather_check(c_mode, wth_cls, mode_list, anim_list):
    """If c_mode is 0 (weather mode), check to see if weather has changed.  If so, update mode_list with matching weather animation from anim_list."""
    if c_mode != 0:
        return
    if wth_cls.update():
        logger.debug(f"Changing whether animation: {wth_cls.id}")
        try:
            mode_list[c_mode][0] = anim_list[str(wth_cls.id)][wth_cls.day_or_night()]
        except KeyError:
            logger.warning(f"KeyError in anim_list: {wth_cls.id} does not exist")
            mode_list[c_mode][0] = anim_list["def"][wth_cls.day_or_night()]


def process_daynight(c_mode, wth_cls, mode_list, anim_list, day_night):
    if day_night == wth_cls.day_or_night():
        return day_night
    else:
        day_night = wth_cls.day_or_night()

    if c_mode != 0:
        return day_night

    mode_list[c_mode][0] = anim_list[str(wth_cls.id)][day_night]
    return day_night


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
        weather_check(c_mode, myWeather, mode_list, weather_anim)
        logger.info(
            f"Condition id: {myWeather.id} Day_night: {myWeather.day_or_night()}"
        )
    if new_mode != c_mode:
        logger.debug(f"Mode changed. prev {c_mode} new: {new_mode}")
        mode_list[c_mode][0].reset()
        reset_strip.animate()
        parameters["current_mode"] = new_mode
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
        if c_mode == 4:
            mode_list[c_mode][0].color = colorhandler.next_color(
                mode_list[c_mode][0]._sparkle_color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][
                0
            ]._sparkle_color
        elif (c_mode == 6) or (c_mode == 7):
            mode_list[c_mode][0].color = colorhandler.next_color(
                mode_list[c_mode][0]._computed_color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][
                0
            ]._computed_color
        else:
            mode_list[c_mode][0].color = colorhandler.next_color(
                mode_list[c_mode][0].color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][0].color
        return
    elif pressed == "Left":
        if c_mode == 4:
            mode_list[c_mode][0].color = colorhandler.prev_color(
                mode_list[c_mode][0]._sparkle_color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][
                0
            ]._sparkle_color
        elif (c_mode == 6) or (c_mode == 7):
            mode_list[c_mode][0].color = colorhandler.prev_color(
                mode_list[c_mode][0]._computed_color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][
                0
            ]._computed_color
        else:
            mode_list[c_mode][0].color = colorhandler.prev_color(
                mode_list[c_mode][0].color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][0].color
        return


def process_intensity_change(c_mode, pressed, mode_list):
    if not ((mode_list[c_mode][2] == "y") and (pressed in ["Up", "Down"])):
        return
    if pressed == "Up":
        if c_mode == 4:
            mode_list[c_mode][0].color = colorhandler.increase_intensity(
                mode_list[c_mode][0]._sparkle_color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][
                0
            ]._sparkle_color
        elif (c_mode == 6) or (c_mode == 7):
            mode_list[c_mode][0].color = colorhandler.increase_intensity(
                mode_list[c_mode][0]._computed_color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][
                0
            ]._computed_color
        else:
            mode_list[c_mode][0].color = colorhandler.increase_intensity(
                mode_list[c_mode][0].color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][0].color
        return
    elif pressed == "Down":
        if c_mode == 4:
            mode_list[c_mode][0].color = colorhandler.decrease_intensity(
                mode_list[c_mode][0]._sparkle_color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][
                0
            ]._sparkle_color
        elif (c_mode == 6) or (c_mode == 7):
            mode_list[c_mode][0].color = colorhandler.decrease_intensity(
                mode_list[c_mode][0]._computed_color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][
                0
            ]._computed_color
        else:
            mode_list[c_mode][0].color = colorhandler.decrease_intensity(
                mode_list[c_mode][0].color
            )
            parameters["mode" + str(c_mode) + "_color"] = mode_list[c_mode][0].color
        return


def process_pattern_change(c_mode, pressed, mode_list, weather_list):
    if not ((c_mode == 9) and (pressed in ["Left", "Right"])):
        return
    cur_idx = weather_list.index(mode_list[c_mode][0])
    if pressed == "Right":
        new_idx = cur_idx + 1
        if new_idx > (len(weather_list) - 1):
            new_idx = 0
    elif pressed == "Left":
        new_idx = cur_idx - 1
        if new_idx < 0:
            new_idx = len(weather_list) - 1
    mode_list[c_mode][0] = weather_list[new_idx]
    parameters["mode9_index"] = new_idx
    reset_strip.animate()
    return


def process_startstop(enabled):
    if enabled:
        reset_strip.animate()
        parameters["is_enabled"] = False
        return False
    elif not enabled:
        parameters["is_enabled"] = True
        return True


def save_state(parameters):
    p = load_configuration()
    has_changed = False
    for key in parameters.keys():
        if (key in p.keys()) and (parameters[key] != p[key]):
            has_changed = True
        elif key not in p.keys():
            has_changed = True
    if has_changed:
        store_configuration(parameters)
    return


signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == "__main__":
    logger.info("Starting main loop . . .")
    main()

""" colorhandler v0.2
Color handler for raspi-cloudlamp
"""

from math import floor


def next_color(rgb, step=10):
    """Helper function to increase hue value from hsv.  Step is provided in degrees"""
    h, s, v = rgb_to_hsv(rgb)
    # Normalzie step value to range of 0 to 1
    step = step / 360
    h += step
    if h > 1:
        h -= 1
    return hsv_to_rgb((h, s, v))


def prev_color(rgb, step=10):
    """Helper function to decrease hue value from hsv. Step is provided in degrees"""
    h, s, v = rgb_to_hsv(rgb)
    # Normalize step value to range of 0 to 1
    step = step / 360
    h -= step
    if h < 0:
        h += 1
    return hsv_to_rgb((h, s, v))


def increase_saturation(rgb, step=0.2):
    """Helper function to increase intensity by modifying the value from hsv"""
    h, s, v = rgb_to_hsv(rgb)
    s = min(s + step, 1)
    return hsv_to_rgb((h, s, v))


def decrease_saturation(rgb, step=0.2):
    """Helper function to increase intensity by modifying the value from hsv"""
    h, s, v = rgb_to_hsv(rgb)
    s = max(0.2, s - step)
    return hsv_to_rgb((h, s, v))


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

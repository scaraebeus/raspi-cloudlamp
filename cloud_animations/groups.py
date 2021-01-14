""" groups v0.2
Pixel groupings used by the various animations """

import random

from adafruit_led_animation.helper import PixelSubset, PixelMap

from . import pixels

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

# Setup stars groups
star_count = 12
star_set = []
while len(star_set) < star_count:
    used = [star for star in star_set]
    stars = [n for n in range(len(pixels)) if n not in used]
    s = random.choice(stars)
    star_set.append(s)

clear_night = PixelMap(pixels, star_set, individual_pixels=True)

# Lightning Path Groups
lightning_path_1 = PixelMap(
    pixels, [26, 28, 30, 19, 11, 2, 46, 42, 38], individual_pixels=True
)

lightning_path_2 = PixelMap(
    pixels, [41, 45, 4, 13, 20, 25, 27, 33, 39], individual_pixels=True
)

lightning_path_3 = PixelMap(
    pixels, [39, 31, 29, 18, 11, 7, 45, 41, 32], individual_pixels=True
)

lightning_path_4 = PixelMap(
    pixels, [6, 10, 20, 29, 17, 39, 38, 42, 47], individual_pixels=True
)

lightning_path_5 = PixelMap(
    pixels, [44, 38, 31, 17, 13, 3, 9, 38, 34], individual_pixels=True
)

lightning_path_6 = PixelMap(
    pixels, [7, 10, 11, 12, 18, 30, 32, 37, 41], individual_pixels=True
)

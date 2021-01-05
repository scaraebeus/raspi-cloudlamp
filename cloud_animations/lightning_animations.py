""" Contains all lightning based animations

Can be called into main module by importing lightning_list which contains
all of the callable Animations. """

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import WHITE
from adafruit_led_animation.sequence import AnimationSequence

from . import pixels
from .lightningflash import LightningFlash
from .groups import (
    lightning_path_1,
    lightning_path_2,
    lightning_path_3,
    lightning_path_4,
    lightning_path_5,
    lightning_path_6,
)

# Lightning Animations
lightningflash = LightningFlash(
    pixels, lower_speed=0.05, upper_speed=0.2, num_pixels=12, color=WHITE
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

lightningstreak4 = Comet(
    lightning_path_4, speed=0.03, color=WHITE, tail_length=3, bounce=False
)

lightningstreak5 = Comet(
    lightning_path_5, speed=0.03, color=WHITE, tail_length=3, bounce=False
)

lightningstreak6 = Comet(
    lightning_path_6, speed=0.03, color=WHITE, tail_length=3, bounce=False
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
    lightningstreak4,
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

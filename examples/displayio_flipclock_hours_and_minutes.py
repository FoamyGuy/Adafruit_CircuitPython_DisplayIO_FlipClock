# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT


import board
from displayio import Group
import adafruit_imageload
import time

from adafruit_displayio_flipclock.flip_clock import FlipClock

ANIMATION_DELAY = 0.01
TRANSPARENT_INDEXES = range(11)
BRIGHTER_LEVEL = 0.99
DARKER_LEVEL = 0.5
MEDIUM_LEVEL = 0.9


display = board.DISPLAY

static_spritesheet, static_palette = adafruit_imageload.load("static_sheet.bmp")
static_palette.make_transparent(0)

top_animation_spritesheet, top_animation_palette = adafruit_imageload.load("grey_top_animation_sheet.bmp")
bottom_animation_spritesheet, bottom_animation_palette = adafruit_imageload.load("grey_bottom_animation_sheet.bmp")

SPRITE_WIDTH = static_spritesheet.width // 3
SPRITE_HEIGHT = (static_spritesheet.height // 4) // 2

clock = FlipClock(
    static_spritesheet, static_palette,
    top_animation_spritesheet, top_animation_palette,
    bottom_animation_spritesheet, bottom_animation_palette,
    SPRITE_WIDTH, SPRITE_HEIGHT, anim_delay=ANIMATION_DELAY, transparent_indexes=TRANSPARENT_INDEXES,
    brighter_level=BRIGHTER_LEVEL, darker_level=DARKER_LEVEL, medium_level=MEDIUM_LEVEL
)

clock.anchor_point = (0.5, 0.5)
clock.anchored_position = (display.width//2, display.height//2)

main_group = Group()
main_group.append(clock)
board.DISPLAY.show(main_group)

cur_hour = clock.first_pair
cur_minute = clock.second_pair
next_minute = None
next_hour = None

while True:
    cur_minute = clock.second_pair
    next_minute = int(cur_minute) + 1
    if next_minute > 59:
        next_minute = 0
        clock.second_pair = str(next_minute)

        cur_hour = clock.first_pair
        next_hour = int(cur_hour) + 1
        if next_hour > 23:
            next_hour = 0

        clock.first_pair = str(next_hour)
    else:
        clock.second_pair = str(next_minute)
    time.sleep(0.1)


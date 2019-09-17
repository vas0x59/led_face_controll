import math


def chech_ch(r):
    if r < 0:
        r = 0
    elif r > 255:
        r = 255
    return int(r)


def check_color(c):
    (r, g, b) = c
    return (chech_ch(r), chech_ch(g), chech_ch(b))

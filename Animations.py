import math
from Utils import *
import time
import random
import Device
import numpy as np


class Linear_time_1:
    def __init__(self, speed=0.1):
        """
        0-100
        """
        self.prev_t = time.time()
        self.i = 0
        self.speed = speed

    def tick(self):
        now = time.time()
        dt = now - self.prev_t
        print(dt)
        if self.i >= 100:
            self.i = 0
        val = self.i
        self.i += self.speed*(1/dt)

        self.prev_t = now
        return val


class Linear_i_1:
    def __init__(self, speed=0.1):
        """
        0-100
        """
        # self.prev_t = time.time()
        self.i = 0
        self.speed = speed

    def tick(self):
        # now = time.time()
        # dt = now - self.prev_t
        # print(dt)
        if self.i >= 100:
            self.i = 0
        val = self.i
        self.i += self.speed

        # self.prev_t = now
        return val/100


class Linear2_i_1:
    def __init__(self, speed=0.1):
        """
        0-100
        """
        # self.prev_t = time.time()
        self.i = 0
        self.speed = speed
        self.dir = False

    def tick(self):
        # now = time.time()
        # dt = now - self.prev_t
        # print(dt)
        if self.i >= 100 and not self.dir:
            self.i = 0
            self.dir = not self.dir
            if self.dir:
                self.i = 100
        if self.i <= 0 and self.dir:
            self.i = 0
            self.dir = not self.dir
            if self.dir:
                self.i = 100
        val = self.i
        if self.dir:
            self.i -= self.speed
        else:
            self.i += self.speed

        # self.prev_t = now
        return val/100


class Sin_n_i_1:
    def __init__(self, speed=0.1):
        """
        0-100
        """
        # self.prev_t = time.time()
        self.i = 0
        self.speed = speed

    def tick(self):
        # now = time.time()
        # dt = now - self.prev_t
        # print(dt)
        if self.i >= 360:
            self.i = 0
        val = math.sin(math.radians(self.i))+1
        self.i += self.speed

        # self.prev_t = now
        return val/2


class RGB_sin_v1_full_led:
    def __init__(self, dev: Device.Device, speed=0.1, b_k=0.8):
        self.j = 0
        self.dev = dev
        self.speed = speed
        self.b_k = b_k
        # self.led_count = dev.led_count
        self.leds = [(0, 0, 0) for i in range(self.dev.led_count)]

    def set_color(self, n, color):
        if n < self.dev.led_count:
            self.leds[n] = check_color(
                tuple([self.dev.brightness*x for x in color]))

    def tick(self):
        # leds = []
        for i in range(self.dev.led_count):
            self.set_color(i, ((math.sin(self.j/57.296)*128+128),
                               (math.cos(self.j/57.296)*128+128),
                               ((i/self.dev.led_count*255) - (math.sin(self.j/57.296)*128+128)*self.b_k)))
            # set_color(i, int((255-j)*brit), int(j*brit), 0)
            # set_color(i, check((math.sin(self.j/57.0)*128+128) * brit),
            #           check((math.cos(self.j/57.0)*128+128) * brit),
            #           check(((i/led_count*255) - (math.sin(self.j/57.0)*128+128)*0.8)*brit))
        if self.j < 360:
            self.j += self.speed
        else:
            self.j = 0
        return self.leds


class Sin_arr_i_1:
    def __init__(self, vals_count, speed=0.1, k=1):
        """
        0-100
        """
        # self.prev_t = time.time()
        self.i = 0
        self.speed = speed
        self.vals = np.zeros(vals_count)
        self.vals_count = vals_count
        self.k = k

    def tick(self):
        # now = time.time()
        # dt = now - self.prev_t
        # print(dt)
        if self.i >= 360:
            self.i = 0
        # val = math.sin(math.radians(self.i))+1/2
        # vals[1:] = vals[0:-1]
        # vals[0] = val
        for q in range(len(self.vals)):
            self.vals[q] = (math.sin(self.i - self.speed*q*self.k)+1)/2
        self.i += self.speed

        # self.prev_t = now
        return self.vals

# class RGB_sin:

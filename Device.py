import socket
import time
import struct
import threading
import math
from Utils import *


class Device:
    def __init__(self, led_count=21, servo_count=3, brightness=0.8, update_rate=50,  ip='192.168.0.112', port=8888):
        self.led_count = led_count
        self.servo_count = servo_count
        self.ip = ip
        self.port = port
        self.update_rate = update_rate
        self.running = False
        self.brightness = brightness

        self.servos = [0 for i in range(self.servo_count)]
        self.leds = [(0, 0, 0) for i in range(self.led_count)]

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.ip, self.port))

    def send(self):
        buf = struct.pack('%sB' % (self.led_count*3+self.servo_count+1+1),
                          self.servo_count, *self.servos, self.led_count, *[self.leds[i//3][i % 3] for i in range(self.led_count*3)])
        self.sock.send(buf)

    def sender(self):
        while self.running:
            self.send()
            time.sleep(1 / self.update_rate)

    def start(self):
        self.s_th = threading.Thread(target=self.sender)
        self.s_th.daemon = True
        self.running = True
        self.s_th.start()

    def stop(self):
        self.running = False

    def set_color(self, n, color):
        if n < self.led_count:
            self.leds[n] = check_color(
                tuple([self.brightness*x for x in color]))

    def set_color_all(self, color):
        for i in range(self.led_count):
            self.set_color(i, color)

    def set_servo(self, n, servo):
        if n < self.servo_count:
            self.servos[n] = chech_ch(servo)

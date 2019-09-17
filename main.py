from Device import Device
import Animations
import math
import time
import threading


dev = Device(led_count=21, servo_count=3, brightness=0.2, update_rate=50)
dev.connect()
dev.start()


################################################################
anim_rate = 70

l1 = Animations.Linear2_i_1(speed=25/anim_rate)
l2 = Animations.Linear_i_1(speed=50/anim_rate)

sin1 = Animations.Sin_n_i_1(speed=120/anim_rate)

rgb_v1 = Animations.RGB_sin_v1_full_led(dev, speed=120/anim_rate)

anim_now = "none"


def anim():
    while True:
        if anim_now == "rgb_v1":
            rgb_v_leds = rgb_v1.tick()
            dev.leds = rgb_v_leds
        elif anim_now == "rg":
            l1_v = l1.tick()
            dev.set_color_all(((l1_v)*255, (1-l1_v)*255, 0))
        elif anim_now == "none":
            dev.set_color_all((0, 0, 0))
        time.sleep(1/anim_rate)


anim_th = threading.Thread(target=anim)
anim_th.daemon = True
anim_th.start()

anim_now = "none"
################################################################


while True:
    time.sleep(5)
    anim_now = "rg"
    time.sleep(5)
    anim_now = "rgb_v1"

    # for j in range(0, 360, 1):
    #     # if a_type != "rgb_fading_old":
    #     #     break
    #     for i in range(dev.led_count):
    #         # set_color(i, int((255-j)*brit), int(j*brit), 0)
    #         dev.set_color(i, ((math.sin(j/57.0)*128+128),
    #                       (math.cos(j/57.0)*128+128),
    #                       ((i/dev.led_count*255) - (math.sin(j/57.0)*128+128)*0.8)))
    #     # servos[1] = j
    #     # print(leds)
    #     time.sleep(0.01)

dev.stop()

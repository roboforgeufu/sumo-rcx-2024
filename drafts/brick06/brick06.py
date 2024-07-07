#!/usr/bin/env pybricks-micropython
from math import pi
from random import randint
from time import sleep

from pybricks.ev3devices import (
    ColorSensor,
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

ANGULO_ABERTURA = 800



class SumoWinged:
    def __init__(self):
        self.ev3 = EV3Brick()
        self.motor_left = Motor(Port.B)
        self.motor_right = Motor(Port.C)
        self.motor_wings = Motor(Port.A)
        self.infra_red = InfraredSensor(Port.S1)
        self.ultra_left = UltrasonicSensor(Port.S2)
        self.ultra_right = UltrasonicSensor(Port.S3)
        self.color = ColorSensor(Port.S4)
        self.wing_is_open = False
        self.motor_wings.reset_angle(0)
        self.motor_wings.reset_angle(0)

    def run(self, speed):
        self.motor_left.run(speed)
        self.motor_right.run(speed)
    
    def run_angle(self, angle, speed):
        self.motor_left.run_angle(angle, speed)
        self.motor_right.run_angle(angle, speed)

    """def wings(self):
        if not self.wing_is_open:
            self.motor_wings.dc(100)
        else:
            self.motor_wings.dc(-100)
        
        if self.motor_wings.angle() >= ANGULO_ABERTURA:
            self.wing_is_open = True
        
        if self.motor_wings.angle() <= 30:
            self.wing_is_open = False"""
    
    def wings(self):
        if not self.wing_is_open:
            direction = 1
        else:
            direction = -1
        print(self.wing_is_open)
        self.motor_wings.run_until_stalled(800 * direction, duty_limit = 60)

        if direction == -1:
            self.wing_is_open = False
        else:
            self.wing_is_open = True

    def ultrasonic_check(self):
        if self.ultra_left.distance() <= 500:
            return True
        else:
            return False
        
def main():

    tijolao = SumoWinged()
    
    dir_sign = 1

    while True:

        if tijolao.color.reflection() >= 60:
            if tijolao.infra_red.distance() <= 90:
                if not tijolao.wing_is_open:
                    tijolao.wings()
                tijolao.run(800)    
            else:
                if tijolao.ultra_leftsonic_check():
                    dir_sign = -1
                else:
                    dir_sign = 1
                if tijolao.wing_is_open:
                    tijolao.wings()
                tijolao.motor_left.run(300*dir_sign)
                tijolao.motor_right.run(-300*dir_sign)
            print(tijolao.infra_red.distance(), tijolao.color1.reflection(), tijolao.color2.reflection())

        """else:
            tijolao.run_angle(500, -300)
            print(tijolao.infra_red.distance(), tijolao.color.reflection())"""


"""def main():
    tijolao = SumoWinged()

    angulo_asas = 0
    wing_is_open = False
    tijolao.motor_wings.reset_angle(0)
    while True:
        angulo_asas = tijolao.motor_wings.angle()
        if not wing_is_open:
            tijolao.motor_wings.dc(100)
        tijolao.motor_left.run(300)
        tijolao.motor_right.run(300)
        if angulo_asas >= ANGULO_ABERTURA:
            tijolao.motor_wings.dc(0)
            wing_is_open = True
    
    print(tijolao.motor_wings.angle())"""


main()
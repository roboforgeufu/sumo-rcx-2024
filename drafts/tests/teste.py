#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep
from math import pi
from random import randint

ev3 = EV3Brick()

class Sumo:
    def _init_(self, wheel_diameter, wheel_distance):
        self.sumo_diameter = 7.7 # em cm
        self.wheel_diameter = wheel_diameter
        self.wheel_length = wheel_diameter * pi
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.A) # Motor Frontal Direito
        self.l_motor = Motor(Port.B) # Motor Traseiro Esquerdo
        self.r1_motor = Motor(Port.D) # Motor Traseiro Direito
        self.l1_motor = Motor(Port.C) # Motor Frontal Esquerdo
        self.ultra_sens1 = UltrasonicSensor(Port.S1) # Sensor ultrassônico frontal direito
        self.infra_sens2 = InfraredSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
        self.color_sens1 = ColorSensor(Port.S3) # Sensor de cor traseiro
    

brick00 = Sumo(4.2, 12.8)

def main():
    brick00.l1_motor.run(400)
    sleep(4)
    brick00.r1_motor.run(400)
    sleep(3)
    brick00.l_motor.run(400)
    sleep(2)
    brick00.r_motor.run(400)
    sleep(1)

main()
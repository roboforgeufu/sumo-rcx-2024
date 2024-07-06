#!/usr/bin/env pybricks-micropython
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


class Sumo:
    def __init__(self, wheel_diameter, wheel_distance):
        self.ev3 = EV3Brick()
        self.stopwatch = StopWatch()
        self.motor_back_right = Motor(Port.A)
        self.motor_back_left = Motor(Port.B)
        self.motor_front_right = Motor(Port.C)
        self.motor_front_left = Motor(Port.D)
        self.color_front = ColorSensor(Port.S1)
        self.ultra_front = UltrasonicSensor(Port.S2)
        self.wheel_diameter = wheel_diameter
        self.wheel_distance = wheel_distance

    def ev3_print(self, *args, clear=False, **kwargs):
        if clear:
            wait(10)
            self.brick.screen.clear()
        self.brick.screen.print(*args, **kwargs)
        print(*args, **kwargs)

    def wait_button_pressed(self, target_button=Button.CENTER):
        self.ev3.speaker.beep()
        while True:
            for button in self.ev3.buttons.pressed():
                if button == target_button:
                    break

    def walk(self, speed=100):
        self.motor_back_right.dc(speed)
        self.synku.motor_front_left.dc(-speed)
        self.motor_back_left.dc(speed)
        self.motor_front_right.dc(-speed)

    def hold_motors(self):
        self.motor_back_right.hold()
        self.motor_front_left.hold()
        self.motor_back_left.hold()
        self.motor_front_right.hold()

    def brake_motors(self):
        self.motor_back_right.brake()
        self.motor_front_left.brake()
        self.motor_back_left.brake()
        self.motor_front_right.brake()

    def turn(self, speed=35):
        self.motor_back_right.dc(-speed)
        self.motor_front_left.dc(-speed)
        self.motor_back_left.dc(speed)
        self.motor_front_right.dc(speed)


VIEW_DISTANCE = 500


def main():
    synku = Sumo(wheel_diameter=5.5, wheel_distance=11.5)

    # sleep(5)
    while True:
        distance = synku.ultra_front.distance()
        if distance < VIEW_DISTANCE:
            while synku.color_front.color() != Color.WHITE and distance < VIEW_DISTANCE:
                previous_distance = distance
                if (
                    distance != 2550
                    and synku.ultra_front.distance() < 10 * previous_distance
                ):
                    distance = synku.ultra_front.distance()
                synku.walk()
            if synku.color_front.color() == Color.WHITE:
                synku.brake_motors()
                synku.walk(speed=-80)
                sleep(1.5)
        else:
            while distance > VIEW_DISTANCE:
                distance = synku.ultra_front.distance()
                if synku.stopwatch.time() > 2000:
                    synku.turn(-35)
                    if synku.stopwatch.time() > 4000:
                        synku.stopwatch.reset()
                else:
                    synku.turn()
        synku.hold_motors()


main()

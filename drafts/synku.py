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

WHEEL_DIAMETER = 5.5
WHEEL_DISTANCE = 11.5

ev3 = EV3Brick()
stopwatch = StopWatch()
ev3.speaker.beep()

motor_back_right = Motor(Port.A)
motor_back_left = Motor(Port.B)
motor_front_right = Motor(Port.C)
motor_front_left = Motor(Port.D)
color_front = ColorSensor(Port.S1)
ultra_front = UltrasonicSensor(Port.S2)


def walk(speed = 100):
    motor_back_right.dc(speed)
    motor_front_left.dc(-speed)
    motor_back_left.dc(speed)
    motor_front_right.dc(-speed)


def hold_motors():
    motor_back_right.hold()
    motor_front_left.hold()
    motor_back_left.hold()
    motor_front_right.hold()
   
def brake_motors():
    motor_back_right.brake()
    motor_front_left.brake()
    motor_back_left.brake()
    motor_front_right.brake()


def scan(speed = 35):
    #print(speed)
    motor_back_right.dc(-speed)
    motor_front_left.dc(-speed)
    motor_back_left.dc(speed)
    motor_front_right.dc(speed)
    

def main():
    robot_distance = 500
    flag = 0
    stopwatch.reset()
    while not flag:
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1
    # sleep(5)
    while True:
        distance = ultra_front.distance()
        if distance < robot_distance:
            while(color_front.color() != Color.WHITE and distance < robot_distance):
                print(ultra_front.distance())
                previous_distance = distance
                if distance != 2550 and ultra_front.distance() < 10*previous_distance: 
                    distance = ultra_front.distance()
                walk()
            if(color_front.color() == Color.WHITE):
                brake_motors()
                walk(speed = -80)
                sleep(1.5)
            hold_motors()
        else:
            while(distance > robot_distance):
                distance = ultra_front.distance()
                if stopwatch.time() > 2000:
                    scan(-35)
                    if stopwatch.time() > 4000:
                        stopwatch.reset()
                else:
                    scan()
            hold_motors()

main()

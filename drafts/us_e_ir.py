#!/usr/bin/env pybricks-micropython
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


def ir_read_to_mm(percentage):
    # https://www.youtube.com/watch?v=kAh2cYn_seI
    if percentage <= 43:
        distance = -0.002 * percentage**2 + 0.3982 * percentage + 1.6040
    else:
        distance = 0.0177 * percentage**2 - 0.9 * percentage + 32.045

    return distance * 10


ev3 = EV3Brick()
us = UltrasonicSensor(Port.S2)
ir = InfraredSensor(Port.S1)
stopwatch = StopWatch()

logger = DataLog("time", "ir", "us", name="ir_us")

# 100% IR == 65 cm, mais ou menos
while True:
    logger.log(stopwatch.time(), ir.distance(), us.distance())
    print(
        us.distance(),
        ir_read_to_mm(ir.distance()),
        us.distance() - ir_read_to_mm(ir.distance()),
    )

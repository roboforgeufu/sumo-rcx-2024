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
    # Parábola obtida através da interpolação dos pontos (https://www.geogebra.org/m/qPAebsAc)
    # 0, 40
    # 50, 440
    # 100, 1200
    return (9 / 125) * percentage**2 + (22 / 5) * percentage + 40


ev3 = EV3Brick()
us = UltrasonicSensor(Port.S2)
ir = InfraredSensor(Port.S1)
stopwatch = StopWatch()

# logger = DataLog("us", "ir", name="ir_us")

# 100% IR == 65 cm, mais ou menos
while True:
    # logger.log(us.distance(), ir_read_to_mm(ir.distance()))
    print(
        us.distance(),
        ir_read_to_mm(ir.distance()),
        us.distance() - ir_read_to_mm(ir.distance()),
    )

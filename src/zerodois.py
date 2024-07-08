#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import (  # type: ignore
    ColorSensor,
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.media.ev3dev import ImageFile, SoundFile  # type: ignore
from pybricks.parameters import Button, Color, Direction, Port, Stop  # type: ignore
from pybricks.robotics import DriveBase  # type: ignore
from pybricks.tools import DataLog, StopWatch, wait  # type: ignore

from core.sumo import FourWheeledSumo


def main():
    zerodois = FourWheeledSumo(
        wheel_diameter=4.3,
        wheel_distance=12.7,
        right_motor_output=Port.A,
        left_motor_output=Port.D,
        right_back_motor_output=Port.C,
        left_back_motor_output=Port.B,
        floor_sensor_output=Port.S1,
        outside_floor_reflection=8,
        sensors=[
            ("us_right", UltrasonicSensor(Port.S3)),
            ("us_left", UltrasonicSensor(Port.S4)),
            ("us_middle", UltrasonicSensor(Port.S2)),
        ],
    )
    VIEW_DISTANCE = 500
    WALK_SPEED = 90
    TURN_SPEED = 50

    wait(5)

    while True:
        while zerodois.is_floor():
            if zerodois.us_middle.distance() < VIEW_DISTANCE:
                zerodois.ev3.light.on(Color.GREEN)
                zerodois.walk(WALK_SPEED)
            elif zerodois.us_left.distance() < VIEW_DISTANCE:
                zerodois.ev3.light.on(Color.YELLOW)
                zerodois.turn(-TURN_SPEED)
            elif zerodois.us_right.distance() < VIEW_DISTANCE:
                zerodois.ev3.light.on(Color.RED)
                zerodois.turn(TURN_SPEED)
            else:
                # rotina de busca
                zerodois.ev3.light.off()
                if zerodois.stopwatch.time() > 2000:
                    zerodois.turn(-TURN_SPEED)
                    if zerodois.stopwatch.time() > 4000:
                        zerodois.stopwatch.reset()
                else:
                    zerodois.turn(TURN_SPEED)

        zerodois.walk(-WALK_SPEED)
        wait(500)
        zerodois.turn(TURN_SPEED)
        wait(500)


main()

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
        floor_sensor_output=Port.S4,
        outside_floor_reflection=8,
        sensors=[
            ("us_right", InfraredSensor(Port.S2)),
            ("us_left", UltrasonicSensor(Port.S3)),
            ("back_floor", ColorSensor(Port.S1)),
            ("us_middle", ColorSensor(Port.S4)),
        ],
    )
    VIEW_DISTANCE = 500
    while True:

        middle_distance = zerodois.us_middle.distance()
        left_distance = zerodois.us_left.distance()
        right_distance = zerodois.us_right.distance()

        if (
            middle_distance < VIEW_DISTANCE
            or left_distance < VIEW_DISTANCE
            or right_distance < VIEW_DISTANCE
        ):
            while zerodois.is_floor() and (
                middle_distance < VIEW_DISTANCE
                or left_distance < VIEW_DISTANCE
                or right_distance < VIEW_DISTANCE
            ):
                previous_distance = middle_distance

                if (
                    middle_distance != 2550
                    and zerodois.us_middle_distance() < 10 * previous_distance
                ):
                    middle_distance = zerodois.us_middle_distance()

                if left_distance < VIEW_DISTANCE:
                    while not middle_distance < VIEW_DISTANCE:
                        zerodois.turn(-35)
                elif right_distance < VIEW_DISTANCE:
                    while not middle_distance < VIEW_DISTANCE:
                        zerodois.turn()
                zerodois.walk()
            if not zerodois.is_floor():
                zerodois.brake_motors()
                zerodois.walk_backwards(speed=-80, time=1500)
        else:
            while middle_distance > VIEW_DISTANCE:
                middle_distance = zerodois.us_middle_distance()
                left_distance = zerodois.us_left_distance()
                right_distance = zerodois.us_right_distance()

                if left_distance < 2550:
                    while not middle_distance < VIEW_DISTANCE:
                        zerodois.turn(50)

                elif right_distance < 2550:
                    while not middle_distance < VIEW_DISTANCE:
                        zerodois.turn(50)

                if zerodois.stopwatch.time() > 2000:
                    zerodois.turn(-35)
                    if zerodois.stopwatch.time() > 4000:
                        zerodois.stopwatch.reset()
                else:
                    zerodois.turn()
        zerodois.hold_motors()


main()

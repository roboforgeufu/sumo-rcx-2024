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
    synku = FourWheeledSumo(
        wheel_diameter=5.5,
        wheel_distance=11.5,
        right_motor_output=Port.C,
        right_back_motor_output=Port.A,
        left_motor_output=Port.D,
        left_back_motor_output=Port.B,
        floor_sensor_output=Port.S1,
        sensors=[
            ("ultra_front", UltrasonicSensor(Port.S2)),
        ],
        outside_floor_reflection=60,
    )

    VIEW_DISTANCE = 500
    while True:
        distance = synku.ultra_front.distance()
        if distance < VIEW_DISTANCE:
            while synku.is_floor() and distance < VIEW_DISTANCE:
                # Enquanto ver o inimigo dentro da arena
                previous_distance = distance
                if (
                    distance != 2550
                    and synku.ultra_front.distance() < 10 * previous_distance
                ):
                    distance = synku.ultra_front.distance()
                synku.walk()
            if not synku.is_floor():
                synku.brake_motors()
                synku.walk(speed=-80)
                wait(1500)
        else:
            while synku.ultra_front.distance() > VIEW_DISTANCE:
                if synku.stopwatch.time() > 2000:
                    synku.turn(-35)
                    if synku.stopwatch.time() > 4000:
                        synku.stopwatch.reset()
                else:
                    synku.turn()
        synku.hold_motors()


if __name__ == "__main__":
    main()

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
from core.utils import ir_read_to_mm


def bool_infrared(sensor, threshold):
    return ir_read_to_mm(sensor.distance()) < threshold


def bool_ultrassonic(us_sensor, ir_sensor, threshold):
    return (
        us_sensor.distance() == 2550 and bool_infrared(ir_sensor, threshold)
    ) or us_sensor.distance() < threshold


def main():
    zerozero = FourWheeledSumo(
        wheel_diameter=4.2,
        wheel_distance=12.8,
        right_motor_output=Port.A,
        left_motor_output=Port.D,
        right_back_motor_output=Port.C,
        left_back_motor_output=Port.B,
        floor_sensor_output=Port.S4,
        outside_floor_reflection=60,
        sensors=[
            ("ir_right", InfraredSensor(Port.S1)),
            ("us_left", UltrasonicSensor(Port.S2)),
            ("back_floor", ColorSensor(Port.S3)),
        ],
    )
    zerozero.wait_button_pressed()
    wait(5000)

    THRESHOLD = 500
    WALK_SPEED = 95
    TURN_SPEED = 95
    INFRARED_TIME_CYCLE = 500

    infrared_seen = 500  # leitura máxima
    turn_direction = 1
    last_seen = 1

    while True:
        while zerozero.is_floor():
            if turn_direction == 0:
                zerozero.walk(WALK_SPEED)
            else:
                zerozero.turn(TURN_SPEED * turn_direction)

            zerozero.ev3_print(
                zerozero.ir_right.distance(),
                zerozero.us_left.distance(),
                clear=True,
            )

            if (
                min(
                    infrared_seen,
                    zerozero.us_left.distance(),
                )
                < THRESHOLD
            ):
                if infrared_seen < THRESHOLD and bool_ultrassonic(
                    zerozero.us_left, zerozero.ir_right, THRESHOLD
                ):
                    turn_direction = 0
                    zerozero.ev3.light.on(Color.GREEN)
                elif infrared_seen < zerozero.us_left.distance():
                    turn_direction = last_seen = 1
                    zerozero.ev3.light.on(Color.RED)
                else:
                    turn_direction = last_seen = -1
                    zerozero.ev3.light.on(Color.ORANGE)
            else:
                turn_direction = last_seen

            if (
                bool_infrared(zerozero.ir_right, THRESHOLD)
                and zerozero.stopwatch.time() < INFRARED_TIME_CYCLE
            ) or ir_read_to_mm(zerozero.ir_right.distance()) < infrared_seen:
                infrared_seen = ir_read_to_mm(zerozero.ir_right.distance())

            if zerozero.stopwatch.time() > INFRARED_TIME_CYCLE:
                zerozero.stopwatch.reset()
                infrared_seen = ir_read_to_mm(zerozero.ir_right.distance())

        zerozero.walk(-WALK_SPEED)
        wait(500)
        zerozero.turn(TURN_SPEED)
        wait(500)


if __name__ == "__main__":
    main()

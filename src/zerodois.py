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

zerodois = FourWheeledSumo(
    wheel_diameter=4.3,
    wheel_distance=12.7,
    right_motor_output=Port.A,
    left_motor_output=Port.D,
    right_back_motor_output=Port.C,
    left_back_motor_output=Port.B,
    floor_sensor_output=Port.S1,
    outside_floor_reflection=60,
    sensors=[
        ("us_right", UltrasonicSensor(Port.S3)),
        ("us_left", UltrasonicSensor(Port.S4)),
        ("us_middle", UltrasonicSensor(Port.S2)),
    ],
)
VIEW_DISTANCE = 500
WALK_SPEED = 95
TURN_SPEED = 50
FAST_TURN_SPEED = 95
SEARCH_CYCLE = 2000
MAX_TURN_DEGREES = 400


def main():
    while True:
        while zerodois.is_floor():
            if zerodois.us_middle.distance() < VIEW_DISTANCE:
                # ataque
                zerodois.ev3.light.on(Color.GREEN)
                zerodois.walk(WALK_SPEED)
                zerodois.reset_motors()

            elif zerodois.us_left.distance() < VIEW_DISTANCE:
                # curva (não resetar motores aqui)
                zerodois.ev3.light.on(Color.YELLOW)
                while (
                    zerodois.us_middle.distance() > VIEW_DISTANCE
                    and zerodois.is_floor()
                    and zerodois.motor_abs_angle_mean() < MAX_TURN_DEGREES
                ):
                    zerodois.turn(-FAST_TURN_SPEED)

            elif zerodois.us_right.distance() < VIEW_DISTANCE:
                # curva (não resetar motores aqui)
                zerodois.ev3.light.on(Color.RED)
                while (
                    zerodois.us_middle.distance() > VIEW_DISTANCE
                    and zerodois.is_floor()
                    and zerodois.motor_abs_angle_mean() < MAX_TURN_DEGREES
                ):
                    zerodois.turn(FAST_TURN_SPEED)

            else:
                # rotina de busca
                zerodois.ev3.light.off()
                if zerodois.stopwatch.time() > SEARCH_CYCLE:
                    zerodois.turn(-TURN_SPEED)
                    if zerodois.stopwatch.time() > 2 * SEARCH_CYCLE:
                        zerodois.stopwatch.reset()
                else:
                    zerodois.turn(TURN_SPEED)
                zerodois.reset_motors()

        # Manobra de retorno
        zerodois.walk(-WALK_SPEED)
        wait(500)


main()

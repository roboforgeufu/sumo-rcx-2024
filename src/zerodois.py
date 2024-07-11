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
    outside_floor_reflection=8,
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


def search_routine(robot):
    if robot.stopwatch.time() > SEARCH_CYCLE:
        robot.turn(-TURN_SPEED)
        if robot.stopwatch.time() > 2 * SEARCH_CYCLE:
            robot.stopwatch.reset()
    else:
        robot.turn(TURN_SPEED)


def return_manouver(robot):
    # Manobra de retorno
    robot.walk(-WALK_SPEED)
    wait(500)


def turn_manouver(robot, direction_sign):
    while (
        robot.us_middle.distance() > VIEW_DISTANCE
        and robot.is_floor()
        and robot.motor_abs_angle_mean() < MAX_TURN_DEGREES
    ):
        robot.turn(FAST_TURN_SPEED * direction_sign)


def attack_manouver(robot, middle_distance):
    # tratativa para estouro do sensor ultrassônico
    while robot.is_floor() and middle_distance < VIEW_DISTANCE:
        previous_middle_dist = middle_distance

        new_middle_dist = robot.us_middle.distance()
        if middle_distance != 2550 and new_middle_dist < 10 * previous_middle_dist:
            # Apenas considera a nova leitura se ela não for 2550 nem muito maior (10x maior)
            middle_distance = new_middle_dist

        robot.walk(WALK_SPEED)
    return middle_distance


def main():
    while True:
        middle_distance = zerodois.us_middle.distance()

        while zerodois.is_floor():
            zerodois.ev3_print(
                zerodois.stopwatch.time(),
                zerodois.us_left.distance(),
                middle_distance,
                zerodois.us_right.distance(),
            )
            # Importante resetar os motores em todas as condições exceto nas manobras de curvas
            if middle_distance < VIEW_DISTANCE:
                # ataque
                zerodois.ev3.light.on(Color.GREEN)
                middle_distance = attack_manouver(zerodois, middle_distance)
                zerodois.reset_motors()

            elif zerodois.us_left.distance() < VIEW_DISTANCE:
                # curva (não resetar motores aqui)
                zerodois.ev3.light.on(Color.YELLOW)
                turn_manouver(zerodois, -1)

            elif zerodois.us_right.distance() < VIEW_DISTANCE:
                # curva (não resetar motores aqui)
                zerodois.ev3.light.on(Color.RED)
                turn_manouver(zerodois, 1)

            else:
                # rotina de busca
                zerodois.ev3.light.off()
                search_routine(zerodois)
                zerodois.reset_motors()

        return_manouver(zerodois)


main()

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

from random import choice

from core.sumo import Sumo

SPEED = 100
WINGS_ANGLE = 800
ULTRA_DIST = 500
INFRA_DIST = 90

tijolao = Sumo(
    wheel_diameter=5.5,
    wheel_distance=11,
    right_motor_output=Port.B,
    left_motor_output=Port.C,
    floor_sensor_output=Port.S1,
    other_motors=[
        ("wings_motor", Motor(Port.A)),
    ],
    sensors=[
        ("infra_front", InfraredSensor(Port.S2)),
        ("ultra_right", UltrasonicSensor(Port.S3)),
        ("ultra_left", UltrasonicSensor(Port.S4)),
    ],
    outside_floor_reflection=75,
)

wing_is_open = False


def wings():  # Controla o movimento das asas, decide se vai abrir ou não
    global wing_is_open
    side = 0

    if (
        tijolao.wings_motor.angle() <= 30 and not wing_is_open
    ):  # As duas variáveis são necessárias para interromper a abertura se necessário
        tijolao.wings_motor.hold()
    elif tijolao.wings_motor.angle() >= WINGS_ANGLE and wing_is_open:
        tijolao.wings_motor.hold()
    else:
        side = 1 if wing_is_open else -1

    tijolao.wings_motor.dc(100 * side)


def ultrasonic_check():
    if (
        tijolao.ultra_right.distance() <= ULTRA_DIST
        or tijolao.ultra_left.distance() <= ULTRA_DIST
    ):
        if (
            abs(tijolao.ultra_right.distance() - tijolao.ultra_left.distance()) <= 70
        ):  # Testar outros valores
            return "center"
        elif tijolao.ultra_right.distance() < tijolao.ultra_left.distance():
            return "right"
        elif tijolao.ultra_right.distance() > tijolao.ultra_left.distance():
            return "left"


def desvio(side, degrees):
    tijolao.left_motor.reset_angle(0)
    tijolao.right_motor.reset_angle(0)

    if side == "right":
        while abs(tijolao.right_motor.angle() - tijolao.left_motor.angle()) <= degrees:
            tijolao.walk(0, -100, -30)
            print(abs(tijolao.right_motor.angle() + tijolao.left_motor.angle()))
    elif side == "left":
        while abs(tijolao.left_motor.angle() - tijolao.right_motor.angle()) <= degrees:
            tijolao.walk(0, -30, -100)

    tijolao.hold_motors()


def main():
    global wing_is_open

    state = "search"
    last_state = "search"
    last_side = "none"
    direction_choice = choice([1, -1])

    tijolao.wait_button_pressed()
    wait(5000)

    while True:
        wings()
        print(wing_is_open, tijolao.wings_motor.angle())

        if state == "return":
            tijolao.ev3.light.off()
            wing_is_open = False

            while not tijolao.is_floor():
                tijolao.walk(-SPEED)
            wait(500)
            state = "search"

        elif state == "search":
            tijolao.ev3.light.on(Color.BLUE)
            if not tijolao.is_floor():
                state = "return"
                continue

            wing_is_open = True

            enemy_position = ultrasonic_check()
            if enemy_position == "center":
                tijolao.walk(30)
            else:
                direction = (
                    direction_choice
                    if enemy_position == "none"
                    else (-1 if enemy_position == "right" else 1)
                )
                direction_choice = direction

            tijolao.turn(30 * direction)

            if last_state == "bait":
                if (
                    tijolao.infra_front.distance() < INFRA_DIST
                    and ultrasonic_check() == "center"
                ):
                    state = "atk"
            else:
                if tijolao.infra_front.distance() < INFRA_DIST:
                    state = "atk"

        elif state == "atk":
            tijolao.ev3.light.on(Color.RED)
            if not tijolao.is_floor():
                state = "return"
                continue
            direction_choice = choice([1, -1])

            wing_is_open = True

            enemy_position = ultrasonic_check()
            if enemy_position == "left":
                tijolao.walk(0, SPEED * 0.85, SPEED)
            elif enemy_position == "right":
                tijolao.walk(0, SPEED, SPEED * 0.85)
            else:
                tijolao.walk(SPEED)

            if tijolao.infra_front.distance() > INFRA_DIST and enemy_position in [
                "left",
                "right",
            ]:
                last_side = enemy_position
                state = "bait"
            elif tijolao.infra_front.distance() > INFRA_DIST:
                state = "search"

        elif state == "bait":
            tijolao.ev3.light.on(Color.GREEN)
            wing_is_open = False

            desvio(last_side, 400)

            last_state = "bait"
            state = "search"


if __name__ == "__main__":
    main()

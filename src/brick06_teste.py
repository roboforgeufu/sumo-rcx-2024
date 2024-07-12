#!/usr/bin/env pybricks-micropython

from random import choice

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

from core.sumo import Sumo

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
    outside_floor_reflection=30,
)

open_wings = False
SPEED = 100
WINGS_ANGLE = 500
ULTRA_DIST = 500
INFRA_DIST = 90
CIRCLE_ANGLE = 1000
CIRCLE_DIFERENCE = 57
TURN_VALUE = 150


def reset_angle():

    tijolao.left_motor.reset_angle(0)
    tijolao.right_motor.reset_angle(0)


# Wings movement
def wings():

    side = 0
    global open_wings

    if tijolao.wings_motor.angle() <= 30 and not open_wings:
        tijolao.wings_motor.hold()

    elif tijolao.wings_motor.angle() >= WINGS_ANGLE and open_wings:
        tijolao.wings_motor.hold()

    elif open_wings:
        side = 1
    elif not open_wings:
        side = -1

    tijolao.wings_motor.dc(100 * side)


# Checks enemy position by ultrasonic
def ultrasonic_check():
    if (
        tijolao.ultra_right.distance() <= ULTRA_DIST
        or tijolao.ultra_left.distance() <= ULTRA_DIST
    ):
        if abs(tijolao.ultra_right.distance() - tijolao.ultra_left.distance()) <= 100:
            side = "center"
        elif tijolao.ultra_right.distance() < tijolao.ultra_left.distance():
            side = "right"
        elif tijolao.ultra_right.distance() > tijolao.ultra_left.distance():
            side = "left"
        else:
            side = "none"
    else:
        side = "none"

    return side


def desvio(side, degrees):

    reset_angle()

    if side == "right":
        while abs(tijolao.right_motor.angle() - tijolao.left_motor.angle()) <= degrees:
            tijolao.walk(0, -100, -30)
            print(abs(tijolao.right_motor.angle() + tijolao.left_motor.angle()))
    elif side == "left":
        while abs(tijolao.left_motor.angle() - tijolao.right_motor.angle()) <= degrees:
            tijolao.walk(0, -30, -100)

    tijolao.hold_motors()


def turn(side, degrees):

    reset_angle()

    while (
        abs(tijolao.right_motor.angle()) + abs(tijolao.left_motor.angle())
    ) / 2 <= degrees:
        if side == "right":
            tijolao.turn(100)
        elif side == "left":
            tijolao.turn(-100)


def choose_direction(button, button2):

    if button == Button.DOWN:
        if button2 == Button.RIGHT:
            while tijolao.right_motor.angle() <= CIRCLE_ANGLE:
                tijolao.walk(0, -100, -CIRCLE_DIFERENCE)
            turn("left", TURN_VALUE)

            side = -1

        elif button2 == Button.LEFT:
            while tijolao.left_motor.angle() <= CIRCLE_ANGLE:
                tijolao.walk(0, -CIRCLE_DIFERENCE, -100)
            turn("right", TURN_VALUE)

            side = 1

    if button == Button.UP:
        if button2 == Button.LEFT:
            while tijolao.right_motor.angle() <= CIRCLE_ANGLE:
                tijolao.walk(0, CIRCLE_DIFERENCE, 100)
            turn("left", TURN_VALUE)

            side = -1

        elif button2 == Button.RIGHT:
            while tijolao.left_motor.angle() <= CIRCLE_ANGLE:
                tijolao.walk(0, 100, CIRCLE_DIFERENCE)
            turn("right", TURN_VALUE)

            side = 1

    return side


def main():

    button = tijolao.wait_button_pressed(
        [Button.UP, Button.CENTER, Button.DOWN], "PATH:"
    )
    if button != Button.CENTER:
        button2 = tijolao.wait_button_pressed([Button.LEFT, Button.RIGHT], button)
        tijolao.ev3_print("PATH:\n", button, "\n", button2, clear=True)

    else:
        tijolao.ev3_print(button)

    tijolao.wait_button_pressed(Button.CENTER, "CENTER TO START")
    tijolao.ev3_print("LET'S FUCKING GO\nOOOOOOOOOOOO\nOOOOOOOOOOO", clear=True)
    wait(5000)

    if button != Button.CENTER:
        direction_choice = choose_direction(button, button2)
    else:
        direction_choice = choice([1, -1])

    global open_wings

    state = "search"  # pode ser tbm "atk" ou "return" ou "bait"
    last_state = "search"
    last_side = "none"

    while True:

        wings()

        print(open_wings, tijolao.wings_motor.angle())

        #
        # Controle de estados de movimento
        #
        # RETORNO
        if state == "return":
            tijolao.hold_motors()
            tijolao.ev3.light.off()

            # Fecha as asas
            open_wings = False

            # manobra de retorno
            while not tijolao.is_floor():
                tijolao.walk(-SPEED)
            wait(500)
            state = "search"
        # PROCURA
        elif state == "search":
            tijolao.ev3.light.on(Color.YELLOW)
            if not tijolao.is_floor():
                state = "return"
                continue

            # Abre a asa
            open_wings = True

            direction = 0

            if ultrasonic_check() == "center":
                tijolao.walk(30)
            else:
                if ultrasonic_check() == "none":
                    direction = direction_choice
                elif ultrasonic_check() == "right":
                    direction = 1
                    direction_choice = direction
                elif ultrasonic_check() == "left":
                    direction = -1
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
        # ATAQUE
        elif state == "atk":
            tijolao.ev3.light.on(Color.RED)
            if not tijolao.is_floor():
                state = "return"
                continue

            # Abre a asa
            open_wings = True

            if ultrasonic_check() == "left":
                tijolao.walk(0, SPEED * 0.85, SPEED)
            elif ultrasonic_check() == "right":
                tijolao.walk(0, SPEED, SPEED * 0.85)
            else:
                tijolao.walk(SPEED)

            if tijolao.infra_front.distance() > INFRA_DIST and (
                ultrasonic_check() == "left"
                or ultrasonic_check() == "right"
                and tijolao.ultra_right.distance() <= 100
                or tijolao.ultra_left.distance() <= 100
            ):
                last_side = ultrasonic_check()
                state = "bait"
            elif tijolao.infra_front.distance() > INFRA_DIST:
                state = "search"
        # DESVIO
        elif state == "bait":
            tijolao.ev3.light.on(Color.GREEN)

            # Fecha a asa
            open_wings = False

            desvio(last_side, 600)

            last_state = "bait"
            state = "search"


main()

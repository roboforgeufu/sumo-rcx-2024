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

tijolao = Sumo(
    wheel_diameter=5.5,
    wheel_distance=9.75,
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
    outside_floor_reflection=60,
)

wing_is_open = False
wing_is_running = False
SPEED = 100
WINGS_ANGLE = 500
ULTRA_DIST = 500


# Wings movement
def wings(side):

    global wing_is_running

    tijolao.wings_motor.reset_angle(0)
    tijolao.wings_motor.dc(100 * side)
    wing_is_running = True


# Checks enemy position by ultrasonic
def ultrasonic_check():
    if (
        tijolao.ultra_right.distance() <= ULTRA_DIST
        or tijolao.ultra_left.distance() <= ULTRA_DIST
    ):
        if abs(tijolao.ultra_right.distance() - tijolao.ultra_left.distance()) <= 70:
            side = "center"
        elif tijolao.ultra_right.distance() < tijolao.ultra_left.distance():
            side = "right"
        elif tijolao.ultra_right.distance() > tijolao.ultra_left.distance():
            side = "left"
        else:
            side = "esquece_estorado"
    else:
        side = "esquece_estorado"

    return side


def main2():
    state = "search"  # pode ser tbm "atk" ou "return"
    direction_choice = choice([1,-1])
    
    while True:
        print(state, tijolao.infra_front.distance())
        if state == "return":
            tijolao.ev3.light.on(Color.GREEN)
            # manobra de retorno
            while not tijolao.is_floor():
                tijolao.walk(-SPEED)
            wait(500)
            state = "search"
        elif state == "search":
            tijolao.ev3.light.on(Color.YELLOW)
            if not tijolao.is_floor():
                state = "return"
                continue

            # Abre a asa se ela não tiver aberta
            if ultrasonic_check() == "esquece_estorado":
                direction = direction_choice
            elif ultrasonic_check() == "right":
                direction = 1
            elif ultrasonic_check() == "left":
                direction = -1

            tijolao.turn(40 * direction)

            if tijolao.infra_front.distance() < 90:
                state = "atk"

        elif state == "atk":
            tijolao.ev3.light.on(Color.RED)
            if not tijolao.is_floor():
                state = "return"
                continue
            direction_choice = choice([1,-1])
            # Fecha a asa se ela não tiver aberta
            if ultrasonic_check() == "left":
                tijolao.walk(0, SPEED * 0.9, SPEED)
            elif ultrasonic_check() == "right":
                tijolao.walk(0, SPEED, SPEED * 0.9)
            else:
                tijolao.walk(SPEED)
            if tijolao.infra_front.distance() > 90:
                state = "search"


def main1():

    global wing_is_open
    global wing_is_running

    while True:

        is_searching = tijolao.infra_front.distance() <= 90 and not tijolao.is_floor()
        print(wing_is_open, wing_is_running)

        # Controle da abertura/fechamento das asas
        if is_searching:
            tijolao.ev3.light.on(Color.ORANGE)
            if not wing_is_open and not wing_is_running:
                wings(1)
        else:
            tijolao.ev3.light.on(Color.GREEN)
            if wing_is_open and not wing_is_running:
                wings(-1)

        # Stop wings movement
        if abs(tijolao.wings_motor.angle()) >= WINGS_ANGLE and wing_is_running:
            tijolao.wings_motor.hold()
            wing_is_running = False
            if tijolao.wings_motor.angle() > 0:
                wing_is_open = True
            else:
                wing_is_open = False


def main():
    global wing_is_open
    global wing_is_running

    while True:

        is_searching = tijolao.infra_front.distance() <= 90 and not tijolao.is_floor()
        ultra = ultrasonic_check()
        print(wing_is_open, wing_is_running)

        if is_searching:
            tijolao.ev3.light.on(Color.ORANGE)
            if not wing_is_open and not wing_is_running:
                wings(1)
        else:
            tijolao.ev3.light.on(Color.GREEN)
            if wing_is_open and not wing_is_running:
                wings(-1)

        # Stop wings movement
        if abs(tijolao.wings_motor.angle()) >= WINGS_ANGLE and wing_is_running:
            tijolao.wings_motor.hold()
            wing_is_running = False
            if tijolao.wings_motor.angle() > 0:
                wing_is_open = True
            else:
                wing_is_open = False

        # Motors movement

        # On arena
        if tijolao.is_floor():
            # Is attacking
            if not is_searching:
                direction_choice = choice([1, -1])
                if ultra == "left":
                    tijolao.walk(0, SPEED * 0.9, SPEED)
                elif ultra == "right":
                    tijolao.walk(0, SPEED, SPEED * 0.9)
                elif ultra == "center":
                    tijolao.walk(SPEED)

            # Is searching
            else:
                if ultra == "esquece_estorado":
                    direction = direction_choice
                elif ultra == "right":
                    direction = 1
                elif ultra == "left":
                    direction = -1

                tijolao.turn(40 * direction)

        # Out of arena
        else:
            while not tijolao.is_floor():
                tijolao.ev3.light.on(Color.RED)
                tijolao.walk(-SPEED)


main2()

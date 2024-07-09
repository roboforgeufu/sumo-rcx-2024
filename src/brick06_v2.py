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
    outside_floor_reflection=8,
)

wing_is_open = False
SPEED = 100
WINGS_ANGLE = 850
ULTRA_DIST = 500
INFRA_DIST = 90


def reset_angle():
    tijolao.left_motor.reset_angle(0)
    tijolao.right_motor.reset_angle(0)

# Wings movement
def wings():

    side = 0
    global wing_is_open

    if tijolao.wings_motor.angle() <= 30 and not wing_is_open:
        tijolao.wings_motor.hold()

    elif tijolao.wings_motor.angle() >= WINGS_ANGLE and wing_is_open:
        tijolao.wings_motor.hold()

    elif wing_is_open:
        side = 1
    elif not wing_is_open:
        side = -1

    tijolao.wings_motor.dc(100 * side)


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


def main():

    global wing_is_open

    print(wing_is_open, tijolao.wings_motor.angle())

    state = "search"  # pode ser tbm "atk" ou "return"
    direction_choice = choice([1, -1])

    while True:

        wings()

        print(wing_is_open, tijolao.wings_motor.angle())

        #
        # Controle de estados de movimento
        #

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

            # Abre a asa
            wing_is_open = True

            if ultrasonic_check() == "esquece_estorado":
                direction = direction_choice
            elif ultrasonic_check() == "right":
                direction = -1
                direction_choice = direction
            elif ultrasonic_check() == "left":
                direction = 1
                direction_choice = direction

            tijolao.turn(30 * direction)

            if tijolao.infra_front.distance() < INFRA_DIST:
                state = "atk"

        elif state == "atk":
            tijolao.ev3.light.on(Color.RED)
            if not tijolao.is_floor():
                state = "return"
                continue
            direction_choice = choice([1, -1])

            # Fecha a asa
            wing_is_open = False

            if ultrasonic_check() == "left":
                tijolao.walk(0, SPEED * 0.9, SPEED)
            elif ultrasonic_check() == "right":
                tijolao.walk(0, SPEED, SPEED * 0.9)
            else:
                tijolao.walk(SPEED)
            if tijolao.infra_front.distance() > INFRA_DIST:
                state = "search"

def main2():

    global wing_is_open

    print(wing_is_open, tijolao.wings_motor.angle())

    state = "search"  # pode ser tbm "atk" ou "return" ou "bait"
    last_state = "search"
    last_side = "esquece_estorado"
    direction_choice = choice([1, -1])

    while True:

        wings()

        print(wing_is_open, tijolao.wings_motor.angle())

        #
        # Controle de estados de movimento
        #

        if state == "return":
            tijolao.ev3.light.off()
            # manobra de retorno
            while not tijolao.is_floor():
                tijolao.walk(-SPEED)
            wait(500)
            state = "search"

        elif state == "search":
            tijolao.ev3.light.on(Color.BLUE)
            if not tijolao.is_floor():
                state = "return"
                continue

            # Abre a asa
            wing_is_open = True

            if ultrasonic_check() == "esquece_estorado":
                direction = direction_choice
            elif ultrasonic_check() == "right":
                direction = -1
                direction_choice = direction
            elif ultrasonic_check() == "left":
                direction = 1
                direction_choice = direction

            tijolao.turn(30 * direction)

            if last_state == "bait do fnx" and tijolao.infra_front.distance() < INFRA_DIST and ultrasonic_check() == "center":
                state = "atk"
            elif last_state != "bait do fnx" and tijolao.infra_front.distance() < INFRA_DIST:
                state = "atk"
                
        elif state == "atk":
            tijolao.ev3.light.on(Color.RED)
            if not tijolao.is_floor():
                state = "return"
                continue
            direction_choice = choice([1, -1])

            # Abre a asa
            wing_is_open = True

            if ultrasonic_check() == "left":
                tijolao.walk(0, SPEED * 0.9, SPEED)
            elif ultrasonic_check() == "right":
                tijolao.walk(0, SPEED, SPEED * 0.9)
            else:
                tijolao.walk(SPEED)

            if tijolao.infra_front.distance() > INFRA_DIST and (ultrasonic_check() == "left" or ultrasonic_check() == "right"):
                last_side = ultrasonic_check()
                state = "bait do fnx"
            elif tijolao.infra_front.distance() > INFRA_DIST:
                state = "search"

        elif state == "bait do fnx":
            tijolao.ev3.light.on(Color.GREEN)

            # Fecha a asa
            wing_is_open = False

            desvias (last_side, 90)
            
            last_state = "bait do fnx"
            state == "search"

            


                
            
def desvias(side, degrees):
    
    reset_angle()

    MOTOR_DEGREES = (degrees * tijolao.wheel_distance)/(tijolao.wheel_diameter * 360)

    if side == "right":
        while abs(tijolao.right_motor.angle() - tijolao.left_motor.angle()) <  MOTOR_DEGREES:
            tijolao.walk(0, -100, -30)
    elif side == "left":
        while abs(tijolao.left_motor.angle() - tijolao.right_motor.angle()) <  MOTOR_DEGREES:
            tijolao.walk(0, -30, -100)      



main()

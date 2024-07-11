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

def reset_angle():

    tijolao.left_motor.reset_angle(0)
    tijolao.right_motor.reset_angle(0)

# Wings movement
def wings():

    wings_side = 0
    global wing_is_open

    if tijolao.wings_motor.angle() <= 30 and not wing_is_open:
        tijolao.wings_motor.hold()
        wings_side = -1

    elif tijolao.wings_motor.angle() >= WINGS_ANGLE and wing_is_open:
        tijolao.wings_motor.hold()
        wings_side = 1

    tijolao.wings_motor.dc(100 * wings_side)


# Checks enemy position by ultrasonic
def ultrasonic_check():
    if (
        tijolao.ultra_right.distance() <= ULTRA_DIST
        or tijolao.ultra_left.distance() <= ULTRA_DIST
    ):
        if abs(tijolao.ultra_right.distance() - tijolao.ultra_left.distance()) <= 70:
            return 0 #center
        elif tijolao.ultra_right.distance() < tijolao.ultra_left.distance():
            return 1 #right
        elif tijolao.ultra_right.distance() > tijolao.ultra_left.distance():
            return -1 #left
        

def avoid(motor_side, degrees):
    
    reset_angle()

    if motor_side == 1:
        while abs(tijolao.right_motor.angle() - tijolao.left_motor.angle()) <=  degrees:
            tijolao.walk(0, -100, -30)
            print (abs(tijolao.right_motor.angle() + tijolao.left_motor.angle()))
    elif motor_side == -1:
        while abs(tijolao.left_motor.angle() - tijolao.right_motor.angle()) <=  degrees:
            tijolao.walk(0, -30, -100)      

    tijolao.hold_motors()

def main():

    global wing_is_open

    print(wing_is_open, tijolao.wings_motor.angle())

    state = "search"  # pode ser tbm "atk" ou "return" ou "bait"
    last_state = "search"
    last_side = "none"
    direction_choice = choice([1, -1])

    while True:

        wings()

        print(wing_is_open, tijolao.wings_motor.angle())

        #
        # Controle de estados de movimento
        #

        if state == "return":
            tijolao.ev3.light.off()

            # Fecha as asas
            wing_is_open = False

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

            if ultrasonic_check() == "center":
                tijolao.walk(30)
            else:
                if ultrasonic_check() == "none":
                    direction = direction_choice
                elif ultrasonic_check() == "right":
                    direction = -1
                    direction_choice = direction
                elif ultrasonic_check() == "left":
                    direction = 1
                    direction_choice = direction

            tijolao.turn(30 * direction)

            if last_state == "bait":
                if tijolao.infra_front.distance() < INFRA_DIST and ultrasonic_check() == "center":
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

            # Abre a asa
            wing_is_open = True

            if ultrasonic_check() == "left":
                tijolao.walk(0, SPEED * 0.85, SPEED)
            elif ultrasonic_check() == "right":
                tijolao.walk(0, SPEED, SPEED * 0.85)
            else:
                tijolao.walk(SPEED)

            if tijolao.infra_front.distance() > INFRA_DIST and (ultrasonic_check() == "left" or ultrasonic_check() == "right"):
                last_side = ultrasonic_check()
                state = "bait"
            elif tijolao.infra_front.distance() > INFRA_DIST:
                state = "search"

        elif state == "bait":
            tijolao.ev3.light.on(Color.GREEN)

            # Fecha a asa
            wing_is_open = False

            avoid(motor_sidet_side, 400)
            
            last_state = "bait"
            state == "search"

            
main()
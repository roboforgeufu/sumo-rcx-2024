#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.

# PARAMETERS

DIAMETRO_RODA = 5.5
DISTANCIA_RODAS = 9.66
DISTANCIA_SENSORES = 4.5
ANGULO_ABERTURA = 1000

# OBJECTS
ev3 = EV3Brick()
motorA = Motor(Port.A)
motorB = Motor(Port.B)
motorC = Motor(Port.C)

# FUNCTIONS
ev3.speaker.beep()

# Abre e fecha as asas
def wings(direction):
    
    motorA.reset_angle(0)
    motorA.run_until_stalled(800 * direction, Stop.COAST, 50)
    print(motorA.angle())
    
    
def main():

    wings(1)
    
#Start
main()
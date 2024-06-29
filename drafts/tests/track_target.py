#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

""" DOCUMENTAÇÃO: Tracks a target angle. This is similar to run_target(), but the usual smooth acceleration is skipped: 
it will move to the target angle as fast as possible. 
This method is useful if you want to continuously change the target angle.

COMENTÁRIO:
Dá o play mas não está com os motores configurados certos
"""

ev3 = EV3Brick()

class Sumo:
    def __init__(self, velocidade, wheel_diameter, wheel_distance):
        self.velocidade = velocidade
        self.wheel_diameter = wheel_diameter
        self.wheel_lenght = wheel_diameter * 3.1415
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.A) 
        self.l_motor = Motor(Port.B)
        self.r1_motor = Motor(Port.D) # Motores que levam sinais de contrário na frente deles
        self.l1_motor = Motor(Port.C) # Motores que levam sinais de contrário na frente deles
        self.ultra_sens1 = UltrasonicSensor(Port.S1) # Sensor ultrassônico frontal direito
        self.ultra_sens2 = UltrasonicSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
     
    def walk(self, speed=300): # Andar para frente, vale ressaltar que os motores de cada lado estão espelhados
        self.r_motor.run(speed)
        self.l_motor.run(speed)
        self.r1_motor.run(-speed)
        self.l1_motor.run(-speed)
    
    def track_target(self, target_angle):
        self.r_motor.track_target(target_angle)
        self.l_motor.track_target(target_angle)
        self.r1_motor.track_target(target_angle)
        self.l1_motor.track_target(target_angle)

robo_sumo = Sumo(100,4.5,11.8)

def main():
    flag = 0
    while not flag:  # Espera pelo botão central.
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1
    while True:
        robo_sumo.track_target(90)
main()
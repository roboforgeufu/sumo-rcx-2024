#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

""" DOCUMENTAÇÃO:
Runs the motor at a constant speed towards a given target angle.

The direction of rotation is automatically selected based on the target angle. 
It does matter if speed is positive or negative.

COMENTÁRIO:
Achei uma função interessante mas o problema é que, pelo que eu entendi, 
os parâmetros são com base no ângulo do motor e não ângulo real
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
    
    def run_target(self, speed, target_angle):
        self.r_motor.run_target(speed, target_angle, then=Stop.HOLD, wait=True)
        self.l_motor.run_target(speed, target_angle, then=Stop.HOLD, wait=True)
        self.r1_motor.run_target(-speed, target_angle, then=Stop.HOLD, wait=True) 
        self.l1_motor.run_target(-speed, target_angle, then=Stop.HOLD, wait=True)

robo_sumo = Sumo(100,4.5,11.8)

def main():
    flag = 0
    while not flag:  # Espera pelo botão central.
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1
    while True:
        
        robo_sumo.run_target(400,90)
main()
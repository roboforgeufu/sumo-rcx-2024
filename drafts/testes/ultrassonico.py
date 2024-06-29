#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase

""" Testar de novo depois
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

robo_sumo = Sumo(100,4.5,11.8)

flag = 0
while not flag:  # Espera pelo botão central.
    for button in ev3.buttons.pressed():
        print(button)
        if button == Button.CENTER:
            flag = 1

while True:
    robo_sumo.walk(400)

    sens1 = robo_sumo.ultra_sens1.distance()
    sens2 = robo_sumo.ultra_sens2.distance()

    while sens1 > 300 and sens2():
        print(f"sensor direito: {sens1}, sensor esquerdo: {sens2}")
        wait(10)

    robo_sumo.straight(-300)

    robo_sumo.turn(120)

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep
from math import pi
from random import randint

ev3 = EV3Brick()

class Sumo:
    def _init_(self, wheel_diameter, wheel_distance):
        self.sumo_diameter = 7.7 # em cm
        self.wheel_diameter = wheel_diameter
        self.wheel_length = wheel_diameter * pi
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.A) # Motor Frontal Direito
        self.l_motor = Motor(Port.B) # Motor Traseiro Esquerdo
        self.r1_motor = Motor(Port.C) # Motor Traseiro Direito
        self.l1_motor = Motor(Port.D) # Motor Frontal Esquerdo
        self.ultra_sens1 = UltrasonicSensor(Port.S1) # Sensor ultrassônico frontal direito
        self.infra_sens2 = InfraredSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
        self.color_sens1 = ColorSensor(Port.S3) # Sensor de cor traseiro

     
    def walk(self, speed=300): # Andar para frente, vale ressaltar que os motores de cada lado estão espelhados
        self.r_motor.run(speed)
        self.l_motor.run(speed)
        self.r1_motor.run(-speed)
        self.l1_motor.run(-speed)
    
    def attack(self, dc): # Função de ataque que controla a potência do robô
        self.r_motor.dc(dc)
        self.l_motor.dc(dc)
        self.r1_motor.dc(-dc)
        self.l1_motor.dc(-dc)


    def hold_motors(self): # Para o motor ativamente e ativamente para no ângulo em questão
        self.r_motor.dc(0)
        self.l_motor.dc(0)
        self.r1_motor.dc(0)
        self.l1_motor.dc(0)

        self.r_motor.hold()
        self.l_motor.hold()
        self.r1_motor.hold()
        self.l1_motor.hold()
    

    def reset_angle(self): # Função para resetar o ângulo dos 4 motores das rodas
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        self.r1_motor.reset_angle(0)
        self.l1_motor.reset_angle(0)


    def turn(self, angle, speed, orientation): # orientation -1 --> esquerda / orientation 1 --> direita
        self.reset_angle()
        media_motor = 0
        graus_motor = angle * (self.wheel_distance / self.wheel_diameter)
        
        while media_motor < graus_motor:
            self.l_motor.run(orientation*speed)
            self.r_motor.run(orientation*speed)
            self.r1_motor.run(orientation*-speed)
            self.l1_motor.run(orientation*-speed)
            media_motor = orientation*(self.l_motor.angle() - self.l1_motor.angle()) - orientation*(self.r_motor.angle() - self.r1_motor.angle()) / 2
        self.hold_motors()
        
    def turn_until_presence(self,speed, orientation, HOLD=True):  # orientation -1 --> esquerda / orientation 1 --> direita
        self.reset_angle()
        while not self.ultra_sens1.distance() and not self.infra_sens2.distance():
            self.l_motor.run(orientation*speed)
            self.r_motor.run(orientation*-speed)
            self.r1_motor.run(orientation*speed)
            self.l1_motor.run(orientation*-speed)
        if HOLD:
            self.hold_motors()

brick00 = Sumo(4.2, 12.8)

def main():
    flag = False
    
    while not flag:  # Espera pelo botão central
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = True

    wheel_lenght = 2*pi*((brick00.wheel_diameter)/2)
    times = 17/wheel_lenght

    brick00.r_motor.run_angle(-500, times*360, then=Stop.HOLD, wait=False)
    brick00.l_motor.run_angle(500, times*360, then=Stop.HOLD, wait=False)
    brick00.r1_motor.run_angle(500, times*360, then=Stop.HOLD, wait=False)
    brick00.l1_motor.run_angle(-500, times*360, then=Stop.HOLD, wait=True)
    while True:
        brick00.turn(90, 500, 1)
        brick00.turn(90, 500, -1)
        

    
    """curve_radius = (brick00.sumo_diameter-2*17)/2
    inner_radius = curve_radius - (brick00.wheel_distance)/2
    outter_radius = curve_radius + (brick00.wheel_distance)/2

    inner_times = 2*pi*inner_radius/wheel_lenght
    outter_times = 2*pi*outter_radius/wheel_lenght

    brick00.r_motor.run_angle(-500, inner_times*360, then=Stop.HOLD, wait=False)
    brick00.l_motor.run_angle(500, outter_times*360, then=Stop.HOLD, wait=False)
    brick00.r1_motor.run_angle(500, inner_times*360, then=Stop.HOLD, wait=False)
    brick00.l1_motor.run_angle(-500, outter_times*360, then=Stop.HOLD, wait=True)
"""

main()
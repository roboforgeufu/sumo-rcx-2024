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

ev3.speaker.beep()

class Sumo:
    def init(self, wheel_diameter, wheel_distance):
        self.sumo_diameter = 7.7 # em cm
        self.wheel_diameter = wheel_diameter
        self.wheel_length = wheel_diameter * pi
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.A) # Motor Frontal Direito
        self.l_motor = Motor(Port.B) # Motor Traseiro Esquerdo
        self.r1_motor = Motor(Port.D) # Motor Traseiro Direito
        self.l1_motor = Motor(Port.C) # Motor Frontal Esquerdo
        self.ultra_sens1 = UltrasonicSensor(Port.S1) # Sensor ultrassônico frontal direito
        self.infra_sens2 = UltrasonicSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
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
        self.r_motor.hold()
        self.l_motor.hold()
        self.r1_motor.hold()
        self.l1_motor.hold()
        

    def reset_angle(self): # Função para resetar o ângulo dos 4 motores das rodas
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        self.r1_motor.reset_angle(0)
        self.l1_motor.reset_angle(0)


    def turn(self, angle, speed): # orientation -1 --> esquerda / orientation 1 --> direita
        signal = angle/abs(angle)
        self.reset_angle()
        media_motor = 0
        graus_motor = angle * (self.wheel_distance / self.wheel_diameter)
        
        while media_motor < graus_motor:
            self.l_motor.run(signal*speed)
            self.r_motor.run(signal*speed)
            self.r1_motor.run(signal*-speed)
            self.l1_motor.run(signal*-speed)
            media_motor = signal*(self.l_motor.angle() - self.l1_motor.angle()) - orientation*(self.r_motor.angle() - self.r1_motor.angle()) / 2
        
        self.hold_motors()


    def turn_until_presence(self,speed, orientation, THRESHOLD):  # orientation -1 --> esquerda / orientation 1 --> direita
        self.reset_angle()
        while self.ultra_sens1.distance() > THRESHOLD and  self.ultra_sens1_sens2.distance() > THRESHOLD:
            self.l_motor.run(orientation*speed)
            self.r_motor.run(orientation*speed)
            self.r1_motor.run(orientation*-speed)
            self.l1_motor.run(orientation*-speed)
        

    def detect_object(self, sensor, threshold=400): # Função para retornar um booleano se detectou algo nessa distância
        return sensor.distance() < threshold


    def detect_color(self, sensor): # Função para retornar um booleano que diz se a cor identificada é branca ou não
        return sensor.color() == Color.WHITE
    

brick00 = Sumo(100, 4.2, 12.8)

def search(speed):
    side = randint(0,1)
    if side:
        brick00.turn_until_presence(speed,1)
    else:
        brick00.turn_until_presence(speed, -1)
    

def search_incrementation(angle,incrementation, speed): # Ainda não está testada
    side = randint(0,1)
    while not brick00.ultra_sens1.distance() and not brick00.infra_sens2():
        if side:
            brick00.right(angle,speed)
            angle = (2*angle) + incrementation
            side = 0 
        else:
            brick00.left(angle, speed)
            angle = (2*angle) + incrementation
            side = 1


def search_star(angle, speed=200):
    brick00.right(angle,speed)
    brick00.walk(speed)
    sleep(1.5)
    brick00.left(angle + 20, speed)
    brick00.walk(100)
    sleep(1.5)


def main():
    THRESHOLD = 700 # em mm

    wait(1)

    while True:
        brick00.turn_until_presence(500, 1, THRESHOLD)

main()
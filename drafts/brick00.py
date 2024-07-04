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
    def _init_(self, velocidade, wheel_diameter, wheel_distance):
        self.velocidade = velocidade
        self.wheel_diameter = wheel_diameter
        self.wheel_length = wheel_diameter * pi
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.A) 
        self.l_motor = Motor(Port.B)
        self.r1_motor = Motor(Port.D) # Motores que levam sinais de contrário na frente deles
        self.l1_motor = Motor(Port.C) # Motores que levam sinais de contrário na frente deles
        self.ultra_sens1 = UltrasonicSensor(Port.S1) # Sensor ultrassônico frontal direito
        self.ultra_sens2 = UltrasonicSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
        self.color_sens1 = ColorSensor(Port.S3) # Sensor de cor traseiro
        self.color_sens2 = ColorSensor(Port.S4) # Sensor de cor frontal
     
    def walk(self, speed=300): # Andar para frente, vale ressaltar que os motores de cada lado estão espelhados
        self.r_motor.run(speed)
        self.l_motor.run(speed)
        self.r1_motor.run(-speed)
        self.l1_motor.run(-speed)
    
    def attack(self, dc): # Função para testar um novo tipo de ataque
        self.r_motor.dc(dc)
        self.l_motor.dc(dc)
        self.r1_motor.dc(-dc)
        self.l1_motor.dc(-dc)

    def hold_motors(self, time=0): # Stops the motor and actively holds it at its current angle (from official documentation)
        self.r_motor.hold()
        self.l_motor.hold()
        self.r1_motor.hold()
        self.l1_motor.hold()
        sleep(time)

    def reset_angle(self): # Função para resetar o ângulo dos 4 motores das rodas
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        self.r1_motor.reset_angle(0)
        self.l1_motor.reset_angle(0)

    def right(self, angle, speed):
        self.reset_angle()
        media_motor = 0
        graus_motor = angle * (brick00.wheel_distance / brick00.wheel_diameter)
        
        while media_motor < graus_motor:
            self.l_motor.run(speed)
            self.r_motor.run(-speed)
            self.r1_motor.run(speed)
            self.l1_motor.run(-speed)
            media_motor = ((brick00.l_motor.angle() - brick00.l1_motor.angle()) - (brick00.r_motor.angle() - brick00.r1_motor.angle())) / 2
            
        self.hold_motors()

    def left(self,angle, speed):
        self.reset_angle()
        media_motor = 0
        graus_motor = angle * (brick00.wheel_distance / brick00.wheel_diameter) 
        while media_motor < graus_motor: # Para de girar até identificar que girou o ângulo ideal
            self.l_motor.run(-speed)
            self.r_motor.run(speed)
            self.r1_motor.run(-speed)
            self.l1_motor.run(speed)
            media_motor = ((- brick00.l_motor.angle() + brick00.l1_motor.angle()) - (- brick00.r_motor.angle() + brick00.r1_motor.angle())) / 2   
              
        self.hold_motors()

    def right_until(self,speed, HOLD=True): # Gira para a direita até encontrar o oponente
        self.reset_angle()
        while not brick00.ultra_sens1.distance() and not brick00.ultra_sens2.distance():
            self.l_motor.run(speed)
            self.r_motor.run(-speed)
            self.r1_motor.run(speed)
            self.l1_motor.run(-speed)
        if HOLD:
            self.hold_motors()
    
    def left_until(self,speed, HOLD=True): # Gira para a esquerda até encontrar o oponente
        self.reset_angle()

        while not brick00.ultra_sens1.distance() and not brick00.ultra_sens2.distance():
            self.l_motor.run(-speed)
            self.r_motor.run(speed)
            self.r1_motor.run(-speed)
            self.l1_motor.run(speed)
        if HOLD:
            self.hold_motors()

    def detect_object(self, sensor, threshold=100): # Função para retornar um booleano se detectou algo nessa distância
        return sensor.distance() < threshold

    def detect_color(self, sensor): # Função para retornar um booleano que diz se a cor identificada é branca ou não
        return sensor.color() == Color.WHITE
    
brick00 = Sumo(100, 4.2, 12.8)
""" Estratégias do brick00 de movimentação"""
def search(speed, HOLD):
    brick00.right_until(speed, HOLD)
    sleep(0.3)
    brick00.left_until(speed, HOLD)

def search_incrementation(angle,incrementation, speed): # Ainda não está testada
    side = randint(0,1)
    while not brick00.color_sens1() and not brick00.color_sens2():
        if side:
            brick00.right(angle,speed)
            angle = (2*angle) + incrementation
            side = 0 # Quero forçar para que na próxma entrada do loop ele vire para a esquerda primeiramente
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

def circle_search():
    if know_quadrante(know_angle, 1) == "Q4":
        brick00.right(180,400)

def know_angle(wheels_rotations, curve_radius):
    brick00_angle = ...
    return brick00_angle

def know_quadrante(brick00_angle, k):
    if brick00_angle < k*90:
        return "Q1"
    elif brick00_angle > k*90 and brick00_angle < k*180:
        return "Q2"
    elif brick00_angle > k*180 and brick00_angle < k*270:
        return "Q3"
    elif brick00_angle > k*270 and brick00_angle < k*360:
        return "Q4"
    
def stuck_wheels(): 
    return True
        return False

def tangent_attack():
    if stuck_wheels():
        brick00.walk(-300)
        sleep(0.5)
        brick00.right_until(400,HOLD=False)
        brick00.attack()
    if brick00.color_sens1.color == Color.WHITE():
        brick00.walk(300)
        sleep(2)


def align_sensors(sensor1, sensor2):
        if sensor1.distance() and not sensor2.distance(): # o que a distance retorna quando não está detectando nada?

        elif sensor2.distance() and not sensor1.distance():


def main():
    THRESHOLD = 100 # 10cm  
    flag = False
    
    while not flag:  # Espera pelo botão central
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = True
    while True:
        search_star(45, 300)

        
main()
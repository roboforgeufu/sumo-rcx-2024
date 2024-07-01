#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

ev3 = EV3Brick()

ev3.speaker.beep()

class Sumo:
    def _init_(self, velocidade, wheel_diameter, wheel_distance):
        self.velocidade = velocidade
        self.wheel_diameter = wheel_diameter
        self.wheel_lenght = wheel_diameter * 3.1415
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.A) 
        self.l_motor = Motor(Port.B)
        self.r1_motor = Motor(Port.D) # Motores que levam sinais de contrário na frente deles
        self.l1_motor = Motor(Port.C) # Motores que levam sinais de contrário na frente deles
        self.ultra_sens1 = UltrasonicSensor(Port.S1) # S ensor ultrassônico frontal direito
        self.ultra_sens2 = UltrasonicSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
        self.color_sens1 = ColorSensor(Port.S3) # Sensor de cor traseiro
        self.color_sens2 = ColorSensor(Port.S4) # Sensor de cor frontal
     
    def walk(self, speed=300): # Andar para frente, vale ressaltar que os motores de cada lado estão espelhados
        self.r_motor.run(speed)
        self.l_motor.run(speed)
        self.r1_motor.run(-speed)
        self.l1_motor.run(-speed)

    def attack(self, speed=450): # Ataque com mais velocidade
            self.r_motor.run(speed)
            self.l_motor.run(speed)
            self.r1_motor.run(-speed)
            self.l1_motor.run(-speed)
    
    def dc(self, dc): # Função para testar um novo tipo de ataque
        self.r_motor.dc(dc)
        self.l_motor.dc(dc)
        self.r1_motor.dc(-dc)
        self.l1_motor.dc(-dc)

    def hold_motors(self): # Stops the motor and actively holds it at its current angle (from official documentation)
        self.r_motor.hold()
        self.l_motor.hold()
        self.r1_motor.hold()
        self.l1_motor.hold()

    def brake_motors(self): # The motor stops due to friction, plus the voltage that is generated while the motor is still moving (from official documentation)
        self.r_motor.brake()
        self.l_motor.brake()
        self.r1_motor.brake()
        self.l1_motor.brake()

    def reset_angle(self): # Função para resetar o ângulo dos 4 motores das rodas
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        self.r1_motor.reset_angle(0)
        self.l1_motor.reset_angle(0)


brick00 = Sumo(100,4.5,11.8)

def right(angle, speed):
        brick00.reset_angle()
        
        media_motor = 0
        graus_motor = angle * (brick00.wheel_distance / brick00.wheel_diameter)
        while media_motor < graus_motor:
            brick00.l_motor.run(speed)
            brick00.r_motor.run(-speed)
            brick00.r1_motor.run(speed)
            brick00.l1_motor.run(-speed)
            
            media_motor = ((abs(brick00.l_motor.angle()) + abs(brick00.l1_motor.angle())) - (abs(brick00.r_motor.angle()) + abs(brick00.r1_motor.angle()))) / 2 
        
        brick00.hold_motors()

def right_until(speed, HOLD=True):
    brick00.reset_angle()

    while not brick00.ultra_sens1.distance() and not brick00.ultra_sens2.distance():
        brick00.l_motor.run(speed)
        brick00.r_motor.run(-speed)
        brick00.r1_motor.run(speed)
        brick00.l1_motor.run(-speed)
    if HOLD:
        brick00.hold_motors()

def left(angle, speed):
        brick00.reset_angle()
       
        media_motor = 0
        graus_motor = angle * (brick00.wheel_distance / brick00.wheel_diameter) 
        while media_motor < graus_motor: # Para de girar até identificar que girou o ângulo ideal
            brick00.l_motor.run(-speed)
            brick00.r_motor.run(speed)
            brick00.r1_motor.run(-speed)
            brick00.l1_motor.run(speed)
            
            media_motor = ((abs(brick00.l_motor.angle()) + abs(brick00.l1_motor.angle())) - (abs(brick00.r_motor.angle()) + abs(brick00.r1_motor.angle()))) / 2 
        
        brick00.hold_motors()
        
def left_until(speed, HOLD=True):
    brick00.reset_angle()

    while not brick00.ultra_sens1.distance() and not brick00.ultra_sens2.distance():
        brick00.l_motor.run(-speed)
        brick00.r_motor.run(speed)
        brick00.r1_motor.run(-speed)
        brick00.l1_motor.run(speed)
    if HOLD:
        brick00.hold_motors()

def search(speed, HOLD):
    brick00.right_until(speed, HOLD)
    sleep(0.3)
    brick00.left_unitl(speed, HOLD)

def detect_object(sensor, threshold = 100): # Talvez transformar como método da classe
    return sensor.distance() < threshold # Retornar um Booleano
        
def detect_color(sensor):
    if sensor.Color.WHITE():
        return True
    return False


""" Estratégia por enquanto: enquanto ele estiver vendo a cor preta ele continua procurando e atacando. Se identificar o branco ele vai "reto" p/ meio
Na verdade precisamos melhorar a identificação dos casos do branco, pq assim tá muito podre
"""
def main():
    THRESHOLD = 100
    flag = 0
    
    while not flag:  # Espera pelo botão central
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1
    while True:
        while not detect_color(brick00.color_sens1) and not detect_color(brick00.color2): 
            search(300, True) 
            brick00.dc(90)
        if detect_color(brick00.color_sens1):
            brick00.walk(300)
            sleep(3)
        if detect_color(brick00.color_sens2):
            brick00.walk(-300)
            sleep(3)
    
main()
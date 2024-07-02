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

    def hold_motors(self, time=0): # Stops the motor and actively holds it at its current angle (from official documentation)
        self.r_motor.hold()
        self.l_motor.hold()
        self.r1_motor.hold()
        self.l1_motor.hold()
        sleep(time)

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

    def detect_object(sensor, threshold=100):
        return sensor.distance() < threshold # Retornar um Booleano
        
    def detect_color(sensor):
        return sensor.color() == Color.WHITE

brick00 = Sumo(100, 4.2, 12.8)
""" Estratégias do brick00 de movimentação"""
def search(speed, HOLD):
    brick00.right_until(speed, HOLD)
    sleep(0.3)
    brick00.left_until(speed, HOLD)

def search_star(angle):
    brick00.right(angle,200)
    brick00.walk(100)
    sleep(1.5)
    brick00.left(angle + 20, 200)
    brick00.walk(100)
    sleep(1.5)

def main():
    THRESHOLD = 100
    flag = False
    
    while not flag:  # Espera pelo botão central
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = True
    while True:
        search_star(45)

        
main()
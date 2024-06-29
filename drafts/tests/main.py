#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

# Mesmo código que o brick00

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
        self.ultra_sens1 = UltrasonicSensor(Port.S1) # Sensor ultrassônico frontal (qual lado?)
        self.ultra_sens2 = UltrasonicSensor(Port.S2) # Sensor ultrassônico frontal (qual lado?)
     
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
    
    def free_left_curve(self, speed = 400): # Função que faz a curva com 2 motores soltos
        self.r_motor.run(speed)
        self.l_motor.run(-speed)
        self.r1_motor.stop()
        self.l1_motor.stop()

    def reset_angle(self): # Função para resetar o ângulo dos 4 motores das rodas
        self.l_motor.reset_angle(0)
        self.r_motor.reset_angle(0)
        self.r1_motor.reset_angle(0)
        self.l1_motor.reset_angle(0)

robo_sumo = Sumo(100,4.5,11.8)

def right(angle, speed):
        print("\n----------------DIREITA----------------")
        robo_sumo.reset_angle()
        
        media_motor = 0
        graus_motor = angle * (robo_sumo.wheel_distance / robo_sumo.wheel_diameter)
        while media_motor < graus_motor:
            robo_sumo.l_motor.run(speed)
            robo_sumo.r_motor.run(-speed)
            robo_sumo.r1_motor.run(speed)
            robo_sumo.l1_motor.run(-speed)
            
            media_motor = ((abs(robo_sumo.l_motor.angle()) + abs(robo_sumo.l1_motor.angle())) - (abs(robo_sumo.r_motor.angle()) + abs(robo_sumo.r1_motor.angle()))) / 2 
            print(media_motor)
        
        robo_sumo.hold_motors()

def left(angle, speed):
        print("\n----------------ESQUERDA----------------")
        robo_sumo.reset_angle()
       
        media_motor = 0
        graus_motor = angle * (robo_sumo.wheel_distance / robo_sumo.wheel_diameter) 
        
        while media_motor < graus_motor: # Para de girar até identificar que girou o ângulo ideal
            robo_sumo.l_motor.run(-speed)
            robo_sumo.r_motor.run(speed)
            robo_sumo.r1_motor.run(-speed)
            robo_sumo.l1_motor.run(speed)
            
            media_motor = ((abs(robo_sumo.l_motor.angle()) + abs(robo_sumo.l1_motor.angle())) - (abs(robo_sumo.r_motor.angle()) + abs(robo_sumo.r1_motor.angle()))) / 2 
            print(media_motor)
        
        robo_sumo.hold_motors()

def search(speed):
    robo_sumo.right(120, speed)
    robo_sumo.hold_motors()
    robo_sumo.left(240, speed)
    robo_sumo.hold_motors()
    robo_sumo.right(90, speed) # Fazer ele retornar do ponto inicial
    sleep(0.5) 

def detect_object(sensor, threshold = 100):
    threshold = 100
    return sensor.distance() < threshold # Retornar um Booleano
        
def main():
    flag = 0
    while not flag:  # Espera pelo botão central.
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1

    robo_sumo.walk()
    sleep(2)
    robo_sumo.free_left_curve()
    sleep(4)
    
    """while True:
        left_sensor = detect_object(robo_sumo.ultra_sens1.distance())
        right_sensor = detect_object(robo_sumo.ultra_sens2.distance())
    
        if left_sensor and not right_sensor:
            robo_sumo.left()
        elif right_sensor and not left_sensor:
            robo_sumo.right()
        elif right_sensor and left_sensor:
            robo_sumo.attack() # colocar nas funções a tratativa de parar se ver a linha da borda
        else:
            search()"""

main()
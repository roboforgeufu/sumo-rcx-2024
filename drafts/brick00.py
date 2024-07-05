#!/usr/bin/env pybricks-micropython
from math import pi
from random import randint
from time import sleep

from pybricks.ev3devices import (
    ColorSensor,
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait


class Sumo:
    def __init__(self, wheel_diameter, wheel_distance):
        self.brick = EV3Brick()
        self.stopwatch = StopWatch()
        self.sumo_diameter = 7.7 # em cm
        self.wheel_diameter = wheel_diameter
        self.wheel_length = wheel_diameter * pi
        self.wheel_distance = wheel_distance
        self.r_motor = Motor(Port.A) # Motor Frontal Direito
        self.l_motor = Motor(Port.B) # Motor Traseiro Esquerdo
        self.r1_motor = Motor(Port.D) # Motor Traseiro Direito
        self.l1_motor = Motor(Port.C) # Motor Frontal Esquerdo
        self.ultra_right = UltrasonicSensor(Port.S1) # Sensor ultrassônico frontal direito
        self.ultra_left = UltrasonicSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
        self.color_sens3 = ColorSensor(Port.S3) # Sensor de cor traseiro

    def ev3_print(self, *args, clear=False, **kwargs):
        if(clear):
            wait(10)
            self.brick.screen.clear()
        self.brick.screen.print(*args, **kwargs)
        print(*args, **kwargs)
     
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
    

    def loopless_turn(self, power):
        self.l_motor.dc(power)
        self.r_motor.dc(power)
        self.r1_motor.dc(-power)
        self.l1_motor.dc(-power)
        

    def turn(self, angle, speed): # orientation -1 --> esquerda / orientation 1 --> direita
        signal = angle/abs(angle)
        self.reset_angle()
        media_motor = 0
        graus_motor = angle * (self.wheel_distance / self.wheel_diameter)
        
        while media_motor < graus_motor:
            self.loopless_turn(speed)
            media_motor = signal*(self.l_motor.angle() - self.l1_motor.angle()) - signal*(self.r_motor.angle() - self.r1_motor.angle()) / 2
        
        self.hold_motors()


    def turn_until_presence(self,speed, THRESHOLD):  # orientation -1 --> esquerda / orientation 1 --> direita
        self.reset_angle()
        while self.ultra_right.distance() > THRESHOLD and self.ultra_left.distance() > THRESHOLD:
            self.loopless_turn(speed)
        

    def detect_object(self, sensor, threshold=400): # Função para retornar um booleano se detectou algo nessa distância
        return sensor.distance() < threshold


    def detect_color(self, sensor): # Função para retornar um booleano que diz se a cor identificada é branca ou não
        return sensor.color() == Color.WHITE
    

brick00 = Sumo(4.2, 12.8)

def search(speed):
    side = randint(0,1)
    if side:
        brick00.turn_until_presence(speed,1)
    else:
        brick00.turn_until_presence(speed, -1)
    

def search_incrementation(angle,incrementation, speed): # Ainda não está testada
    side = randint(0,1)
    while not brick00.ultra_right.distance() and not brick00.ultra_left.distance():
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

    logger = DataLog("time", "us_right", "us_left", name="us_finder")
    
    THRESHOLD = 500 # em mm
    ACCEPTABLE_DIFF = 100

    wait(1)

    turn_direction = 1
    last_seen = 1

    while True:

        brick00.loopless_turn(60*turn_direction)
        logger.log(brick00.stopwatch.time(), brick00.ultra_right.distance(), brick00.ultra_left.distance())
        brick00.ev3_print(
            brick00.ultra_right.distance(),
            brick00.ultra_left.distance(),
            "|",
            brick00.ultra_right.distance() - brick00.ultra_left.distance(),
            turn_direction,
            clear=True
        )

        if min(brick00.ultra_right.distance(), brick00.ultra_left.distance()) < THRESHOLD:
            if abs(brick00.ultra_right.distance() - brick00.ultra_left.distance()) <= ACCEPTABLE_DIFF:
                turn_direction = 0
                brick00.brick.light.on(Color.GREEN)
            elif brick00.ultra_right.distance() < brick00.ultra_left.distance():
                turn_direction = last_seen = 1
                brick00.brick.light.on(Color.RED)
            else:
                turn_direction = last_seen = -1
                brick00.brick.light.on(Color.ORANGE)
        else:
            turn_direction = last_seen


main()
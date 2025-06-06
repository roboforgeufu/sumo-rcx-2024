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
        self.front_right_motor = Motor(Port.A) # Motor Frontal Direito
        self.back_left_motor = Motor(Port.B) # Motor Traseiro Esquerdo
        self.front_left_motor = Motor(Port.D) # Motor Frontal Esquerdo
        self.back_right_motor = Motor(Port.C) # Motor Traseiro Direito
        self.right_infra_sens = InfraredSensor(Port.S1) # Sensor ultrassônico frontal direito
        self.left_infra_sens = InfraredSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
        self.back_color_sens = ColorSensor(Port.S3) # Sensor de cor traseiro
        self.front_color_sens = ColorSensor(Port.S4) # Sensor de cor frontal

    def ev3_print(self, *args, clear=False, **kwargs):
        if(clear):
            wait(10)
            self.brick.screen.clear()
        self.brick.screen.print(*args, **kwargs)
        print(*args, **kwargs)
     
    def walk(self, speed=300): # Andar para frente, vale ressaltar que os motores de cada lado estão espelhados
        self.front_right_motor.run(-speed)
        self.back_left_motor.run(speed)
        self.front_left_motor.run(-speed)
        self.back_right_motor.run(speed)

    def attack(self, dc): # Função de ataque que controla a potência do robô
        self.front_right_motor.dc(-dc)
        self.back_left_motor.dc(dc)
        self.front_left_motor.dc(-dc)
        self.back_right_motor.dc(dc)

    def hold_motors(self): # Para o motor ativamente e ativamente para no ângulo em questão 
        self.front_right_motor.run(0)
        self.back_left_motor.run(0)
        self.front_left_motor.run(0)
        self.back_right_motor.run(0)
        self.front_right_motor.hold()
        self.back_left_motor.hold()
        self.front_left_motor.hold()
        self.back_right_motor.hold()
        
    def reset_angle(self): # Função para resetar o ângulo dos 4 motores das rodas
        self.back_left_motor.reset_angle(0)
        self.front_right_motor.reset_angle(0)
        self.front_left_motor.reset_angle(0)
        self.back_right_motor.reset_angle(0)
    
    def loopless_turn(self, power):
        self.back_left_motor.dc(power)
        self.front_right_motor.dc(power)
        self.front_left_motor.dc(-power)
        self.back_right_motor.dc(-power)
        
    def turn(self, angle, speed): 
        signal = angle/abs(angle)
        self.reset_angle()
        media_motor = 0
        graus_motor = angle * (self.wheel_distance / self.wheel_diameter)
        
        while media_motor < graus_motor:
            self.loopless_turn(speed)
            media_motor = signal*(self.back_left_motor.angle() - self.back_right_motor.angle()) - signal*(self.front_right_motor.angle() - self.front_left_motor.angle()) / 2
        
        self.hold_motors()


    def turn_until_presence(self,speed, THRESHOLD): 
        self.reset_angle()
        while self.ultra_right.distance() > THRESHOLD and self.ultra_left.distance() > THRESHOLD:
            self.loopless_turn(speed)
        

    def detect_object(self, sensor, threshold=400):
        return sensor.distance() < threshold
    

brick00 = Sumo(4.2, 12.8)

def search(speed):
    side = randint(0,1)
    if side:
        brick00.turn_until_presence(speed,1)
    else:
        brick00.turn_until_presence(speed, -1)
    
def bool_infrared(sensor):
    THRESHOLD = 50 # %
    if sensor.distance() < THRESHOLD:
        return True
    return False

def bool_ultrassonic(sensor):
    THRESHOLD = 500 # em mm
    if (sensor.distance() == 2550 and bool_infrared()) or sensor.distance() < THRESHOLD:
        return True
    return False
    

def main():
    
    THRESHOLD = 500 # em mm
    ACCEPTABLE_DIFF = 10 # em mm
    WALK_SPEED = 90
    TURN_SPEED = 90

    flag = 0
    while not flag:
        for button in brick00.brick.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                flag = 1
    sleep(1) # lembrar de mudar para 5s
    
    turn_direction = 1
    last_seen = 1

    while True:
        while brick00.front_color_sens.reflection() < 30:
            if turn_direction == 0:
                brick00.attack(WALK_SPEED)
            else:
                brick00.loopless_turn(TURN_SPEED*turn_direction)
            
            brick00.ev3_print(brick00.right_infra_sens.distance(), brick00.left_infra_sens.distance(), clear=True)

            if bool_infrared() and bool_ultrassonic():
                    turn_direction = 0
                    brick00.brick.light.on(Color.GREEN)
            elif brick00.right_infra_sens.distance() < brick00.left_infra_sens.distance():
                turn_direction = last_seen = 1
                brick00.brick.light.on(Color.RED)
            else:
                turn_direction = last_seen = -1
                brick00.brick.light.on(Color.ORANGE)
        else:
                turn_direction = last_seen
        brick00.attack(-WALK_SPEED)
        wait(500)
        brick00.loopless_turn(TURN_SPEED)
        wait(500)

main()

#!/usr/bin/env pybricks-micropython
from math import pi

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
        self.ultra_sens1 = UltrasonicSensor(Port.S1) # Sensor ultrassônico frontal direito
        self.ultra_sens2 = UltrasonicSensor(Port.S2) # Sensor ultrassônico frontal esquerdo
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
        while self.ultra_sens1.distance() > THRESHOLD and self.ultra_sens2.distance() > THRESHOLD:
            self.loopless_turn(speed)
        

    def detect_object(self, sensor, threshold=400): # Função para retornar um booleano se detectou algo nessa distância
        return sensor.distance() < threshold


    def detect_color(self, sensor): # Função para retornar um booleano que diz se a cor identificada é branca ou não
        return sensor.color() == Color.WHITE
    

brick00 = Sumo(4.2, 12.8)


def main(): # para testar a entrada e saída dele do tapete
    while brick00.color_sens3.color != Color.WHITE:
        brick00.walk(500)
    
    wheel_lenght = 2*pi*((brick00.wheel_diameter)/2) 
    times = 5/wheel_lenght
    brick00.r_motor.run_angle(-500, times*360, then=Stop.HOLD, wait=False)
    brick00.l_motor.run_angle(500, times*360, then=Stop.HOLD, wait=False)
    brick00.r1_motor.run_angle(500, times*360, then=Stop.HOLD, wait=False)
    brick00.l1_motor.run_angle(-500, times*360, then=Stop.HOLD, wait=True)

    while brick00.color_sens3.color != Color.BLACK:
        brick00.walk(-500)

    times2 = 5/wheel_lenght
    brick00.r_motor.run_angle(-500, times2*360, then=Stop.HOLD, wait=False)
    brick00.l_motor.run_angle(500, times2*360, then=Stop.HOLD, wait=False)
    brick00.r1_motor.run_angle(500, times2*360, then=Stop.HOLD, wait=False)
    brick00.l1_motor.run_angle(-500, times2*360, then=Stop.HOLD, wait=True)

main()
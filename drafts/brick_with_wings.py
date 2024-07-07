#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

#Checar as portas e se os sensores de cor estão conectados
DIAMETRO_RD = 5.5 #DIAMETRO DA RODA
DIST_DE_RD = 9.5 #DISTANCIA ENTRE AS RODAS

ev3 = EV3Brick()
stopwatch = StopWatch()

motor_direita = Motor(Port.B) 
motor_esquerda = Motor(Port.C) 
cor_direita = ColorSensor(Port.S2) #TROCAR PORTA
cor_esquerda = ColorSensor(Port.S3) #TROCAR PORTA 
infra_red = InfraredSensor(Port.S1) 

inimigo = 100 #distancia algo do inimigo

#Função para procurar o robo inimigo enquanto não vê inimigo e o branco, ele procura
def find(): 
    while infra_red.distance() >= inimigo and cor_direita.color() == Color.WHITE and cor_esquerda.color() == Color.WHITE:
        turn(50)
        turn(-100)
    hold()

#Função para seguir em frente no ataque
def walk(speed = 100):
    motor_direita.dc(speed)
    motor_esquerda.dc(speed)

#Função para segurar no angulo o robô
def hold():
    motor_direita.hold()
    motor_esquerda.hold()

#Função para parar o robô
def brake():
    motor_direita.brake()
    motor_esquerda.brake()

def turn(graus): #melhorar a curva com as medidas corretas
    motor_direita.reset_angle(0)
    motor_esquerda.reset_angle(0)
    media_motor = 0
    graus_motor = graus * (DIST_DE_RD / DIAMETRO_RD)
    if graus > 0:
        while media_motor < graus_motor:
            motor_direita.run(200)
            motor_esquerda.run(-200)
            media_motor = (motor_direita.angle() - motor_esquerda.angle()) / 2
        
    else:
        while media_motor > graus_motor:
            motor_direita.run(-200)
            motor_esquerda.run(200)
            media_motor = (motor_direita.angle() - motor_esquerda.angle()) / 2
    hold()

def see_line(): # melhorar para voltar para a origem
    if cor_direita.color() != Color.WHITE or cor_esquerda.color() != Color.WHITE:
        brake()
        walk(-50)
        sleep(2)
        hold()
        turn(180)


def main():
    sinal = 0
    stopwatch.reset()
    while not sinal:
        for button in ev3.buttons.pressed():
            print(button)
            if button == Button.CENTER:
                sinal = 1
    sleep(2)
    while True:
        """abrir as asas PARA O BRUNO FAZER
        scaneia
        Se vê inimigo fecha asas e ataque
        Se vê branco, fazer manobra de retorno e voltar a origem
        """
        #abre asas
        #função de scanear 50 graus para a direita e 100 para esquerda
        #Talvez seja necessário aumentar esses angulos
        find()
        if infra_red.distance() < inimigo:
            #fazer o fecha asas do bruno
            while cor_direita.color() == Color.WHITE and cor_esquerda.color() == Color.WHITE:
                walk(90)
            hold()
            sleep(1)
            see_line()

        elif cor_direita.color() != Color.WHITE or cor_esquerda.color() != Color.WHITE:
            hold(1)
            see_line()
            

main()


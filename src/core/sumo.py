from time import sleep

from pybricks.ev3devices import (  # type: ignore
    ColorSensor,
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.media.ev3dev import ImageFile, SoundFile  # type: ignore
from pybricks.parameters import Button, Color, Direction, Port, Stop  # type: ignore
from pybricks.robotics import DriveBase  # type: ignore
from pybricks.tools import DataLog, StopWatch, wait  # type: ignore


class Sumo:
    """Clase básica para robô de sumô com dois motores.

    Classes de robôs mais complexos podem ser escritas a partir desta (herança).
    """

    def __init__(
        self,
        wheel_diameter,
        wheel_distance,
        right_motor_output,
        left_motor_output,
        floor_sensor_output,
        debug=True,
        sensors=[],
        outside_floor_reflection=50,
    ):
        """
        - `sensors`: lista de tuplas trazendo o nome e objeto referente ao sensor. Exemplo: ("ultra_front", UltrasonicSensor(Port.S1))
        """
        self.ev3 = EV3Brick()
        self.stopwatch = StopWatch()
        self.wheel_diameter = wheel_diameter
        self.wheel_distance = wheel_distance

        # Motores
        self.right_motor = Motor(right_motor_output)
        self.left_motor = Motor(left_motor_output)
        self.debug = debug

        self.outside_floor_reflection = outside_floor_reflection

        # Sensores principais
        self.floor_sensor = ColorSensor(floor_sensor_output)

        # Sensores secundários
        self.sensors = {s_name: s_obj for s_name, s_obj in sensors}

    def ev3_print(self, *args, clear=False, **kwargs):
        """Imprime na tela do robô e no terminal do PC ao mesmo tempo. A opção `clear` controla se a tela do EV3 é limpada a cada novo print."""
        if self.debug:
            if clear:
                wait(10)
                self.ev3.screen.clear()
            self.ev3.screen.print(*args, **kwargs)
            print(*args, **kwargs)

    def walk(self, speed=100, speed_left=None, speed_right=None):
        if speed_left is None:
            speed_left = speed
        if speed_right is None:
            speed_right = speed

        self.left_motor.dc(speed_left)
        self.right_motor_motor.dc(speed_right)

    def hold_motors(self):
        self.left_motor.hold()
        self.right_motor.hold()

    def brake_motors(self):
        self.left_motor.brake()
        self.right_motor.brake()

    def turn(self, speed=35):
        self.left_motor.dc(speed)
        self.right_motor.dc(-speed)

    def __getattr__(self, name: str):
        """Tratativa pra acesso simplificado aos sensores"""
        return self.sensors.get(name, None)

    def is_floor(self):
        ACCEPTABLE_DIFF = 5
        return (
            abs(self.floor_sensor.reflection() - self.outside_floor_reflection)
            >= ACCEPTABLE_DIFF
        )


class FourWheeledSumo(Sumo):
    def __init__(
        self,
        wheel_diameter,
        wheel_distance,
        right_motor_output,
        right_back_motor_output,
        left_motor_output,
        left_back_motor_output,
        floor_sensor_output,
        debug=True,
        sensors=[],
        outside_floor_reflection=50,
    ):
        super().__init__(
            wheel_diameter,
            wheel_distance,
            right_motor_output,
            left_motor_output,
            floor_sensor_output,
            debug,
            sensors,
            outside_floor_reflection,
        )

        # Motores traseiros (secundários)
        self.right_back_motor = Motor(right_back_motor_output)
        self.left_back_motor = Motor(left_back_motor_output)

    # override
    def walk(self, speed=100, speed_left=None, speed_right=None):
        if speed_left is None:
            speed_left = speed
        if speed_right is None:
            speed_right = speed

        self.right_back_motor.dc(speed_right)
        self.left_motor.dc(-speed_left)
        self.left_back_motor.dc(speed_left)
        self.right_motor.dc(-speed_right)

    # override
    def hold_motors(self):
        self.walk(0)
        self.right_motor.hold()
        self.right_back_motor.hold()
        self.left_back_motor.hold()
        self.left_back_motor.hold()

    # override
    def brake_motors(self):
        self.right_motor.brake()
        self.right_back_motor.brake()
        self.left_back_motor.brake()
        self.left_back_motor.brake()

    # override
    def turn(self, speed=35):
        self.right_back_motor.dc(-speed)
        self.left_motor.dc(-speed)
        self.left_back_motor.dc(speed)
        self.right_motor.dc(speed)

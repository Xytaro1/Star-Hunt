import arcade
import random
from enum import Enum
from settings import *


class PowerType(Enum):
    LIFE = "life"
    SHIELD = "shield"
    DOUBLE = "double"
    TRIPLE = "triple"
    LASER = "laser"
    RAPID = "rapid"


class PowerUp(arcade.Sprite):
    """
    Класс бафов, которые выпадают из врагов.
    """

    TEXTURES = {
        PowerType.LIFE: ":resources:images/items/coinGold.png",
        PowerType.SHIELD: ":resources:images/items/gemBlue.png",
        PowerType.DOUBLE: ":resources:images/items/gemRed.png",
        PowerType.TRIPLE: ":resources:images/items/gemGreen.png",
        PowerType.LASER: ":resources:images/items/star.png",
        PowerType.RAPID: ":resources:images/items/gemYellow.png",
    }

    # Шансы выпадения (можешь балансить игру)
    DROP_WEIGHTS = {
        PowerType.LIFE: 20,     # редкий
        PowerType.SHIELD: 10,
        PowerType.DOUBLE: 20,
        PowerType.TRIPLE: 15,
        PowerType.LASER: 20,    # имба — делаем редким
        PowerType.RAPID: 20,
    }

    def __init__(self, x, y, power_type: PowerType):
        texture = self.TEXTURES[power_type]

        super().__init__(texture, scale=0.5)

        self.center_x = x
        self.center_y = y

        self.type = power_type

        # лёгкое вращение — выглядит дороже
        self.angle = random.randint(0, 360)
        self.change_angle = random.uniform(-3, 3)

        # падение
        self.change_y = -2

    def update(self, delta_time=1/60):

        self.center_y += self.change_y
        self.angle += self.change_angle

        # удаляем если улетел
        if self.top < 0:
            self.remove_from_sprite_lists()

    @staticmethod
    def get_random_power():
        """
        Возвращает случайный баф с учетом весов.
        (намного профессиональнее random.choice)
        """

        powers = list(PowerUp.DROP_WEIGHTS.keys())
        weights = list(PowerUp.DROP_WEIGHTS.values())

        return random.choices(powers, weights=weights, k=1)[0]

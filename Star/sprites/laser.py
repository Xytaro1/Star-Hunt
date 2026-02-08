import arcade
from settings import *


class Laser(arcade.Sprite):
    """
    Класс лазера игрока.
    Лазер — это не пуля, а длинный вертикальный луч,
    который уничтожает всех врагов по линии X.
    """

    def __init__(self, x, y):
        # Инициализируем спрайт лазера
        super().__init__(
            ":resources:images/space_shooter/laserRed01.png",
            scale=1.2
        )

        # Позиция лазера по X — всегда совпадает с игроком
        self.center_x = x

        # Центр по Y ставим примерно в центр экрана,
        # потому что лазер занимает всю высоту
        self.center_y = SCREEN_HEIGHT // 2 + 100

        # Делаем лазер очень высоким — на весь экран
        self.height = SCREEN_HEIGHT

        # Узкий луч
        self.width = 18

        # Поворачиваем спрайт так, чтобы он смотрел вверх
        self.angle = 180

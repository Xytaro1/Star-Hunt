import arcade
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Star:
    """
    Класс одной звезды на фоне.
    Используется для создания эффекта движущегося звёздного неба.
    """

    def __init__(self):
        # Случайная позиция звезды на экране
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)

        # Скорость падения звезды вниз
        self.speed = random.uniform(1, 3)

        # Размер звезды (маленькие точки)
        self.size = random.randint(1, 3)

    def update(self):
        # Двигаем звезду вниз
        self.y -= self.speed

        # Если звезда ушла за нижний край экрана —
        # переносим её обратно наверх
        if self.y < 0:
            self.y = SCREEN_HEIGHT
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self):
        # Рисуем звезду как маленький белый круг
        arcade.draw_circle_filled(
            self.x,
            self.y,
            self.size,
            arcade.color.WHITE
        )

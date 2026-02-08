import arcade
from settings import *


class Player(arcade.Sprite):
    """
    Класс игрока.
    Отвечает за корабль игрока, его позицию и движение.
    """

    def __init__(self):
        # Загружаем спрайт корабля игрока
        super().__init__(
            ":resources:images/space_shooter/playerShip1_orange.png",
            scale=0.7
        )

        # Начальная позиция игрока по центру экрана
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 80

        # Направление движения:
        # -1 — влево, 1 — вправо, 0 — стоим
        self.move_dir = 0

    def update(self, delta_time=1/60):
        # Двигаем игрока влево или вправо
        self.center_x += self.move_dir * PLAYER_SPEED

        # Ограничиваем движение, чтобы корабль
        # не выходил за границы экрана
        self.center_x = max(
            30,
            min(SCREEN_WIDTH - 30, self.center_x)
        )

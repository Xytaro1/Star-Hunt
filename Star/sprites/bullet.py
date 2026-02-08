import arcade
import math
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet(arcade.Sprite):

    def __init__(self, x, y, angle, speed):
        super().__init__(
            ":resources:images/space_shooter/laserBlue01.png",
            scale=0.6
        )

        self.center_x = x
        self.center_y = y

        self.angle = angle

        # правильная физика движения по углу
        rad = math.radians(angle)
        self.change_x = math.cos(rad) * speed
        self.change_y = math.sin(rad) * speed

    def update(self, delta_time=1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if (
            self.top < 0
            or self.bottom > SCREEN_HEIGHT
            or self.left < 0
            or self.right > SCREEN_WIDTH
        ):
            self.remove_from_sprite_lists()

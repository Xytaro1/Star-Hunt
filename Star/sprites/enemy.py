import arcade
import random
from settings import *


class Enemy(arcade.Sprite):

    def __init__(self, speed, fire_rate):
        super().__init__(
            ":resources:images/space_shooter/playerShip1_green.png",
            scale=0.6
        )

        self.center_x = random.randint(40, SCREEN_WIDTH - 40)
        self.center_y = SCREEN_HEIGHT + 40

        self.speed = speed
        self.timer = random.randint(fire_rate, fire_rate + 60)

    def update(self, delta_time=1/60):
        self.center_y -= self.speed
        self.timer -= 1

        if self.top < 0:
            self.remove_from_sprite_lists()

    def can_shoot(self, fire_rate):
        if self.timer <= 0:
            self.timer = random.randint(fire_rate, fire_rate + 40)
            return True
        return False

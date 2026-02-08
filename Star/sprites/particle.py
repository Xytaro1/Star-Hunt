import arcade
import random
import math


class Particle(arcade.Sprite):

    def __init__(self, x, y, color):
        # маленький кружок
        texture = arcade.make_circle_texture(6, color)
        super().__init__(texture)

        self.center_x = x
        self.center_y = y

        # случайное направление
        angle = random.uniform(0, 360)
        speed = random.uniform(2, 6)

        self.change_x = math.cos(math.radians(angle)) * speed
        self.change_y = math.sin(math.radians(angle)) * speed

        self.life = 30  # кадров жизни

    def update(self, delta_time=1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.alpha -= 8
        self.life -= 1

        if self.life <= 0:
            self.remove_from_sprite_lists()
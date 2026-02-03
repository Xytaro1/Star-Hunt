import arcade
import random
import math
import os

# ======================================================
# НАСТРОЙКИ
# ======================================================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Space Shooter Deluxe"

SOUND_PATH = "sounds"
HIGHSCORE_FILE = "highscore.txt"

PLAYER_SPEED = 7
BULLET_SPEED = 12
START_LIVES = 3
STAR_COUNT = 120


# ======================================================
# ЗВЁЗДЫ ФОНА
# ======================================================
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(1, 4)
        self.size = random.randint(1, 3)

    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = SCREEN_HEIGHT
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.size, arcade.color.WHITE
        )


# ======================================================
# ЧАСТИЦЫ (ВЗРЫВЫ)
# ======================================================
class Particle(arcade.Sprite):
    def __init__(self, x, y, color):
        texture = arcade.make_circle_texture(4, color)
        super().__init__(texture)
        self.center_x = x
        self.center_y = y

        angle = random.uniform(0, 360)
        speed = random.uniform(2, 6)
        self.change_x = math.cos(math.radians(angle)) * speed
        self.change_y = math.sin(math.radians(angle)) * speed
        self.life = 25

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.alpha -= 10
        self.life -= 1

        if self.life <= 0:
            self.remove_from_sprite_lists()


# ======================================================
# ПУЛЯ
# ======================================================
class Bullet(arcade.Sprite):
    def __init__(self, x, y, dy):
        super().__init__(
            ":resources:images/space_shooter/laserBlue01.png",
            scale=0.6
        )
        self.center_x = x
        self.center_y = y
        self.change_y = dy
        self.angle = 90 if dy > 0 else -90

    def update(self, delta_time: float = 1 / 60):
        self.center_y += self.change_y
        if self.top < 0 or self.bottom > SCREEN_HEIGHT:
            self.remove_from_sprite_lists()


# ======================================================
# ИГРОК
# ======================================================
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(
            ":resources:images/space_shooter/playerShip1_orange.png",
            scale=0.7
        )
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 80
        self.move_dir = 0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.move_dir * PLAYER_SPEED
        self.center_x = max(30, min(SCREEN_WIDTH - 30, self.center_x))


# ======================================================
# ВРАГ
# ======================================================
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

    def update(self, delta_time: float = 1 / 60):
        self.center_y -= self.speed
        self.timer -= 1
        if self.top < 0:
            self.remove_from_sprite_lists()

    def can_shoot(self, fire_rate):
        if self.timer <= 0:
            self.timer = random.randint(fire_rate, fire_rate + 40)
            return True
        return False


# ======================================================
# МЕНЮ
# ======================================================
class MenuView(arcade.View):
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "SPACE SHOOTER",
            SCREEN_WIDTH // 2,
            450,
            arcade.color.WHITE,
            48,
            anchor_x="center"
        )
        arcade.draw_text(
            "ENTER - START",
            SCREEN_WIDTH // 2,
            350,
            arcade.color.GRAY,
            22,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            game.setup()
            self.window.show_view(game)


# ======================================================
# GAME OVER
# ======================================================
class GameOverView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH // 2,
            450,
            arcade.color.RED,
            48,
            anchor_x="center"
        )
        arcade.draw_text(
            f"Score: {self.score}",
            SCREEN_WIDTH // 2,
            350,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )
        arcade.draw_text(
            "ENTER - RESTART",
            SCREEN_WIDTH // 2,
            280,
            arcade.color.GRAY,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            game.setup()
            self.window.show_view(game)


# ======================================================
# ИГРА
# ======================================================
class GameView(arcade.View):
    def setup(self):
        # -------- ЗВУКИ --------
        self.shoot_sound = arcade.load_sound(
            os.path.join(SOUND_PATH, "shoot.wav")
        )
        self.explosion_sound = arcade.load_sound(
            os.path.join(SOUND_PATH, "explosion.wav")
        )
        self.game_over_sound = arcade.load_sound(
            os.path.join(SOUND_PATH, "game_over.wav")
        )

        # -------- РЕКОРД --------
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                self.highscore = int(f.read())
        else:
            self.highscore = 0

        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullets = arcade.SpriteList()
        self.enemy_bullets = arcade.SpriteList()
        self.particles = arcade.SpriteList()

        self.player_list.append(self.player)
        self.stars = [Star() for _ in range(STAR_COUNT)]

        self.score = 0
        self.lives = START_LIVES
        self.level = 1
        self.spawn_timer = 0

    def on_draw(self):
        self.clear()

        for star in self.stars:
            star.draw()

        arcade.draw_text(
            f"Highscore: {self.highscore}",
            10, 70,
            arcade.color.AQUA,
            16
        )

        self.player_list.draw()
        self.enemy_list.draw()
        self.player_bullets.draw()
        self.enemy_bullets.draw()
        self.particles.draw()

        arcade.draw_text(f"Score: {self.score}", 10, 10, arcade.color.WHITE, 16)
        arcade.draw_text(f"Lives: {self.lives}", 10, 30, arcade.color.RED, 16)
        arcade.draw_text(f"Level: {self.level}", 10, 50, arcade.color.YELLOW, 16)

    def on_update(self, delta_time: float):
        for star in self.stars:
            star.update()

        self.level = 1 + self.score // 10
        enemy_speed = 2 + self.level
        fire_rate = max(25, 80 - self.level * 6)
        spawn_rate = max(20, 50 - self.level * 4)

        self.spawn_timer += 1
        if self.spawn_timer % spawn_rate == 0:
            self.enemy_list.append(Enemy(enemy_speed, fire_rate))

        self.player_list.update()
        self.enemy_list.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.particles.update()

        for enemy in self.enemy_list:
            if enemy.can_shoot(fire_rate):
                self.enemy_bullets.append(
                    Bullet(enemy.center_x, enemy.bottom, -8)
                )

        for bullet in self.player_bullets:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.enemy_list
            )
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    arcade.play_sound(self.explosion_sound)
                    self.score += 1
                    for _ in range(20):
                        self.particles.append(
                            Particle(
                                enemy.center_x,
                                enemy.center_y,
                                arcade.color.YELLOW
                            )
                        )

        if arcade.check_for_collision_with_list(
            self.player, self.enemy_bullets
        ):
            for bullet in arcade.check_for_collision_with_list(
                self.player, self.enemy_bullets
            ):
                bullet.remove_from_sprite_lists()

            self.lives -= 1
            for _ in range(25):
                self.particles.append(
                    Particle(
                        self.player.center_x,
                        self.player.center_y,
                        arcade.color.RED
                    )
                )

            if self.lives <= 0:
                arcade.play_sound(self.game_over_sound)
                if self.score > self.highscore:
                    with open(HIGHSCORE_FILE, "w") as f:
                        f.write(str(self.score))
                self.window.show_view(GameOverView(self.score))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.player_bullets.append(
                Bullet(self.player.center_x, self.player.top, BULLET_SPEED)
            )
            arcade.play_sound(self.shoot_sound)

        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.move_dir = -1
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.player.move_dir = 1

    def on_key_release(self, key, modifiers):
        if key in (
            arcade.key.LEFT,
            arcade.key.RIGHT,
            arcade.key.A,
            arcade.key.D
        ):
            self.player.move_dir = 0


# ======================================================
# ЗАПУСК
# ======================================================
def main():
    window = arcade.Window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_TITLE
    )
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()

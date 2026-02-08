import arcade
import random
import os
import math

from settings import *

from sprites.player import Player
from sprites.enemy import Enemy
from sprites.bullet import Bullet
from sprites.powerup import PowerUp, PowerType
from sprites.star import Star
from utils.power_manager import PowerManager


class GameView(arcade.View):

    def __init__(self, difficulty="normal"):
        super().__init__()

        # выбранная сложность (easy / normal / expert)
        self.difficulty = difficulty

        # менеджер бафов
        self.powers = PowerManager()

        # лазер (отдельный список спрайтов)
        self.laser_list = arcade.SpriteList()
        self.laser_active = False

        # игрок (создаётся в setup)
        self.player = None

        # списки спрайтов
        self.player_list = None
        self.enemy_list = None
        self.player_bullets = None
        self.enemy_bullets = None
        self.powerups = None

        # частицы взрыва
        self.particles = arcade.SpriteList()

        # игровые параметры
        self.score = 0
        self.level = 1
        self.spawn_timer = 0

        # таймеры бафов (в кадрах)
        self.shield_timer = 0
        self.double_timer = 0
        self.triple_timer = 0
        self.laser_timer = 0
        self.rapid_timer = 0


    # --------------------------------------------------
    # Подготовка игры (вызывается один раз при старте)
    # --------------------------------------------------
    def setup(self):
        from settings import DIFFICULTIES

        # настройки сложности
        config = DIFFICULTIES[self.difficulty]
        self.lives = config["lives"]

        # загрузка звуков
        self.shoot_sound = arcade.load_sound(
            os.path.join(SOUND_PATH, "shoot.wav")
        )

        self.explosion_sound = arcade.load_sound(
            os.path.join(SOUND_PATH, "explosion.wav")
        )

        self.game_over_sound = arcade.load_sound(
            os.path.join(SOUND_PATH, "game_over.wav")
        )

        # создание игрока
        self.player = Player()

        # инициализация списков спрайтов
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullets = arcade.SpriteList()
        self.enemy_bullets = arcade.SpriteList()
        self.powerups = arcade.SpriteList()

        self.player_list.append(self.player)

        # фоновые звёзды
        self.stars = [Star() for _ in range(120)]


    # --------------------------------------------------
    # Отрисовка кадра
    # --------------------------------------------------
    def on_draw(self):

        self.clear()

        # фон
        for star in self.stars:
            star.draw()

        # все игровые объекты
        self.laser_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.player_bullets.draw()
        self.enemy_bullets.draw()
        self.powerups.draw()
        self.particles.draw()

        # UI: счёт
        arcade.draw_text(
            f"Score: {self.score}",
            10, 10,
            arcade.color.WHITE,
            16
        )

        # UI: жизни
        arcade.draw_text(
            f"Lives: {self.lives}",
            10, 30,
            arcade.color.RED,
            16
        )

        # UI: уровень
        arcade.draw_text(
            f"Level: {self.level}",
            10, 50,
            arcade.color.YELLOW,
            16
        )

        # визуализация щита
        if self.powers.active("shield"):
            arcade.draw_circle_outline(
                self.player.center_x,
                self.player.center_y,
                45,
                arcade.color.CYAN,
                4
            )


    # --------------------------------------------------
    # Логика игры (обновляется каждый кадр)
    # --------------------------------------------------
    def on_update(self, delta_time):
        from settings import DIFFICULTIES
        config = DIFFICULTIES[self.difficulty]

        # обновление бафов и частиц
        self.powers.update()
        self.particles.update()

        # движение звёзд
        for star in self.stars:
            star.update()

        # уровень растёт от счёта
        self.level = 1 + self.score // 10

        # параметры врагов зависят от сложности и уровня
        enemy_speed = config["enemy_speed"] + self.level
        fire_rate = max(10, config["enemy_fire_rate"] - self.level * 2)
        spawn_rate = max(20, config["spawn_rate"] - self.level * 2)

        # таймер спавна врагов
        self.spawn_timer += 1
        if self.spawn_timer % spawn_rate == 0:
            self.enemy_list.append(
                Enemy(enemy_speed, fire_rate)
            )

        # если активен лазер — двигаем его вместе с игроком
        if self.laser_active and self.laser_list:
            laser = self.laser_list[0]
            laser.center_x = self.player.center_x

            # уничтожение врагов лучом
            for enemy in self.enemy_list[:]:
                if abs(enemy.center_x - laser.center_x) < 20:
                    arcade.play_sound(self.explosion_sound, volume=0.4)
                    enemy.remove_from_sprite_lists()
                    self.score += 1

        # обновление всех спрайтов
        self.player_list.update()
        self.enemy_list.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.powerups.update()

        # уменьшение таймеров бафов
        self.shield_timer = max(0, self.shield_timer - 1)
        self.double_timer = max(0, self.double_timer - 1)
        self.triple_timer = max(0, self.triple_timer - 1)
        self.laser_timer = max(0, self.laser_timer - 1)
        self.rapid_timer = max(0, self.rapid_timer - 1)

        # стрельба врагов
        for enemy in self.enemy_list:
            if enemy.can_shoot(fire_rate):
                bullet = Bullet(
                    enemy.center_x,
                    enemy.bottom,
                    270,  # вниз
                    config["enemy_bullet_speed"]
                )
                self.enemy_bullets.append(bullet)

        # попадание пуль игрока по врагам
        from sprites.particle import Particle

        for bullet in self.player_bullets:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.enemy_list
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for enemy in hit_list:
                    # частицы взрыва
                    for _ in range(20):
                        self.particles.append(
                            Particle(
                                enemy.center_x,
                                enemy.center_y,
                                arcade.color.YELLOW
                            )
                        )

                    enemy.remove_from_sprite_lists()
                    arcade.play_sound(self.explosion_sound)
                    self.score += 1

                    # дроп бафа
                    if random.random() < 1:
                        power_type = random.choice(list(PowerType))
                        power = PowerUp(enemy.center_x, enemy.center_y, power_type)
                        self.powerups.append(power)

        # подбор бафов игроком
        collected = arcade.check_for_collision_with_list(
            self.player, self.powerups
        )

        for power in collected:
            self.apply_power(power.type)
            power.remove_from_sprite_lists()

        # попадание по игроку
        if self.shield_timer <= 0:
            if arcade.check_for_collision_with_list(
                    self.player, self.enemy_bullets):

                for bullet in arcade.check_for_collision_with_list(
                        self.player, self.enemy_bullets):
                    bullet.remove_from_sprite_lists()

                if self.powers.active("shield"):
                    # щит ломается
                    self.powers.timers["shield"] = 0
                else:
                    self.lives -= 1

                # конец игры
                if self.lives <= 0:
                    from views.game_over_view import GameOverView
                    self.window.show_view(
                        GameOverView(self.score, self.difficulty)
                    )


    # --------------------------------------------------
    # Применение бафов
    # --------------------------------------------------
    def apply_power(self, power_type):

        if power_type == PowerType.LIFE:
            self.lives += 1

        elif power_type == PowerType.SHIELD:
            self.powers.activate("shield", 300)

        elif power_type == PowerType.DOUBLE:
            self.double_timer = 300

        elif power_type == PowerType.TRIPLE:
            self.triple_timer = 300

        elif power_type == PowerType.LASER:
            self.laser_timer = 240

        elif power_type == PowerType.RAPID:
            self.rapid_timer = 300


    # --------------------------------------------------
    # Нажатия клавиш
    # --------------------------------------------------
    def on_key_press(self, key, modifiers):

        # движение игрока
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.move_dir = -1

        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.move_dir = 1

        # стрельба
        if key == arcade.key.SPACE:

            # лазер
            if self.laser_timer > 0 and not self.laser_active:
                from sprites.laser import Laser
                laser = Laser(self.player.center_x, self.player.top)
                self.laser_list.append(laser)
                self.laser_active = True
                return

            # тройной выстрел
            elif self.triple_timer > 0:
                for angle in [80, 90, 100]:
                    bullet = Bullet(
                        self.player.center_x,
                        self.player.top,
                        angle,
                        BULLET_SPEED
                    )
                    self.player_bullets.append(bullet)

            # двойной выстрел
            elif self.double_timer > 0:
                for offset in [-12, 12]:
                    bullet = Bullet(
                        self.player.center_x + offset,
                        self.player.top,
                        90,
                        BULLET_SPEED
                    )
                    self.player_bullets.append(bullet)

            # обычный выстрел
            else:
                bullet = Bullet(
                    self.player.center_x,
                    self.player.top,
                    90,
                    BULLET_SPEED
                )
                self.player_bullets.append(bullet)

            arcade.play_sound(self.shoot_sound)


    # --------------------------------------------------
    # Отпускание клавиш
    # --------------------------------------------------
    def on_key_release(self, key, modifiers):

        # выключение лазера
        if key == arcade.key.SPACE and self.laser_active:
            self.laser_list.clear()
            self.laser_active = False

        # остановка движения
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.move_dir = 0

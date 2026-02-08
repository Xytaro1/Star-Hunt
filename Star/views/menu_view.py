import arcade
from settings import *


class MenuView(arcade.View):
    """
    Главное меню игры
    """

    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.selected_difficulty = "normal"

    def on_show_view(self):
        """
        Вызывается при открытии меню
        """
        arcade.set_background_color(self.background_color)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            f"DIFFICULTY: {self.selected_difficulty.upper()}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 40,
            arcade.color.YELLOW,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            "1 - EASY    2 - NORMAL    3 - EXPERT",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 80,
            arcade.color.GRAY,
            16,
            anchor_x="center"
        )

        # Заголовок
        arcade.draw_text(
            "STAR HUNT",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 120,
            arcade.color.WHITE,
            48,
            anchor_x="center"
        )

        # Кнопка старта
        arcade.draw_text(
            "PRESS ENTER TO START",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.GRAY,
            24,
            anchor_x="center"
        )

        # Управление
        arcade.draw_text(
            "Move: A / D  or  ← →\nShoot: SPACE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
            align="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.KEY_1:
            self.selected_difficulty = "easy"

        elif key == arcade.key.KEY_2:
            self.selected_difficulty = "normal"

        elif key == arcade.key.KEY_3:
            self.selected_difficulty = "expert"

        elif key == arcade.key.ENTER:
            from views.game_view import GameView

            game = GameView(self.selected_difficulty)
            game.setup()
            self.window.show_view(game)

import arcade
from settings import HIGHSCORE_FILE, SCREEN_WIDTH, SCREEN_HEIGHT
import os
from settings import SOUND_PATH


# -------------------------------
# Загрузка рекорда из файла
# -------------------------------
def load_highscore():
    try:
        # Пытаемся открыть файл с рекордом
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except:
        # Если файла нет или ошибка — рекорд = 0
        return 0


# -------------------------------
# Сохранение рекорда в файл
# -------------------------------
def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))


# ==================================================
# ЭКРАН GAME OVER (появляется после смерти игрока)
# ==================================================
class GameOverView(arcade.View):

    def __init__(self, score, difficulty):
        super().__init__()

        # Загружаем звук поражения
        self.game_over_sound = arcade.load_sound(
            os.path.join(SOUND_PATH, "game_over.wav")
        )

        # Счёт за текущую игру
        self.score = score

        # Сложность (нужна для корректного рестарта)
        self.difficulty = difficulty

        # Загружаем рекорд
        self.highscore = load_highscore()

        # Если текущий счёт больше рекорда — обновляем
        if self.score > self.highscore:
            self.highscore = self.score
            save_highscore(self.highscore)


    # ----------------------------------------------
    # Вызывается, когда экран показывается
    # ----------------------------------------------
    def on_show_view(self):
        # Устанавливаем чёрный фон
        arcade.set_background_color(arcade.color.BLACK)

        # Проигрываем звук поражения
        arcade.play_sound(self.game_over_sound)


    # ----------------------------------------------
    # Отрисовка экрана Game Over
    # ----------------------------------------------
    def on_draw(self):
        self.clear()

        # Заголовок GAME OVER
        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 140,
            arcade.color.RED,
            48,
            anchor_x="center"
        )

        # Текущий результат
        arcade.draw_text(
            f"Your Score: {self.score}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 60,
            arcade.color.WHITE,
            28,
            anchor_x="center"
        )

        # Лучший результат
        arcade.draw_text(
            f"High Score: {self.highscore}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 20,
            arcade.color.GOLD,
            24,
            anchor_x="center"
        )

        # Подсказка — рестарт
        arcade.draw_text(
            "Press ENTER to Restart",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 60,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center"
        )

        # Подсказка — возврат в меню
        arcade.draw_text(
            "Press ESC to Menu",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            arcade.color.GRAY,
            16,
            anchor_x="center"
        )


    # ----------------------------------------------
    # Обработка нажатий клавиш
    # ----------------------------------------------
    def on_key_press(self, key, modifiers):

        # ENTER — рестарт игры
        if key == arcade.key.ENTER:
            from views.game_view import GameView

            # Создаём новую игру с той же сложностью
            game = GameView(self.difficulty)
            game.setup()

            # Показываем игровой экран
            self.window.show_view(game)

        # ESC — возврат в главное меню
        elif key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())

import arcade

# ---------------- НАСТРОЙКИ ----------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Space Battles"

# ---------------- КНОПКИ ----------------
class MenuButton:
    def __init__(self, x, y, width, height, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action

    def draw(self):
        # draw_lbwh_rectangle_filled: left-bottom-width-height
        arcade.draw_lbwh_rectangle_filled(
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height,
            arcade.color.DARK_BLUE
        )
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            anchor_y="center"
        )

    def check_click(self, x, y):
        if self.x - self.width/2 < x < self.x + self.width/2 and \
           self.y - self.height/2 < y < self.y + self.height/2:
            self.action()


# ---------------- МЕНЮ ----------------
class MenuView(arcade.View):
    def on_show_view(self):
        # фон через SpriteList
        self.background_list = arcade.SpriteList()
        background_sprite = arcade.Sprite(":resources:images/backgrounds/stars.png")
        background_sprite.center_x = SCREEN_WIDTH / 2
        background_sprite.center_y = SCREEN_HEIGHT / 2
        background_sprite.scale = max(
            SCREEN_WIDTH / background_sprite.width,
            SCREEN_HEIGHT / background_sprite.height
        )
        self.background_list.append(background_sprite)

        # кнопки выбора сложности
        self.buttons = [
            MenuButton(SCREEN_WIDTH//2, 400, 200, 50, "Лёгкий", lambda: self.start_game(1)),
            MenuButton(SCREEN_WIDTH//2, 320, 200, 50, "Средний", lambda: self.start_game(2)),
            MenuButton(SCREEN_WIDTH//2, 240, 200, 50, "Сложный", lambda: self.start_game(3))
        ]

    def start_game(self, difficulty):
        # Пока просто закрываем меню — позже заменим на переход в GameView
        pass

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        arcade.draw_text(
            "SPACE BATTLES",
            SCREEN_WIDTH//2,
            550,
            arcade.color.WHITE,
            50,
            anchor_x="center"
        )
        for button in self.buttons:
            button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.check_click(x, y)


# ---------------- ЗАПУСК ----------------
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()

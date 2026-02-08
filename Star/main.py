import arcade
from settings import *
from views.menu_view import MenuView


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

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Space Shooter Deluxe"
DIFFICULTIES = {
    "easy": {
        "lives": 5,
        "enemy_speed": 2,
        "enemy_fire_rate": 45,   # меньше = чаще
        "enemy_bullet_speed": 7,
        "spawn_rate": 70
    },
    "normal": {
        "lives": 3,
        "enemy_speed": 3,
        "enemy_fire_rate": 30,
        "enemy_bullet_speed": 9,
        "spawn_rate": 50
    },
    "expert": {
        "lives": 1,
        "enemy_speed": 4,
        "enemy_fire_rate": 18,
        "enemy_bullet_speed": 12,
        "spawn_rate": 35
    }
}

PLAYER_SPEED = 7
BULLET_SPEED = 12
START_LIVES = 3
STAR_COUNT = 120

SOUND_PATH = "sounds"
HIGHSCORE_FILE = "highscore.txt"
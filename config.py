# --- Основные настройки ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GAME_TITLE = "Xiaomi-Казино"

# --- Цвета (Это просто кортежи, они безопасны) ---
WHITE, BLACK, GOLD, RED, GREEN, BLUE = ((255, 255, 255), (0, 0, 0), (255, 215, 0),
                                        (200, 0, 0), (0, 150, 0), (0, 100, 150))

# --- Шрифты (Храним только размеры, а не объекты) ---
FONT_SIZES = {
    "large": 48,
    "medium": 36,
    "small": 24
}

# --- Игровые настройки ---
WIN_CHANCE_BASE = 0.25
REEL_PRICES = {1: 0, 2: 200, 3: 500}

# --- Файлы ---
PHONE_DATA_FILE = "phones.txt"
SAVE_FILES = {
    1: "save_slot_1.json",
    2: "save_slot_2.json",
    3: "save_slot_3.json",
}
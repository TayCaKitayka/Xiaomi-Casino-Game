import pygame
import random
import sys
import os

# Импортируем наши модули правильно
from config import *
import data_handler 
import game_states

# --- 1. ИНИЦИАЛИЗАЦИЯ PYGAME ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# --- 2. СОЗДАНИЕ РЕСУРСОВ ---
FONTS = {
    "large": pygame.font.Font(None, FONT_SIZES["large"]),
    "medium": pygame.font.Font(None, FONT_SIZES["medium"]),
    "small": pygame.font.Font(None, FONT_SIZES["small"])
}
PHONES = data_handler.parse_phones_data(data_handler.resource_path(PHONE_DATA_FILE))
if PHONES is None:
    print(f"Критическая ошибка: файл {PHONE_DATA_FILE} не найден.")
    pygame.quit()
    sys.exit()

# Эта функция должна быть здесь или в data_handler, оставим ее здесь для простоты
def load_and_scale_phone_images(target_size=(100, 100)):
    images = {}
    placeholder = pygame.Surface(target_size); placeholder.fill(WHITE)
    for name, data in PHONES.items():
        image_path = data_handler.resource_path(os.path.join("assets", data["image_file"])) 
        try:
            images[name] = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), target_size)
        except pygame.error: images[name] = placeholder
    return images
    
phone_images = load_and_scale_phone_images()
try:
    background_path = data_handler.resource_path(os.path.join("assets", "background.png"))
    background_image = pygame.image.load(background_path)
except: 
    background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); background_image.fill((20, 20, 40))

# --- 3. ИГРОВЫЕ ПЕРЕМЕННЫЕ ---
game_state = "casino"
player = {"balance": 1000, "inventory": []}
reels_result = random.choices(list(PHONES.keys()), k=3)
message, message_color, message_timer = "", WHITE, 0

# --- 4. ОСНОВНОЙ ЦИКЛ ИГРЫ ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # ### ПЕРЕПИСАННЫЙ БЛОК ОБРАБОТКИ СОБЫТИЙ ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # --- Логика для состояния "КАЗИНО" ---
            if game_state == "casino":
                # Кнопки смены состояния
                if pygame.Rect(650, 10, 140, 40).collidepoint(mouse_pos): game_state = "saving"
                elif pygame.Rect(650, 60, 140, 40).collidepoint(mouse_pos): game_state = "loading"
                elif pygame.Rect(10, 450, 200, 40).collidepoint(mouse_pos): game_state = "selling"

                # Кнопки вращения барабанов (проверяются отдельно)
                spin_buttons = {1: (50, 500), 2: (300, 500), 3: (550, 500)}
                for tier, (x, y) in spin_buttons.items():
                    if pygame.Rect(x, y, 200, 50).collidepoint(mouse_pos):
                        price = REEL_PRICES[tier]
                        if player["balance"] >= price:
                            player["balance"] -= price
                            # Логика самого вращения
                            possible = [name for name, data in PHONES.items() if data["tier"] == tier]
                            if possible:
                                if random.random() < WIN_CHANCE_BASE:
                                    won_phone = random.choice(possible)
                                    reels_result = [won_phone] * 3
                                else:
                                    reels_result = random.choices(possible, k=3)
                                
                                if reels_result.count(reels_result[0]) == 3:
                                    won_phone = reels_result[0]
                                    player["inventory"].append(won_phone)
                                    message, message_color = f"Вы выиграли {won_phone}!", GOLD
                                else:
                                    message, message_color = "Попробуйте еще раз!", WHITE
                                message_timer = pygame.time.get_ticks()
                        else:
                            message, message_color = "Недостаточно средств!", RED

            # --- Логика для состояния "ПРОДАЖА" ---
            elif game_state == "selling":
                if pygame.Rect(300, 500, 200, 50).collidepoint(mouse_pos): game_state = "casino" # Назад
                elif pygame.Rect(50, 500, 200, 50).collidepoint(mouse_pos): # Продать все
                    if player["inventory"]:
                        total_sale = sum(int(PHONES[item]["value"] * 0.8) for item in player["inventory"])
                        player["balance"] += total_sale
                        player["inventory"].clear()
                        message, message_color = f"Все продано за {total_sale}!", GREEN
                        message_timer = pygame.time.get_ticks()
                else: # Продажа по одному
                    for i, item in enumerate(player["inventory"]):
                        if pygame.Rect(50, 80 + i * 35, 700, 30).collidepoint(mouse_pos):
                            sell_price = int(PHONES[item]["value"] * 0.8)
                            player["balance"] += sell_price
                            player["inventory"].pop(i)
                            message, message_color = f"Продан {item}!", GREEN
                            message_timer = pygame.time.get_ticks()
                            break

            # --- Логика для состояний "СОХРАНЕНИЕ" и "ЗАГРУЗКА" ---
            elif game_state in ["saving", "loading"]:
                if pygame.Rect(300, 500, 200, 50).collidepoint(mouse_pos): game_state = "casino"
                for slot in range(1, 4):
                    if pygame.Rect(150, 100 + (slot - 1) * 100, 500, 80).collidepoint(mouse_pos):
                        if game_state == "saving":
                            message, message_color = data_handler.save_game(slot, player)
                        else:
                            loaded_data, msg, color = data_handler.load_game(slot)
                            if loaded_data: player = loaded_data
                            message, message_color = msg, color
                        message_timer = pygame.time.get_ticks()
                        game_state = "casino"

    # --- ОТРИСОВКА ---
    screen.blit(background_image, (0, 0))
    
    if game_state == "casino":
        game_states.draw_casino_screen(screen, player, reels_result, phone_images, FONTS)
    elif game_state == "selling":
        game_states.draw_selling_screen(screen, player, PHONES, mouse_pos, FONTS)
    elif game_state in ["saving", "loading"]:
        title = "Выберите слот для сохранения" if game_state == "saving" else "Выберите слот для загрузки"
        game_states.draw_slots_screen(screen, title, mouse_pos, FONTS)

    # Общие элементы
    btn_save = pygame.Rect(650, 10, 140, 40); pygame.draw.rect(screen, BLUE, btn_save); game_states.draw_text("Сохранить", FONTS["small"], WHITE, screen, btn_save.centerx, btn_save.centery, center=True)
    btn_load = pygame.Rect(650, 60, 140, 40); pygame.draw.rect(screen, BLUE, btn_load); game_states.draw_text("Загрузить", FONTS["small"], WHITE, screen, btn_load.centerx, btn_load.centery, center=True)
    if message and pygame.time.get_ticks() - message_timer < 2500:
        game_states.draw_text(message, FONTS["medium"], message_color, screen, SCREEN_WIDTH / 2, 450, center=True)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
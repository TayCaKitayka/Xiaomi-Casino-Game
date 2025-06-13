import pygame
from config import * # Импортируем только константы (цвета, размеры)
import data_handler

def draw_text(text, font, color, surface, x, y, center=False):
    """Универсальная функция для отрисовки текста."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_casino_screen(surface, player, reels_result, phone_images, FONTS):
    """Отрисовывает главный экран казино."""
    draw_text(f"Баланс: {player['balance']}", FONTS["medium"], WHITE, surface, 10, 10)
    draw_text("Инвентарь:", FONTS["small"], WHITE, surface, 10, 50)
    for i, item in enumerate(player["inventory"]):
        draw_text(f"- {item}", FONTS["small"], WHITE, surface, 10, 80 + i * 25)
    
    for i, name in enumerate(reels_result):
        surface.blit(phone_images[name], (240 + i * 110, 200))

    # Отрисовка кнопок барабанов
    btn_spin1 = pygame.Rect(50, 500, 200, 50); pygame.draw.rect(surface, GREEN, btn_spin1); draw_text(f"Redmi ({REEL_PRICES[1]})", FONTS["small"], WHITE, surface, btn_spin1.centerx, btn_spin1.centery, center=True)
    btn_spin2 = pygame.Rect(300, 500, 200, 50); pygame.draw.rect(surface, GOLD, btn_spin2); draw_text(f"Poco ({REEL_PRICES[2]})", FONTS["small"], WHITE, surface, btn_spin2.centerx, btn_spin2.centery, center=True)
    btn_spin3 = pygame.Rect(550, 500, 200, 50); pygame.draw.rect(surface, RED, btn_spin3); draw_text(f"Xiaomi ({REEL_PRICES[3]})", FONTS["small"], WHITE, surface, btn_spin3.centerx, btn_spin3.centery, center=True)
    btn_sell_open = pygame.Rect(10, 450, 200, 40); pygame.draw.rect(surface, BLUE, btn_sell_open); draw_text("Продать телефон", FONTS["small"], WHITE, surface, btn_sell_open.centerx, btn_sell_open.centery, center=True)

def draw_selling_screen(surface, player, phones_data, mouse_pos, FONTS):
    """Отрисовывает экран продажи."""
    draw_text("Выберите телефон для продажи", FONTS["large"], GOLD, surface, SCREEN_WIDTH/2, 20, center=True)
    if not player["inventory"]:
        draw_text("Инвентарь пуст!", FONTS["medium"], WHITE, surface, SCREEN_WIDTH/2, 250, center=True)
    for i, item in enumerate(player["inventory"]):
        sell_price = int(phones_data[item]["value"] * 0.8)
        item_text = f"{item} (Продажа: {sell_price} у.е.)"
        item_rect = pygame.Rect(50, 80 + i * 35, 700, 30)
        if item_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, (50, 50, 100), item_rect)
        draw_text(item_text, FONTS["small"], WHITE, surface, 60, 85 + i * 35)
    
    btn_back = pygame.Rect(300, 500, 200, 50); pygame.draw.rect(surface, RED, btn_back); draw_text("Назад", FONTS["medium"], WHITE, surface, btn_back.centerx, btn_back.centery, center=True)
    btn_sell_all = pygame.Rect(50, 500, 200, 50); pygame.draw.rect(surface, GREEN, btn_sell_all); draw_text("Продать всё", FONTS["medium"], WHITE, surface, btn_sell_all.centerx, btn_sell_all.centery, center=True)

def draw_slots_screen(surface, title, mouse_pos, FONTS):
    """Отрисовывает экран выбора слота для сохранения/загрузки."""
    draw_text(title, FONTS["large"], GOLD, surface, SCREEN_WIDTH / 2, 40, center=True)
    for slot in range(1, 4):
        slot_rect = pygame.Rect(150, 100 + (slot - 1) * 100, 500, 80)
        # ### ИСПРАВЛЕНИЕ ЗДЕСЬ ###
        info_text = data_handler.get_slot_info(slot) 
        # ... (остальная часть функции без изменений)
        color = (50, 50, 100) if slot_rect.collidepoint(mouse_pos) else (30, 30, 70)
        pygame.draw.rect(surface, color, slot_rect, border_radius=10)
        draw_text(f"Слот {slot}", FONTS["medium"], WHITE, surface, slot_rect.centerx, slot_rect.centery - 15, center=True)
        draw_text(info_text, FONTS["small"], (200, 200, 200), surface, slot_rect.centerx, slot_rect.centery + 15, center=True)
    
    btn_back = pygame.Rect(300, 500, 200, 50); pygame.draw.rect(surface, RED, btn_back); draw_text("Назад", FONTS["medium"], WHITE, surface, btn_back.centerx, btn_back.centery, center=True)
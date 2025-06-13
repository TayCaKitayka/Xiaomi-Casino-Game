import os
import sys
import json
import pygame
from config import *

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, который УПАКОВАН ВНУТРЬ .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

### НОВАЯ ФУНКЦИЯ ДЛЯ СОХРАНЕНИЙ ###
def get_persistent_path(relative_path):
    """ Получает абсолютный путь к файлу в папке, где лежит .exe """
    # Проверяем, запущена ли программа как .exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        # Если запущена как обычный .py скрипт
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(application_path, relative_path)

def parse_phones_data(filename):
    """Читает и парсит файл с данными о телефонах."""
    phones_dict = {}
    tier_map = {"redmi:": 1, "poco:": 2, "xiaomi:": 3}
    current_tier = 0
    # Для чтения данных ИСПОЛЬЗУЕМ resource_path, т.к. файл внутри .exe
    filepath = resource_path(filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().lower()
                if line in tier_map: current_tier = tier_map[line]; continue
                if ":" in line and current_tier != 0:
                    try:
                        name, img_file, value_str = line.split(":")
                        phones_dict[name.title()] = {"value": int(value_str), "tier": current_tier, "image_file": img_file}
                    except ValueError: print(f"Предупреждение: Пропускаю строку -> {line}")
    except FileNotFoundError: return None
    return phones_dict

### ИЗМЕНЯЕМ ФУНКЦИИ НИЖЕ, ЧТОБЫ ОНИ ИСПОЛЬЗОВАЛИ НОВЫЙ ПУТЬ ###

def save_game(slot_number, player_data):
    """Сохраняет данные игрока в указанный слот."""
    # ИСПОЛЬЗУЕМ get_persistent_path, чтобы сохранить РЯДОМ с .exe
    filepath = get_persistent_path(SAVE_FILES[slot_number])
    with open(filepath, 'w') as f:
        json.dump(player_data, f)
    return f"Игра сохранена в Слот {slot_number}", GREEN

def load_game(slot_number):
    """Загружает данные игрока из указанного слота."""
    # ИСПОЛЬЗУЕМ get_persistent_path, чтобы загрузить ИЗ ПАПКИ .exe
    filepath = get_persistent_path(SAVE_FILES[slot_number])
    try:
        with open(filepath, 'r') as f:
            player_data = json.load(f)
        return player_data, f"Игра загружена из Слота {slot_number}", GREEN
    except FileNotFoundError:
        return None, f"Слот {slot_number} пуст!", RED

def get_slot_info(slot_number):
    """Получает информацию о слоте для отображения в меню."""
    # ИСПОЛЬЗУЕМ get_persistent_path, чтобы прочитать ИЗ ПАПКИ .exe
    filepath = get_persistent_path(SAVE_FILES[slot_number])
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        balance = data.get("balance", "N/A")
        inventory_len = len(data.get("inventory", []))
        return f"Баланс: {balance} | Телефонов: {inventory_len}"
    except (FileNotFoundError, json.JSONDecodeError):
        return "[ Пустой слот ]"
"""
Скрипт для скачивания всех 78 карт Таро Rider-Waite
Источник: Internet Archive (Public Domain)
"""
import requests
import os
from pathlib import Path
import time

# Базовый URL
BASE_URL = "https://archive.org/download/rider-waite-tarot/"

# ВСЕ 78 КАРТ ТАРО

# Старшие Арканы (22 карты)
MAJOR_ARCANA = [
    ("00_fool", "major_arcana_fool.png"),
    ("01_magician", "major_arcana_magician.png"),
    ("02_high_priestess", "major_arcana_high_priestess.png"),
    ("03_empress", "major_arcana_empress.png"),
    ("04_emperor", "major_arcana_emperor.png"),
    ("05_hierophant", "major_arcana_hierophant.png"),
    ("06_lovers", "major_arcana_lovers.png"),
    ("07_chariot", "major_arcana_chariot.png"),
    ("08_strength", "major_arcana_strength.png"),
    ("09_hermit", "major_arcana_hermit.png"),
    ("10_fortune", "major_arcana_fortune.png"),
    ("11_justice", "major_arcana_justice.png"),
    ("12_hanged", "major_arcana_hanged.png"),
    ("13_death", "major_arcana_death.png"),
    ("14_temperance", "major_arcana_temperance.png"),
    ("15_devil", "major_arcana_devil.png"),
    ("16_tower", "major_arcana_tower.png"),
    ("17_star", "major_arcana_star.png"),
    ("18_moon", "major_arcana_moon.png"),
    ("19_sun", "major_arcana_sun.png"),
    ("20_judgement", "major_arcana_judgement.png"),
    ("21_world", "major_arcana_world.png"),
]

# Младшие Арканы - Жезлы (14 карт)
WANDS = [
    ("wands_ace", "minor_arcana_wands_ace.png"),
    ("wands_02", "minor_arcana_wands_02.png"),
    ("wands_03", "minor_arcana_wands_03.png"),
    ("wands_04", "minor_arcana_wands_04.png"),
    ("wands_05", "minor_arcana_wands_05.png"),
    ("wands_06", "minor_arcana_wands_06.png"),
    ("wands_07", "minor_arcana_wands_07.png"),
    ("wands_08", "minor_arcana_wands_08.png"),
    ("wands_09", "minor_arcana_wands_09.png"),
    ("wands_10", "minor_arcana_wands_10.png"),
    ("wands_page", "minor_arcana_wands_page.png"),
    ("wands_knight", "minor_arcana_wands_knight.png"),
    ("wands_queen", "minor_arcana_wands_queen.png"),
    ("wands_king", "minor_arcana_wands_king.png"),
]

# Младшие Арканы - Кубки (14 карт)
CUPS = [
    ("cups_ace", "minor_arcana_cups_ace.png"),
    ("cups_02", "minor_arcana_cups_02.png"),
    ("cups_03", "minor_arcana_cups_03.png"),
    ("cups_04", "minor_arcana_cups_04.png"),
    ("cups_05", "minor_arcana_cups_05.png"),
    ("cups_06", "minor_arcana_cups_06.png"),
    ("cups_07", "minor_arcana_cups_07.png"),
    ("cups_08", "minor_arcana_cups_08.png"),
    ("cups_09", "minor_arcana_cups_09.png"),
    ("cups_10", "minor_arcana_cups_10.png"),
    ("cups_page", "minor_arcana_cups_page.png"),
    ("cups_knight", "minor_arcana_cups_knight.png"),
    ("cups_queen", "minor_arcana_cups_queen.png"),
    ("cups_king", "minor_arcana_cups_king.png"),
]

# Младшие Арканы - Мечи (14 карт)
SWORDS = [
    ("swords_ace", "minor_arcana_swords_ace.png"),
    ("swords_02", "minor_arcana_swords_02.png"),
    ("swords_03", "minor_arcana_swords_03.png"),
    ("swords_04", "minor_arcana_swords_04.png"),
    ("swords_05", "minor_arcana_swords_05.png"),
    ("swords_06", "minor_arcana_swords_06.png"),
    ("swords_07", "minor_arcana_swords_07.png"),
    ("swords_08", "minor_arcana_swords_08.png"),
    ("swords_09", "minor_arcana_swords_09.png"),
    ("swords_10", "minor_arcana_swords_10.png"),
    ("swords_page", "minor_arcana_swords_page.png"),
    ("swords_knight", "minor_arcana_swords_knight.png"),
    ("swords_queen", "minor_arcana_swords_queen.png"),
    ("swords_king", "minor_arcana_swords_king.png"),
]

# Младшие Арканы - Пентакли (14 карт)
PENTACLES = [
    ("pentacles_ace", "minor_arcana_pentacles_ace.png"),
    ("pentacles_02", "minor_arcana_pentacles_02.png"),
    ("pentacles_03", "minor_arcana_pentacles_03.png"),
    ("pentacles_04", "minor_arcana_pentacles_04.png"),
    ("pentacles_05", "minor_arcana_pentacles_05.png"),
    ("pentacles_06", "minor_arcana_pentacles_06.png"),
    ("pentacles_07", "minor_arcana_pentacles_07.png"),
    ("pentacles_08", "minor_arcana_pentacles_08.png"),
    ("pentacles_09", "minor_arcana_pentacles_09.png"),
    ("pentacles_10", "minor_arcana_pentacles_10.png"),
    ("pentacles_page", "minor_arcana_pentacles_page.png"),
    ("pentacles_knight", "minor_arcana_pentacles_knight.png"),
    ("pentacles_queen", "minor_arcana_pentacles_queen.png"),
    ("pentacles_king", "minor_arcana_pentacles_king.png"),
]

def download_card(url, save_path):
    """Скачать одну карту"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"❌ Ошибка: {save_path.name} - {e}")
        return False

def download_deck(deck_list, deck_name):
    """Скачать колоду карт"""
    images_dir = Path("images/tarot")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📦 Скачиваю {deck_name}...")
    success = 0
    
    for local_name, remote_name in deck_list:
        url = BASE_URL + remote_name
        save_path = images_dir / f"{local_name}.jpg"
        
        if download_card(url, save_path):
            print(f"✅ {local_name}.jpg")
            success += 1
            time.sleep(0.1)  # Небольшая задержка между запросами
        else:
            print(f"❌ {local_name}.jpg")
    
    return success

def main():
    """Основная функция"""
    print("=" * 60)
    print("🎴 СКАЧИВАНИЕ ПОЛНОЙ КОЛОДЫ ТАРО RIDER-WAITE")
    print("=" * 60)
    print()
    
    total_success = 0
    total_cards = 78
    
    # Скачиваем по категориям
    total_success += download_deck(MAJOR_ARCANA, "Старшие Арканы (22 карты)")
    total_success += download_deck(WANDS, "Жезлы (14 карт)")
    total_success += download_deck(CUPS, "Кубки (14 карт)")
    total_success += download_deck(SWORDS, "Мечи (14 карт)")
    total_success += download_deck(PENTACLES, "Пентакли (14 карт)")
    
    print()
    print("=" * 60)
    print(f"✅ Успешно скачано: {total_success}/{total_cards}")
    print(f"❌ Ошибок: {total_cards - total_success}")
    print("=" * 60)
    
    if total_success == total_cards:
        print("\n🎉 Отлично! Все карты скачаны!")
    elif total_success > 0:
        print("\n⚠️  Некоторые карты не загрузились.")
        print("Попробуйте запустить скрипт еще раз или скачайте вручную:")
        print("https://archive.org/details/rider-waite-tarot")
    else:
        print("\n❌ Не удалось скачать карты.")
        print("Проверьте интернет-соединение или скачайте вручную:")
        print("https://archive.org/details/rider-waite-tarot")

if __name__ == "__main__":
    main()

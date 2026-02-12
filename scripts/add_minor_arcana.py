"""
Скрипт для добавления Младших Арканов в колоду Таро
Добавляет 56 карт: 4 масти × 14 карт
"""
import json
from pathlib import Path

# Младшие Арканы - 14 карт в каждой масти
def generate_minor_arcana():
    suits = {
        'wands': {
            'name_ru': 'Жезлы',
            'element': 'Огонь',
            'theme': 'действие, энергия, страсть, творчество'
        },
        'cups': {
            'name_ru': 'Кубки', 
            'element': 'Вода',
            'theme': 'эмоции, любовь, отношения, интуиция'
        },
        'swords': {
            'name_ru': 'Мечи',
            'element': 'Воздух', 
            'theme': 'мысли, конфликты, решения, истина'
        },
        'pentacles': {
            'name_ru': 'Пентакли',
            'element': 'Земля',
            'theme': 'деньги, материальное, работа, стабильность'
        }
    }
    
    # Придворные карты
    court_cards = {
        'page': ('Паж', 'молодость, начинания, вести'),
        'knight': ('Рыцарь', 'действие, движение, стремление'),
        'queen': ('Королева', 'зрелость, забота, мастерство'),
        'king': ('Король', 'власть, контроль, достижения')
    }
    
    minor_arcana = {}
    
    for suit_en, suit_info in suits.items():
        cards = []
        suit_ru = suit_info['name_ru']
        theme = suit_info['theme']
        
        # Числовые карты (Туз + 2-10)
        for num in range(1, 11):
            if num == 1:
                card_name = f"Туз {suit_ru}"
                meaning = f"Начало в области {theme}. Новые возможности и потенциал."
            else:
                card_name = f"{num} {suit_ru}"
                meaning = f"Развитие энергии {suit_ru.lower()} на уровне {num}. {theme.capitalize()}."
            
            cards.append({
                "name": card_name,
                "name_en": f"{num} of {suit_en.capitalize()}",
                "suit": suit_en,
                "number": num,
                "type": "pip",
                "meaning": meaning,
                "love": f"В любви: влияние {suit_ru.lower()} проявляется через {theme}.",
                "work": f"В работе: энергия {suit_ru.lower()} помогает в делах.",
                "image": f"{suit_en}_{num:02d}.jpg"
            })
        
        # Придворные карты
        for rank_en, (rank_ru, rank_meaning) in court_cards.items():
            card_name = f"{rank_ru} {suit_ru}"
            cards.append({
                "name": card_name,
                "name_en": f"{rank_en.capitalize()} of {suit_en.capitalize()}",
                "suit": suit_en,
                "rank": rank_en,
                "type": "court",
                "meaning": f"{rank_meaning}. Энергия {suit_ru.lower()}: {theme}.",
                "love": f"В любви: личность с качествами {rank_ru.lower()} {suit_ru.lower()}.",
                "work": f"В работе: подход {rank_ru.lower()} к делам.",
                "image": f"{suit_en}_{rank_en}.jpg"
            })
        
        minor_arcana[suit_en] = cards
    
    return minor_arcana

# Дополним недостающие Старшие Арканы
def complete_major_arcana():
    missing_major = [
        {
            "number": 7, "name": "Колесница", "name_en": "The Chariot",
            "meaning": "Победа, контроль, движение вперёд. Преодоление препятствий.",
            "love": "Активные действия в отношениях. Контроль ситуации.",
            "work": "Продвижение, победа в конкуренции.", 
            "image": "07_chariot.jpg"
        },
        {
            "number": 8, "name": "Сила", "name_en": "Strength",
            "meaning": "Внутренняя сила, мужество, терпение. Контроль над инстинктами.",
            "love": "Страсть, сильные чувства под контролем.",
            "work": "Преодоление трудностей силой духа.",
            "image": "08_strength.jpg"
        },
        {
            "number": 9, "name": "Отшельник", "name_en": "The Hermit",
            "meaning": "Одиночество, поиск истины, мудрость. Время для размышлений.",
            "love": "Одиночество, отстранённость от отношений.",
            "work": "Работа в одиночку, глубокие исследования.",
            "image": "09_hermit.jpg"
        },
        {
            "number": 10, "name": "Колесо Фортуны", "name_en": "Wheel of Fortune",
            "meaning": "Судьба, цикличность, перемены. Поворот событий.",
            "love": "Судьбоносная встреча, перемены в отношениях.",
            "work": "Неожиданные изменения, удача или неудача.",
            "image": "10_wheel.jpg"
        },
        {
            "number": 11, "name": "Справедливость", "name_en": "Justice",
            "meaning": "Справедливость, баланс, правда. Юридические вопросы.",
            "love": "Честность в отношениях, баланс интересов.",
            "work": "Контракты, судебные дела, справедливая оценка.",
            "image": "11_justice.jpg"
        },
        {
            "number": 12, "name": "Повешенный", "name_en": "The Hanged Man",
            "meaning": "Жертва, новый взгляд, пауза. Переоценка ценностей.",
            "love": "Жертвенность, ожидание, неопределённость.",
            "work": "Застой, необходимость изменить точку зрения.",
            "image": "12_hanged.jpg"
        },
        {
            "number": 13, "name": "Смерть", "name_en": "Death",
            "meaning": "Трансформация, конец цикла, перерождение. Необратимые изменения.",
            "love": "Окончание отношений, трансформация чувств.",
            "work": "Увольнение, смена профессии, конец проекта.",
            "image": "13_death.jpg"
        },
        {
            "number": 14, "name": "Умеренность", "name_en": "Temperance",
            "meaning": "Баланс, гармония, умеренность. Смешение противоположностей.",
            "love": "Гармония, баланс в отношениях.",
            "work": "Компромиссы, сотрудничество, дипломатия.",
            "image": "14_temperance.jpg"
        },
        {
            "number": 15, "name": "Дьявол", "name_en": "The Devil",
            "meaning": "Зависимость, искушение, материализм. Ловушка иллюзий.",
            "love": "Страсть, зависимость, токсичные отношения.",
            "work": "Алчность, нечестность, манипуляции.",
            "image": "15_devil.jpg"
        },
        {
            "number": 16, "name": "Башня", "name_en": "The Tower",
            "meaning": "Разрушение, кризис, внезапные перемены. Крах иллюзий.",
            "love": "Разрыв, скандал, разоблачение.",
            "work": "Увольнение, крах проектов, банкротство.",
            "image": "16_tower.jpg"
        },
        {
            "number": 17, "name": "Звезда", "name_en": "The Star",
            "meaning": "Надежда, вдохновение, исцеление. Светлое будущее.",
            "love": "Надежда на любовь, исцеление после разрыва.",
            "work": "Новые возможности, вдохновение.",
            "image": "17_star.jpg"
        },
        {
            "number": 18, "name": "Луна", "name_en": "The Moon",
            "meaning": "Иллюзии, страхи, подсознание. Неясность ситуации.",
            "love": "Обман, секреты, неопределённость чувств.",
            "work": "Обман, скрытые враги, неясность.",
            "image": "18_moon.jpg"
        },
        {
            "number": 19, "name": "Солнце", "name_en": "The Sun",
            "meaning": "Радость, успех, ясность. Достижение целей.",
            "love": "Счастливые отношения, брак, дети.",
            "work": "Успех, признание, процветание.",
            "image": "19_sun.jpg"
        },
        {
            "number": 20, "name": "Суд", "name_en": "Judgement",
            "meaning": "Возрождение, прощение, призвание. Второй шанс.",
            "love": "Возобновление отношений, прощение.",
            "work": "Новое призвание, оценка результатов.",
            "image": "20_judgement.jpg"
        }
    ]
    return missing_major

# Обновляем файл
def update_tarot_cards():
    data_path = Path(__file__).parent.parent / 'data' / 'tarot_cards.json'
    
    # Читаем текущие данные
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Дополняем Старшие Арканы
    existing_major_numbers = {card['number'] for card in data['major_arcana']}
    missing_major = [card for card in complete_major_arcana() 
                     if card['number'] not in existing_major_numbers]
    data['major_arcana'].extend(missing_major)
    data['major_arcana'].sort(key=lambda x: x['number'])
    
    # Добавляем Младшие Арканы
    data['minor_arcana'] = generate_minor_arcana()
    
    # Сохраняем
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    total_cards = len(data['major_arcana']) + sum(len(cards) for cards in data['minor_arcana'].values())
    print("Koloda obnovlena!")
    print(f"Starshih Arkanov: {len(data['major_arcana'])}")
    print(f"Mladshih Arkanov: {sum(len(cards) for cards in data['minor_arcana'].values())}")
    print(f"Vsego kart: {total_cards}")

if __name__ == '__main__':
    update_tarot_cards()

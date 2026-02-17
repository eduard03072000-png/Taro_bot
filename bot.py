from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
from modules.tarot import TarotExtended
from modules.matrix import MatrixExtended
from modules.numerology import NumerologyExtended
from modules.matrix_chart import generate_matrix_image, calculate_matrix

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Инициализация модулей
tarot = TarotExtended()
matrix = MatrixExtended()
numerology = NumerologyExtended()

# Словарь для хранения состояний пользователей
user_states = {}
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню"""
    keyboard = [
        [InlineKeyboardButton("🎴 Расклады Таро", callback_data='tarot_menu')],
        [InlineKeyboardButton("⭐ Матрица Судьбы", callback_data='matrix_menu')],
        [InlineKeyboardButton("🔢 Нумерология", callback_data='numerology_menu')],
        [InlineKeyboardButton("🎯 Да или Нет?", callback_data='yes_no')],
        [InlineKeyboardButton("ℹ️ О сервисе", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """
🔮 **MYSTICAL BOT - PREMIUM EDITION** 🔮

Добро пожаловать в профессиональный мир эзотерики!

**Что я умею:**

🎴 **ТАРО** - 7 видов раскладов (новинка: расклад на неделю!)
⭐ **МАТРИЦА СУДЬБЫ** - полный расчёт по 22 арканам  
🔢 **НУМЕРОЛОГИЯ** - 9 ключевых показателей
🎯 **ДА/НЕТ** - быстрый ответ на ваш вопрос

Выберите интересующее направление:
    """
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# ============ ТАРО МЕНЮ ============

async def tarot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расширенное меню раскладов Таро"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🌅 Карта дня", callback_data='tarot_day')],
        [InlineKeyboardButton("🎴 Три карты", callback_data='tarot_three')],
        [InlineKeyboardButton("📅 Расклад на неделю", callback_data='tarot_week')],
        [InlineKeyboardButton("✨ Кельтский крест (10 карт)", callback_data='tarot_celtic')],
        [InlineKeyboardButton("❤️ Расклад на отношения", callback_data='tarot_love')],
        [InlineKeyboardButton("💰 Расклад на финансы", callback_data='tarot_money')],
        [InlineKeyboardButton("💼 Расклад на карьеру", callback_data='tarot_career')],
        [InlineKeyboardButton("◀️ Главное меню", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
🎴 **РАСКЛАДЫ ТАРО** 🎴

**Выберите тип расклада:**

🌅 **Карта дня** - энергия сегодняшнего дня
🎴 **Три карты** - прошлое, настоящее, будущее
📅 **Расклад на неделю** - прогноз на 7 дней  
✨ **Кельтский крест** - глубокий анализ ситуации
❤️ **На отношения** - любовь и партнёрство
💰 **На финансы** - денежные потоки
💼 **На карьеру** - профессиональный путь

Что интересует?
    """
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def tarot_day_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Карта дня"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    card_text = tarot.card_of_the_day(user_id)
    
    keyboard = [
        [InlineKeyboardButton("🔄 Ещё карта", callback_data='tarot_day')],
        [InlineKeyboardButton("◀️ Меню Таро", callback_data='tarot_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(card_text, reply_markup=reply_markup, parse_mode='Markdown')

async def tarot_three_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос вопроса для расклада три карты"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_tarot_three_question'
    
    text = """
🎴 **РАСКЛАД "ТРИ КАРТЫ"** 🎴

Этот расклад раскрывает динамику ситуации:
• Прошлое - что привело к текущему
• Настоящее - ваше положение сейчас  
• Будущее - куда движется ситуация

**Напишите свой вопрос** в следующем сообщении.
Например: "Что ждёт меня в работе?" или "Как развиваются мои отношения?"

_Или нажмите "Без вопроса" для общего расклада._
    """
    
    keyboard = [
        [InlineKeyboardButton("🔮 Без вопроса", callback_data='tarot_three_no_question')],
        [InlineKeyboardButton("◀️ Назад", callback_data='tarot_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем новое сообщение вместо редактирования
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def tarot_celtic_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кельтский крест"""
    query = update.callback_query
    await query.answer()
    
    text = tarot.celtic_cross()
    
    keyboard = [
        [InlineKeyboardButton("🔄 Новый расклад", callback_data='tarot_celtic')],
        [InlineKeyboardButton("◀️ Меню Таро", callback_data='tarot_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def tarot_love_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расклад на отношения"""
    query = update.callback_query
    await query.answer()
    
    text = tarot.love_spread()
    
    keyboard = [
        [InlineKeyboardButton("🔄 Новый расклад", callback_data='tarot_love')],
        [InlineKeyboardButton("◀️ Меню Таро", callback_data='tarot_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def tarot_money_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расклад на финансы"""
    query = update.callback_query
    await query.answer()
    
    text, cards = tarot.money_spread()
    
    keyboard = [
        [InlineKeyboardButton("🔄 Новый расклад", callback_data='tarot_money')],
        [InlineKeyboardButton("◀️ Меню Таро", callback_data='tarot_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def tarot_career_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расклад на карьеру"""
    query = update.callback_query
    await query.answer()
    
    text, cards = tarot.career_spread()
    
    keyboard = [
        [InlineKeyboardButton("🔄 Новый расклад", callback_data='tarot_career')],
        [InlineKeyboardButton("◀️ Меню Таро", callback_data='tarot_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def tarot_week_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расклад на неделю"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    text, cards = tarot.week_spread(user_id)
    
    keyboard = [
        [InlineKeyboardButton("🔄 Новый расклад", callback_data='tarot_week')],
        [InlineKeyboardButton("◀️ Меню Таро", callback_data='tarot_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def yes_no_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало гадания Да/Нет"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_yes_no_question'
    
    text = """
🎯 **ГАДАНИЕ "ДА ИЛИ НЕТ"** 🎯

Задайте вопрос, на который можно ответить "Да" или "Нет".

**Примеры вопросов:**
• Стоит ли мне менять работу?
• Получится ли у меня этот проект?
• Ответит ли мне этот человек?
• Стоит ли инвестировать в это?

**Напишите свой вопрос** в следующем сообщении.
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# ============ МАТРИЦА СУДЬБЫ ============

async def matrix_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню матрицы судьбы"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🔮 Круговая диаграмма", callback_data='matrix_chart')],
        [InlineKeyboardButton("📊 Полный расчёт", callback_data='matrix_full')],
        [InlineKeyboardButton("💑 Совместимость", callback_data='matrix_compatibility')],
        [InlineKeyboardButton("👶 Детская матрица", callback_data='matrix_child')],
        [InlineKeyboardButton("🃏 22 аркана — описания", callback_data='matrix_arcanas_list')],
        [InlineKeyboardButton("📚 Аспекты Матрицы", callback_data='matrix_aspects_menu')],
        [InlineKeyboardButton("◀️ Главное меню", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
⭐ **МАТРИЦА СУДЬБЫ** ⭐

**Выберите тип расчёта:**

📊 **Полный расчёт** - все аспекты личности
💑 **Совместимость** - анализ отношений  
👶 **Детская матрица** - потенциал ребёнка

Матрица основана на 22 энергиях арканов Таро и раскрывает:
• Личные качества и таланты
• Предназначение и жизненный путь
• Линию денег и карьеры
• Линию любви и отношений
• Кармические задачи

Что рассчитываем?
    """
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def matrix_full_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало полного расчёта матрицы"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_matrix_date'
    user_data[user_id] = {}
    
    text = """
⭐ **ПОЛНЫЙ РАСЧЁТ МАТРИЦЫ СУДЬБЫ** ⭐

Для точного расчёта мне нужна информация:

**Шаг 1 из 4: Дата рождения**
Формат: ДД.ММ.ГГГГ
Пример: 15.05.1990
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data='matrix_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def matrix_compatibility_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало расчёта совместимости"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_compatibility_date1'
    user_data[user_id] = {}
    
    text = """
💑 **СОВМЕСТИМОСТЬ ПАРТНЕРОВ** 💑

Для расчёта совместимости нужны даты рождения обоих партнеров.

**Шаг 1 из 2: Первый партнер**
Введите дату рождения первого партнера
Формат: ДД.ММ.ГГГГ
Пример: 15.05.1990
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data='matrix_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def matrix_child_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало расчёта детской матрицы"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_child_date'
    user_data[user_id] = {}
    
    text = """
👶 **ДЕТСКАЯ МАТРИЦА** 👶

Расчёт потенциала и предназначения ребёнка.

**Введите дату рождения ребёнка**
Формат: ДД.ММ.ГГГГ
Пример: 15.05.2020
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data='matrix_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# ============ НУМЕРОЛОГИЯ ============

async def numerology_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расширенное меню нумерологии"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📊 Полный отчёт", callback_data='num_full')],
        [InlineKeyboardButton("👤 Число Жизненного Пути", callback_data='num_lifepath')],
        [InlineKeyboardButton("🎯 Персональный год 2026", callback_data='num_year')],
        [InlineKeyboardButton("🔢 Квадрат Пифагора", callback_data='num_pythagoras')],
        [InlineKeyboardButton("◀️ Главное меню", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
🔢 **НУМЕРОЛОГИЯ** 🔢

Наука о числах и их влиянии на судьбу!

**Что можно узнать:**

📊 **Полный отчёт** - все числа  
👤 **Число Жизненного Пути** - ваше предназначение
🎯 **Персональный год** - энергия 2026 года
🔢 **Квадрат Пифагора** - психоматрица

**Полный отчёт включает:**
• Число Жизненного Пути  
• Число Судьбы
• Число Души
• Число Личности
• Число Зрелости
• Кармические числа
• Персональный год (2026)
• Персональный месяц
• Пиковые циклы

Что хотите узнать?
    """
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def numerology_full_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало полного нумерологического отчёта"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_numerology_full'
    user_data[user_id] = {}
    
    text = """
📊 **ПОЛНЫЙ НУМЕРОЛОГИЧЕСКИЙ ОТЧЁТ** 📊

Введите данные в следующем формате:

**Строка 1:** Дата рождения (ДД.ММ.ГГГГ)
**Строка 2:** Полное имя (Фамилия Имя Отчество)
**Строка 3:** Время рождения (ЧЧ:ММ) - опционально
**Строка 4:** Место рождения (город) - опционально

**Пример:**
```
15.05.1990
Иванов Иван Иванович
14:30
Москва
```

Минимум нужна дата и имя.
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data='numerology_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def numerology_lifepath_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расчёт Числа Жизненного Пути"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_lifepath_date'
    user_data[user_id] = {}
    
    text = """
👤 **ЧИСЛО ЖИЗНЕННОГО ПУТИ** 👤

Это главное число в нумерологии - ваше предназначение!

**Введите дату рождения**
Формат: ДД.ММ.ГГГГ
Пример: 15.05.1990
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data='numerology_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def numerology_year_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расчёт Персонального года"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_year_date'
    user_data[user_id] = {}
    
    text = """
🎯 **ПЕРСОНАЛЬНЫЙ ГОД 2026** 🎯

Узнайте энергию вашего года!

**Введите дату рождения**
Формат: ДД.ММ.ГГГГ
Пример: 15.05.1990
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data='numerology_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def numerology_pythagoras_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Расчёт Квадрата Пифагора"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = 'waiting_pythagoras_date'
    user_data[user_id] = {}
    
    text = """
🔢 **КВАДРАТ ПИФАГОРА** 🔢

Психоматрица - уникальный портрет личности!

**Введите дату рождения**
Формат: ДД.ММ.ГГГГ
Пример: 15.05.1990
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data='numerology_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# ============ ИНФОРМАЦИЯ ============

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация о боте"""
    query = update.callback_query
    await query.answer()
    
    text = """
ℹ️ **О СЕРВИСЕ PREMIUM** ℹ️

**🎴 ТАРО:**
• Колода Райдера-Уайта (78 карт)
• 6 типов раскладов
• Профессиональные толкования

**⭐ МАТРИЦА СУДЬБЫ:**
• 22 энергии старших арканов
• Расчёт по методу Натальи Ладини
• Линии денег, любви, здоровья
• Кармические задачи
• Совместимость партнёров

**🔢 НУМЕРОЛОГИЯ:**
• 9 ключевых чисел
• Квадрат Пифагора
• Персональные прогнозы
• Кармические уроки
• Циклы жизни

**📚 Источники:**
• "Таро Райдера-Уайта" - А. Уайт
• "Матрица Судьбы" - Н. Ладини  
• "Нумерология" - Пифагор

⚠️ Помните: эзотерика - инструмент познания, решения принимаете вы!
    """
    
    keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# ============ ОБРАБОТКА ТЕКСТА ============

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    user_id = update.message.from_user.id
    text = update.message.text
    
    state = user_states.get(user_id)

    # Обработка команд /arcana_N и /karma_X-Y-Z прямо в тексте
    if text.startswith('/arcana_'):
        try:
            arcana_num = int(text.replace('/arcana_', '').strip())
            await handle_arcana_command(update, context, arcana_num)
        except ValueError:
            await update.message.reply_text("⚠️ Используйте формат: /arcana_7 (1-22)")
        return

    if text.startswith('/karma_'):
        from modules.matrix_descriptions import KARMIC_PROGRAMS, get_karmic_program
        key = text.replace('/karma_', '').strip().replace('_', '-')
        result = get_karmic_program(key)
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    if text.startswith('/aspect_'):
        from modules.matrix_descriptions import get_aspect_description
        key = text.replace('/aspect_', '').strip()
        result = get_aspect_description(key)
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    if state == 'waiting_chart_date':
        import re
        if re.match(r'^\d{2}\.\d{2}\.\d{4}$', text.strip()):
            birth_date = text.strip()
            user_data.setdefault(user_id, {})['birth_date'] = birth_date
            user_states.pop(user_id, None)
            await _send_matrix_chart(update.message, user_id, birth_date)
        else:
            await update.message.reply_text(
                "⚠️ Неверный формат. Введите дату в виде <b>ДД.ММ.ГГГГ</b>\nНапример: <code>15.03.1990</code>",
                parse_mode='HTML'
            )
        return

    if state == 'waiting_tarot_three_question':
        # Получен вопрос для расклада три карты
        question = text
        result_text, cards = tarot.three_card_spread()
        
        # Добавляем вопрос в начало
        final_text = f"**Ваш вопрос:** _{question}_\n\n{result_text}"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Новый расклад", callback_data='tarot_three')],
            [InlineKeyboardButton("◀️ Меню Таро", callback_data='tarot_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(final_text, reply_markup=reply_markup, parse_mode='Markdown')
        user_states.pop(user_id, None)
    
    elif state == 'waiting_yes_no_question':
        # Получен вопрос для гадания Да/Нет
        question = text
        result = tarot.yes_no_spread(question)
        
        keyboard = [
            [InlineKeyboardButton("🔄 Новый вопрос", callback_data='yes_no')],
            [InlineKeyboardButton("◀️ Главное меню", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(result, reply_markup=reply_markup, parse_mode='Markdown')
        user_states.pop(user_id, None)
    
    elif state == 'waiting_matrix_date':
        # Сохраняем дату и запрашиваем время
        user_data[user_id]['birth_date'] = text
        user_states[user_id] = 'waiting_matrix_time'
        
        keyboard = [[InlineKeyboardButton("⏩ Пропустить", callback_data='matrix_skip_time')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "**Шаг 2 из 4: Время рождения**\nФормат: ЧЧ:ММ\nПример: 14:30\n\nМожно пропустить.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif state == 'waiting_matrix_time':
        # Сохраняем время и запрашиваем место
        user_data[user_id]['birth_time'] = text
        user_states[user_id] = 'waiting_matrix_place'
        
        keyboard = [[InlineKeyboardButton("⏩ Пропустить", callback_data='matrix_skip_place')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "**Шаг 3 из 4: Место рождения**\nУкажите город\nПример: Москва\n\nМожно пропустить.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif state == 'waiting_matrix_place':
        # Сохраняем место и запрашиваем пол
        user_data[user_id]['birth_place'] = text
        user_states[user_id] = 'waiting_matrix_gender'
        
        keyboard = [
            [InlineKeyboardButton("👨 Мужской", callback_data='matrix_gender_male')],
            [InlineKeyboardButton("👩 Женский", callback_data='matrix_gender_female')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "**Шаг 4 из 4: Пол**\nВыберите пол:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif state == 'waiting_compatibility_date1':
        # Сохраняем первую дату и запрашиваем вторую
        user_data[user_id]['date1'] = text
        user_states[user_id] = 'waiting_compatibility_date2'
        
        await update.message.reply_text(
            "**Шаг 2 из 2: Второй партнер**\nВведите дату рождения второго партнера\nФормат: ДД.ММ.ГГГГ",
            parse_mode='Markdown'
        )
    
    elif state == 'waiting_compatibility_date2':
        # Сохраняем вторую дату и делаем расчёт
        date1 = user_data[user_id].get('date1')
        date2 = text
        
        result = matrix.calculate_compatibility(date1, date2)
        
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(result, reply_markup=reply_markup, parse_mode='Markdown')
        
        user_states.pop(user_id, None)
        user_data.pop(user_id, None)
    
    elif state == 'waiting_child_date':
        # Расчёт детской матрицы
        result = matrix.full_calculation(text)
        
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(result, reply_markup=reply_markup, parse_mode='Markdown')
        
        user_states.pop(user_id, None)
        user_data.pop(user_id, None)
    
    elif state == 'waiting_numerology_full':
        # Расчёт полной нумерологии
        lines = text.strip().split('\n')
        
        if len(lines) < 2:
            await update.message.reply_text(
                "❌ Пожалуйста, укажите минимум дату рождения и полное имя (каждое на новой строке)"
            )
            return
        
        birth_date = lines[0].strip()
        full_name = lines[1].strip()
        birth_time = lines[2].strip() if len(lines) > 2 else None
        birth_place = lines[3].strip() if len(lines) > 3 else None
        
        result = numerology.full_report(birth_date, full_name, birth_time, birth_place)
        
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(result, reply_markup=reply_markup, parse_mode='Markdown')
        user_states.pop(user_id, None)
        user_data.pop(user_id, None)
    
    elif state == 'waiting_lifepath_date':
        # Расчёт Числа Жизненного Пути
        result_data = numerology.calculate_life_path(text)
        
        if 'error' in result_data:
            await update.message.reply_text(f"❌ {result_data['error']}")
            return
        
        result = f"👤 **ЧИСЛО ЖИЗНЕННОГО ПУТИ: {result_data['number']}**\n\n"
        result += f"**{result_data['meaning']['name']}**\n\n"
        result += f"📋 {result_data['meaning']['description']}\n\n"
        result += f"✅ **Сильные стороны:**\n{result_data['meaning']['traits']}\n\n"
        result += f"⚠️ **Вызовы:**\n{result_data['meaning']['challenges']}\n\n"
        result += f"💼 **Карьера:**\n{result_data['meaning']['career']}"
        
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(result, reply_markup=reply_markup, parse_mode='Markdown')
        user_states.pop(user_id, None)
        user_data.pop(user_id, None)
    
    elif state == 'waiting_year_date':
        # Расчёт Персонального года
        result_data = numerology.calculate_personal_year(text)
        
        if 'error' in result_data:
            await update.message.reply_text(f"❌ {result_data['error']}")
            return
        
        result = f"🎯 **ПЕРСОНАЛЬНЫЙ ГОД {result_data['year']}: {result_data['number']}**\n\n"
        result += f"**Тема:** {result_data['info']['theme']}\n\n"
        result += f"📋 {result_data['info']['description']}\n\n"
        result += f"💡 **Совет:**\n{result_data['info']['advice']}"
        
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(result, reply_markup=reply_markup, parse_mode='Markdown')
        user_states.pop(user_id, None)
        user_data.pop(user_id, None)
    
    elif state == 'waiting_pythagoras_date':
        # Расчёт Квадрата Пифагора
        result_data = numerology.calculate_pythagoras_square(text)
        
        if 'error' in result_data:
            await update.message.reply_text(f"❌ {result_data['error']}")
            return
        
        result = "🔢 **КВАДРАТ ПИФАГОРА** 🔢\n\n"
        result += "**Психоматрица:**\n\n"
        
        qualities_names = {
            'character': '💪 Характер',
            'energy': '⚡ Энергия', 
            'interest': '🧠 Интерес к наукам',
            'health': '❤️ Здоровье',
            'logic': '🤔 Логика',
            'labor': '💼 Трудолюбие',
            'luck': '🍀 Удача',
            'duty': '⚖️ Долг',
            'memory': '📚 Память'
        }
        
        for key, name in qualities_names.items():
            count = result_data['qualities'][key]
            result += f"{name}: {'●' * count if count > 0 else 'нет'} ({count})\n"
        
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(result, reply_markup=reply_markup, parse_mode='Markdown')
        user_states.pop(user_id, None)
        user_data.pop(user_id, None)
    
    else:
        # Неизвестное состояние
        await start(update, context)

# ============ ОБРАБОТКА CALLBACK ============

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    data = query.data
    logging.info(f"[BUTTON] user={query.from_user.id} data={data}")
    user_id = query.from_user.id
    
    # Главное меню
    if data == 'back':
        user_states.pop(user_id, None)
        user_data.pop(user_id, None)
        await start(update, context)
    
    # Таро
    elif data == 'tarot_menu':
        await tarot_menu(update, context)
    elif data == 'tarot_day':
        await tarot_day_reading(update, context)
    elif data == 'tarot_three':
        await tarot_three_reading(update, context)
    elif data == 'tarot_week':
        await tarot_week_reading(update, context)
    elif data == 'tarot_celtic':
        await tarot_celtic_reading(update, context)
    elif data == 'tarot_love':
        await tarot_love_reading(update, context)
    elif data == 'tarot_money':
        await tarot_money_reading(update, context)
    elif data == 'tarot_career':
        await tarot_career_reading(update, context)
    elif data == 'tarot_three_no_question':
        # Расклад три карты без вопроса
        text, cards = tarot.three_card_spread()
        keyboard = [
            [InlineKeyboardButton("🔄 Новый расклад", callback_data='tarot_three')],
            [InlineKeyboardButton("◀️ Меню Таро", callback_data='tarot_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        user_states.pop(user_id, None)
    
    # Матрица
    elif data == 'matrix_menu':
        await matrix_menu(update, context)
    elif data == 'matrix_full':
        await matrix_full_start(update, context)
    elif data == 'matrix_compatibility':
        await matrix_compatibility_start(update, context)
    elif data == 'matrix_child':
        await matrix_child_start(update, context)
    elif data == 'matrix_chart':
        await query.answer()
        birth_date = user_data.get(user_id, {}).get('birth_date')
        if not birth_date:
            # Запрашиваем дату прямо сейчас
            user_states[user_id] = 'waiting_chart_date'
            keyboard = [[InlineKeyboardButton("◀️ Отмена", callback_data='matrix_menu')]]
            await query.message.reply_text(
                "🔮 <b>Круговая диаграмма Матрицы Судьбы</b>\n\n"
                "Введите дату рождения в формате <b>ДД.ММ.ГГГГ</b>\n"
                "Например: <code>15.03.1990</code>",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='HTML'
            )
        else:
            await _send_matrix_chart(query.message, user_id, birth_date)

    elif data == 'matrix_arcanas_list':
        await query.answer()
        text = matrix.get_all_arcanas_list()
        keyboard = [[InlineKeyboardButton("◀️ Меню Матрицы", callback_data='matrix_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    elif data == 'matrix_aspects_menu':
        await query.answer()
        text = matrix.get_aspects_menu()
        keyboard = [[InlineKeyboardButton("◀️ Меню Матрицы", callback_data='matrix_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    elif data == 'matrix_full_detailed':
        await query.answer()
        birth_date = user_data.get(user_id, {}).get('birth_date')
        if not birth_date:
            await query.message.reply_text("⚠️ Сначала рассчитайте Матрицу через меню — Э Матрица Судьбы")
            return
        birth_time = user_data.get(user_id, {}).get('birth_time')
        birth_place = user_data.get(user_id, {}).get('birth_place')
        gender = user_data.get(user_id, {}).get('gender', 'female')
        matrix_data = matrix.calculate_full_matrix(birth_date, birth_time, birth_place)
        result = matrix.format_full_matrix_result(matrix_data, gender)
        MAX_LEN = 4000
        parts = [result[i:i+MAX_LEN] for i in range(0, len(result), MAX_LEN)]
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        for i, part in enumerate(parts):
            markup = reply_markup if i == len(parts) - 1 else None
            await query.message.reply_text(part, reply_markup=markup, parse_mode='HTML')
    elif data == 'matrix_skip_time':
        user_data[user_id]['birth_time'] = None
        user_states[user_id] = 'waiting_matrix_place'
        await query.answer()
        
        keyboard = [[InlineKeyboardButton("⏩ Пропустить", callback_data='matrix_skip_place')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            "**Шаг 3 из 4: Место рождения**\nУкажите город\nПример: Москва",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif data == 'matrix_skip_place':
        user_data[user_id]['birth_place'] = None
        user_states[user_id] = 'waiting_matrix_gender'
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("👨 Мужской", callback_data='matrix_gender_male')],
            [InlineKeyboardButton("👩 Женский", callback_data='matrix_gender_female')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            "**Шаг 4 из 4: Пол**\nВыберите пол:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif data in ['matrix_gender_male', 'matrix_gender_female']:
        await query.answer()
        gender = 'male' if data == 'matrix_gender_male' else 'female'
        
        # Получаем данные
        birth_date = user_data[user_id].get('birth_date')
        birth_time = user_data[user_id].get('birth_time')
        birth_place = user_data[user_id].get('birth_place')
        
        # Сохраняем гендер для /matrix_full
        user_data[user_id]['gender'] = gender

        # Расчёт матрицы
        result = matrix.full_calculation(birth_date, birth_time, birth_place, gender)
        
        keyboard = [
            [InlineKeyboardButton("🔮 Круговая диаграмма", callback_data='matrix_chart')],
            [InlineKeyboardButton("📜 Полная расшифровка", callback_data='matrix_full_detailed')],
            [InlineKeyboardButton("◀️ Главное меню", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(result, reply_markup=reply_markup, parse_mode='Markdown')
        
        user_states.pop(user_id, None)
        # Не чистим user_data - оставляем для /matrix_full
    
    # Нумерология
    elif data == 'numerology_menu':
        await numerology_menu(update, context)
    elif data == 'num_full':
        await numerology_full_start(update, context)
    elif data == 'num_lifepath':
        await numerology_lifepath_start(update, context)
    elif data == 'num_year':
        await numerology_year_start(update, context)
    elif data == 'num_pythagoras':
        await numerology_pythagoras_start(update, context)
    
    # Да/Нет
    elif data == 'yes_no':
        await yes_no_start(update, context)
    
    # Информация
    elif data == 'info':
        await info(update, context)

# ========================
# ОБРАБОТЧИКИ КОМАНД МАТРИЦЫ СУДЬБЫ
# ========================

async def cmd_arcanas_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Список всех 22 арканов"""
    text = matrix.get_all_arcanas_list()
    keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text, reply_markup=reply_markup, parse_mode='HTML'
    )

async def cmd_aspects_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню аспектов Матрицы"""
    text = matrix.get_aspects_menu()
    keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text, reply_markup=reply_markup, parse_mode='HTML'
    )

async def cmd_matrix_full(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Полная расшифровка сохранённой матрицы"""
    user_id = update.effective_user.id
    birth_date = user_data.get(user_id, {}).get('birth_date')
    if not birth_date:
        await update.message.reply_text(
            "⚠️ Сначала рассчитайте Матрицу через главное меню — ⭐ Матрица Судьбы"
        )
        return
    birth_time = user_data.get(user_id, {}).get('birth_time')
    birth_place = user_data.get(user_id, {}).get('birth_place')
    gender = user_data.get(user_id, {}).get('gender', 'female')
    matrix_data = matrix.calculate_full_matrix(birth_date, birth_time, birth_place)
    result = matrix.format_full_matrix_result(matrix_data, gender)
    # Делим на части если слишком длинная
    MAX_LEN = 4000
    parts = [result[i:i+MAX_LEN] for i in range(0, len(result), MAX_LEN)]
    keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    for i, part in enumerate(parts):
        markup = reply_markup if i == len(parts) - 1 else None
        await update.message.reply_text(part, reply_markup=markup, parse_mode='HTML')

async def handle_arcana_command(update: Update, context: ContextTypes.DEFAULT_TYPE, arcana_num: int):
    """Отобразить описание аркана"""
    if not 1 <= arcana_num <= 22:
        await update.message.reply_text("⚠️ Аркан должен быть от 1 до 22")
        return
    text = matrix.get_arcana_description(arcana_num)
    keyboard = [
        [InlineKeyboardButton("🃏 Список всех арканов", callback_data='matrix_arcanas_list')],
        [InlineKeyboardButton("◀️ Главное меню", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')

async def handle_dynamic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик динамических команд: /arcana_N, /karma_X-Y-Z, /aspect_X"""
    text = update.message.text.split()[0]  # берём только команду без аргументов

    if text.startswith('/arcana_'):
        try:
            arcana_num = int(text.replace('/arcana_', '').strip())
            await handle_arcana_command(update, context, arcana_num)
        except ValueError:
            await update.message.reply_text("⚠️ Используйте формат: /arcana_7 (от 1 до 22)")

    elif text.startswith('/karma_'):
        from modules.matrix_descriptions import get_karmic_program
        key = text.replace('/karma_', '').strip().replace('_', '-')
        result = get_karmic_program(key)
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    elif text.startswith('/aspect_'):
        from modules.matrix_descriptions import get_aspect_description
        key = text.replace('/aspect_', '').strip()
        result = get_aspect_description(key)
        keyboard = [[InlineKeyboardButton("◀️ Главное меню", callback_data='back')]]
        await update.message.reply_text(result, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def _send_matrix_chart(message, user_id: int, birth_date: str):
    """Генерирует и отправляет диаграмму матрицы"""
    import io
    await message.reply_text("⏳ Генерирую диаграмму...")
    try:
        name = user_data.get(user_id, {}).get('name', '')
        img_bytes = generate_matrix_image(birth_date, name)
        mdata = calculate_matrix(birth_date)
        caption = (
            f"🔮 <b>Матрица Судьбы</b>\n"
            f"📅 {birth_date}\n\n"
            f"☁ Небо: <b>{mdata['top']}</b>  🌍 Земля: <b>{mdata['bottom']}</b>\n"
            f"♀ Женское: <b>{mdata['left']}</b>  ♂ Мужское: <b>{mdata['right']}</b>\n"
            f"⭐ Предназначение: <b>{mdata['center']}</b>\n\n"
            f"👤 Личное: <b>{mdata['personal']}</b>  "
            f"👥 Социальное: <b>{mdata['social']}</b>  "
            f"🌟 Духовное: <b>{mdata['spiritual']}</b>"
        )
        keyboard = [
            [InlineKeyboardButton("📜 Полная расшифровка", callback_data='matrix_full_detailed')],
            [InlineKeyboardButton("◀️ Меню Матрицы", callback_data='matrix_menu')]
        ]
        await message.reply_photo(
            photo=io.BytesIO(img_bytes),
            caption=caption,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await message.reply_text(f"❌ Ошибка генерации: {e}")

def main():
    """Запуск бота"""
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if not BOT_TOKEN:
        print("Ошибка: не найден BOT_TOKEN!")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("arcanas", cmd_arcanas_list))
    app.add_handler(CommandHandler("aspects", cmd_aspects_menu))
    app.add_handler(CommandHandler("matrix_full", cmd_matrix_full))
    app.add_handler(CallbackQueryHandler(button_handler))
    # Обработчик динамических команд /arcana_N, /karma_X, /aspect_X
    app.add_handler(MessageHandler(filters.Regex(r'^/(arcana_|karma_|aspect_)'), handle_dynamic_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Бот PREMIUM запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

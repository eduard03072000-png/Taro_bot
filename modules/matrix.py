"""
Расширенный модуль Матрицы Судьбы
Полный расчет по дате, времени и месту рождения
С полными описаниями всех арканов и аспектов
"""
from datetime import datetime
from typing import Dict, List, Tuple
import math
from modules.matrix_descriptions import ARCANAS as ARCANAS_FULL, ASPECTS, KARMIC_PROGRAMS, get_arcana_full_description, get_aspect_description

class MatrixExtended:
    def __init__(self):
        self.arcanas = self._load_arcanas()
    
    def _load_arcanas(self) -> Dict[int, Dict]:
        """Загрузить значения 22 Арканов"""
        return {
            1: {
                'name': 'Маг',
                'description': 'Энергия действия, силы воли, начинаний',
                'plus': 'Уверенность, харизма, лидерство, активность',
                'minus': 'Манипуляции, обман, самонадеянность'
            },
            2: {
                'name': 'Жрица',
                'description': 'Интуиция, мудрость, тайные знания',
                'plus': 'Глубокое понимание, экстрасенсорика, мудрость',
                'minus': 'Скрытность, пассивность, оторванность от реальности'
            },
            3: {
                'name': 'Императрица',
                'description': 'Женская энергия, творчество, красота, плодородие',
                'plus': 'Творческий потенциал, забота, изобилие',
                'minus': 'Зависимость от мнения, жертвенность'
            },
            4: {
                'name': 'Император',
                'description': 'Власть, структура, порядок, стабильность',
                'plus': 'Организованность, ответственность, защита',
                'minus': 'Тирания, жесткость, контроль'
            },
            5: {
                'name': 'Иерофант',
                'description': 'Традиции, обучение, духовность',
                'plus': 'Мудрость, наставничество, традиции',
                'minus': 'Догматизм, консерватизм'
            },
            6: {
                'name': 'Влюбленные',
                'description': 'Выбор, отношения, партнерство',
                'plus': 'Гармония в отношениях, правильный выбор',
                'minus': 'Сомнения, зависимость, неверный выбор'
            },
            7: {
                'name': 'Колесница',
                'description': 'Победа, движение вперед, целеустремленность',
                'plus': 'Достижение целей, контроль, успех',
                'minus': 'Агрессия, упрямство, потеря контроля'
            },
            8: {
                'name': 'Справедливость',
                'description': 'Баланс, истина, кармические последствия',
                'plus': 'Честность, объективность, справедливость',
                'minus': 'Жестокость, фанатизм правил'
            },
            9: {
                'name': 'Отшельник',
                'description': 'Одиночество, поиск истины, внутренняя мудрость',
                'plus': 'Самопознание, мудрость, духовный рост',
                'minus': 'Изоляция, одиночество, уход от жизни'
            },
            10: {
                'name': 'Колесо Фортуны',
                'description': 'Удача, судьба, перемены, цикличность',
                'plus': 'Везение, новые возможности, изменения к лучшему',
                'minus': 'Нестабильность, зависимость от обстоятельств'
            },
            11: {
                'name': 'Сила',
                'description': 'Внутренняя сила, мужество, контроль над инстинктами',
                'plus': 'Смелость, терпение, власть над собой',
                'minus': 'Слабость, страхи, неконтролируемые эмоции'
            },
            12: {
                'name': 'Повешенный',
                'description': 'Жертва, новый взгляд, пауза, трансформация',
                'plus': 'Переосмысление, духовный рост, терпение',
                'minus': 'Жертвенность, застой, страдания'
            },
            13: {
                'name': 'Смерть',
                'description': 'Трансформация, окончание, новое начало',
                'plus': 'Обновление, освобождение, трансформация',
                'minus': 'Страх перемен, разрушение, потери'
            },
            14: {
                'name': 'Умеренность',
                'description': 'Баланс, гармония, исцеление',
                'plus': 'Гармония, терпение, исцеление',
                'minus': 'Дисбаланс, крайности'
            },
            15: {
                'name': 'Дьявол',
                'description': 'Зависимости, материальное, искушения',
                'plus': 'Материальное изобилие, страсть, магнетизм',
                'minus': 'Зависимости, рабство, искушения'
            },
            16: {
                'name': 'Башня',
                'description': 'Разрушение, кризис, озарение',
                'plus': 'Освобождение от иллюзий, озарение',
                'minus': 'Кризис, разрушение, потрясения'
            },
            17: {
                'name': 'Звезда',
                'description': 'Надежда, вдохновение, исцеление',
                'plus': 'Вдохновение, надежда, исцеление',
                'minus': 'Разочарование, потеря веры'
            },
            18: {
                'name': 'Луна',
                'description': 'Иллюзии, подсознание, страхи',
                'plus': 'Интуиция, творчество, мистицизм',
                'minus': 'Иллюзии, страхи, обман'
            },
            19: {
                'name': 'Солнце',
                'description': 'Радость, успех, ясность',
                'plus': 'Радость, успех, жизненная энергия',
                'minus': 'Эгоизм, высокомерие'
            },
            20: {
                'name': 'Суд',
                'description': 'Возрождение, призвание, оценка',
                'plus': 'Возрождение, исцеление рода, призвание',
                'minus': 'Осуждение, застревание в прошлом'
            },
            21: {
                'name': 'Мир',
                'description': 'Завершение, гармония, успех',
                'plus': 'Завершение цикла, гармония, успех',
                'minus': 'Незавершенность, застой'
            },
            22: {
                'name': 'Шут',
                'description': 'Начало, спонтанность, свобода',
                'plus': 'Новые начинания, свобода, оптимизм',
                'minus': 'Безответственность, наивность, хаос'
            }
        }
    
    def _reduce_to_arcana(self, number: int) -> int:
        """Привести число к диапазону 1-22"""
        while number > 22:
            number = sum(int(d) for d in str(number))
        return number if number > 0 else 22
    
    def calculate_full_matrix(self, birth_date: str, birth_time: str = None, 
                             birth_place: str = None) -> Dict:
        """
        Полный расчет Матрицы Судьбы
        Args:
            birth_date: дата рождения в формате DD.MM.YYYY
            birth_time: время рождения в формате HH:MM (опционально)
            birth_place: место рождения (опционально)
        """
        try:
            day, month, year = map(int, birth_date.split('.'))
        except:
            return {'error': 'Неверный формат даты. Используйте DD.MM.YYYY'}
        
        # Базовые расчеты
        point_a = self._reduce_to_arcana(day + month + year)
        point_b = self._reduce_to_arcana(day + month)
        point_c = self._reduce_to_arcana(month + year)
        point_d = self._reduce_to_arcana(day + year)
        point_e = self._reduce_to_arcana(day)
        
        # Центр матрицы (предназначение)
        center = self._reduce_to_arcana(point_a + point_b + point_c + point_d)
        
        # Линия неба (духовное)
        heaven_1 = self._reduce_to_arcana(point_a + point_b)
        heaven_2 = self._reduce_to_arcana(point_b + point_c)
        
        # Линия земли (материальное)
        earth_1 = self._reduce_to_arcana(point_c + point_d)
        earth_2 = self._reduce_to_arcana(point_d + point_e)
        
        # Точка комфорта
        comfort = self._reduce_to_arcana(day)
        
        result = {
            'date': birth_date,
            'time': birth_time,
            'place': birth_place,
            'center': center,
            'point_a': point_a,
            'point_b': point_b,
            'point_c': point_c,
            'point_d': point_d,
            'point_e': point_e,
            'heaven_line': [heaven_1, heaven_2],
            'earth_line': [earth_1, earth_2],
            'comfort': comfort
        }
        
        return result
    
    def format_matrix_result(self, matrix_data: Dict) -> str:
        """Форматировать результат матрицы для отображения"""
        if 'error' in matrix_data:
            return matrix_data['error']
        
        result = "🔮 *<b>МАТРИЦА СУДЬБЫ</b>*\n\n"
        result += f"📅 Дата рождения: {matrix_data['date']}\n"
        if matrix_data.get('time'):
            result += f"🕐 Время: {matrix_data['time']}\n"
        if matrix_data.get('place'):
            result += f"📍 Место: {matrix_data['place']}\n"
        result += "\n"
        
        # Центр - Предназначение
        center = matrix_data['center']
        arcana = self.arcanas[center]
        result += f"⭐ *<b>ПРЕДНАЗНАЧЕНИЕ</b>* (Центр)\n"
        result += f"Аркан {center}: {arcana['name']}\n"
        result += f"{arcana['description']}\n"
        result += f"➕ {arcana['plus']}\n"
        result += f"➖ {arcana['minus']}\n\n"
        
        # Личные качества
        result += f"👤 *<b>ЛИЧНЫЕ КАЧЕСТВА</b>*\n"
        for key, label in [('point_a', 'Личность'), ('point_b', 'Таланты'), 
                          ('point_c', 'Энергия'),('point_d', 'Здоровье')]:
            arcana_num = matrix_data[key]
            arcana = self.arcanas[arcana_num]
            result += f"• {label} - Аркан {arcana_num}: {arcana['name']}\n"
        result += "\n"
        
        # Линия любви
        result += f"❤️ *<b>ЛИНИЯ ЛЮБВИ И ОТНОШЕНИЙ</b>*\n"
        for i, arcana_num in enumerate(matrix_data['heaven_line'], 1):
            arcana = self.arcanas[arcana_num]
            result += f"Энергия {i}: Аркан {arcana_num} - {arcana['name']}\n"
            result += f"{arcana['description']}\n"
        result += "\n"
        
        # Линия денег
        result += f"💰 *<b>ЛИНИЯ ДЕНЕГ И ФИНАНСОВ</b>*\n"
        for i, arcana_num in enumerate(matrix_data['earth_line'], 1):
            arcana = self.arcanas[arcana_num]
            result += f"Энергия {i}: Аркан {arcana_num} - {arcana['name']}\n"
            result += f"{arcana['description']}\n"
        result += "\n"
        
        # Точка комфорта
        comfort_arcana = self.arcanas[matrix_data['comfort']]
        result += f"🏠 *<b>ТОЧКА КОМФОРТА</b>*\n"
        result += f"Аркан {matrix_data['comfort']}: {comfort_arcana['name']}\n"
        result += f"Где вы чувствуете себя комфортно:\n{comfort_arcana['plus']}\n"
        
        return result
    
    def calculate_compatibility(self, date1: str, date2: str) -> str:
        """Расчет совместимости двух людей"""
        matrix1 = self.calculate_full_matrix(date1)
        matrix2 = self.calculate_full_matrix(date2)
        
        if 'error' in matrix1 or 'error' in matrix2:
            return "❌ Ошибка в формате дат"
        
        # Расчет совместимости по центрам
        center1 = matrix1['center']
        center2 = matrix2['center']
        compatibility_score = self._reduce_to_arcana(center1 + center2)
        
        result = "💑 *<b>СОВМЕСТИМОСТЬ ПАРТНЕРОВ</b>*\n\n"
        result += f"Партнер 1: Аркан {center1} - {self.arcanas[center1]['name']}\n"
        result += f"Партнер 2: Аркан {center2} - {self.arcanas[center2]['name']}\n\n"
        
        result += f"Энергия пары: Аркан {compatibility_score}\n"
        arcana = self.arcanas[compatibility_score]
        result += f"*<b>{arcana['name']}</b>*\n"
        result += f"{arcana['description']}\n\n"
        
        # Анализ совместимости
        diff = abs(center1 - center2)
        if diff <= 3:
            result += "✅ *<b>Высокая совместимость</b>*\n"
            result += "У вас схожие жизненные цели и ценности\n"
        elif diff <= 7:
            result += "⚖️ *<b>Средняя совместимость</b>*\n"
            result += "Требуется работа над отношениями и компромиссы\n"
        else:
            result += "⚠️ *<b>Низкая совместимость</b>*\n"
            result += "Очень разные энергии, нужно много усилий\n"
        
        return result
    
    def get_personal_year(self, birth_date: str, current_year: int = 2026) -> str:
        """Расчет персонального года"""
        try:
            day, month, _ = map(int, birth_date.split('.'))
        except:
            return "❌ Неверный формат даты"
        
        personal_year_num = self._reduce_to_arcana(day + month + current_year)
        arcana = self.arcanas[personal_year_num]
        
        result = f"🗓️ *<b>ПЕРСОНАЛЬНЫЙ ГОД {current_year}</b>*\n\n"
        result += f"Ваша энергия года: Аркан {personal_year_num}\n"
        result += f"*<b>{arcana['name']}</b>*\n\n"
        result += f"📋 Описание: {arcana['description']}\n\n"
        result += f"✅ Что развивать:\n{arcana['plus']}\n\n"
        result += f"⚠️ Чего избегать:\n{arcana['minus']}\n"
        
        return result

    # ========================
    # НОВЫЕ МЕТОДЫ С ПОЛНЫМИ ОПИСАНИЯМИ
    # ========================

    def get_arcana_description(self, arcana_num: int) -> str:
        """Получить полное описание аркана из matrix_descriptions"""
        return get_arcana_full_description(arcana_num)

    def format_full_matrix_result(self, matrix_data: dict, gender: str = 'female') -> str:
        """
        Полная развёрнутая расшифровка всех позиций Матрицы Судьбы
        со ссылками на полные описания арканов
        """
        if 'error' in matrix_data:
            return matrix_data['error']

        def arc_name(n):
            return ARCANAS_FULL.get(n, {}).get('name', str(n))

        def arc_symbol(n):
            return ARCANAS_FULL.get(n, {}).get('symbol', '🔮')

        def arc_keywords(n):
            return ARCANAS_FULL.get(n, {}).get('keywords', '')

        def arc_description(n):
            return ARCANAS_FULL.get(n, {}).get('description', '')

        def arc_plus(n):
            return ARCANAS_FULL.get(n, {}).get('plus', '')

        def arc_minus(n):
            return ARCANAS_FULL.get(n, {}).get('minus', '')

        def arc_karma(n):
            return ARCANAS_FULL.get(n, {}).get('karma', '')

        pronoun = 'Она' if gender == 'female' else 'Он'
        pronoun2 = 'её' if gender == 'female' else 'его'

        lines = []
        lines.append(f"🔮 <b>МАТРИЦА СУДЬБЫ — ПОЛНАЯ РАСШИФРОВКА</b>")
        lines.append(f"📅 Дата рождения: {matrix_data['date']}")
        if matrix_data.get('time'):
            lines.append(f"🕐 Время: {matrix_data['time']}")
        if matrix_data.get('place'):
            lines.append(f"📍 Место: {matrix_data['place']}")
        lines.append("")

        # 1. Личность — точка A
        a = matrix_data['point_a']
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"👤 <b>ХАРАКТЕР И ЛИЧНОСТЬ</b> (Точка A)")
        lines.append(f"{arc_symbol(a)} Аркан {a} — {arc_name(a)}")
        lines.append(f"🔑 {arc_keywords(a)}")
        lines.append(arc_description(a))
        lines.append(f"✅ {arc_plus(a)}")
        lines.append(f"❌ {arc_minus(a)}")
        lines.append("")

        # 2. Таланты — точка B
        b = matrix_data['point_b']
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🌟 <b>ТАЛАНТЫ И СПОСОБНОСТИ</b> (Точка B)")
        lines.append(f"{arc_symbol(b)} Аркан {b} — {arc_name(b)}")
        lines.append(f"🔑 {arc_keywords(b)}")
        lines.append(arc_description(b))
        lines.append(f"✅ {arc_plus(b)}")
        lines.append(f"❌ {arc_minus(b)}")
        lines.append("")

        # 3. Задачи до 40 лет — точка C
        c = matrix_data['point_c']
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"⏳ <b>ЗАДАЧИ ДУШИ ДО 40 ЛЕТ</b> (Точка C)")
        lines.append(ASPECTS['soul_task_40']['description'])
        lines.append(f"{arc_symbol(c)} Аркан {c} — {arc_name(c)}")
        lines.append(f"🔑 {arc_keywords(c)}")
        lines.append(arc_description(c))
        lines.append(f"✅ Что развивать: {arc_plus(c)}")
        lines.append(f"❌ Что прорабатывать: {arc_minus(c)}")
        lines.append(f"🔮 {arc_karma(c)}")
        lines.append("")

        # 4. Главная проработка — точка D
        d = matrix_data['point_d']
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🎯 <b>ГЛАВНАЯ ПРОРАБОТКА ВСЕЙ ЖИЗНИ</b> (Точка D)")
        lines.append(ASPECTS['main_development']['description'])
        lines.append(f"{arc_symbol(d)} Аркан {d} — {arc_name(d)}")
        lines.append(f"🔑 {arc_keywords(d)}")
        lines.append(arc_description(d))
        lines.append(f"✅ В плюсе: {arc_plus(d)}")
        lines.append(f"❌ В минусе: {arc_minus(d)}")
        lines.append(f"🔮 {arc_karma(d)}")
        lines.append("")

        # 5. Зона комфорта — точка E
        e = matrix_data['point_e']
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🏠 <b>ЗОНА КОМФОРТА И ГАРМОНИИ</b> (Точка E)")
        lines.append(ASPECTS['comfort_zone']['description'])
        lines.append(f"{arc_symbol(e)} Аркан {e} — {arc_name(e)}")
        lines.append(f"🔑 {arc_keywords(e)}")
        lines.append(arc_description(e))
        lines.append(f"✅ {arc_plus(e)}")
        lines.append("")

        # 6. Предназначение — центр
        ctr = matrix_data['center']
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"⭐ <b>ПРЕДНАЗНАЧЕНИЕ — ЦЕНТР МАТРИЦЫ</b>")
        lines.append(ASPECTS['destiny']['description'])
        lines.append(f"{arc_symbol(ctr)} Аркан {ctr} — {arc_name(ctr)}")
        lines.append(f"🔑 {arc_keywords(ctr)}")
        lines.append(arc_description(ctr))
        lines.append(f"✅ {arc_plus(ctr)}")
        lines.append(f"❌ {arc_minus(ctr)}")
        lines.append(f"🔮 {arc_karma(ctr)}")
        lines.append("")

        # 7. Линия любви
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"❤️ <b>ЛИНИЯ ЛЮБВИ И ОТНОШЕНИЙ</b>")
        for i, arcana_num in enumerate(matrix_data['heaven_line'], 1):
            lines.append(f"Энергия {i}: {arc_symbol(arcana_num)} Аркан {arcana_num} — {arc_name(arcana_num)}")
            lines.append(f"🔑 {arc_keywords(arcana_num)}")
            lines.append(arc_description(arcana_num))
            lines.append(f"✅ {arc_plus(arcana_num)}")
            lines.append(f"❌ {arc_minus(arcana_num)}")
        lines.append("")

        # 8. Линия денег
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"💰 <b>ФИНАНСОВЫЙ КАНАЛ И ЛИНИЯ ДЕНЕГ</b>")
        lines.append(ASPECTS['money_channel']['description'])
        for i, arcana_num in enumerate(matrix_data['earth_line'], 1):
            lines.append(f"Энергия {i}: {arc_symbol(arcana_num)} Аркан {arcana_num} — {arc_name(arcana_num)}")
            lines.append(f"🔑 {arc_keywords(arcana_num)}")
            lines.append(arc_description(arcana_num))
            lines.append(f"✅ {arc_plus(arcana_num)}")
            lines.append(f"❌ {arc_minus(arcana_num)}")
        lines.append("")

        # 9. Кармический хвост
        comfort = matrix_data['comfort']
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🌀 <b>КАРМИЧЕСКИЙ ХВОСТ</b>")
        lines.append(ASPECTS['karmic_tail']['description'])
        lines.append(f"{arc_symbol(comfort)} Аркан {comfort} — {arc_name(comfort)}")
        lines.append(f"🔑 {arc_keywords(comfort)}")
        lines.append(arc_description(comfort))
        lines.append(f"✅ {arc_plus(comfort)}")
        lines.append(f"❌ {arc_minus(comfort)}")
        lines.append(f"🔮 {arc_karma(comfort)}")
        lines.append("")

        return "\n".join(lines)

    def format_matrix_short(self, matrix_data: dict) -> str:
        """Краткая версия матрицы для первого отображения"""
        if 'error' in matrix_data:
            return matrix_data['error']

        def arc_name(n):
            return ARCANAS_FULL.get(n, {}).get('name', str(n))

        def arc_symbol(n):
            return ARCANAS_FULL.get(n, {}).get('symbol', '🔮')

        lines = []
        lines.append(f"🔮 <b>МАТРИЦА СУДЬБЫ</b>")
        lines.append(f"📅 Дата рождения: {matrix_data['date']}")
        lines.append("")
        lines.append(f"⭐ <b>Предназначение (центр):</b>")
        ctr = matrix_data['center']
        lines.append(f"{arc_symbol(ctr)} Аркан {ctr} — {arc_name(ctr)}")
        lines.append(ARCANAS_FULL.get(ctr, {}).get('keywords', ''))
        lines.append("")
        lines.append(f"👤 <b>Личность (А):</b> {arc_symbol(matrix_data['point_a'])} Аркан {matrix_data['point_a']} — {arc_name(matrix_data['point_a'])}")
        lines.append(f"🌟 <b>Таланты (B):</b> {arc_symbol(matrix_data['point_b'])} Аркан {matrix_data['point_b']} — {arc_name(matrix_data['point_b'])}")
        lines.append(f"⏳ <b>Задачи до 40 (C):</b> {arc_symbol(matrix_data['point_c'])} Аркан {matrix_data['point_c']} — {arc_name(matrix_data['point_c'])}")
        lines.append(f"🎯 <b>Главная проработка (D):</b> {arc_symbol(matrix_data['point_d'])} Аркан {matrix_data['point_d']} — {arc_name(matrix_data['point_d'])}")
        lines.append(f"🏠 <b>Зона комфорта (E):</b> {arc_symbol(matrix_data['point_e'])} Аркан {matrix_data['point_e']} — {arc_name(matrix_data['point_e'])}")
        lines.append("")
        love1, love2 = matrix_data['heaven_line']
        lines.append(f"❤️ <b>Линия любви:</b> {arc_symbol(love1)} {arc_name(love1)} + {arc_symbol(love2)} {arc_name(love2)}")
        money1, money2 = matrix_data['earth_line']
        lines.append(f"💰 <b>Линия денег:</b> {arc_symbol(money1)} {arc_name(money1)} + {arc_symbol(money2)} {arc_name(money2)}")
        lines.append("")
        lines.append("💬 Нажмите /matrix_full для <b>полной развёрнутой расшифровки</b> всех позиций")
        lines.append("📖 Нажмите /arcana_[число] для описания любого аркана (напр. /arcana_7)")
        return "\n".join(lines)

    def get_aspects_menu(self) -> str:
        """Меню всех доступных аспектов"""
        lines = ["📚 <b>РАЗДЕЛЫ МАТРИЦЫ СУДЬБЫ</b>", ""]
        for key, asp in ASPECTS.items():
            lines.append(f"• {asp['title']} — /aspect_{key}")
        lines.append("")
        lines.append("🌀 <b>Кармические программы:</b>")
        for key, prog in KARMIC_PROGRAMS.items():
            lines.append(f"• {prog['name']} ({key}) — /karma_{key.replace('-', '_')}")
        return "\n".join(lines)

    def get_all_arcanas_list(self) -> str:
        """Список всех 22 арканов"""
        lines = ["🃏 <b>22 АРКАНА МАТРИЦЫ СУДЬБЫ</b>", ""]
        for num, arc in ARCANAS_FULL.items():
            lines.append(f"{arc['symbol']} <b>Аркан {num} — {arc['name']}</b>")
            lines.append(f"🔑 {arc['keywords']}")
            lines.append(f"└ /arcana_{num}")
            lines.append("")
        return "\n".join(lines)

    # ============= ОБЁРТКА ДЛЯ СОВМЕСТИМОСТИ С BOT.PY =============
    def full_calculation(self, birth_date_str: str, birth_time: str = None, 
                        birth_place: str = None, gender: str = 'male') -> str:
        """
        Обёртка для метода calculate_full_matrix для совместимости с bot.py
        Args:
            birth_date_str: дата рождения в формате DD.MM.YYYY
            birth_time: время рождения в формате HH:MM (не используется в текущей версии)
            birth_place: место рождения (не используется в текущей версии)
            gender: пол (не используется в текущей версии)
        Returns:
            Форматированная строка с результатами расчёта
        """
        # Вызываем основной метод расчёта
        matrix_data = self.calculate_full_matrix(birth_date_str, birth_time, birth_place)
        
        # Если есть ошибка, возвращаем её
        if isinstance(matrix_data, dict) and 'error' in matrix_data:
            return f"❌ {matrix_data['error']}"
        
        # Форматируем результат - используем краткую версию + предложение полной
        return self.format_matrix_short(matrix_data)

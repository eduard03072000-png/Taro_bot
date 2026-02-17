"""
Генератор круговой диаграммы Матрицы Судьбы
Рисует диаграмму в виде квадрата с 4 угловыми точками, промежуточными и центром
Совместимо с методикой gadalkindom.ru
"""
import io
import math
from PIL import Image, ImageDraw, ImageFont


def reduce_to_arcana(n: int) -> int:
    """Привести число к диапазону 1-22"""
    while n > 22:
        n = sum(int(d) for d in str(n))
    if n == 0:
        n = 22
    return n


def calculate_matrix(birth_date: str) -> dict:
    """
    Рассчитать все точки Матрицы Судьбы
    Дата в формате DD.MM.YYYY
    Возвращает dict со всеми точками
    """
    try:
        parts = birth_date.split('.')
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
    except Exception:
        return {'error': 'Неверный формат даты'}

    yr = sum(int(d) for d in str(year))

    # Четыре угловые точки
    top    = reduce_to_arcana(day)       # Верх   (Небо)
    left   = reduce_to_arcana(month)     # Лево   (Женское)
    right  = reduce_to_arcana(yr)        # Право  (Мужское)
    bottom = reduce_to_arcana(day + month + yr)  # Низ (Земля)

    # Промежуточные точки (середины сторон)
    top_left     = reduce_to_arcana(top + left)
    left_bottom  = reduce_to_arcana(left + bottom)
    bottom_right = reduce_to_arcana(bottom + right)
    right_top    = reduce_to_arcana(right + top)

    # Центр матрицы (предназначение)
    center = reduce_to_arcana(top + left + right + bottom)

    # Предназначения
    personal   = reduce_to_arcana(bottom + top)        # Личное (Земля + Небо)
    social     = reduce_to_arcana(left + right)         # Социальное (Жен + Муж)  
    spiritual  = reduce_to_arcana(personal + social)    # Духовное

    # Дополнительные точки диагоналей
    diag1 = reduce_to_arcana(top + bottom)     # Вертикальная диагональ
    diag2 = reduce_to_arcana(left + right)     # Горизонтальная диагональ

    return {
        'date': birth_date,
        # Углы
        'top': top,          # Небо
        'left': left,        # Женское
        'right': right,      # Мужское
        'bottom': bottom,    # Земля
        # Промежуточные
        'top_left': top_left,
        'left_bottom': left_bottom,
        'bottom_right': bottom_right,
        'right_top': right_top,
        # Центр
        'center': center,
        # Предназначения
        'personal': personal,
        'social': social,
        'spiritual': spiritual,
    }


def generate_matrix_image(birth_date: str, name: str = '') -> bytes:
    """
    Генерирует PNG-изображение круговой диаграммы Матрицы Судьбы
    Возвращает байты PNG
    """
    data = calculate_matrix(birth_date)
    if 'error' in data:
        raise ValueError(data['error'])

    # Размер холста
    W, H = 900, 1000
    img = Image.new('RGB', (W, H), color='#1a0a2e')
    draw = ImageDraw.Draw(img)

    # Шрифты
    try:
        font_big   = ImageFont.truetype("arial.ttf", 36)
        font_med   = ImageFont.truetype("arial.ttf", 26)
        font_small = ImageFont.truetype("arial.ttf", 20)
        font_tiny  = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font_big   = ImageFont.load_default()
        font_med   = font_big
        font_small = font_big
        font_tiny  = font_big

    # Цвета
    C_BG       = '#1a0a2e'   # тёмно-фиолетовый фон
    C_SQUARE   = '#2d1b4e'   # цвет квадрата
    C_LINE     = '#9b59b6'   # линии
    C_DIAG     = '#e74c3c'   # диагонали
    C_CIRCLE   = '#2980b9'   # кружки чисел
    C_CIRCLE_C = '#e74c3c'   # кружок центра
    C_CIRCLE_P = '#27ae60'   # предназначения
    C_TEXT     = '#ffffff'   # белый текст
    C_GOLD     = '#f1c40f'   # золотой акцент
    C_PINK     = '#e91e8c'   # женское
    C_BLUE     = '#2196f3'   # мужское

    # Координаты квадрата (со смещением для заголовка)
    margin = 80
    sq_top   = margin + 60
    sq_left  = margin
    sq_right = W - margin
    sq_bot   = H - 240   # место для предназначений снизу

    sq_w = sq_right - sq_left
    sq_h = sq_bot - sq_top
    sq_size = min(sq_w, sq_h)
    cx = (sq_left + sq_right) // 2
    cy = (sq_top + sq_bot) // 2
    half = sq_size // 2

    # Угловые координаты квадрата
    pts = {
        'top':    (cx, cy - half),
        'left':   (cx - half, cy),
        'right':  (cx + half, cy),
        'bottom': (cx, cy + half),
    }
    # Промежуточные точки (середины сторон квадрата-ромба)
    pts['top_left']     = ((pts['top'][0]    + pts['left'][0])  // 2,
                           (pts['top'][1]    + pts['left'][1])  // 2)
    pts['left_bottom']  = ((pts['left'][0]   + pts['bottom'][0])// 2,
                           (pts['left'][1]   + pts['bottom'][1])// 2)
    pts['bottom_right'] = ((pts['bottom'][0] + pts['right'][0]) // 2,
                           (pts['bottom'][1] + pts['right'][1]) // 2)
    pts['right_top']    = ((pts['right'][0]  + pts['top'][0])   // 2,
                           (pts['right'][1]  + pts['top'][1])   // 2)

    # --- РИСОВАНИЕ ---

    # Заголовок
    title = f"МАТРИЦА СУДЬБЫ"
    draw.text((W//2, 30), title, fill=C_GOLD, font=font_big, anchor='mm')
    if name:
        draw.text((W//2, 68), name, fill=C_TEXT, font=font_med, anchor='mm')
    draw.text((W//2, 68 + (24 if name else 0)), birth_date, fill='#aaa', font=font_small, anchor='mm')

    # Фоновый квадрат (ромб)
    rhombus = [pts['top'], pts['right'], pts['bottom'], pts['left']]
    draw.polygon(rhombus, fill='#220d40', outline=C_LINE, width=2)

    # Внутренний квадрат (меньший ромб)
    inner_scale = 0.5
    inner = [
        (cx + (p[0]-cx)*inner_scale, cy + (p[1]-cy)*inner_scale)
        for p in [pts['top'], pts['right'], pts['bottom'], pts['left']]
    ]
    draw.polygon(inner, fill=None, outline='#4a2a7a', width=1)

    # Диагональные линии (крест внутри ромба)
    draw.line([pts['top'], pts['bottom']], fill=C_DIAG, width=2)
    draw.line([pts['left'], pts['right']], fill=C_DIAG, width=2)

    # Стороны ромба
    for a, b in [('top','left'), ('left','bottom'), ('bottom','right'), ('right','top')]:
        draw.line([pts[a], pts[b]], fill=C_LINE, width=2)

    # Линии от промежуточных точек к центру
    for key in ['top_left', 'left_bottom', 'bottom_right', 'right_top']:
        draw.line([pts[key], (cx, cy)], fill='#4a2a7a', width=1)

    def draw_circle(pos, number, color=C_CIRCLE, radius=28, font=font_med):
        x, y = pos
        r = radius
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color, outline='#ffffff', width=2)
        draw.text((x, y), str(number), fill='white', font=font, anchor='mm')

    def draw_label(pos, text, color=C_GOLD, offset=(0, -42), font=font_tiny):
        x, y = pos
        draw.text((x + offset[0], y + offset[1]), text, fill=color, font=font, anchor='mm')

    # Центр — большой кружок
    draw_circle((cx, cy), data['center'], color=C_CIRCLE_C, radius=38, font=font_big)
    draw_label((cx, cy), 'Предназначение', color=C_GOLD, offset=(0, -48), font=font_tiny)

    # Углы
    draw_circle(pts['top'],    data['top'],    color='#1565c0', radius=30, font=font_med)
    draw_label(pts['top'],  '☁ Небо',     color='#90caf9', offset=(0, -42))

    draw_circle(pts['left'],   data['left'],   color='#880e4f', radius=30, font=font_med)
    draw_label(pts['left'],  '♀ Женское', color=C_PINK, offset=(-56, 0))

    draw_circle(pts['right'],  data['right'],  color='#0d47a1', radius=30, font=font_med)
    draw_label(pts['right'], '♂ Мужское', color=C_BLUE, offset=(56, 0))

    draw_circle(pts['bottom'], data['bottom'], color='#2e7d32', radius=30, font=font_med)
    draw_label(pts['bottom'], '🌍 Земля',   color='#a5d6a7', offset=(0, 42))

    # Промежуточные точки
    draw_circle(pts['top_left'],     data['top_left'],     color='#4a148c', radius=24)
    draw_circle(pts['left_bottom'],  data['left_bottom'],  color='#4a148c', radius=24)
    draw_circle(pts['bottom_right'], data['bottom_right'], color='#4a148c', radius=24)
    draw_circle(pts['right_top'],    data['right_top'],    color='#4a148c', radius=24)

    # --- Блок предназначений внизу ---
    dest_y = sq_bot + 30
    block_w = 220
    spacing = (W - 3 * block_w) // 4

    positions = [
        (spacing + block_w//2,            dest_y, data['personal'],  '👤 Личное\n(до 40 лет)'),
        (spacing*2 + block_w + block_w//2, dest_y, data['social'],   '👥 Социальное\n(до 60 лет)'),
        (spacing*3 + block_w*2 + block_w//2, dest_y, data['spiritual'], '🌟 Духовное\n(после 60)'),
    ]

    for bx, by, num, label in positions:
        # Фоновый прямоугольник
        draw.rounded_rectangle([bx - block_w//2, by, bx + block_w//2, by + 90],
                                radius=12, fill='#2d1b4e', outline=C_LINE, width=1)
        # Число
        draw.text((bx, by + 30), str(num), fill=C_GOLD, font=font_big, anchor='mm')
        # Подпись
        for i, line in enumerate(label.split('\n')):
            draw.text((bx, by + 58 + i*18), line, fill='#bbb', font=font_tiny, anchor='mm')

    # Разделительная линия
    draw.line([(margin, sq_bot + 20), (W - margin, sq_bot + 20)], fill='#4a2a7a', width=1)

    # Формула предназначений
    formula_y = H - 45
    draw.text((W//2, formula_y),
              f"Небо {data['top']} + Земля {data['bottom']} = Личное {data['personal']}   |   "
              f"Жен {data['left']} + Муж {data['right']} = Социальное {data['social']}   |   "
              f"Духовное {data['spiritual']}",
              fill='#888', font=font_tiny, anchor='mm')

    # Сохраняем в байты
    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)
    return buf.getvalue()

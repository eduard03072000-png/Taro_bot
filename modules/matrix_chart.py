"""
Генератор круговой диаграммы Матрицы Судьбы
Детальная диаграмма — как на gadalkindom.ru
"""
import io
import math
from PIL import Image, ImageDraw, ImageFont


def red(n: int) -> int:
    while n > 22:
        n = sum(int(d) for d in str(n))
    return max(n, 1)


def calculate_matrix(birth_date: str) -> dict:
    """Полный расчёт всех точек матрицы. Дата DD.MM.YYYY"""
    try:
        parts = birth_date.strip().split('.')
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
    except Exception:
        return {'error': 'Неверный формат даты. Используйте ДД.ММ.ГГГГ'}

    yr = sum(int(d) for d in str(year))

    # 4 угла (основные энергии)
    top    = red(day)
    left   = red(month)
    right  = red(yr)
    bottom = red(day + month + yr)

    # 4 точки на сторонах ромба
    tl = red(top + left)
    lb = red(left + bottom)
    br = red(bottom + right)
    rt = red(right + top)

    # Центр (предназначение)
    center = red(top + left + right + bottom)

    # 4 внутренние точки (центр ↔ угол)
    ct = red(center + top)
    cl = red(center + left)
    cb = red(center + bottom)
    cr = red(center + right)

    # Предназначения
    personal  = red(bottom + top)
    social    = red(left + right)
    spiritual = red(personal + social)

    # Возрастные периоды (внешнее кольцо)
    # Годовые точки по часовой стрелке от верха
    age_points = {}
    # Период 0-20: верхняя левая сторона (top -> tl -> left)
    age_points[0]  = top
    age_points[10] = tl
    age_points[20] = left
    # Период 20-40: нижняя левая (left -> lb -> bottom)
    age_points[30] = lb
    age_points[40] = bottom
    # Период 40-60: нижняя правая (bottom -> br -> right)
    age_points[50] = br
    age_points[60] = right
    # Период 60-80: верхняя правая (right -> rt -> top)
    age_points[70] = rt

    return {
        'date': birth_date, 'day': day, 'month': month, 'year': year,
        'top': top, 'left': left, 'right': right, 'bottom': bottom,
        'tl': tl, 'lb': lb, 'br': br, 'rt': rt,
        'center': center,
        'ct': ct, 'cl': cl, 'cb': cb, 'cr': cr,
        'personal': personal, 'social': social, 'spiritual': spiritual,
        'age_points': age_points,
    }


def _font(path, size, fallback_size=None):
    """Загрузить шрифт с fallback"""
    import os
    fonts = [
        path,
        'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/ArialMT.ttf',
        'C:/Windows/Fonts/segoeui.ttf',
    ]
    for f in fonts:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()


def generate_matrix_image(birth_date: str, name: str = '') -> bytes:
    """Генерирует PNG диаграммы Матрицы Судьбы. Возвращает байты PNG."""
    d = calculate_matrix(birth_date)
    if 'error' in d:
        raise ValueError(d['error'])

    # ── Размер холста ──────────────────────────────────────────
    W, H = 1300, 1400
    img = Image.new('RGB', (W, H), '#0d0820')
    draw = ImageDraw.Draw(img)

    # ── Шрифты ────────────────────────────────────────────────
    fn_title  = _font('', 52)
    fn_name   = _font('', 36)
    fn_date   = _font('', 28)
    fn_num_lg = _font('', 46)   # числа в главных кружках
    fn_num_md = _font('', 34)   # числа в средних кружках
    fn_num_sm = _font('', 26)   # числа в малых кружках
    fn_label  = _font('', 22)
    fn_tiny   = _font('', 19)
    fn_age    = _font('', 20)

    # ── Цвета ────────────────────────────────────────────────
    BG        = '#0d0820'
    C_RHOMBUS = '#16092e'
    C_INNER   = '#1e0f3a'
    C_LINE    = '#7b3fa0'
    C_DIAG    = '#c0392b'
    C_GOLD    = '#f1c40f'
    C_WHITE   = '#ffffff'
    C_GRAY    = '#888888'
    C_LBLUE   = '#90caf9'
    C_LPINK   = '#f48fb1'
    C_LGREEN  = '#a5d6a7'
    # Кружки
    CK_TOP    = '#1565c0'   # Небо — синий
    CK_BOT    = '#2e7d32'   # Земля — зелёный
    CK_LEFT   = '#880e4f'   # Женское — розовый
    CK_RIGHT  = '#0d47a1'   # Мужское — тёмно-синий
    CK_CENTER = '#b71c1c'   # Центр — красный
    CK_SIDE   = '#4a148c'   # Стороны — фиолетовый
    CK_INNER  = '#1a237e'   # Внутренние — тёмно-синий
    CK_DEST   = '#1b5e20'   # Предназначения — тёмно-зелёный
    CK_AGE    = '#212121'   # Возрастные — почти чёрный

    # ── Геометрия ─────────────────────────────────────────────
    header_h = 140          # высота шапки
    footer_h = 200          # высота блока предназначений
    pad      = 110           # отступ от краёв

    diagram_top  = header_h + pad
    diagram_bot  = H - footer_h - pad
    diagram_cx   = W // 2
    diagram_cy   = (diagram_top + diagram_bot) // 2
    half         = min((diagram_bot - diagram_top) // 2,
                       (W - 2 * pad) // 2) - 20

    # Координаты 4 углов
    P = {
        'top':    (diagram_cx,          diagram_cy - half),
        'left':   (diagram_cx - half,   diagram_cy),
        'right':  (diagram_cx + half,   diagram_cy),
        'bottom': (diagram_cx,          diagram_cy + half),
    }
    # 4 точки на серединах сторон
    def mid(a, b): return ((a[0]+b[0])//2, (a[1]+b[1])//2)
    P['tl'] = mid(P['top'], P['left'])
    P['lb'] = mid(P['left'], P['bottom'])
    P['br'] = mid(P['bottom'], P['right'])
    P['rt'] = mid(P['right'], P['top'])

    cx, cy = diagram_cx, diagram_cy

    # 4 внутренние точки (между центром и углом, на 50%)
    def inner_pt(corner, frac=0.5):
        return (int(cx + (P[corner][0]-cx)*frac),
                int(cy + (P[corner][1]-cy)*frac))

    P['ct'] = inner_pt('top',    0.52)
    P['cl'] = inner_pt('left',   0.52)
    P['cb'] = inner_pt('bottom', 0.52)
    P['cr'] = inner_pt('right',  0.52)

    # Внешнее кольцо: точки возрастных периодов (чуть дальше углов)
    age_r = half + 60
    def age_pos(angle_deg):
        a = math.radians(angle_deg)
        return (int(cx + age_r * math.sin(a)),
                int(cy - age_r * math.cos(a)))
    # 0° = верх, по часовой
    age_positions = {
        0:  age_pos(0),
        10: age_pos(45),
        20: age_pos(90),
        30: age_pos(135),
        40: age_pos(180),
        50: age_pos(225),
        60: age_pos(270),
        70: age_pos(315),
    }

    # ── РИСОВАНИЕ ─────────────────────────────────────────────

    # Заголовок
    draw.text((W//2, 38), 'МАТРИЦА СУДЬБЫ', fill=C_GOLD, font=fn_title, anchor='mm')
    y_sub = 90
    if name:
        draw.text((W//2, y_sub), name, fill=C_WHITE, font=fn_name, anchor='mm')
        y_sub += 36
    draw.text((W//2, y_sub), birth_date, fill=C_GRAY, font=fn_date, anchor='mm')

    # Внешнее кольцо возрастов — линии от ближайшего угла ромба
    age_to_corner = {
        0: 'top', 10: 'tl', 20: 'left', 30: 'lb',
        40: 'bottom', 50: 'br', 60: 'right', 70: 'rt'
    }
    for ang, pos in age_positions.items():
        nearest = age_to_corner[ang]
        draw.line([P[nearest], pos], fill='#2a1a3a', width=1)

    # Основной ромб (заливка)
    rhombus_pts = [P['top'], P['right'], P['bottom'], P['left']]
    draw.polygon(rhombus_pts, fill=C_RHOMBUS, outline=C_LINE, width=3)

    # Внутренний ромб (50% масштаб)
    inner_pts = [(int(cx+(p[0]-cx)*0.5), int(cy+(p[1]-cy)*0.5)) for p in rhombus_pts]
    draw.polygon(inner_pts, fill=C_INNER, outline='#5a2a8a', width=2)

    # Диагонали (крест)
    draw.line([P['top'], P['bottom']], fill=C_DIAG, width=3)
    draw.line([P['left'], P['right']], fill=C_DIAG, width=3)

    # Линии от центра до боковых точек
    for k in ['tl','lb','br','rt']:
        draw.line([(cx,cy), P[k]], fill='#3a1a5a', width=2)

    # Линии центр ↔ внутренние точки
    for k in ['ct','cl','cb','cr']:
        draw.line([(cx,cy), P[k]], fill='#2a1050', width=1)

    # ── Вспомогательные функции рисования ──────────────────────
    def circle(pos, r, fill, outline='#ffffff', width=2):
        x, y = pos
        draw.ellipse([x-r, y-r, x+r, y+r], fill=fill, outline=outline, width=width)

    def num_circle(pos, number, fill, r=36, font=fn_num_md):
        circle(pos, r, fill)
        draw.text(pos, str(number), fill=C_WHITE, font=font, anchor='mm')

    def label(pos, text, color=C_GOLD, font=fn_label, dx=0, dy=-50):
        draw.text((pos[0]+dx, pos[1]+dy), text, fill=color, font=font, anchor='mm')

    # ── Возрастные кружки ──────────────────────────────────────
    age_data = d['age_points']
    for ang, pos in age_positions.items():
        circle(pos, 26, CK_AGE, outline='#444', width=1)
        draw.text(pos, str(age_data[ang]), fill='#aaa', font=fn_num_sm, anchor='mm')
        # Подпись возраста
        label_offset = {
            0:  (0,   -36), 10: (36,  -26), 20: (42,   0),
            30: (36,   26), 40: (0,    36), 50: (-36,  26),
            60: (-42,   0), 70: (-36, -26),
        }
        dx, dy = label_offset[ang]
        draw.text((pos[0]+dx, pos[1]+dy), f"{ang}л", fill='#666', font=fn_tiny, anchor='mm')

    # ── Боковые точки (4 на сторонах ромба) ──────────────────
    num_circle(P['tl'], d['tl'], CK_SIDE, r=30)
    num_circle(P['lb'], d['lb'], CK_SIDE, r=30)
    num_circle(P['br'], d['br'], CK_SIDE, r=30)
    num_circle(P['rt'], d['rt'], CK_SIDE, r=30)

    # ── Внутренние точки (4 между центром и углами) ───────────
    num_circle(P['ct'], d['ct'], CK_INNER, r=27, font=fn_num_sm)
    num_circle(P['cl'], d['cl'], CK_INNER, r=27, font=fn_num_sm)
    num_circle(P['cb'], d['cb'], CK_INNER, r=27, font=fn_num_sm)
    num_circle(P['cr'], d['cr'], CK_INNER, r=27, font=fn_num_sm)

    # ── Угловые точки ──────────────────────────────────────────
    # Небо (верх)
    num_circle(P['top'],    d['top'],    CK_TOP,   r=42, font=fn_num_lg)
    draw.text((P['top'][0], P['top'][1] - 62), 'НЕБО', fill=C_LBLUE, font=fn_label, anchor='mm')
    draw.text((P['top'][0], P['top'][1] - 44), '(день)', fill='#888', font=fn_tiny, anchor='mm')

    # Земля (низ)
    num_circle(P['bottom'], d['bottom'], CK_BOT,   r=42, font=fn_num_lg)
    draw.text((P['bottom'][0], P['bottom'][1] + 60), 'ЗЕМЛЯ', fill=C_LGREEN, font=fn_label, anchor='mm')
    draw.text((P['bottom'][0], P['bottom'][1] + 78), '(д+м+г)', fill='#888', font=fn_tiny, anchor='mm')

    # Женское (лево) — метка левее
    num_circle(P['left'],   d['left'],   CK_LEFT,  r=42, font=fn_num_lg)
    draw.text((P['left'][0] - 130, P['left'][1] - 16), 'ЖЕНСКОЕ',
              fill=C_LPINK, font=fn_label, anchor='mm')
    draw.text((P['left'][0] - 130, P['left'][1] + 14), f"(месяц)",
              fill='#888', font=fn_tiny, anchor='mm')

    # Мужское (право) — метка правее
    num_circle(P['right'],  d['right'],  CK_RIGHT, r=42, font=fn_num_lg)
    draw.text((P['right'][0] + 130, P['right'][1] - 16), 'МУЖСКОЕ',
              fill=C_LBLUE, font=fn_label, anchor='mm')
    draw.text((P['right'][0] + 130, P['right'][1] + 14), f"(год)",
              fill='#888', font=fn_tiny, anchor='mm')

    # ── Центр ──────────────────────────────────────────────────
    # Большой декоративный круг под центром
    circle((cx,cy), 58, '#1a0030', outline=C_GOLD, width=3)
    num_circle((cx,cy), d['center'], CK_CENTER, r=48, font=fn_num_lg)
    label((cx,cy), 'ПРЕДНАЗНАЧЕНИЕ', color=C_GOLD, font=fn_tiny, dy=-64)

    # ── Блок предназначений (снизу) ────────────────────────────
    dest_y0 = H - footer_h + 10
    draw.line([(pad, dest_y0 - 10), (W-pad, dest_y0 - 10)], fill=C_LINE, width=1)

    # Заголовок блока
    draw.text((W//2, dest_y0 + 14), 'ЖИЗНЕННОЕ ПРЕДНАЗНАЧЕНИЕ',
              fill=C_GOLD, font=fn_label, anchor='mm')

    # Три блока
    bw = (W - 2*pad - 60) // 3
    bh = 120
    by = dest_y0 + 42
    specs = [
        (d['personal'],  '👤 ЛИЧНОЕ',     'до 40 лет',  '#1b5e20', '#a5d6a7',
         f"Земля {d['bottom']} + Небо {d['top']} = {d['personal']}"),
        (d['social'],    '👥 СОЦИАЛЬНОЕ', 'до 60 лет',  '#0d47a1', '#90caf9',
         f"Жен {d['left']} + Муж {d['right']} = {d['social']}"),
        (d['spiritual'], '🌟 ДУХОВНОЕ',   'после 60',   '#4a148c', '#ce93d8',
         f"Личное {d['personal']} + Соц {d['social']} = {d['spiritual']}"),
    ]
    for i, (num, title, period, bg, fg, formula) in enumerate(specs):
        bx = pad + i * (bw + 30)
        draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=14,
                                fill=bg, outline=fg, width=2)
        draw.text((bx + bw//2, by + 28), str(num),
                  fill=C_GOLD, font=fn_num_lg, anchor='mm')
        draw.text((bx + bw//2, by + 66), title,
                  fill=fg, font=fn_label, anchor='mm')
        draw.text((bx + bw//2, by + 90), period,
                  fill='#aaa', font=fn_tiny, anchor='mm')
        draw.text((bx + bw//2, by + 112), formula,
                  fill='#888', font=fn_tiny, anchor='mm')

    # ── Нижняя строка ─────────────────────────────────────────
    footer_text = (f"Небо {d['top']}  ·  Земля {d['bottom']}  ·  "
                   f"Женское {d['left']}  ·  Мужское {d['right']}  ·  Центр {d['center']}")
    draw.text((W//2, H - 18), footer_text, fill='#555', font=fn_tiny, anchor='mm')

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)
    return buf.getvalue()

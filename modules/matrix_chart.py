"""
Матрица Судьбы v3 — полная диаграмма
"""
import io, math
from PIL import Image, ImageDraw, ImageFont

ARCANA = {
    1:'Маг', 2:'Жрица', 3:'Императрица', 4:'Император', 5:'Иерофант',
    6:'Влюблённые', 7:'Колесница', 8:'Справедливость', 9:'Отшельник',
    10:'Колесо', 11:'Сила', 12:'Повешенный', 13:'Смерть', 14:'Умеренность',
    15:'Дьявол', 16:'Башня', 17:'Звезда', 18:'Луна', 19:'Солнце',
    20:'Суд', 21:'Мир', 22:'Шут',
}

def red(n):
    while n > 22:
        n = sum(int(d) for d in str(n))
    return max(n, 1)

def calculate_matrix(birth_date: str) -> dict:
    try:
        p = birth_date.strip().split('.')
        day, month, year = int(p[0]), int(p[1]), int(p[2])
    except:
        return {'error': 'Неверный формат. Используйте ДД.ММ.ГГГГ'}
    yr = sum(int(c) for c in str(year))
    top    = red(day)
    left   = red(month)
    right  = red(yr)
    bottom = red(day + month + yr)
    tl = red(top + left);   lb = red(left + bottom)
    br = red(bottom + right); rt = red(right + top)
    center = red(top + left + right + bottom)
    ct = red(center + top);  cl = red(center + left)
    cb = red(center + bottom); cr = red(center + right)
    personal  = red(bottom + top)
    social    = red(left + right)
    spiritual = red(personal + social)
    # Линия женского рода: left -> tl -> top -> rt -> right
    # Линия мужского рода: left -> lb -> bottom -> br -> right
    return {
        'date': birth_date, 'day': day, 'month': month, 'year': year,
        'top': top, 'left': left, 'right': right, 'bottom': bottom,
        'tl': tl, 'lb': lb, 'br': br, 'rt': rt,
        'center': center,
        'ct': ct, 'cl': cl, 'cb': cb, 'cr': cr,
        'personal': personal, 'social': social, 'spiritual': spiritual,
    }

def _fnt(size):
    for f in ['C:/Windows/Fonts/arial.ttf','C:/Windows/Fonts/segoeui.ttf']:
        try: return ImageFont.truetype(f, size)
        except: pass
    return ImageFont.load_default()

def generate_matrix_image(birth_date: str, name: str = '') -> bytes:
    d = calculate_matrix(birth_date)
    if 'error' in d:
        raise ValueError(d['error'])

    W, H = 1500, 1680
    img = Image.new('RGB', (W, H), '#080616')
    draw = ImageDraw.Draw(img)

    # --- Шрифты ---
    F = {
        'title':  _fnt(58), 'name': _fnt(38), 'date': _fnt(28),
        'big':    _fnt(52), 'med':  _fnt(36), 'sm':   _fnt(26),
        'arcana': _fnt(19), 'label':_fnt(22), 'tiny': _fnt(17),
        'age':    _fnt(20), 'age_n':_fnt(22),
    }

    # --- Цвета ---
    CK = {
        'top':    '#1565c0',  # Небо — синий
        'bottom': '#1b5e20',  # Земля — зелёный
        'left':   '#880e4f',  # Женское — малиновый
        'right':  '#1a237e',  # Мужское — тёмно-синий
        'center': '#b71c1c',  # Предназначение — красный
        'side':   '#4a148c',  # Боковые — фиолетовый
        'inner':  '#0d47a1',  # Внутренние — синий
        'age':    '#1a1030',  # Возрастные — тёмный
        'female_line': '#e91e8c',  # Линия женского рода
        'male_line':   '#2196f3',  # Линия мужского рода
        'diag':   '#c62828',
        'grid':   '#6a1b9a',
        'gold':   '#f1c40f',
        'white':  '#ffffff',
        'gray':   '#777777',
        'lblue':  '#90caf9',
        'lpink':  '#f48fb1',
        'lgreen': '#a5d6a7',
        'lpur':   '#ce93d8',
    }

    # --- Геометрия ---
    HDR = 150    # шапка
    FTR = 260    # блок предназначений
    PAD = 160    # боковые отступы

    cx = W // 2
    dia_top = HDR + PAD
    dia_bot = H - FTR - PAD
    cy = (dia_top + dia_bot) // 2
    half = min((dia_bot - dia_top)//2, (W - 2*PAD)//2) - 30

    def pt(key):
        coords = {
            'top':    (cx,        cy - half),
            'bottom': (cx,        cy + half),
            'left':   (cx - half, cy),
            'right':  (cx + half, cy),
        }
        if key in coords: return coords[key]
        base = {
            'tl': (pt('top'), pt('left')),   'lb': (pt('left'), pt('bottom')),
            'br': (pt('bottom'), pt('right')),'rt': (pt('right'), pt('top')),
            'ct': ((cx,cy), pt('top')),      'cl': ((cx,cy), pt('left')),
            'cb': ((cx,cy), pt('bottom')),   'cr': ((cx,cy), pt('right')),
        }
        a, b = base[key]
        return ((a[0]+b[0])//2, (a[1]+b[1])//2)

    P = {k: pt(k) for k in ['top','bottom','left','right','tl','lb','br','rt','ct','cl','cb','cr']}

    # Возрастные точки — по диагоналям за пределами ромба
    age_r = half + 80
    def age_pt(deg):
        a = math.radians(deg)
        return (int(cx + age_r*math.sin(a)), int(cy - age_r*math.cos(a)))

    AGE_POS = {0:age_pt(0), 10:age_pt(45), 20:age_pt(90), 30:age_pt(135),
               40:age_pt(180), 50:age_pt(225), 60:age_pt(270), 70:age_pt(315)}
    AGE_CORNER = {0:'top',10:'tl',20:'left',30:'lb',40:'bottom',50:'br',60:'right',70:'rt'}
    AGE_DATA = {0:d['top'],10:d['tl'],20:d['left'],30:d['lb'],
                40:d['bottom'],50:d['br'],60:d['right'],70:d['rt']}

    # ======================== РИСОВАНИЕ ========================

    # --- Шапка ---
    draw.text((cx, 50), 'МАТРИЦА СУДЬБЫ', fill=CK['gold'], font=F['title'], anchor='mm')
    y = 105
    if name:
        draw.text((cx, y), name, fill=CK['white'], font=F['name'], anchor='mm')
        y += 38
    draw.text((cx, y), birth_date, fill=CK['gray'], font=F['date'], anchor='mm')

    # --- Фоновый ромб ---
    rhombus = [P['top'], P['right'], P['bottom'], P['left']]
    draw.polygon(rhombus, fill='#130828', outline=CK['grid'], width=3)

    # Внутренний ромб (50%)
    inner_r = [(cx+(x-cx)//2, cy+(y-cy)//2) for x,y in rhombus]
    draw.polygon(inner_r, fill='#1a0d35', outline='#5a2a8a', width=2)

    # --- ЛИНИИ РОДОВ (до основных линий, чтобы были под кружками) ---
    # Женский род: top -> tl -> left -> cl -> center (розовый)
    female_path = [P['top'], P['tl'], P['left'], P['cl'], (cx,cy)]
    for i in range(len(female_path)-1):
        draw.line([female_path[i], female_path[i+1]], fill=CK['female_line'], width=4)

    # Мужской род: top -> rt -> right -> cr -> center (синий)
    male_path = [P['top'], P['rt'], P['right'], P['cr'], (cx,cy)]
    for i in range(len(male_path)-1):
        draw.line([male_path[i], male_path[i+1]], fill=CK['male_line'], width=4)

    # Легенда родов (вверху)
    lx = PAD + 10
    draw.line([(lx, HDR-30),(lx+40, HDR-30)], fill=CK['female_line'], width=4)
    draw.text((lx+48, HDR-30), 'Женский род', fill=CK['female_line'], font=F['tiny'], anchor='lm')
    draw.line([(lx+170, HDR-30),(lx+210, HDR-30)], fill=CK['male_line'], width=4)
    draw.text((lx+218, HDR-30), 'Мужской род', fill=CK['male_line'], font=F['tiny'], anchor='lm')

    # --- Диагонали ---
    draw.line([P['top'], P['bottom']], fill=CK['diag'], width=3)
    draw.line([P['left'], P['right']], fill=CK['diag'], width=3)

    # Линии от центра к боковым точкам
    for k in ['tl','lb','br','rt']:
        draw.line([(cx,cy), P[k]], fill='#3a1a5a', width=2)

    # Линии центр ↔ внутренние
    for k in ['ct','cl','cb','cr']:
        draw.line([(cx,cy), P[k]], fill='#251050', width=1)

    # --- Возрастные линии ---
    for age, pos in AGE_POS.items():
        draw.line([P[AGE_CORNER[age]], pos], fill='#1f1040', width=1)

    # ======================== КРУЖКИ ========================

    def circle(pos, r, fill, outline='#ffffff', w=2):
        x,y = pos
        draw.ellipse([x-r,y-r,x+r,y+r], fill=fill, outline=outline, width=w)

    def num_node(pos, num, fill, r_big=44, r_sm=30, font_big=F['med'], show_arcana=True):
        """Кружок с числом + название аркана под ним"""
        circle(pos, r_big, fill, outline='#ffffff', w=2)
        draw.text(pos, str(num), fill=CK['white'], font=font_big, anchor='mm')
        if show_arcana:
            name_arc = ARCANA.get(num, '')
            draw.text((pos[0], pos[1]+r_big+13), name_arc,
                      fill='#cccccc', font=F['arcana'], anchor='mm')

    def age_node(pos, num, age):
        """Возрастной кружок"""
        circle(pos, 28, CK['age'], outline='#3a2a5a', w=1)
        draw.text(pos, str(num), fill='#aaaaaa', font=F['age_n'], anchor='mm')
        # Подпись возраста
        off = {0:(0,-42), 10:(38,-28), 20:(44,0), 30:(38,28),
               40:(0,42), 50:(-38,28), 60:(-44,0), 70:(-38,-28)}
        dx,dy = off[age]
        draw.text((pos[0]+dx, pos[1]+dy), f'{age}л', fill='#555', font=F['tiny'], anchor='mm')

    # --- Возрастные узлы ---
    for age, pos in AGE_POS.items():
        age_node(pos, AGE_DATA[age], age)

    # --- Боковые точки (середины сторон) ---
    for key in ['tl','lb','br','rt']:
        num_node(P[key], d[key], CK['side'], r_big=32, font_big=F['sm'])

    # --- Внутренние точки ---
    for key in ['ct','cl','cb','cr']:
        num_node(P[key], d[key], CK['inner'], r_big=26, font_big=F['sm'], show_arcana=False)

    # --- Угловые точки ---
    # Небо (верх)
    num_node(P['top'], d['top'], CK['top'], r_big=48, font_big=F['big'])
    draw.text((P['top'][0], P['top'][1]-62), 'НЕБО', fill=CK['lblue'], font=F['label'], anchor='mm')
    draw.text((P['top'][0], P['top'][1]-44), 'день', fill=CK['gray'], font=F['tiny'], anchor='mm')

    # Земля (низ)
    num_node(P['bottom'], d['bottom'], CK['bottom'], r_big=48, font_big=F['big'])
    draw.text((P['bottom'][0], P['bottom'][1]+66), 'ЗЕМЛЯ', fill=CK['lgreen'], font=F['label'], anchor='mm')
    draw.text((P['bottom'][0], P['bottom'][1]+84), 'д+м+г', fill=CK['gray'], font=F['tiny'], anchor='mm')

    # Женское (лево)
    num_node(P['left'], d['left'], CK['left'], r_big=48, font_big=F['big'])
    lx = P['left'][0] - 160
    draw.text((lx, P['left'][1]-16), 'ЖЕНСКОЕ', fill=CK['lpink'], font=F['label'], anchor='mm')
    draw.text((lx, P['left'][1]+6),  'месяц',   fill=CK['gray'],  font=F['tiny'],  anchor='mm')

    # Мужское (право)
    num_node(P['right'], d['right'], CK['right'], r_big=48, font_big=F['big'])
    rx = P['right'][0] + 160
    draw.text((rx, P['right'][1]-16), 'МУЖСКОЕ', fill=CK['lblue'], font=F['label'], anchor='mm')
    draw.text((rx, P['right'][1]+6),  'год',      fill=CK['gray'],  font=F['tiny'],  anchor='mm')

    # --- Центр ---
    circle((cx,cy), 62, '#200040', outline=CK['gold'], w=3)
    circle((cx,cy), 54, CK['center'], outline='#ff6666', w=2)
    draw.text((cx,cy), str(d['center']), fill=CK['white'], font=F['big'], anchor='mm')
    draw.text((cx, cy-70), 'ПРЕДНАЗНАЧЕНИЕ', fill=CK['gold'], font=F['tiny'], anchor='mm')
    draw.text((cx, cy+68), ARCANA.get(d['center'],''), fill=CK['gold'], font=F['arcana'], anchor='mm')

    # =================== ВОЗРАСТНАЯ ШКАЛА ===================
    # Горизонтальная шкала под диаграммой
    scale_y = H - FTR - 30
    scale_x0 = PAD + 60
    scale_x1 = W - PAD - 60
    scale_w = scale_x1 - scale_x0
    ages = [0, 10, 20, 30, 40, 50, 60, 70]
    seg_w = scale_w // (len(ages)-1)

    draw.line([(scale_x0, scale_y),(scale_x1, scale_y)], fill='#3a1a5a', width=2)
    for i, age in enumerate(ages):
        sx = scale_x0 + i*seg_w
        num = AGE_DATA[age]
        draw.ellipse([sx-16,scale_y-16,sx+16,scale_y+16], fill='#1a0d35', outline='#6a3a9a', width=1)
        draw.text((sx, scale_y), str(num), fill='#aaa', font=F['tiny'], anchor='mm')
        draw.text((sx, scale_y+26), f'{age}л', fill='#555', font=F['tiny'], anchor='mm')
        draw.text((sx, scale_y-26), ARCANA.get(num,'')[:7], fill='#555', font=F['tiny'], anchor='mm')

    # =================== БЛОК ПРЕДНАЗНАЧЕНИЙ ===================
    dest_y = H - FTR + 20
    draw.line([(PAD, dest_y-10),(W-PAD, dest_y-10)], fill='#4a2a7a', width=1)
    draw.text((cx, dest_y+12), 'ЖИЗНЕННОЕ ПРЕДНАЗНАЧЕНИЕ', fill=CK['gold'], font=F['label'], anchor='mm')

    bw = (W - 2*PAD - 80) // 3
    bh = 140
    by = dest_y + 36
    specs = [
        (d['personal'],  'ЛИЧНОЕ',     'до 40 лет', '#1b5e20','#a5d6a7',
         f"Земля {d['bottom']} + Небо {d['top']} = {d['personal']}"),
        (d['social'],    'СОЦИАЛЬНОЕ', 'до 60 лет', '#0d47a1','#90caf9',
         f"Женское {d['left']} + Мужское {d['right']} = {d['social']}"),
        (d['spiritual'], 'ДУХОВНОЕ',   'после 60',  '#4a148c','#ce93d8',
         f"Личное {d['personal']} + Соц {d['social']} = {d['spiritual']}"),
    ]
    for i,(num,title,period,bg,fg,formula) in enumerate(specs):
        bx = PAD + i*(bw+40)
        draw.rounded_rectangle([bx,by,bx+bw,by+bh], radius=14, fill=bg, outline=fg, width=2)
        draw.text((bx+bw//2, by+30), str(num),   fill=CK['gold'],  font=F['big'],   anchor='mm')
        draw.text((bx+bw//2, by+58), ARCANA.get(num,''), fill=fg, font=F['sm'],    anchor='mm')
        draw.text((bx+bw//2, by+82), title,       fill=fg,          font=F['label'], anchor='mm')
        draw.text((bx+bw//2, by+104),period,      fill='#aaa',      font=F['tiny'],  anchor='mm')
        draw.text((bx+bw//2, by+124),formula,     fill='#777',      font=F['tiny'],  anchor='mm')

    # Нижняя строка
    draw.text((cx, H-18),
        f"Небо {d['top']} · Земля {d['bottom']} · Женское {d['left']} · Мужское {d['right']} · Центр {d['center']}",
        fill='#444', font=F['tiny'], anchor='mm')

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)
    return buf.getvalue()

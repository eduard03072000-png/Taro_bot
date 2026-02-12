"""
Создание красивой профессиональной аватарки для Telegram бота
"""
from PIL import Image, ImageDraw, ImageFont
import math

def create_professional_avatar():
    # Создаём изображение 512x512
    size = 512
    img = Image.new('RGB', (size, size), color='#0a0a1f')  # Почти чёрный синий
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = size // 2, size // 2
    
    # Создаём градиент от центра
    for i in range(256, 0, -1):
        alpha = i
        radius = int(256 * (i / 256))
        color = (10 + i//4, 10 + i//4, 31 + i//2)
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                     fill=color)
    
    # Главный круг - идеально ровный
    main_radius = 200
    # Внешний круг с градиентом золота
    for i in range(8, 0, -1):
        r = main_radius + i * 2
        opacity = int(255 * (i / 8))
        color = (255 - i * 10, 215 - i * 10, i * 10)
        draw.ellipse([center_x - r, center_y - r,
                     center_x + r, center_y + r],
                     outline=color, width=1)
    
    # Основной золотой круг
    draw.ellipse([center_x - main_radius, center_y - main_radius,
                 center_x + main_radius, center_y + main_radius],
                 outline='#FFD700', width=4)
    
    # Внутренний фиолетовый круг
    inner_radius = 185
    draw.ellipse([center_x - inner_radius, center_y - inner_radius,
                 center_x + inner_radius, center_y + inner_radius],
                 fill='#1a0f3d')
    
    # Рисуем идеальную карту Таро в центре
    card_width = 100
    card_height = 140
    card_x = center_x - card_width // 2
    card_y = center_y - card_height // 2
    
    # Тень карты для объёма
    shadow_offset = 5
    draw.rounded_rectangle(
        [card_x + shadow_offset, card_y + shadow_offset, 
         card_x + card_width + shadow_offset, card_y + card_height + shadow_offset],
        radius=8, fill='#000000', outline=None
    )
    
    # Сама карта - белая с золотой каймой
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_width, card_y + card_height],
        radius=8, fill='#FFFFFF', outline='#FFD700', width=3
    )
    
    # Декоративная рамка внутри карты
    margin = 10
    draw.rounded_rectangle(
        [card_x + margin, card_y + margin, 
         card_x + card_width - margin, card_y + card_height - margin],
        radius=5, outline='#9370DB', width=2
    )
    
    # Загружаем шрифт
    try:
        font_symbols = ImageFont.truetype("seguisym.ttf", 50)
        font_small = ImageFont.truetype("arial.ttf", 20)
    except:
        try:
            font_symbols = ImageFont.truetype("C:\\Windows\\Fonts\\seguisym.ttf", 50)
            font_small = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 20)
        except:
            font_symbols = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Символ звезды в центре карты
    star_symbol = "★"
    # Получаем размер текста для центрирования
    bbox = draw.textbbox((0, 0), star_symbol, font=font_symbols)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = card_x + (card_width - text_width) // 2
    text_y = card_y + (card_height - text_height) // 2 - 5
    
    # Тень для звезды
    draw.text((text_x + 2, text_y + 2), star_symbol, fill='#cccccc', font=font_symbols)
    # Сама звезда
    draw.text((text_x, text_y), star_symbol, fill='#9370DB', font=font_symbols)
    
    # Рисуем 12 точек по кругу (как часы) - символизируют 12 месяцев/знаков
    dot_radius = 165
    dot_size = 6
    for i in range(12):
        angle = 2 * math.pi * i / 12 - math.pi / 2
        x = center_x + dot_radius * math.cos(angle)
        y = center_y + dot_radius * math.sin(angle)
        
        # Золотые точки
        draw.ellipse([x - dot_size, y - dot_size, 
                     x + dot_size, y + dot_size],
                     fill='#FFD700')
        
        # Белый центр точки для объёма
        draw.ellipse([x - dot_size//2, y - dot_size//2, 
                     x + dot_size//2, y + dot_size//2],
                     fill='#FFF8DC')
    
    # Добавляем декоративные линии от точек к центру (очень тонкие)
    for i in range(12):
        angle = 2 * math.pi * i / 12 - math.pi / 2
        x1 = center_x + dot_radius * math.cos(angle)
        y1 = center_y + dot_radius * math.sin(angle)
        x2 = center_x + (inner_radius - 5) * math.cos(angle)
        y2 = center_y + (inner_radius - 5) * math.sin(angle)
        
        # Очень тонкие линии
        draw.line([(x1, y1), (x2, y2)], fill='#FFD700', width=1)
    
    # Внешние декоративные дуги
    arc_radius = 220
    arc_width = 3
    # 4 дуги по углам
    for i in range(4):
        start_angle = 90 * i + 20
        end_angle = 90 * i + 70
        draw.arc([center_x - arc_radius, center_y - arc_radius,
                 center_x + arc_radius, center_y + arc_radius],
                 start=start_angle, end=end_angle, 
                 fill='#9370DB', width=arc_width)
    
    # Добавляем звёзды на фоне
    import random
    random.seed(42)
    for _ in range(80):
        x = random.randint(0, size)
        y = random.randint(0, size)
        # Только вне главного круга
        if math.sqrt((x - center_x)**2 + (y - center_y)**2) > main_radius + 30:
            brightness = random.randint(150, 255)
            star_size = random.choice([1, 1, 1, 2])
            draw.ellipse([x, y, x + star_size, y + star_size], 
                        fill=(brightness, brightness, 255))
    
    # Сохраняем
    output_path = "C:\\Project\\Taro_bot\\avatar.png"
    img.save(output_path, 'PNG', quality=95)
    print(f"Krasivaya avatarka sozdana: {output_path}")
    print("Razmer: 512x512")
    print("\nChtoby ustanovit':")
    print("1. Otkroyte @BotFather v Telegram")
    print("2. Otpravte /setuserpic")
    print("3. Vyberte vashego bota")
    print("4. Otpravte fail avatar.png")
    
    return output_path

if __name__ == '__main__':
    create_professional_avatar()

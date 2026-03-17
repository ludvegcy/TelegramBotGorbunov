# food_database.py

# База продуктов (КБЖУ на 100г продукта)
FOODS = {
    # --- МЯСО И ПТИЦА ---
    "курица": {"protein": 23, "fat": 1.9, "carbs": 0.4, "kcal": 113},
    "куриная грудка": {"protein": 23, "fat": 1.9, "carbs": 0.4, "kcal": 113},
    "куриное филе": {"protein": 23, "fat": 1.9, "carbs": 0.4, "kcal": 113},
    "куриное бедро": {"protein": 19, "fat": 15, "carbs": 0, "kcal": 210},
    "куриная голень": {"protein": 18, "fat": 12, "carbs": 0, "kcal": 180},
    "куриные крылья": {"protein": 18, "fat": 16, "carbs": 0, "kcal": 220},
    "индейка": {"protein": 21, "fat": 5, "carbs": 0, "kcal": 135},
    "говядина": {"protein": 26, "fat": 16, "carbs": 0, "kcal": 250},
    "говяжий фарш": {"protein": 20, "fat": 17, "carbs": 0, "kcal": 240},
    "свинина": {"protein": 16, "fat": 27, "carbs": 0, "kcal": 315},
    "свиная вырезка": {"protein": 20, "fat": 7, "carbs": 0, "kcal": 150},
    "баранина": {"protein": 17, "fat": 21, "carbs": 0, "kcal": 260},
    "кролик": {"protein": 21, "fat": 8, "carbs": 0, "kcal": 160},
    "печень куриная": {"protein": 20, "fat": 6, "carbs": 1, "kcal": 140},
    "печень говяжья": {"protein": 17, "fat": 3, "carbs": 5, "kcal": 120},
    "сердце куриное": {"protein": 16, "fat": 10, "carbs": 0.5, "kcal": 155},
    "язык говяжий": {"protein": 16, "fat": 12, "carbs": 0, "kcal": 175},

    # --- КОЛБАСНЫЕ ИЗДЕЛИЯ ---
    "сосиска": {"protein": 11, "fat": 23, "carbs": 1, "kcal": 260},
    "сосиски": {"protein": 11, "fat": 23, "carbs": 1, "kcal": 260},
    "сардельки": {"protein": 10, "fat": 25, "carbs": 2, "kcal": 280},
    "колбаса вареная": {"protein": 12, "fat": 20, "carbs": 2, "kcal": 240},
    "докторская колбаса": {"protein": 12, "fat": 22, "carbs": 2, "kcal": 250},
    "колбаса полукопченая": {"protein": 16, "fat": 38, "carbs": 2, "kcal": 410},
    "колбаса копченая": {"protein": 18, "fat": 42, "carbs": 1, "kcal": 460},
    "сервелат": {"protein": 16, "fat": 40, "carbs": 2, "kcal": 430},
    "салями": {"protein": 18, "fat": 45, "carbs": 1, "kcal": 490},
    "ветчина": {"protein": 14, "fat": 8, "carbs": 2, "kcal": 140},
    "бекон": {"protein": 13, "fat": 45, "carbs": 1, "kcal": 470},
    "грудинка": {"protein": 10, "fat": 50, "carbs": 0, "kcal": 510},
    "шпикачки": {"protein": 10, "fat": 30, "carbs": 2, "kcal": 320},
    "колбаски охотничьи": {"protein": 15, "fat": 35, "carbs": 2, "kcal": 390},

    # --- РЫБА И МОРЕПРОДУКТЫ ---
    "лосось": {"protein": 20, "fat": 13, "carbs": 0, "kcal": 197},
    "семга": {"protein": 20, "fat": 15, "carbs": 0, "kcal": 220},
    "форель": {"protein": 19, "fat": 14, "carbs": 0, "kcal": 210},
    "горбуша": {"protein": 20, "fat": 7, "carbs": 0, "kcal": 150},
    "кета": {"protein": 22, "fat": 6, "carbs": 0, "kcal": 145},
    "тунец": {"protein": 23, "fat": 1, "carbs": 0, "kcal": 110},
    "скумбрия": {"protein": 18, "fat": 13, "carbs": 0, "kcal": 195},
    "сельдь": {"protein": 17, "fat": 15, "carbs": 0, "kcal": 210},
    "треска": {"protein": 16, "fat": 0.6, "carbs": 0, "kcal": 75},
    "минтай": {"protein": 16, "fat": 0.9, "carbs": 0, "kcal": 75},
    "хек": {"protein": 17, "fat": 2, "carbs": 0, "kcal": 90},
    "камбала": {"protein": 16, "fat": 3, "carbs": 0, "kcal": 95},
    "щука": {"protein": 18, "fat": 1, "carbs": 0, "kcal": 85},
    "окунь": {"protein": 19, "fat": 1, "carbs": 0, "kcal": 90},
    "кальмар": {"protein": 18, "fat": 2, "carbs": 0, "kcal": 95},
    "креветки": {"protein": 18, "fat": 1, "carbs": 0, "kcal": 85},
    "мидии": {"protein": 12, "fat": 2, "carbs": 4, "kcal": 85},
    "краб": {"protein": 18, "fat": 1, "carbs": 0, "kcal": 85},
    "крабовые палочки": {"protein": 8, "fat": 2, "carbs": 10, "kcal": 90},

    # --- ЯЙЦА И МОЛОЧНЫЕ ПРОДУКТЫ ---
    "яйцо": {"protein": 12.7, "fat": 11.5, "carbs": 0.7, "kcal": 157},
    "яйца": {"protein": 12.7, "fat": 11.5, "carbs": 0.7, "kcal": 157},
    "яичный белок": {"protein": 11, "fat": 0, "carbs": 0, "kcal": 45},
    "яичный желток": {"protein": 16, "fat": 30, "carbs": 1, "kcal": 350},
    "молоко 3.2%": {"protein": 3, "fat": 3.2, "carbs": 4.7, "kcal": 60},
    "молоко 2.5%": {"protein": 3, "fat": 2.5, "carbs": 4.7, "kcal": 55},
    "молоко 1.5%": {"protein": 3, "fat": 1.5, "carbs": 4.7, "kcal": 45},
    "кефир 3.2%": {"protein": 3, "fat": 3.2, "carbs": 4, "kcal": 60},
    "кефир 2.5%": {"protein": 3, "fat": 2.5, "carbs": 4, "kcal": 55},
    "кефир 1%": {"protein": 3, "fat": 1, "carbs": 4, "kcal": 40},
    "ряженка": {"protein": 3, "fat": 4, "carbs": 4.5, "kcal": 70},
    "йогурт натуральный": {"protein": 4, "fat": 3, "carbs": 6, "kcal": 70},
    "йогурт питьевой": {"protein": 3, "fat": 2, "carbs": 12, "kcal": 80},
    "творог 9%": {"protein": 17, "fat": 9, "carbs": 2, "kcal": 160},
    "творог 5%": {"protein": 17, "fat": 5, "carbs": 3, "kcal": 125},
    "творог 2%": {"protein": 18, "fat": 2, "carbs": 3, "kcal": 105},
    "творог обезжиренный": {"protein": 18, "fat": 0.5, "carbs": 3, "kcal": 90},
    "сметана 20%": {"protein": 2.5, "fat": 20, "carbs": 3, "kcal": 210},
    "сметана 15%": {"protein": 2.5, "fat": 15, "carbs": 3, "kcal": 165},
    "сливки 10%": {"protein": 3, "fat": 10, "carbs": 4, "kcal": 120},
    "сливки 20%": {"protein": 2.5, "fat": 20, "carbs": 4, "kcal": 210},
    "сыр твердый": {"protein": 25, "fat": 30, "carbs": 0, "kcal": 400},
    "сыр пармезан": {"protein": 35, "fat": 25, "carbs": 1, "kcal": 390},
    "сыр моцарелла": {"protein": 20, "fat": 20, "carbs": 1, "kcal": 260},
    "сыр фета": {"protein": 15, "fat": 20, "carbs": 4, "kcal": 260},
    "сыр плавленый": {"protein": 15, "fat": 25, "carbs": 2, "kcal": 290},
    "масло сливочное": {"protein": 0.5, "fat": 82.5, "carbs": 0.8, "kcal": 750},
    "масло топленое": {"protein": 0.3, "fat": 99, "carbs": 0, "kcal": 895},

    # --- КРУПЫ И МАКАРОНЫ ---
    "гречка": {"protein": 13, "fat": 3.4, "carbs": 72, "kcal": 343},
    "гречневая крупа": {"protein": 13, "fat": 3.4, "carbs": 72, "kcal": 343},
    "рис белый": {"protein": 7, "fat": 1, "carbs": 79, "kcal": 360},
    "рис бурый": {"protein": 7.4, "fat": 2.2, "carbs": 73, "kcal": 337},
    "рис дикий": {"protein": 15, "fat": 1, "carbs": 75, "kcal": 370},
    "овсянка": {"protein": 12.3, "fat": 6.1, "carbs": 62, "kcal": 342},
    "овсяные хлопья": {"protein": 12, "fat": 6, "carbs": 60, "kcal": 340},
    "геркулес": {"protein": 12, "fat": 6, "carbs": 60, "kcal": 340},
    "пшено": {"protein": 11, "fat": 3.3, "carbs": 67, "kcal": 345},
    "перловка": {"protein": 9.5, "fat": 1.2, "carbs": 66, "kcal": 320},
    "ячневая крупа": {"protein": 10, "fat": 1.3, "carbs": 66, "kcal": 320},
    "кукурузная крупа": {"protein": 8.5, "fat": 1.2, "carbs": 75, "kcal": 340},
    "манка": {"protein": 10.5, "fat": 1, "carbs": 70, "kcal": 330},
    "булгур": {"protein": 12, "fat": 1.5, "carbs": 78, "kcal": 370},
    "кускус": {"protein": 13, "fat": 0.5, "carbs": 72, "kcal": 350},
    "киноа": {"protein": 14, "fat": 6, "carbs": 64, "kcal": 370},
    "чечевица": {"protein": 24, "fat": 1.5, "carbs": 50, "kcal": 310},
    "нут": {"protein": 20, "fat": 5, "carbs": 50, "kcal": 330},
    "горох": {"protein": 20, "fat": 2, "carbs": 50, "kcal": 300},
    "фасоль": {"protein": 21, "fat": 2, "carbs": 47, "kcal": 290},
    "макароны": {"protein": 12, "fat": 1.5, "carbs": 70, "kcal": 340},
    "спагетти": {"protein": 12, "fat": 1.5, "carbs": 70, "kcal": 340},

    # --- ХЛЕБ И ВЫПЕЧКА ---
    "хлеб белый": {"protein": 8, "fat": 1, "carbs": 50, "kcal": 240},
    "хлеб черный": {"protein": 7, "fat": 1.5, "carbs": 45, "kcal": 220},
    "хлеб ржаной": {"protein": 7, "fat": 1, "carbs": 45, "kcal": 210},
    "хлеб цельнозерновой": {"protein": 9, "fat": 2, "carbs": 45, "kcal": 230},
    "батон": {"protein": 7.5, "fat": 3, "carbs": 50, "kcal": 260},
    "лаваш": {"protein": 8, "fat": 1, "carbs": 55, "kcal": 260},
    "сухари": {"protein": 10, "fat": 3, "carbs": 70, "kcal": 350},
    "хлебцы": {"protein": 10, "fat": 2, "carbs": 60, "kcal": 300},

    # --- ОВОЩИ ---
    "картофель": {"protein": 2, "fat": 0.1, "carbs": 17, "kcal": 77},
    "картошка": {"protein": 2, "fat": 0.1, "carbs": 17, "kcal": 77},
    "морковь": {"protein": 1.3, "fat": 0.1, "carbs": 7, "kcal": 35},
    "лук": {"protein": 1.4, "fat": 0.2, "carbs": 8, "kcal": 40},
    "лук репчатый": {"protein": 1.4, "fat": 0.2, "carbs": 8, "kcal": 40},
    "чеснок": {"protein": 6.5, "fat": 0.5, "carbs": 30, "kcal": 150},
    "капуста белокочанная": {"protein": 1.8, "fat": 0.1, "carbs": 4.7, "kcal": 27},
    "капуста цветная": {"protein": 2.5, "fat": 0.3, "carbs": 4, "kcal": 30},
    "брокколи": {"protein": 2.8, "fat": 0.4, "carbs": 5.2, "kcal": 34},
    "томаты": {"protein": 0.9, "fat": 0.2, "carbs": 3.9, "kcal": 20},
    "помидоры": {"protein": 0.9, "fat": 0.2, "carbs": 3.9, "kcal": 20},
    "огурцы": {"protein": 0.8, "fat": 0.1, "carbs": 2.8, "kcal": 15},
    "перец болгарский": {"protein": 1.3, "fat": 0.1, "carbs": 5, "kcal": 26},
    "кабачки": {"protein": 0.6, "fat": 0.3, "carbs": 4.5, "kcal": 23},
    "баклажаны": {"protein": 1.2, "fat": 0.1, "carbs": 5, "kcal": 25},
    "тыква": {"protein": 1, "fat": 0.1, "carbs": 6, "kcal": 28},
    "свекла": {"protein": 1.5, "fat": 0.1, "carbs": 9, "kcal": 42},
    "редис": {"protein": 1.2, "fat": 0.1, "carbs": 3.5, "kcal": 20},
    "зелень": {"protein": 2.5, "fat": 0.5, "carbs": 3, "kcal": 25},
    "укроп": {"protein": 2.5, "fat": 0.5, "carbs": 4, "kcal": 30},
    "петрушка": {"protein": 3, "fat": 0.5, "carbs": 6, "kcal": 40},
    "салат": {"protein": 1.5, "fat": 0.2, "carbs": 2, "kcal": 16},

    # --- ФРУКТЫ И ЯГОДЫ ---
    "яблоко": {"protein": 0.4, "fat": 0.4, "carbs": 11, "kcal": 52},
    "яблоки": {"protein": 0.4, "fat": 0.4, "carbs": 11, "kcal": 52},
    "банан": {"protein": 1.5, "fat": 0.2, "carbs": 22, "kcal": 96},
    "бананы": {"protein": 1.5, "fat": 0.2, "carbs": 22, "kcal": 96},
    "апельсин": {"protein": 0.9, "fat": 0.2, "carbs": 8, "kcal": 40},
    "мандарин": {"protein": 0.8, "fat": 0.2, "carbs": 7.5, "kcal": 35},
    "лимон": {"protein": 0.9, "fat": 0.1, "carbs": 3, "kcal": 16},
    "грейпфрут": {"protein": 0.7, "fat": 0.2, "carbs": 6.5, "kcal": 32},
    "киви": {"protein": 1, "fat": 0.6, "carbs": 10, "kcal": 50},
    "ананас": {"protein": 0.5, "fat": 0.2, "carbs": 11.5, "kcal": 50},
    "груша": {"protein": 0.4, "fat": 0.3, "carbs": 10, "kcal": 45},
    "персик": {"protein": 0.9, "fat": 0.1, "carbs": 9.5, "kcal": 42},
    "абрикос": {"protein": 0.9, "fat": 0.1, "carbs": 9, "kcal": 41},
    "слива": {"protein": 0.8, "fat": 0.3, "carbs": 9.5, "kcal": 45},
    "виноград": {"protein": 0.6, "fat": 0.2, "carbs": 16, "kcal": 70},
    "арбуз": {"protein": 0.6, "fat": 0.1, "carbs": 6, "kcal": 27},
    "дыня": {"protein": 0.6, "fat": 0.2, "carbs": 7.5, "kcal": 35},
    "клубника": {"protein": 0.8, "fat": 0.4, "carbs": 7, "kcal": 35},
    "малина": {"protein": 0.8, "fat": 0.5, "carbs": 8, "kcal": 40},
    "черника": {"protein": 1, "fat": 0.5, "carbs": 8, "kcal": 40},
    "клюква": {"protein": 0.5, "fat": 0.2, "carbs": 4, "kcal": 20},

    # --- ОРЕХИ И СУХОФРУКТЫ ---
    "грецкий орех": {"protein": 15, "fat": 65, "carbs": 14, "kcal": 650},
    "миндаль": {"protein": 19, "fat": 54, "carbs": 13, "kcal": 610},
    "фундук": {"protein": 15, "fat": 61, "carbs": 10, "kcal": 630},
    "кешью": {"protein": 18, "fat": 44, "carbs": 30, "kcal": 560},
    "арахис": {"protein": 26, "fat": 45, "carbs": 10, "kcal": 560},
    "фисташки": {"protein": 20, "fat": 50, "carbs": 15, "kcal": 580},
    "кедровые орехи": {"protein": 14, "fat": 68, "carbs": 13, "kcal": 670},
    "семечки подсолнуха": {"protein": 21, "fat": 51, "carbs": 11, "kcal": 580},
    "тыквенные семечки": {"protein": 24, "fat": 45, "carbs": 15, "kcal": 540},
    "курага": {"protein": 5, "fat": 0.3, "carbs": 51, "kcal": 230},
    "чернослив": {"protein": 2.5, "fat": 0.5, "carbs": 58, "kcal": 250},
    "изюм": {"protein": 3, "fat": 0.5, "carbs": 70, "kcal": 300},
    "финики": {"protein": 2.5, "fat": 0.5, "carbs": 70, "kcal": 290},
    "инжир": {"protein": 3, "fat": 1, "carbs": 58, "kcal": 250},

    # --- МАСЛА И СОУСЫ ---
    "масло оливковое": {"protein": 0, "fat": 99.9, "carbs": 0, "kcal": 900},
    "масло подсолнечное": {"protein": 0, "fat": 99.9, "carbs": 0, "kcal": 900},
    "масло льняное": {"protein": 0, "fat": 99.9, "carbs": 0, "kcal": 900},
    "майонез": {"protein": 0.5, "fat": 67, "carbs": 2.5, "kcal": 620},
    "кетчуп": {"protein": 1.5, "fat": 0.5, "carbs": 20, "kcal": 90},
    "горчица": {"protein": 5, "fat": 5, "carbs": 8, "kcal": 100},
    "соевый соус": {"protein": 7, "fat": 0, "carbs": 5, "kcal": 50},
    "томатная паста": {"protein": 4, "fat": 0.5, "carbs": 16, "kcal": 85},

    # --- СЛАДОСТИ ---
    "сахар": {"protein": 0, "fat": 0, "carbs": 99.8, "kcal": 400},
    "мед": {"protein": 0.3, "fat": 0, "carbs": 80, "kcal": 320},
    "шоколад молочный": {"protein": 6, "fat": 35, "carbs": 55, "kcal": 550},
    "шоколад горький": {"protein": 7, "fat": 42, "carbs": 45, "kcal": 580},
    "печенье": {"protein": 7, "fat": 20, "carbs": 70, "kcal": 480},
    "вафли": {"protein": 5, "fat": 25, "carbs": 65, "kcal": 520},
    "халва": {"protein": 12, "fat": 30, "carbs": 50, "kcal": 520},
    "зефир": {"protein": 0.5, "fat": 0, "carbs": 80, "kcal": 320},
    "пастила": {"protein": 0.5, "fat": 0, "carbs": 80, "kcal": 320},
    "мармелад": {"protein": 0.5, "fat": 0, "carbs": 80, "kcal": 320},
    "варенье": {"protein": 0.5, "fat": 0, "carbs": 70, "kcal": 280},

    # --- НАПИТКИ ---
    "вода": {"protein": 0, "fat": 0, "carbs": 0, "kcal": 0},
    "чай": {"protein": 0, "fat": 0, "carbs": 0, "kcal": 0},
    "кофе": {"protein": 0, "fat": 0, "carbs": 0, "kcal": 0},
    "сок апельсиновый": {"protein": 0.7, "fat": 0.1, "carbs": 10, "kcal": 45},
    "сок яблочный": {"protein": 0.5, "fat": 0.1, "carbs": 9, "kcal": 40},
    "кола": {"protein": 0, "fat": 0, "carbs": 10, "kcal": 40},
    "газировка": {"protein": 0, "fat": 0, "carbs": 8, "kcal": 32},
    "квас": {"protein": 0.2, "fat": 0, "carbs": 5, "kcal": 25},
    "пиво": {"protein": 0.5, "fat": 0, "carbs": 4, "kcal": 45},
    "вино сухое": {"protein": 0.1, "fat": 0, "carbs": 0.5, "kcal": 75},
}


def search_food(query):
    """Поиск продуктов по названию"""
    results = []
    query = query.lower().strip()

    # Точное совпадение
    if query in FOODS:
        results.append((query, FOODS[query]))

    # Частичное совпадение
    for name, data in FOODS.items():
        if query != name and query in name:
            results.append((name, data))

    # Убираем дубликаты и возвращаем
    seen = set()
    unique_results = []
    for name, data in results:
        if name not in seen:
            seen.add(name)
            unique_results.append((name, data))

    return unique_results


def get_all_products():
    """Получить все продукты"""
    return list(FOODS.keys())


def get_products_by_category(category):
    """Получить продукты по категории"""
    categories = {
        "мясо": ["курица", "говядина", "свинина", "индейка", "баранина"],
        "колбаса": ["сосиска", "колбаса", "ветчина", "сардельки"],
        "рыба": ["лосось", "семга", "треска", "минтай", "скумбрия"],
        "молочные": ["молоко", "кефир", "творог", "сыр", "йогурт"],
        "крупы": ["гречка", "рис", "овсянка", "макароны"],
        "овощи": ["картофель", "морковь", "капуста", "помидоры", "огурцы"],
        "фрукты": ["яблоко", "банан", "апельсин", "груша"],
        "орехи": ["грецкий орех", "миндаль", "арахис"],
        "напитки": ["вода", "чай", "кофе", "сок"]
    }
    return categories.get(category, [])
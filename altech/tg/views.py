from django.shortcuts import render
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from .models import Log, User, Catalog, Product, Savat, Brand, Subcategory

# Create your views here.


contact = ReplyKeyboardMarkup([
    [KeyboardButton("Contact", request_contact=True)]
], resize_keyboard=True)


def inline_btns(type=None, dona=1, user=None):
    if type == "prod":
        btn = [
            [InlineKeyboardButton("-", callback_data="-"),
             InlineKeyboardButton(f"{dona}", callback_data=f"{dona}"),
             InlineKeyboardButton("+", callback_data="+")],

            [InlineKeyboardButton("📥 Корзина", callback_data="savat")]

        ]
        return InlineKeyboardMarkup(btn)
    elif type == "savat":
        btn = [
            [InlineKeyboardButton("⬅Назад", callback_data='back'),
             InlineKeyboardButton("🚖Заказать", callback_data='buyurtma')],
            [InlineKeyboardButton("🗑Очистить корзину", callback_data='clear'),
             InlineKeyboardButton("⏳Доставка", callback_data='dostavka')],
        ]
        savat = Savat.objects.filter(user_id=user.id)
        for i in savat:
            btn.append([InlineKeyboardButton(f"✖{i.product}", callback_data=i.slug)])

    return InlineKeyboardMarkup(btn)


def btns(type=None, ctg=None, ctgs=None, brand=None, subctg_id=None):
    btn = []
    if type == "menu":
        btn = [
            [KeyboardButton("Каталог"),
             KeyboardButton("Бренды")],
            [KeyboardButton("📥 Корзина"),
             KeyboardButton("Настройки")],
        ]
    elif type == "lang":
        btn = [
            [KeyboardButton("UZ🇺🇿"), KeyboardButton("RU🇷🇺")]

        ]
    elif type == "langg":
        btn = [
            [KeyboardButton("🇺🇿UZ🇺🇿"), KeyboardButton("🇷🇺RU🇷🇺")],
            [KeyboardButton("⬅Назад")]
        ]

    elif type == "ctg":
        ctgs = Catalog.objects.all()
        for i in range(1, len(ctgs), 2):
            btn.append([
                KeyboardButton(ctgs[i].content), KeyboardButton(ctgs[i - 1].content),
            ])
        if len(ctgs) % 2:
            btn.append([
                KeyboardButton(ctgs[len(ctgs) - 1].content)
            ])
        btn.append([
            KeyboardButton("⬅Назад")
        ])
    elif type == "subctg":
        subctgs = Subcategory.objects.filter(ctg_id=subctg_id)
        for i in range(1, len(subctgs), 2):
            btn.append([
                KeyboardButton(subctgs[i].content), KeyboardButton(subctgs[i - 1].content),
            ])
        if len(subctgs) % 2:
            btn.append([
                KeyboardButton(subctgs[len(subctgs) - 1].content)
            ])
        btn.append([
            KeyboardButton("⬅Назад")
        ])

    elif type == "brand":
        brands = Brand.objects.all()
        for i in range(1, len(brands), 2):
            btn.append([
                KeyboardButton(brands[i].content), KeyboardButton(brands[i - 1].content),
            ])
        if len(brands) % 2:
            btn.append([
                KeyboardButton(brands[len(ctgs) - 1].content)
            ])
        btn.append([
            KeyboardButton("⬅Назад")
        ])

    elif type == "prod":
        subctg = Subcategory.objects.get(pk=subctg_id)
        prods = Product.objects.filter(subctg=subctg)

        for i in range(1, len(prods), 2):
            btn.append([
                KeyboardButton(prods[i].name), KeyboardButton(prods[i - 1].name),
            ])
        if len(prods) % 2:
            btn.append([
                KeyboardButton(prods[len(prods) - 1].name)
            ])
        elif type == "characteristics":
            category = Catalog.objects.get(content=ctg)
            character = Product.objects.filter(ctg=category)

            for i in range(1, len(character), 2):
                btn.append([
                    KeyboardButton(character[i].tarkibi), KeyboardButton(character[i - 1].tarkibi),
                ])
            if len(character) % 2:
                btn.append([
                    KeyboardButton(character[len(character) - 1].tarkibi)
                ])
        # btn.append([
        #     KeyboardButton("📥 Корзина")
        # ])
        btn.append([
            KeyboardButton("⬅Назад")
        ])
    elif type == "prod_brand":

        brand = Brand.objects.get(content=brand)
        prods = Product.objects.filter(brand=brand)

        for i in range(1, len(prods), 2):
            btn.append([
                KeyboardButton(prods[i].name), KeyboardButton(prods[i - 1].name),
            ])
        if len(prods) % 2:
            btn.append([
                KeyboardButton(prods[len(prods) - 1].name)
            ])

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def start(update, context, ):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()

    msg = update.message.text
    print(msg)

    if not tglog:
        tglog = Log()
        tglog.user_id = user.id
        tglog.save()

    log = tglog.messages
    try:
        tg_user = User.objects.get(user_id=user.id)
    except:
        tg_user = User()
        tg_user.user_id = user.id
        tg_user.username = user.username
        tg_user.save()

    if log['state'] >= 10:
        log.clear()
        log['state'] = 10
        update.message.reply_text("Выберите меню:", reply_markup=btns("menu"))
    else:

        log.clear()
        log['state'] = 0

        update.message.reply_text(f"Здравствуйте\nВыберите язык чтобы зарегестрироваться.",
                                  reply_markup=btns("lang"))

    tglog.messages = log
    tglog.save()


def message_handler(update, context):
    msg = update.message.text
    user = update.message.from_user
    tg_user = User.objects.get(user_id=user.id)
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    if msg == "Настройки":
        log['state'] = 40
        log['til'] = msg
        update.message.reply_text("Выберите язык:", reply_markup=btns("langg"))
    elif msg == "🇺🇿UZ🇺🇿":
        log['state'] = 41
        tg_user.til = msg
        tg_user.save()
        update.message.reply_text("Til ozgartirildi")
        update.message.reply_text("Выберите меню:", reply_markup=btns("menu"))
    elif msg == "🇷🇺RU🇷🇺":
        log['state'] = 42
        tg_user.til = msg
        tg_user.save()
        update.message.reply_text("Язык изменён")
        update.message.reply_text("Выберите меню:", reply_markup=btns("menu"))

    if msg == "⬅Назад":
        if log['state'] == 13:
            log['state'] = 12
            update.message.reply_text("Выберите из каталога:", reply_markup=btns('ctg'))
        elif log['state'] == 12:
            log['state'] = 11
            update.message.reply_text("Выберите меню:", reply_markup=btns("menu"))
        elif log['state'] == 22:
            log['state'] = 11
            update.message.reply_text("Выберите меню:", reply_markup=btns("menu"))
        elif log['state'] == 23:
            log['state'] = 22
            update.message.reply_text("Выберите бренд:", reply_markup=btns('brand'))
        elif log['state'] == 14:
            log['state'] = 13
            ctg = Catalog.objects.get(content=log['ctg'])
            update.message.reply_text("Выберите ниже⬇:", reply_markup=btns("subctg", subctg_id=ctg.id))
    elif msg == "📥 Корзина":
        savat = Savat.objects.filter(user_id=user.id)
        log['state'] = 50
        if savat:
            summa = 0
            mahsulot = ''

            for i in savat:
                mahsulot += f"{i.dona}✖{i.product}\n"
                summa += i.dona * i.price

            update.message.reply_text(f"В корзине: \n{mahsulot}В сумме: {summa}$",
                                      reply_markup=inline_btns("savat", user=user))
        else:
            update.message.reply_text("Корзина пуста")

    else:
        if msg == 'Бренды':
            log['state'] = 21

        if msg == 'Каталог':
            log['state'] = 11
        if log['state'] == 0:
            log['state'] = 1
            log['ism'] = msg
            update.message.reply_text(f"А теперь введите имя:")
        elif log['state'] == 1:
            log['state'] = 2
            log['familiya'] = msg
            update.message.reply_text("Отправьте мне свой номер", reply_markup=contact)
        elif log['state'] == 2:
            update.message.reply_text("Пожалуйста нажмите на кнопку contact.")
        elif log['state'] == 11:
            log['state'] = 12
            update.message.reply_text("Выберите из каталога:", reply_markup=btns('ctg'))
        elif log['state'] == 21:
            log['state'] = 22
            update.message.reply_text("Выберите бренд:", reply_markup=btns('brand'))
        elif log['state'] == 22:
            log['state'] = 23
            log['brand'] = msg
            update.message.reply_text("Выберите компьютер:", reply_markup=btns("prod_brand"))

        elif log['state'] == 12:
            log['state'] = 13
            log['ctg'] = msg
            ctg = Catalog.objects.get(content=msg)
            update.message.reply_text("Выберите ниже⬇:", reply_markup=btns("subctg", subctg_id=ctg.id))

        elif log['state'] == 13:
            log['subctg'] = msg
            log['state'] = 14
            subctg = Subcategory.objects.get(content=msg)
            update.message.reply_text("Выберите ниже:", reply_markup=btns('prod', subctg_id=subctg.id))
        elif log['state'] == 14:
            log['state'] = 14
            log['product'] = msg
            pro = Product.objects.get(name=msg)
            log['price'] = pro.price
            update.message.reply_text("Выберите ниже⬇:", reply_markup=btns("prod", subctg_id=pro.id))
            context.bot.send_photo(
                caption=f"Характеристика: {pro.characteristics} \n Цена: {pro.price}$",
                photo=open(pro.img.path, 'rb'),
                chat_id=user.id,
                reply_markup=inline_btns('prod')
            )

        elif log['state'] == 23:
            pro = Product.objects.get(name=msg)
            log['product'] = pro.name
            log['price'] = pro.price
            context.bot.send_photo(
                caption=f"Характеристика: {pro.characteristics} \n Цена: {pro.price}$",
                photo=open(pro.img.path, 'rb'),
                chat_id=user.id,
                reply_markup=inline_btns('prod')
            )
    print(log)
    tglog.messages = log
    tglog.save()


def contact_handler(update, context):
    contact = update.message.contact
    user = update.message.from_user
    tg_user = User.objects.get(user_id=user.id)
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages

    if log['state'] == 2:
        tg_user.first_name = log['ism']
        tg_user.phone = contact.phone_number
        tg_user.save()
        log.clear()

        log["state"] = 10
        update.message.reply_text("Выберите меню.", reply_markup=btns("menu"))

    tglog.messages = log
    tglog.save()


def inline_handler(update, context):
    query = update.callback_query
    data = query.data
    user = query.from_user
    tg_user = User.objects.get(user_id=user.id)
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    if data == "+":
        log['dona'] = log.get('dona', 1) + 1
        query.edit_message_reply_markup(inline_btns('prod', log['dona']))

    elif data == "-":
        if log.get('dona', 1) == 1:
            pass
        else:
            log['dona'] = log.get('dona', 1) - 1
            query.edit_message_reply_markup(inline_btns('prod', log['dona']))
    elif log['state'] == 50:
        if data == "buyurtma":
            query.message.delete()
            query.message.reply_text("Ваш заказ принят.\nМы ваш заказ доставим в течении 3 часов ")
            Savat.objects.filter(user_id=user.id).delete()
        elif data == "dostavka":
            query.message.reply_text("Время доставки 3 часа")
        elif data == "clear":
            Savat.objects.filter(user_id=user.id).delete()
            query.message.delete()
            query.message.reply_text("Корзина пуста")
        elif data == "back":
            query.message.delete()
            log['state'] = 11
            query.message.reply_text("Выберите меню.", reply_markup=btns("menu"))
        else:
            savat = Savat.objects.filter(slug=data, user_id=user.id).first()
            if savat:
                savat.delete()
            query.message.delete()
            savat = Savat.objects.filter(user_id=user.id)
            log['state'] = 50
            if savat:
                summa = 0
                mahsulot = ''

                for i in savat:
                    mahsulot += f"{i.dona}✖{i.product}\n"
                    summa += i.dona * i.price

                    query.message.reply_text(f"В корзине: \n{mahsulot}В сумме: {summa}$",
                                             reply_markup=inline_btns("savat", user=user))
            else:
                query.message.reply_text("Корзина пуста")

    elif data == "savat":
        savat = Savat.objects.filter(product=log['product']).first()
        if savat:
            savat.price = log['price']
            savat.dona += log.get('dona', 1)
            savat.user_id = user.id
            savat.save()
        else:
            savat = Savat()
            savat.product = log['product']
            savat.price = log['price']
            savat.dona = log.get('dona', 1)
            savat.user_id = user.id
            savat.save()
        query.message.delete()
        update.callback_query.answer("Корзина пуста")
        query.message.reply_text("Выберите меню:", reply_markup=btns("menu"))

    tglog.messages = log
    tglog.save()

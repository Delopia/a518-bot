import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile, WebAppInfo
from aiohttp import web

TOKEN = "9003935603:AAGlZ4bamHdiuvxh1Mo4iuEt7Mzt0v5W9oc"

# Твой ID администратора
ADMIN_ID = 299433630

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Функция главного меню (инлайн-кнопки с картинкой)
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="✈️ Тарифы и сроки", callback_data="tariffs")
    builder.button(text="📦 Разрешено / Запрещено", callback_data="rules")
    builder.button(text="🛡 Страхование груза", callback_data="insurance")
    builder.button(text="⏱ Компенсации при задержке", callback_data="compensation")
    builder.button(text="🤝 Как мы работаем", callback_data="workflow")
    builder.button(text="📞 Контакты и QR-коды", callback_data="contacts")
    # Кнопка открытия сайта внутри Telegram (Web App)
    builder.button(
        text="🌐 Открыть сайт A518", 
        web_app=WebAppInfo(url="https://a518-aviaexpert.vercel.app/")
    )
    builder.adjust(1)
    return builder.as_markup()


# Вспомогательная функция для отправки текста вместо фото (чтобы не падало с Bad Request)
async def show_text_or_edit(callback: types.CallbackQuery, text: str, reply_markup):
    if callback.message.photo:
        try:
            await callback.message.delete()
        except Exception:
            pass
        await callback.message.answer(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        try:
            await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception:
            await callback.message.answer(text, reply_markup=reply_markup, parse_mode="Markdown")


# Команда /start (отправляет картинку с инлайн-меню)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    caption = (
        f"Привет, {message.from_user.first_name}!\n"
        "Добро пожаловать в официальный бот **A518 Эксперт по авиаперевозкам** (Китай — Казахстан).\n\n"
        "Выберите нужный раздел из меню ниже:"
    )
    try:
        photo = FSInputFile("menu_logo.png")
        await message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    except Exception:
        await message.answer(
            caption,
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )


# Обработка нажатий на инлайн-кнопки
@dp.callback_query()
async def process_callbacks(callback: types.CallbackQuery):
    data = callback.data
    builder = InlineKeyboardBuilder()

    if data == "tariffs":
        text = (
            "✈️ **Цены на авиаперевозки (Гуанчжоу, Иу, Пекин — Алматы):**\n\n"
            "• **1 – 500 кг:** 5 000 тенге/кг\n"
            "• **500 – 1000 кг:** 4 500 тенге/кг\n"
            "*(Менее 1 кг оплачивается как 1 кг)*\n\n"
            "⏱ **Срок доставки:** 3 дня / 72 часа\n"
            "*(День отправки и день деления груза не учитываются)*\n\n"
            "⚠️ Все расходы из-за сокрытия или неверного описания груза несет клиент!"
        )
        builder.button(text="◀️ Назад в меню", callback_data="back_to_menu")
        builder.adjust(1)
        await show_text_or_edit(callback, text, builder.as_markup())

    elif data == "rules":
        text = (
            "📦 **Правила по товарам (Авиаперевозки):**\n\n"
            "Выберите категорию, чтобы ознакомиться со списками:"
        )
        builder.button(text="✅ Разрешенные товары", callback_data="allowed_list")
        builder.button(text="❌ Запрещенные товары", callback_data="forbidden_list")
        builder.button(text="◀️ Назад в меню", callback_data="back_to_menu")
        builder.adjust(1)
        await show_text_or_edit(callback, text, builder.as_markup())

    elif data == "allowed_list":
        text = (
            "✅ **Примеры разрешенных товаров (более 50 видов):**\n\n"
            "• Одежда (мужская, женская, детская), обувь, головные уборы, шарфы\n"
            "• Меховые и кожаные изделия, искусственная кожа\n"
            "• Сумки (без магнитных кнопок), фурнитура\n"
            "• Текстиль, ткани, домашний текстиль, пледы\n"
            "• Образцы, механические изделия, автозапчасти\n"
            "• Компьютерные и мобильные аксессуары, электроника без батарей\n"
            "• Электрооборудование, ручной и электроинструмент\n"
            "• Металлоизделия, стройматериалы (мелкие), светильники\n"
            "• Бытовая техника без аккумуляторов, посуда, столовые приборы\n"
            "• Игрушки, сувениры, канцелярия, спорт-инвентарь (без электрики)\n"
            "• Ролики, скейтборды, музыкальные инструменты (без батарей)\n"
            "• Фототехника, очки, солнцезащитные очки, часы\n"
            "• Ювелирные изделия (в основном серебро), косметика без жидкостей\n"
            "• Товары для фитнеса, автоковрики, товары для дома и уборки\n"
            "• Детские товары (подгузники, бутылочки), книги, картины, упаковка\n"
            "• Пластиковые, стальные, стеклянные изделия (мелкие), электросамокаты без аккумуляторов и многое другое."
        )
        builder.button(text="◀️ К выбору правил", callback_data="rules")
        builder.button(text="◀️ Назад в меню", callback_data="back_to_menu")
        builder.adjust(1)
        await show_text_or_edit(callback, text, builder.as_markup())

    elif data == "forbidden_list":
        text = (
            "❌ **Примеры запрещенных товаров (более 50 видов):**\n\n"
            "• Мобильные телефоны, ноутбуки, планшеты\n"
            "• Электроника с аккумуляторами, пауэрбанки, зарядные устройства\n"
            "• Изделия и сумки с магнитами, магнитные игрушки\n"
            "• Все виды батарей (литиевые, сухие), часы с аккумулятором/магнитом\n"
            "• Дроны, рации, электронные сигареты, лазерное оборудование\n"
            "• Диктофоны, видеокамеры, умная носимая электроника\n"
            "• Жидкости, лаки, духи, косметика, масла, мази, пластыри\n"
            "• Алкоголь, лекарства, травяные сборы, чай\n"
            "• Порошки (мука, молоко, химия), маски, средства по уходу, зубная паста, шампуни\n"
            "• Взрывоопасные предметы, аэрозоли, баллоны под давлением\n"
            "• Коррозионные вещества, краски, растворители, пестициды, гербициды\n"
            "• Дезинфицирующие средства, главные платы с питанием, смазочные масла\n"
            "• Автозапчасти с аккумуляторами, подушки безопасности с пиропатроном\n"
            "• Драгоценные металлы и камни, животные, растения, семена\n"
            "• Продукты питания (мясо, морепродукты), шины, крупное оборудование, табак."
        )
        builder.button(text="◀️ К выбору правил", callback_data="rules")
        builder.button(text="◀️ Назад в меню", callback_data="back_to_menu")
        builder.adjust(1)
        await show_text_or_edit(callback, text, builder.as_markup())

    elif data == "insurance":
        text = (
            "🛡 **Условия страхования груза:**\n\n"
            "Страхование является **добровольным**. Вы сами решаете, страховать груз или нет.\n\n"
            "💰 **Тарифы страхования (в процентах от заявленной стоимости груза):**\n"
            "• Груз стоимостью **до $30/кг** — страховка **1%**\n"
            "• Груз стоимостью **от $30 до $50/кг** — страховка **2%**\n"
            "• Груз стоимостью **от $50 до $200/кг** — страховка **3%**\n\n"
            "⚠️ **Если вы отказались от страховки:**\n"
            "В случае утери незастрахованного груза выплачивается фиксированная компенсация в размере **5 000 тенге за 1 кг** веса."
        )
        builder.button(text="◀️ Назад в меню", callback_data="back_to_menu")
        builder.adjust(1)
        await show_text_or_edit(callback, text, builder.as_markup())

    elif data == "compensation":
        text = (
            "⏱ **Компенсация при задержке доставки в Алматы:**\n\n"
            "Если доставка задерживается по сравнению с оговоренным сроком:\n"
            "• **С 7-го дня просрочки:** скидка/компенсация **0,5 доллара США за 1 кг**\n"
            "• **С 10-го дня просрочки:** расчет **3 доллара США за 1 кг**"
        )
        builder.button(text="◀️ Назад в меню", callback_data="back_to_menu")
        builder.adjust(1)
        await show_text_or_edit(callback, text, builder.as_markup())

    elif data == "workflow":
        text = (
            "🤝 **Как мы работаем и наши преимущества:**\n\n"
            "1️⃣ Создаем персональную группу в мессенджере для связи.\n"
            "2️⃣ Сообщаем сразу, как склад в Китае принимает ваш груз.\n"
            "3️⃣ Менеджер связывается для подтверждения описи и деталей.\n"
            "4️⃣ Оповещаем звонком по прибытии груза в Алматы.\n"
            "5️⃣ Полная прозрачность и поддержка 24/7!"
        )
        builder.button(text="◀️ Назад в меню", callback_data="back_to_menu")
        builder.adjust(1)
        await show_text_or_edit(callback, text, builder.as_markup())

    elif data == "contacts":
        text = (
            "📞 **Контакты A518 Карго:**\n\n"
            "• 📱 **Единый номер / WhatsApp:** +7 700 745 45 28\n\n"
            "📍 **Адрес:** ул. Бокейханова, 510Б, оф. 62 (Алматы)\n\n"
            "Нажмите на кнопку ниже, чтобы получить QR-код для связи:"
        )
        builder.button(text="💚 Получить QR WeChat", callback_data="qr_wechat")
        builder.button(text="💬 Получить QR WhatsApp", callback_data="qr_whatsapp")
        builder.button(text="◀️ Назад в меню", callback_data="back_to_menu")
        builder.adjust(1)
        await show_text_or_edit(callback, text, builder.as_markup())

    elif data == "qr_wechat":
        builder.button(text="◀️ Назад к контактам", callback_data="contacts")
        builder.adjust(1)
        try:
            photo = FSInputFile("wechat_qr.png")
            try:
                await callback.message.delete()
            except Exception:
                pass
            await callback.message.answer_photo(photo=photo, caption="💚 Наш WeChat QR-код для связи",
                                                reply_markup=builder.as_markup())
        except Exception:
            await show_text_or_edit(callback, "⚠️ Файл картинки `wechat_qr.png` не найден!", builder.as_markup())

    elif data == "qr_whatsapp":
        builder.button(text="◀️ Назад к контактам", callback_data="contacts")
        builder.adjust(1)
        try:
            photo = FSInputFile("whatsapp_qr.png")
            try:
                await callback.message.delete()
            except Exception:
                pass
            await callback.message.answer_photo(photo=photo, caption="💬 Наш WhatsApp QR-код для связи",
                                                reply_markup=builder.as_markup())
        except Exception:
            await show_text_or_edit(callback, "⚠️ Файл картинки `whatsapp_qr.png` не найден!", builder.as_markup())

    elif data == "back_to_menu":
        menu_text = "Главное меню. Выберите интересующий вас раздел:"
        try:
            await callback.message.delete()
        except Exception:
            pass
        
        try:
            photo = FSInputFile("menu_logo.png")
            await callback.message.answer_photo(
                photo=photo,
                caption=menu_text,
                reply_markup=get_main_menu()
            )
        except Exception:
            await callback.message.answer(
                menu_text,
                reply_markup=get_main_menu()
            )

    await callback.answer()


# Пересылка сообщений от пользователей
@dp.message()
async def forward_to_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        if (message.text and len(message.text.strip()) > 3) or message.photo or message.document:
            try:
                await message.forward(chat_id=ADMIN_ID)
                await message.answer("💬 Ваше сообщение отправлено менеджеру. Скоро с вами свяжемся!")
            except Exception:
                pass
        else:
            await message.answer("⚠️ Пожалуйста, напишите ваш вопрос подробнее, чтобы менеджер смог вам помочь.")


# Установка кнопки "Меню" в интерфейсе Telegram
async def set_bot_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="🚀 Запустить главное меню A518")
    ]
    await bot.set_my_commands(commands)


# Веб-сервер для Render и UptimeRobot
async def handle_ping(request):
    return web.Response(text="A518 Cargo Bot is active!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()


async def main():
    await start_web_server()
    await set_bot_commands(bot)
    print("Бот A518 запущен и работает...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

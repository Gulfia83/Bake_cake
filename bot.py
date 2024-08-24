import os
import telegram
import django
import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from django.db.models import Q


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bake_cake.settings')
django.setup()

from tg_bot.models import Client, Cake, Order, Level, Shape, Topping, Berries, Decor


def start(update: Update, context: CallbackContext) -> None:
    telegram_id = update.effective_user.id
    if Client.objects.filter(telegram_id=telegram_id).first():
        update_main_menu(update.message)
    else:
        show_main_menu(update.message)


def show_main_menu(message) -> None:
    keyboard = [
        [InlineKeyboardButton("Документ 'Соглашение на обработку данных'", callback_data='consent_file')],
        [InlineKeyboardButton('Даю согласие на обработку данных', callback_data='consent')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text('Привет! Я бот bake_cake. Благодаря мне ты сможешь заказать на свой вкус любого рода торт. Такой торт, о котором ты мечтал, любой формы и цвета.\n'
                       'И поэтому, прежде чем производить заказ, необходимо согласие на обработку данных. Чтобы мы смогли исполнить вашу мечту', reply_markup=reply_markup)


def main_menu_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'consent_file':
        with open("static/согласие на обработку ПД.pdf", "rb") as file:
            query.message.reply_document(document=file, filename="согласие на обработку ПД.pdf")
    elif query.data == 'consent':
        selection_cakes(query)
    elif query.data == 'order_status':
        get_order_status(query)


def selection_cakes(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Список готовых тортов", callback_data='list_cakes')],
        [InlineKeyboardButton("Кастомизация торта", callback_data='cake_customization')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Хотите выбрать уже готовый торт или же создадите свой:', reply_markup=reply_markup)


def show_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'list_cakes':
        get_cakes(query)
    elif query.data == 'cake_customization':
        get_customization_cakes(query)
    elif query.data == 'menu_cakes':
        selection_cakes(query)


def get_cakes(query) -> None:
    cakes = Cake.objects.filter(ready_to_order=True)
    keyboards = [[InlineKeyboardButton('Вернуться в главное меню', callback_data='menu_cakes')]]
    for cake in cakes:
        keyboard = [InlineKeyboardButton(f'{cake.id}. {cake.title} - {cake.end_price}',
                                         callback_data=f'cake_{cake.id}')]
        keyboards.append(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboards)
    query.message.reply_text('Заказ будет готов в течении 3-х дней с 09:00 по 18:00. Выберите торт который вы хотите:',
                             reply_markup=reply_markup)


def get_customization_cakes(query) -> None:
    keyboard = [
        [InlineKeyboardButton('Количество уровней', callback_data='cb_level')],
        [InlineKeyboardButton('Форма', callback_data='cb_shape')],
        [InlineKeyboardButton('Топпинг', callback_data='cb_topping')],
        [InlineKeyboardButton('Ягоды', callback_data='cb_berries')],
        [InlineKeyboardButton('Декор', callback_data='cb_decor')],
        [InlineKeyboardButton('Надпись', callback_data='cb_text')],
        [InlineKeyboardButton('Оформить заказ', callback_data='cb_finalize_order')],
        [InlineKeyboardButton('Вернуться в главное меню', callback_data='menu_cakes')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выберите улучшение вашему торту:', reply_markup=reply_markup)


def logic_customization(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    telegram_id = query.from_user.id

    cake = context.user_data.get('selected_cake_id')
    if not cake:
        cake = Cake.objects.create()
        cake.title = f'Кастомный торт {cake.id}'
        context.user_data['selected_cake_id'] = cake

    if query.data == 'cb_level':
        if cake.level:
            query.message.reply_text(f'Вы уже выбрали {cake.level.number} уровней. Вы не можете выбрать это повторно.')
        else:
            levels = Level.objects.all()
            keyboard = [
                [InlineKeyboardButton(f'{level.number} уровней - {level.price} руб.', callback_data=f'level_{level.id}')]
                for level in levels]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text('Выберите уровень:', reply_markup=reply_markup)
    elif query.data.startswith('level_'):
        level_id = int(query.data.split('_')[1])
        level = Level.objects.get(id=level_id)
        cake.level = level
        cake.end_price += level.price
        cake.save()
        query.message.reply_text(
            f'Вы выбрали {level.number} уровень. Стоимость: {level.price} руб.\nТекущая цена: {cake.end_price} руб.')
        get_customization_cakes(query)

    elif query.data == 'cb_shape':
        if cake.shape:
            query.message.reply_text(f'Вы уже выбрали Форму. Вы не можете выбрать это повторно.')
        else:
            shapes = Shape.objects.all()
            keyboard = [[InlineKeyboardButton(f'{shape.name} - {shape.price} руб.', callback_data=f'shape_{shape.id}')]
                        for shape in shapes]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text('Выберите форму торта:', reply_markup=reply_markup)
    elif query.data.startswith('shape_'):
        shape_id = int(query.data.split('_')[1])
        shape = Shape.objects.get(id=shape_id)
        cake.shape = shape
        cake.end_price += shape.price
        cake.save()
        query.message.reply_text(
            f'Вы выбрали {shape.name}. Стоимость: {shape.price} руб.\nТекущая цена: {cake.end_price} руб.')
        get_customization_cakes(query)

    elif query.data == 'cb_topping':
        if cake.topping:
            query.message.reply_text(f'Вы уже выбрали Топпинг. Вы не можете выбрать это повторно.')
        else:
            toppings = Topping.objects.all()
            keyboard = [[InlineKeyboardButton(f'{topping.name} - {topping.price} руб.', callback_data=f'topping_{topping.id}')]
                        for topping in toppings]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text('Выберите топпинг торта:', reply_markup=reply_markup)
    elif query.data.startswith('topping_'):
        topping_id = int(query.data.split('_')[1])
        topping = Topping.objects.get(id=topping_id)
        cake.topping = topping
        cake.end_price += topping.price
        cake.save()
        query.message.reply_text(
            f'Вы выбрали {topping.name}. Стоимость: {topping.price} руб.\nТекущая цена: {cake.end_price} руб.')
        get_customization_cakes(query)

    elif query.data == 'cb_berries':
        if cake.berries:
            query.message.reply_text(f'Вы уже выбрали ягоды. Вы не можете выбрать это повторно.')
        else:
            berries = Berries.objects.all()
            keyboard = [[InlineKeyboardButton(f'{berry.name} - {berry.price} руб.', callback_data=f'shape_{berry.id}')]
                        for berry in berries]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text('Выберите ягоды торта:', reply_markup=reply_markup)
    elif query.data.startswith('berries_'):
        berries_id = int(query.data.split('_')[1])
        berry = Berries.objects.get(id=berries_id)
        cake.berries = berry
        cake.end_price += berry.price
        cake.save()
        query.message.reply_text(
            f'Вы выбрали форму: {berry.name}. Стоимость: {berry.price} руб.\nТекущая цена: {cake.end_price} руб.')
        get_customization_cakes(query)

    elif query.data == 'cb_decor':
        if cake.decor:
            query.message.reply_text(f'Вы уже выбрали Декор. Вы не можете выбрать это повторно.')
        else:
            decors = Decor.objects.all()
            keyboard = [[InlineKeyboardButton(f'{decor.name} - {decor.price} руб.', callback_data=f'shape_{decor.id}')]
                        for decor in decors]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text('Выберите декор торта:', reply_markup=reply_markup)
    elif query.data.startswith('decor_'):
        decors_id = int(query.data.split('_')[1])
        decor = Decor.objects.get(id=decors_id)
        cake.decor = decor
        cake.end_price += decor.price
        cake.save()
        query.message.reply_text(
            f'Вы выбрали форму: {decor.name}. Стоимость: {decor.price} руб.\nТекущая цена: {cake.end_price} руб.')
        get_customization_cakes(query)

    elif query.data == 'cb_finalize_order':
        new_order(update, context)

    elif query.data == 'customization_back':
        get_customization_cakes(query)


def logic_ready_cakes(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    cakes = Cake.objects.all()
    for cake_q in cakes:
        if query.data == f'cake_{cake_q.id}':
            new_order(update, context)
            cake = Cake.objects.get(id=cake_q.id)
            context.user_data['selected_cake_id'] = cake


def new_order(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    telegram_id = update.effective_user.id
    if Client.objects.filter(telegram_id=telegram_id).exists():
        client = Client.objects.get(telegram_id=telegram_id)
        context.user_data['full_name'] = client.name
        context.user_data['phone'] = client.phonenumber
        context.user_data['client'] = client
    else:
        query.message.reply_text('Пожалуйста, введите Ваше ФИО:')
        context.user_data['awaiting_full_name'] = True
        context.user_data['awaiting_address'] = False
        context.user_data['awaiting_phone'] = False
        return
    query.message.reply_text('Введите ваш адрес доставки:')
    context.user_data['awaiting_address'] = True


def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text

    if context.user_data.get('awaiting_full_name'):
        context.user_data['full_name'] = message_text
        update.message.reply_text('Введите ваш номер телефона:')
        context.user_data['awaiting_phone'] = True
        context.user_data['awaiting_full_name'] = False
        return
    if context.user_data.get('awaiting_phone'):
        context.user_data['phone'] = message_text
        update.message.reply_text('Введите ваш адрес доставки:')
        context.user_data['awaiting_address'] = True
        context.user_data['awaiting_phone'] = False
        return
    if context.user_data.get('awaiting_address'):
        context.user_data['address'] = message_text
        update.message.reply_text('Есть ли у вас какие-нибудь комментарии?')
        context.user_data['awaiting_comment'] = True
        context.user_data['awaiting_address'] = False
        return
    if context.user_data.get('awaiting_comment'):
        context.user_data['comment'] = message_text
        update.message.reply_text('Ваши данные собраны. Срок выполнения заказа 3-(три) дня')
        context.user_data['awaiting_comment'] = False
        process_address(update, context)
        return


def process_address(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Да", callback_data='accelerate_yes')],
        [InlineKeyboardButton("Нет", callback_data='accelerate_no')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Желаете ли вы ускорить процесс доставки?', reply_markup=reply_markup)


def handle_acceleration_response(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'accelerate_yes':
        keyboard = [
            [InlineKeyboardButton("Ускорить на 1 день", callback_data='accelerate_1_day')],
            [InlineKeyboardButton("Ускорить на 2 дня", callback_data='accelerate_2_days')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('Выберите вариант ускорения:', reply_markup=reply_markup)

    elif query.data == 'accelerate_no':
        query.message.reply_text('Ваши данные собраны. Обрабатываем заказ...')
        process_cake(update, context)


def handle_acceleration_days(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'accelerate_1_day':
        context.user_data['price_multiplier'] = 1.1
        context.user_data['delivery_time'] = 2
    elif query.data == 'accelerate_2_days':
        context.user_data['price_multiplier'] = 1.2
        context.user_data['delivery_time'] = 1

    keyboard = [
        [InlineKeyboardButton('с 09:00 до 12:00', callback_data='time_9_12')],
        [InlineKeyboardButton('с 13:00 до 16:00', callback_data='time_13_16')],
        [InlineKeyboardButton('с 17:00 до 20:00', callback_data='time_17_20')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выберите удобное для вас время. Данное время будет добавлено в ваши комментарии',
                             reply_markup=reply_markup)
    handle_acceleration_times(update, context)


def handle_acceleration_times(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    time_slot = query.data
    if time_slot == 'time_9_12':
        context.user_data['delivery_time_slot'] = 'с 09:00 до 12:00'
    elif time_slot == 'time_13_16':
        context.user_data['delivery_time_slot'] = 'с 13:00 до 16:00'
    elif time_slot == 'time_17_20':
        context.user_data['delivery_time_slot'] = 'с 17:00 до 20:00'
    else:
        return
    query.message.reply_text('Ваш заказ будет ускорен. Обрабатываем заказ...')
    process_cake(update, context)


def process_cake(update: Update, context: CallbackContext) -> None:
    if not context.user_data.get('delivery_time_slot'):
        time_ = None
    else:
        time_ = context.user_data['delivery_time_slot']
    cake = context.user_data['selected_cake_id']
    full_name = context.user_data['full_name']
    address = context.user_data['address']
    comments = context.user_data['comment']
    phone = context.user_data['phone']
    telegram_id = update.effective_user.id

    delivery_time = context.user_data.get('delivery_time', 3)
    price_multiplier = context.user_data.get('price_multiplier', 1.0)

    if not context.user_data.get('client'):
        client = Client.objects.create(
            telegram_id=telegram_id,
            name=full_name,
            phonenumber=phone)
    else:
        client = context.user_data['client']
    final_price = cake.end_price * price_multiplier

    order = Order.objects.create(
        cake=cake,
        client=client,
        address=address,
        delivery_date=delivery_time,
        price=final_price,
        comments=comments + f'\n    Просьба доставить - {time_}',
    )

    if update.message:
        reply_target = update.message
    else:
        reply_target = update.callback_query.message

    reply_target.reply_text(f'''Ваш заказ - №{order.id} на сумму {order.price} принят.
    Спасибо за вашу заявку. Наш менеджер свяжется с вами.''')
    reply_target.reply_text('Для запуска бота введите команду "/start"')

    chat_id = os.environ['TG_ID']
    order_details = f"""Получен новый заказ
    № - {order.id}
    Клиент: {order.client.name}
    Номер телефона: {order.client.phonenumber}
    Торт: {order.cake.title}
    Цена: {order.price}
    Адрес доставки: {order.address}
    Комментарии: {order.comments}
    Дата создания заказа: {order.created_at}
    Сделать торт за дн.: {order.delivery_date}
    """
    send_order_confirmation(chat_id, order_details, telegram_api)
    context.user_data.clear()


def get_order_status(query) -> None:
    telegram_id = query.from_user.id
    client = Client.objects.get(telegram_id=telegram_id)
    orders = Order.objects.filter(client=client)
    keyboard = [
        [InlineKeyboardButton('Главное меню', callback_data='menu_cakes')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    orders_info = ''
    for order in orders:
        status_display = order.get_status_display()
        orders_info += f'№{order.id}: статус - {status_display}\n'
    query.message.reply_text(f'Ваши заказы:\n{orders_info}', reply_markup=reply_markup)


def update_main_menu(message) -> None:
    keyboard = [
        [InlineKeyboardButton('Произвести заказ', callback_data='consent')],
        [InlineKeyboardButton('Статус заказа', callback_data='order_status')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text('Вами ранее уже был произведен заказ, хотите заказать еще?', reply_markup=reply_markup)


def send_order_confirmation(chat_id: int, order_details: str, bot_token: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': order_details,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Сообщение успешно отправлено.")
    else:
        print(f"Ошибка отправки сообщения: {response.text}")


if __name__ == '__main__':
    load_dotenv()

    telegram_api = os.environ["TG_BOT_CAKE"]
    bot = telegram.Bot(token=telegram_api)
    updater = Updater(token=telegram_api)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(main_menu_handler, pattern='^(consent_file|consent|order_status)$'))
    dispatcher.add_handler(CallbackQueryHandler(show_handler, pattern='^(list_cakes|cake_customization|order_status|menu_cakes)$'))
    dispatcher.add_handler(CallbackQueryHandler(logic_ready_cakes, pattern=r'^cake_\d+$'))
    dispatcher.add_handler(CallbackQueryHandler(logic_customization, pattern='^(cb_|level_|shape_|topping_|berries_|decor_|cb_finalize_order)'))
    dispatcher.add_handler(
        CallbackQueryHandler(handle_acceleration_response, pattern='^(accelerate_yes|accelerate_no)$'))
    dispatcher.add_handler(
        CallbackQueryHandler(handle_acceleration_days, pattern='^(accelerate_1_day|accelerate_2_days)$'))
    dispatcher.add_handler(
        CallbackQueryHandler(handle_acceleration_times, pattern='^(time_9_12|time_13_16|time_17_20)$'))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print('Бот в сети')
    updater.idle()





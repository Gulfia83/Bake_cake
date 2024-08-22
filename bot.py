import os
import telegram
import django
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from django.db.models import Q


load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bake_cake.settings')
django.setup()

from tg_bot.models import Client, Cake, Order


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
        with open("documents/согласие на обработку ПД.pdf", "rb") as file:
            query.message.reply_document(document=file, filename="согласие на обработку ПД.pdf")
    elif query.data == 'consent':
        selection_cakes(query)


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
    cakes = Cake.objects.all()
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
        [InlineKeyboardButton('Вернуться в главное меню', callback_data='menu_cakes')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выберите улучшение вашему торту:', reply_markup=reply_markup)


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
    query.message.reply_text('Торт выбран, а теперь необходимо представиться.')
    query.message.reply_text('Пожалуйста, введите Ваше ФИО:')
    context.user_data['awaiting_full_name'] = True


def handle_message(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query:
        query.answer()
        if context.user_data.get('selected_cake_id'):
            process_cake(update, context)
    else:
        if context.user_data.get('awaiting_full_name'):
            process_full_name(update, context)
        elif context.user_data.get('awaiting_address'):
            process_address(update, context)
        elif context.user_data.get('awaiting_phone'):
            process_phone_number(update, context)
        elif context.user_data.get('selected_cake_id'):
            process_cake(update, context)


def process_full_name(update: Update, context: CallbackContext) -> None:
    context.user_data['full_name'] = update.message.text
    update.message.reply_text('Введите ваш адрес:')
    context.user_data['awaiting_address'] = True
    context.user_data['awaiting_full_name'] = False


def process_address(update: Update, context: CallbackContext) -> None:
    context.user_data['address'] = update.message.text
    update.message.reply_text('Введите номер телефона:')
    context.user_data['awaiting_phone'] = True
    context.user_data['awaiting_address'] = False


def process_phone_number(update: Update, context: CallbackContext) -> None:
    context.user_data['phone'] = update.message.text
    update.message.reply_text('Введите ваш электронный адрес:')
    context.user_data['awaiting_phone'] = False


def process_cake(update: Update, context: CallbackContext) -> None:
    cake = context.user_data['selected_cake_id']
    full_name = context.user_data['full_name']
    address = context.user_data['address']
    phone = context.user_data['phone']
    telegram_id = update.effective_user.id
    if not Client.objects.filter(telegram_id=telegram_id).exists():
        client = Client.objects.create(telegram_id=telegram_id, name=full_name, phonenumber=phone)
    else:
        client = Client.objects.get(telegram_id=telegram_id)

    order = Order.objects.create(cake=cake, client=client, address=address, price=cake.end_price)
    update.message.reply_text(f'''Ваш заказ - №{order.id} на сумму {order.price} принят.
    Спасибо за вашу заявку. Наш менеджер свяжется с вами.''')
    update.message.reply_text('Для запуска бота введите команду "/start"')


def update_main_menu(message) -> None:
    keyboard = [
        [InlineKeyboardButton('Произвести заказ', callback_data='consent')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text('Вами ранее уже был произведен заказ, хотите заказать еще?', reply_markup=reply_markup)


if __name__ == '__main__':
    load_dotenv()

    telegram_api = os.environ["TG_BOT_CAKE"]
    telegram_id = os.environ["TG_ID_CAKE"]
    bot = telegram.Bot(token=telegram_api)
    updater = Updater(token=telegram_api)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(main_menu_handler, pattern='^(consent_file|consent)$'))
    dispatcher.add_handler(CallbackQueryHandler(show_handler, pattern='^(list_cakes|cake_customization|menu_cakes)$'))
    dispatcher.add_handler(CallbackQueryHandler(logic_ready_cakes, pattern=r'^cake_\d+$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_message, pattern=r'^(selected_cake_id)$'))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print('Бот в сети')
    updater.idle()

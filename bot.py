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

from tg_bot.models import Client, Cake, Catalog

def start(update: Update, context: CallbackContext) -> None:
    # telegram_id = update.effective_user.id
    # if Client.objects.filter(telegram_id=telegram_id).first():
    #     update_main_menu(update.message)
    # else:
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
        with open("documents/Соглашение на обработку данных.pdf", "rb") as file:
            query.message.reply_document(document=file, filename="Соглашение на обработку данных.pdf")
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
    # client_id = query.from_user.id
    # client = Client.objects.filter(telegram_id=client_id).first()
    catalogs = Catalog.objects.all()
    keyboards = []
    for catalog in catalogs:
        keyboard = [InlineKeyboardButton(f'{catalog.id}. {catalog.title} - {catalog.price}', callback_data=f'cake_{catalog.id}')]
        keyboards.append(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboards)
    query.message.reply_text('Заказ будет готов в течении 3-х дней с 09:00 по 18:00. Выберите торт который вы хотите:', reply_markup=reply_markup)


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

    updater.start_polling()
    print('Бот в сети')
    updater.idle()

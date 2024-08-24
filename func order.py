
def new_order(update: Update, context: CallbackContext) -> None:
    if update.callback_query:
        query = update.callback_query
        query.answer()
        message = query.message
    else:
        message = update.message

    telegram_id = update.effective_user.id
    if Client.objects.filter(telegram_id=telegram_id).exists():
        client = Client.objects.get(telegram_id=telegram_id)
        context.user_data['full_name'] = client.name
        context.user_data['phone'] = client.phonenumber
        context.user_data['client'] = client
    else:
        message.reply_text('Пожалуйста, введите Ваше ФИО:')
        context.user_data['awaiting_full_name'] = True
        context.user_data['awaiting_address'] = False
        context.user_data['awaiting_phone'] = False
        return
    message.reply_text('Введите ваш адрес доставки:')
    context.user_data['awaiting_address'] = True
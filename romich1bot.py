import telebot
import requests
bot = telebot.TeleBot('8761173652:AAG8js1JUu9UgP3E8tm163yIr-pJN2C6-b0')
known_users = set()
pinned_messages = {}
last_rates_update = {}
RATES_INTERVAL = 1 * 10  # обновлять курс 
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите имя')
    
    usd_rub, eth_usd = get_rates()
    text = f'💵 Доллар: {usd_rub} ₽\n🔷 Эфир: {eth_usd} $'
    
    #chat_id = message.chat.id
    #if chat_id in pinned_messages:
    #    try:
    #        bot.edit_message_text(text, chat_id, pinned_messages[chat_id])
    #    except:
    #        sent = bot.send_message(chat_id, text)
    #        bot.pin_chat_message(chat_id, sent.message_id, disable_notification=True)
    #        pinned_messages[chat_id] = sent.message_id
    #else:
    #    sent = bot.send_message(chat_id, text)
    #    bot.pin_chat_message(chat_id, sent.message_id, disable_notification=True)
    #    pinned_messages[chat_id] = sent.message_id
    #bot.register_next_step_handler(message, get_operation)
    
    sent = bot.send_message(message.chat.id, text)
    #bot.pin_chat_message(message.chat.id, sent.message_id, disable_notification=True)
    bot.register_next_step_handler(message, get_operation)
def get_operation(message):
    #if not message.text:
    #    bot.register_next_step_handler(message, get_operation)
    #    return
        
    chat_id = message.chat.id
    update_rates_if_needed(chat_id)
    
    global operation
    operation = message.text.strip()
    op = operation.lower()
    if op == 'рома':
        bot.send_message(message.chat.id, 'Завозной')
    elif op == 'ян':
        bot.send_message(message.chat.id, 'васап хоуми')
    elif op in ('таня', 'татьяна'):
        bot.send_message(message.chat.id, 'Так это же любимая жиночка')
    elif op == 'артем':
        bot.send_message(message.chat.id, 'Фрукт френд')
    elif op == 'ваня':
        bot.send_message(message.chat.id, 'Скажите, пожалуйста, ваш номер СНИЛС')
        bot.register_next_step_handler(message, check_snils)
        return
    elif op == 'паша':
        bot.send_message(message.chat.id, 'Френд')
    elif op in ('погода в санкт петербурге', 'погода в спб', 'спб'):
        try:
            response = requests.get('https://wttr.in/Saint+Petersburg?format=j1', timeout=5)
            data = response.json()
            temp = data['current_condition'][0]['temp_C']
            feels_like = data['current_condition'][0]['FeelsLikeC']
            bot.send_message(message.chat.id, f'Погода в Санкт-Петербурге: {temp}°C, ощущается как {feels_like}°C')
        except Exception as e:
            bot.send_message(message.chat.id, 'Не удалось получить погоду, попробуйте позже')
    elif op in ('погода в москве', 'москва'):
        try:
            response = requests.get('https://wttr.in/Moscow?format=j1', timeout=5)
            data = response.json()
            temp = data['current_condition'][0]['temp_C']
            feels_like = data['current_condition'][0]['FeelsLikeC']
            bot.send_message(message.chat.id, f'Погода в Москве: {temp}°C, ощущается как {feels_like}°C')
        except Exception as e:
            bot.send_message(message.chat.id, 'Не удалось получить погоду, попробуйте позже')
    else:
        bot.send_message(message.chat.id, 'Такой мне не известен')
    bot.register_next_step_handler(message, get_operation)
def check_snils(message):
    if message.text.strip() == '123':
        bot.send_message(message.chat.id, 'Вы обманщик')
    else:
        bot.send_message(message.chat.id, 'Все четко, списала бабос')
    bot.register_next_step_handler(message, get_operation)



@bot.message_handler(func=lambda message: True)
def greet_new_user(message):
    if message.chat.id not in known_users:
        known_users.add(message.chat.id)
        bot.send_message(message.chat.id, 'Привет! Я заместитель Романа Викторовича. Введи какое нибудь имя и я подскажу кем он ему приходится. Напиши /start чтобы начать.')
        
        
        
def get_rates():
    try:
        usd = requests.get('https://www.cbr-xml-daily.ru/daily_json.js', timeout=5).json()
        usd_rub = round(usd['Valute']['USD']['Value'], 2)
    except:
        usd_rub = 'нет данных'
    try:
        eth = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd', timeout=5).json()
        eth_usd = round(eth['ethereum']['usd'], 2)
    except:
        eth_usd = 'нет данных'
    return usd_rub, eth_usd      


def update_rates_if_needed(chat_id):
    now = time.time()
    last = last_rates_update.get(chat_id, 0)
    sent = bot.send_message(chat_id, 'проходит тут апдейт рейтс')
    if now - last < RATES_INTERVAL:
        return
    try:
        usd_rub, eth_usd = get_rates()
        text = f'💵 Доллар: {usd_rub} ₽\n🔷 Эфир: {eth_usd} $'
        sent = bot.send_message(chat_id, text) ###############
        if chat_id in pinned_messages:
            try:
                bot.edit_message_text(text, chat_id, pinned_messages[chat_id])
            except:
                sent = bot.send_message(chat_id, text)
                bot.pin_chat_message(chat_id, sent.message_id, disable_notification=True)
                pinned_messages[chat_id] = sent.message_id
        else:
            sent = bot.send_message(chat_id, text)
            bot.pin_chat_message(chat_id, sent.message_id, disable_notification=True)
            pinned_messages[chat_id] = sent.message_id
        last_rates_update[chat_id] = now
    except:
        pass    
        
bot.polling(none_stop=True)
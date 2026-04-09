import telebot
import requests
import time
import threading
bot = telebot.TeleBot('8761173652:AAG8js1JUu9UgP3E8tm163yIr-pJN2C6-b0')
known_users = set()
active_chats = set()  
pinned_messages = {}
last_rates_update = {}
RATES_INTERVAL = 1 * 10  # обновлять курс 
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите имя')
    
    usd_rub, eth_usd = get_rates()
    text = f'💵 Доллар: {usd_rub} ₽\n🔷 Эфир: {eth_usd} $'    
    
    sent = bot.send_message(message.chat.id, text)
  
    bot.register_next_step_handler(message, get_operation)
def get_operation(message):
   
   
    
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

def rates_sender():
    while True:
        usd_rub, eth_usd = get_rates()
        bot.send_message(chat_id, 'поток')
        text = f'📊 АКТУАЛЬНЫЕ КУРСЫ:\n💵 Доллар: {usd_rub} ₽\n🔷 Эфир: {eth_usd} $'
        for chat_id in list(active_chats):  # копия списка для безопасности
            try:
                bot.send_message(chat_id, text)
            except:
                pass  # если чат недоступен, пропускаем
        time.sleep(30)  # ждем 30 сек

# Запуск потока рассылки и polling
sender_thread = threading.Thread(target=rates_sender, daemon=True)
sender_thread.start()

bot.polling(none_stop=True)
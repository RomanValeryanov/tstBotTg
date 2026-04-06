import telebot
import requests
bot = telebot.TeleBot('8761173652:AAG8js1JUu9UgP3E8tm163yIr-pJN2C6-b0')
known_users = set()
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите имя')
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
def get_num1(message):
    global num1
    try:
        num1 = float(message.text)
        bot.send_message(message.chat.id, 'Введите второе число:')
        bot.register_next_step_handler(message, get_num2)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Введите число. /start для повторa')
        bot.register_next_step_handler(message, get_num1)
def get_num2(message):
    global num2
    try:
        num2 = float(message.text)
        result = calculate(num1, num2, operation)
        bot.send_message(message.chat.id, f'Результат: {result}')
        bot.send_message(message.chat.id, '/start для новой операции')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Введите число. /start')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}. /start')
def calculate(a, b, op):
    if op == '+': return a + b
    elif op == '-': return a - b
    elif op == '*': return a * b
    elif op == '/':
        if b == 0: raise ValueError('Деление на ноль!')
        return a / b
    else:
        raise ValueError('Неверная операция!')
@bot.message_handler(func=lambda message: True)
def greet_new_user(message):
    if message.chat.id not in known_users:
        known_users.add(message.chat.id)
        bot.send_message(message.chat.id, 'Привет! Я заместитель Романа Викторовича. Введи какое нибудь имя и я подскажу кем он ему приходится. Напиши /gg чтобы начать.')
bot.polling(none_stop=True)
import paho.mqtt.client as mqtt
import config
import telebot
import requests
import json
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
user_dict = {}
client = mqtt.Client()


class ZoomMessage:
    """Класс для хранения данных при запуске трансляции на плафторе ZOOM"""

    def __init__(self, name):
        self.platform = name
        self.aud = None
        self.login = None
        self.password = None


class LmsMessage:
    """Класс для хранения данных при запуске трансляции на плафторе LMS.MAI"""

    def __init__(self, name):
        self.platform = name
        self.aud = None
        self.link = None


def on_connect(clinet, userdata, flags, rc):
    print("Connected with Code :" + str(rc))
    client.subscribe("smart_university/response/#")  # Бот подписывается на топик для обратной свзяи


def on_message(client, userdata, msg):
    callback = json.loads(msg.payload.decode("utf-8", "ignore"))
    bot.send_message(int(callback['id']),
                     str(callback['answer']))  # Получает из обратной связи id и сообщение, посылает его пользователю


client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(config.USER, config.PASSWORD)
client.connect(config.SERVER, config.PORT, 60)

client.loop_start()


def keyboard():
    # клавиатура для приветсвия
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton("Запустить новую трансляцию")
    btn2 = types.KeyboardButton("/help")
    markup.add(btn1, btn2)
    return markup


def keyboard_2():
    # клавиатура для выбора платформы
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton("ZOOM")
    btn2 = types.KeyboardButton("LMS.MAI")
    btn3 = types.KeyboardButton("Выйти")
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


def keyboard_3():
    # кнопка для выхода
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton("Выйти")
    markup.add(btn1)
    return markup


def keyboard_4():
    # кнопка остановки трансялции
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton("Остановить трансляцию")
    markup.add(btn1)
    return markup


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('bot_hello_sticker.tgs', 'rb')
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>".format(message.from_user,
                                                                                           bot.get_me()),
                     parse_mode='html')
    bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())


@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id,
                     "/start - Приветственное сообщение\n/help - Список команд\n/send - Начать трансляцию",
                     reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    """Бот проверяет наличие пользователя в базе преподавателей, если он там есть, то
    предлагает пользователю выбрать платоформу"""
    if (message.text == '/send') or (message.text == 'Запустить новую трансляцию'):
        # ЧТОБЫ ЗАРАБОТАЛО С РЕСТОМ - раскомментить следующие 2 строчки, закомментить 3-ю 
        # url ="http://"+config.REST_SERVER+":"+config.REST_PORT+"/users_list/"+str(message.chat.id) 
        # statement = requests.get(url).text
        statement = "True"

        if statement == "True":
            msg = bot.send_message(message.chat.id, 'Какую платформу выберете?', reply_markup=keyboard_2())
            bot.register_next_step_handler(msg, check_platform_step)
        elif statement == "False":
            bot.send_message(message.chat.id, 'Уходи')
        else:
            bot.send_message(message.chat.id, 'Меня сломали')


def check_platform_step(message):
    """В зависимости от выбора пользователя начинает определенную последователньость действий"""

    try:
        if message.text != 'Выйти':
            if message.text == 'ZOOM':
                chat_id = message.chat.id
                platform = message.text
                send = ZoomMessage(platform)
                user_dict[chat_id] = send
                msg = bot.send_message(message.chat.id, 'Введите номер аудитории: ', reply_markup=keyboard_3())
                bot.register_next_step_handler(msg,
                                               zoom_process_aud_step)  # посылает на следующий шаг последовательности ZOOM
            elif message.text == 'LMS.MAI':
                chat_id = message.chat.id
                platform = message.text
                send = LmsMessage(platform)
                user_dict[chat_id] = send
                msg = bot.send_message(message.chat.id, 'Введите номер аудитории: ', reply_markup=keyboard_3())
                bot.register_next_step_handler(msg,
                                               lms_process_aud_step)  # посылает на следующий шаг последовательности LMS.MAI
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, воспользуйтесь кнопками внизу диалога!',
                                       reply_markup=keyboard_2())
                bot.register_next_step_handler(msg, check_platform_step)
        else:
            sti = open('bot_menu_sticker.tgs', 'rb')
            bot.send_message(message.chat.id, 'Чем займемся?')
            bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


"""Начало последовательности для платформы ZOOM"""


def zoom_process_aud_step(message):
    try:
        if message.text != 'Выйти':
            chat_id = message.chat.id
            aud = message.text
            send = user_dict[chat_id]
            send.aud = aud
            msg = bot.send_message(message.chat.id, 'Введите логин конференции: ', reply_markup=keyboard_3())
            bot.register_next_step_handler(msg, zoom_process_login_step)
        else:
            sti = open('bot_menu_sticker.tgs', 'rb')
            bot.send_message(message.chat.id, 'Чем займемся?')
            bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


def zoom_process_login_step(message):
    try:
        if message.text != 'Выйти':
            chat_id = message.chat.id
            login = message.text
            send = user_dict[chat_id]
            send.login = login
            msg = bot.send_message(message.chat.id, 'Введите пароль конференции: ', reply_markup=keyboard_3())
            bot.register_next_step_handler(msg, zoom_process_password_step)
        else:
            sti = open('bot_menu_sticker.tgs', 'rb')
            bot.send_message(message.chat.id, 'Чем займемся?')
            bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


def zoom_process_password_step(message):
    try:
        if message.text != 'Выйти':
            chat_id = message.chat.id
            password = message.text
            send = user_dict[chat_id]
            send.password = password
            mqtt_message = '{"id":"' + str(chat_id) + '","driver": "' + str(
                send.platform) + '", "command": "ON", "params": {"meeting_id": "' + str(
                send.login) + '", "password": "' + str(send.password) + '"}} '
            topik = 'smart_university/' + str(send.aud) + '/execute_comand'
            client.publish(topik, mqtt_message)
            msg = bot.send_message(chat_id, 'Запрос отправлен!', reply_markup=keyboard_4())
            bot.register_next_step_handler(msg, zoom_process_end_step)
        else:
            sti = open('bot_menu_sticker.tgs', 'rb')
            bot.send_message(message.chat.id, 'Чем займемся?')
            bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


def zoom_process_end_step(message):
    try:
        if message.text == 'Остановить трансляцию':
            chat_id = message.chat.id
            send = user_dict[chat_id]
            mqtt_message = '{"id":"' + str(chat_id) + '","driver": "' + str(
                send.platform) + '", "command": "OFF", "params": {"meeting_id": "' + str(
                send.login) + '", "password": "' + str(send.password) + '"}}'

            topik = 'smart_university/' + str(send.aud) + '/execute_comand'
            client.publish(topik, mqtt_message)
            bot.send_message(chat_id, 'Запрос отправлен!', reply_markup=keyboard())
        else:
            pass
            sti = open('bot_menu_sticker.tgs', 'rb')
            bot.send_message(message.chat.id, 'Чем займемся?')
            bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


"""Конец последовательности для платформы ZOOM"""

"""Начало последовательности для платформы LMS.MAI"""


def lms_process_aud_step(message):
    try:
        if message.text != 'Выйти':
            chat_id = message.chat.id
            aud = message.text
            send = user_dict[chat_id]
            send.aud = aud
            msg = bot.send_message(message.chat.id, 'Вставьте ссылку на трансляцию: ', reply_markup=keyboard_3())
            bot.register_next_step_handler(msg, lms_process_link_step)
        else:
            sti = open('bot_menu_sticker.tgs', 'rb')
            bot.send_message(message.chat.id, 'Чем займемся?')
            bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


def lms_process_link_step(message):
    try:
        if message.text != 'Выйти':
            chat_id = message.chat.id
            link = str(message.text)

            send = user_dict[chat_id]
            send.link = link
            mqtt_message = '{"id":"' + str(chat_id) + '","driver": "' + str(
                send.platform) + '", "command": "ON", "params": {"link": "' + str(send.link) + '"}}'
            topik = 'smart_university/' + str(send.aud) + '/execute_comand'
            client.publish(topik, mqtt_message)
            msg = bot.send_message(chat_id, 'Запрос отправлен!', reply_markup=keyboard_4())
            bot.register_next_step_handler(msg, lms_process_end_step)
        else:
            sti = open('bot_menu_sticker.tgs', 'rb')
            bot.send_message(message.chat.id, 'Чем займемся?')
            bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


def lms_process_end_step(message):
    try:
        if message.text == 'Остановить трансляцию':
            chat_id = message.chat.id
            send = user_dict[chat_id]
            mqtt_message = '{"id":"' + str(chat_id) + '","driver": "' + str(
                send.platform) + '", "command": "OFF", "params": {"link": "' + str(
                send.link) + '"}}'

            topik = 'smart_university/' + str(send.aud) + '/execute_comand'
            client.publish(topik, mqtt_message)
            bot.send_message(chat_id, 'Запрос отправлен!', reply_markup=keyboard())
        else:
            pass
            sti = open('bot_menu_sticker.tgs', 'rb')
            bot.send_message(message.chat.id, 'Чем займемся?')
            bot.send_sticker(message.chat.id, sti, reply_markup=keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


"""Конец последовательности для платформы LMS.MAI"""

bot.enable_save_next_step_handlers(delay=1)

bot.load_next_step_handlers()

bot.polling()

client.loop_stop()
client.disconnect()

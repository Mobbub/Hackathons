import telebot, pickle, datetime, os
import gpt_yandex
from telebot import types
from geopy.geocoders import Nominatim
from telebot.handler_backends import BaseMiddleware, CancelUpdate

bot = telebot.TeleBot('', use_class_middlewares = True)

class SimpleMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']

    def pre_process(self, message, data):
        if not message.from_user.id in self.last_time:
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            bot.send_message(message.chat.id, 'Вы превысили скорость в отправке сообщений!🛑\n🚫Бот не будет реагировать на такую скорость🚫')
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date

    def post_process(self, message, data, exception):
        pass

bot.setup_middleware(SimpleMiddleware(0.01))

def load_session():
    try:
        with open('session.pickle', 'rb') as f:
            session = pickle.load(f)
    except FileNotFoundError:
        session = {}
    return session

def save_session(session):
    with open('session.pickle', 'wb') as f:
        pickle.dump(session, f)

session = load_session()
adm_session = {}

def prov(mes, vopr, chat_id):
    if vopr == 'ФИО':
         if len(mes.split()) == 3:
             return True
         return False
    elif vopr == 'ДР' or vopr == 'ДС':
        try:
            date = datetime.datetime.strptime(mes, "%d.%m.%Y").date()
            if vopr == 'ДР':
                if date <= date.today():
                    return True
                return False
            elif vopr == 'ДС':
                if date >= datetime.datetime.strptime(session[chat_id]['dr'], "%d.%m.%Y").date() and date <= date.today():
                    return True
                return False
        except ValueError:
            return False
    elif vopr == 'МР' or vopr == 'МС' or vopr == 'ГРАЖ':
            geolocator = Nominatim(user_agent = "my_application")
            location = geolocator.geocode(mes)
            if location is not None:
                return True
            return False
    elif vopr == 'Дети' or vopr == 'Внуки' or vopr == 'Супруг':
        mes_nov = ''
        schet = 1
        for i in range(len(mes)):
            if mes[i] != ',':
                mes_nov += mes[i]
            else:
                schet += 1
        if (len(mes_nov.split()) % 3 == 0) and (len(mes_nov.split()) / 3 == schet):
            return True
        return False
    else:
        if len(mes) >= 3:
            return True
        return False

def main(fio, dr, ds, mr, ms, supr, obr, rd, graj, deti, vnuki, dost):
    massiv_otv = {
        'fio': fio,
        'dr': dr,
        'ds': ds,
        'mr': mr,
        'ms': ms,
        'supr': supr,
        'obr': obr,
        'rd': rd,
        'graj': graj,
        'deti': deti,
        'vnuki': vnuki,
        'dost': dost,
    }
    massiv_bio = {
        'deys': 'биография'
    }
    massiv_epi = {
        'deys': 'эпитафия'
    }
    for key, value in massiv_otv.items():
        if value == 'Следующий вопрос▶️':
            massiv_otv[key] = 'Не указано'
    otv = otv = f'Вот страница памяти о человеке, про которого вы писали\n\n\`ФИО: {massiv_otv["fio"]};\n\nД.р.: {massiv_otv["dr"]};\n\nД.с.: {massiv_otv["ds"]};\n\nМесто рождения: {massiv_otv["mr"]};\n\nМесто смерти: {massiv_otv["ms"]};\n\nСупруг(а): {massiv_otv["supr"]};\n\nОбразование: {massiv_otv["obr"]};\n\nРод деятельности: {massiv_otv["rd"]};\n\nГражданство: {massiv_otv["graj"]};\n\nДети: {massiv_otv["deti"]};\n\nВнуки: {massiv_otv["vnuki"]};\n\nНаграды, премии или достижения: {massiv_otv["dost"]}\`;\n\nБиография:\`\n{gpt_yandex.get_yandexgpt_response(massiv_otv, massiv_bio)}\`\n\nЭпитафия:\`\n{gpt_yandex.get_yandexgpt_response(massiv_otv, massiv_epi)}\`'
    return otv

@bot.message_handler(commands = ['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn1 = types.KeyboardButton(text = 'Начнём')
    kb.add(btn1)
    chat_id = message.chat.id
    if chat_id not in session:
        session[chat_id] = {'flag_admin': False, 'flag1': False, 'flag2': False, 'flag3': False, 'flag4': False, 'flag5': False, 'flag6': False, 'flag7': False, 'flag8': False, 'flag9': False, 'flag10': False, 'flag11': False, 'flag12': False, 'fio': '', 'dr': '', 'ds': '', 'mr': '', 'ms': '', 'supr': '', 'obr': '', 'rd': '', 'graj': '', 'deti': '', 'vnuki': '', 'dost': ''}
        save_session(session)
    bot.send_message(message.chat.id, 'Приветствую!👋 \nЯ буду задавать вам простые и однострочные вопросы, на которые вы должны будете отвечать, для составления страницы памяти.\n<b><i>Если у вас по какой-то причине нет ответа на вопрос, то нажмите на кнопку "Следующий вопрос</i></b>🔼<b><i>"</i></b>.\nЕсли вы хотите получить больше информации о боте, то используйте команду /info', parse_mode = 'HTML')
    bot.send_message(message.chat.id, 'Начнём?', reply_markup=kb)

@bot.message_handler(commands = ['info'])
def info_sys(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn3 = types.KeyboardButton(text = '/start')
    kb.add(btn3)
    chat_id = message.chat.id
    session[chat_id] = {'flag_admin': False, 'flag1': False, 'flag2': False, 'flag3': False, 'flag4': False, 'flag5': False, 'flag6': False, 'flag7': False, 'flag8': False, 'flag9': False, 'flag10': False, 'flag11': False, 'flag12': False, 'fio': '', 'dr': '', 'ds': '', 'mr': '', 'ms': '', 'supr': '', 'obr': '', 'rd': '', 'graj': '', 'deti': '', 'vnuki': '', 'dost': ''}
    save_session(session)
    bot.send_message(message.chat.id, 'Что и как?\nДанный telegram бот создан для того, чтоб облегчить заполнение страницы об умершем человеке, а именно, он за вас напишет биографию или эпитафию по информации, которую вы дадите.\n<b><i>Маленькая подсказка: если на вопрос у вас есть несколько ответов, то просто перечислите их через запятую.</i></b>\n\nНавигация по командам:\n/start - начальная команда запуска бота.\n/info - информация об этом telegram боте.\n\nНавигация по кнопкам:\n├<b><i>Эпитафия</i></b> - бот начнёт запрашивать у вас информацию об человеке, для составления эпитафии.\n├<b><i>Биография</i></b> - бот начнёт запрашивать у вас информацию об человеке, для составления эпитафии.\n├<b><i>Следующий вопрос</i></b> 🔼 - если у вас нет ответа на вопрос, то нажмите эту кнопку, бот так и посчитает, что нет информации.\n├<b><i>Прошлый вопрос</i></b> 🔽 - если вы ошибочно ответили на прошлый вопрос или решили поменять ответ, то эта кнопка позволяет вернуться на одну стадию назад и ввести новый ответ.\n├<b><i>Начать заново</i></b> ↩️ - эта кнопка позволяет вернуться в самое начало и заново начать использовать этого бота.\n├<b><i>Другая страница</i></b> 🔄 - эта копка позволяет заменять биографию/эпитафию об этом же человеке, при том условии, если она вам не понравилась.\n\nХорошего использования!', reply_markup = kb, parse_mode = "HTML")

@bot.message_handler(commands = ['admin'])
def admin(message):
    chat_id = message.chat.id
    if chat_id in adm_session:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn_adm_1 = types.KeyboardButton(text = 'Работа с сессиями')
        kb.add(btn_adm_1)
        session[chat_id]['flag_admin'] = True
        save_session(session)
        bot.send_message(message.chat.id, '<b><i>Вы успешно вошли в админ панель</i></b>✅\n<b><i>Выбери нужное вам действие под этим сообщением</i></b> ⬇️', reply_markup = kb,  parse_mode = 'HTML')
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так⛔️')

@bot.message_handler(func = lambda message: message.text == 'Работа с сессиями')
def deytv_session(message):
    chat_id = message.chat.id
    if session[chat_id]['flag_admin'] == True:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn_adm_2 = types.KeyboardButton(text = 'Просмотреть сессии')
        btn_adm_3 = types.KeyboardButton(text = 'Очистить сессии')
        btn_adm_4 = types.KeyboardButton(text = '◀️Назад')
        kb.add(btn_adm_2)
        kb.add(btn_adm_3)
        kb.add(btn_adm_4)
        bot.send_message(message.chat.id, '<b><i>Что будем делать?</i></b>\n\n├<b><i>Просмотреть сессии - вывод всех сессий, которые есть в бд на данный момент</i></b>\n├<b><i>Очистить сессии - удалить все сессии, которые есть на данный момент</i></b>', reply_markup = kb, parse_mode = 'HTML')
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так⛔️')

@bot.message_handler(func = lambda message: message.text == 'Просмотреть сессии')
def check_ses(message):
    chat_id = message.chat.id
    if session[chat_id]['flag_admin'] == True:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn_adm_4 = types.KeyboardButton(text = 'Просмотреть сессии')
        btn_adm_5 = types.KeyboardButton(text = 'Очистить сессии')
        btn_adm_6 = types.KeyboardButton(text = '◀️Назад')
        kb.add(btn_adm_4)
        kb.add(btn_adm_5)
        kb.add(btn_adm_6)
        MESS_MAX_LENGTH = 4096
        try:
            with open('session.pickle', 'rb') as f:
                data = pickle.load(f)
                data1 = str(data)
            for x in range(0, len(data1), MESS_MAX_LENGTH):
                mess = data1[x: x + MESS_MAX_LENGTH]
                bot.send_message(message.chat.id, mess, reply_markup = kb)
        except FileNotFoundError:
            bot.send_message(message.chat.id, '<b><i>Сессий нет</i></b>', reply_markup = kb, parse_mode = 'HTML')
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так⛔️')

@bot.message_handler(func = lambda message: message.text == 'Очистить сессии')
def ochist_ses(message):
    chat_id = message.chat.id
    if session[chat_id]['flag_admin'] == True:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn_adm_7 = types.KeyboardButton(text = 'Просмотреть сессии')
        btn_adm_8 = types.KeyboardButton(text = 'Очистить сессии')
        btn_adm_9 = types.KeyboardButton(text = '◀️Назад')
        kb.add(btn_adm_7)
        kb.add(btn_adm_8)
        kb.add(btn_adm_9)
        try:
            file_path = 'session.pickle'
            os.remove(file_path)
            bot.send_message(message.chat.id, '<b><i>Сессии удалены</i></b>', reply_markup = kb, parse_mode = 'HTML')
        except FileNotFoundError:
            bot.send_message(message.chat.id, '<b><i>Сессий нет</i></b>', reply_markup = kb, parse_mode = 'HTML')
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так⛔️')

@bot.message_handler(func = lambda message: message.text == '◀️Назад')
def nazad(message):
    chat_id = message.chat.id
    if chat_id in adm_session:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn_adm_10 = types.KeyboardButton(text = 'Работа с сессиями')
        kb.add(btn_adm_10)
        bot.send_message(message.chat.id, '<b><i>Выбери нужное вам действие под этим сообщением</i></b> ⬇️', reply_markup = kb,  parse_mode = 'HTML')
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так⛔️')

@bot.message_handler(func = lambda message: message.text == 'Начнём')
def epitafia(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn4 = types.KeyboardButton(text = 'Начать заново↩️')
    kb.add(btn4)
    chat_id = message.chat.id
    session[chat_id]['flag1'] = True
    save_session(session)
    bot.send_message(message.chat.id, 'Введите <b><i>ФИО</i></b> 👤\nНапример: <i><code>Иванов Иван Иванович</code></i>', reply_markup = kb, parse_mode = "HTML")

@bot.message_handler(func = lambda message: message.text == 'Другая страница🔄')
def noviy(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    chat_id = message.chat.id
    btn4 = types.KeyboardButton(text = 'Начать заново↩️')
    kb.add(btn4)
    chat_id = message.chat.id
    session[chat_id] = {'flag1': False, 'flag2': False, 'flag3': False, 'flag4': False, 'flag5': False, 'flag6': False, 'flag7': False, 'flag8': False, 'flag9': False, 'flag10': False, 'flag11': False, 'flag12': False, 'fio': '', 'dr': '', 'ds': '', 'mr': '', 'ms': '', 'supr': '', 'obr': '', 'rd': '', 'graj': '', 'deti': '', 'vnuki': '', 'dost': '',}
    save_session(session)
    session[chat_id]['flag1'] = True
    save_session(session)
    bot.send_message(message.chat.id, 'Введите <b><i>ФИО</i></b> 👤\nНапример: <i><code>Иванов Иван Иванович</code></i>', reply_markup = kb, parse_mode = "HTML")

@bot.message_handler(func = lambda message: message.text == 'Начать заново↩️')
def zanovo(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn1 = types.KeyboardButton(text = 'Начнём')
    kb.add(btn1)
    chat_id = message.chat.id
    session[chat_id] = {'flag_admin': False, 'flag1': False, 'flag2': False, 'flag3': False, 'flag4': False, 'flag5': False, 'flag6': False, 'flag7': False, 'flag8': False, 'flag9': False, 'flag10': False, 'flag11': False, 'flag12': False, 'fio': '', 'dr': '', 'ds': '', 'mr': '', 'ms': '', 'supr': '', 'obr': '', 'rd': '', 'graj': '', 'deti': '', 'vnuki': '', 'dost': ''}
    save_session(session)
    bot.send_message(message.chat.id, 'Приветствую!👋 \nЯ буду задавать вам простые и однострочные вопросы, на которые вы должны будете отвечать, для составления страницы памяти.\n<b><i>Если у вас по какой-то причине нет ответа на вопрос, то нажмите на кнопку "Следующий вопрос</i></b>🔼<b><i>"</i></b>.\nЕсли вы хотите получить больше информации о боте, то используйте команду /info', parse_mode = 'HTML')
    bot.send_message(message.chat.id, 'Начнём?', reply_markup=kb)

@bot.message_handler(func = lambda message: message.text == '◀️Прошлый вопрос')
def prosh_vopr(message):
    chat_id = message.chat.id
    if session[chat_id]['flag2']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn10 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn10)
        session[chat_id]['flag1'] = True
        bot.send_message(message.chat.id, 'Введите <b><i>ФИО</i></b> 👤\nНапример: <i><code>Иванов Иван Иванович</code></i>', reply_markup = kb, parse_mode = "HTML")
    elif session[chat_id]['flag3']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn11 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn12 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn11)
        kb.add(btn12)
        session[chat_id]['flag2'] = True
        bot.send_message(message.chat.id, 'Введите <b><i>дату рождения</i></b> 👶\nНапример: <code>30.12.2000</code>', reply_markup = kb, parse_mode = "HTML")
    elif session[chat_id]['flag4']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn13 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn14 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn13)
        kb.add(btn14)
        session[chat_id]['flag3'] = True
        bot.send_message(message.chat.id, 'Введите <b><i>дату смерти</i></b> 🥀\nНапример: <code>30.12.2000</code>', reply_markup = kb, parse_mode = "HTML")
    elif session[chat_id]['flag5']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn15 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn16 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn17 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn16, btn15)
        kb.add(btn17)
        session[chat_id]['flag4'] = True
        bot.send_message(message.chat.id, 'Введите <b><i>место рождения</i></b> 🏳️\nНапример: <code>Россия, Москва</code>', reply_markup = kb, parse_mode = "HTML")
    elif session[chat_id]['flag6']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn18 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn19 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn20 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn19, btn18)
        kb.add(btn20)
        session[chat_id]['flag5'] = True
        bot.send_message(message.chat.id, 'Введите <b><i>место смерти</i></b> 🪦\nНапример: <code>Россия, Москва</code>', reply_markup = kb, parse_mode = "HTML")
    elif session[chat_id]['flag7']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn21 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn22 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn23 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn22, btn21)
        kb.add(btn23)
        session[chat_id]['flag6'] = True
        bot.send_message(message.chat.id, 'Введите <b><i>ФИО супруга(ги)</i></b> 👫\nНапример: <code>Иванов Иван Иванович</code>', reply_markup = kb, parse_mode = "HTML")
    elif session[chat_id]['flag8']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn24 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn25 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn26 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn25, btn24)
        kb.add(btn26)
        session[chat_id]['flag7'] = True
        bot.send_message(message.chat.id, 'Укажите <b><i>образование (учебное заведение), которое есть у человека</i></b> 🎓\nНапример: <code>КФУ им. Вернадского, информатика и вычислительная техника</code>', reply_markup = kb, parse_mode = "HTML")
    elif session[chat_id]['flag9']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn27 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn28 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn29 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn28, btn27)
        kb.add(btn29)
        session[chat_id]['flag8'] = True
        bot.send_message(message.chat.id, 'Укажите <b><i>род деятельности человека</i></b> 👨🏻‍🔧\nНапример: <code>Учёный-математик</code>', reply_markup = kb, parse_mode = "HTML")
    elif session[chat_id]['flag10']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn30 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn31 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn32 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn31, btn30)
        kb.add(btn32)
        session[chat_id]['flag9'] = True
        bot.send_message(message.chat.id, 'Укажите <b><i>гражданство человека</i></b> 👳🏽‍♀️\nНапример: <code>Россия Федерация</code>', reply_markup = kb, parse_mode="HTML")
    elif session[chat_id]['flag11']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn33 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn34 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn35 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn34, btn33)
        kb.add(btn35)
        session[chat_id]['flag10'] = True
        bot.send_message(message.chat.id, 'Укажите <b><i>ФИО детей</i></b> 👨‍👩‍👧‍👦\nНапример: <code>Иванов Иван Иванович</code>', reply_markup = kb, parse_mode="HTML")
    elif session[chat_id]['flag12']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn36 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn37 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn38 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn37, btn36)
        kb.add(btn38)
        session[chat_id]['flag11'] = True
        bot.send_message(message.chat.id, 'Укажите <b><i>ФИО внуков</i></b> 👨‍👧‍👦\nНапример: <code>Иванов Иван Иванович</code>', reply_markup = kb, parse_mode="HTML")
    else:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn39 = types.KeyboardButton(text = 'Эпитафия')
        btn40 = types.KeyboardButton(text = 'Биография')
        kb.add(btn39)
        kb.add(btn40)
        bot.send_message(message.chat.id, 'Извините, я вас не понимаю... 😔')
        bot.send_message(message.chat.id, 'Что вас интересует?', reply_markup=kb)

@bot.message_handler(func = lambda message: True)
def info(message):
    chat_id = message.chat.id
    if session[chat_id]['flag1']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn41 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn42 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn41)
        kb.add(btn42)
        if prov(message.text, 'ФИО', chat_id):
            session[chat_id]['fio'] = message.text
            session[chat_id]['flag2'] = True
            message.text = ''
            session[chat_id]['flag1'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Введите <b><i>дату рождения</i></b> 👶\nНапример: <code>30.12.2000</code>', reply_markup=kb, parse_mode = "HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите ФИО ещё раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Иванов Иван Иванович</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag2']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn43 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn44 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn43)
        kb.add(btn44)
        if prov(message.text, 'ДР', chat_id):
            session[chat_id]['dr'] = message.text
            session[chat_id]['flag3'] = True
            message.text = ''
            session[chat_id]['flag2'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Введите <b><i>дату смерти</i></b> 🥀\nНапример: <code>30.12.2000</code>', reply_markup=kb, parse_mode = "HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите дату рождения ещё раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>30.12.2000</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag3']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn45 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn46 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn47 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn46, btn45)
        kb.add(btn47)
        if prov(message.text, 'ДС', chat_id):
            session[chat_id]['ds'] = message.text
            session[chat_id]['flag4'] = True
            message.text = ''
            session[chat_id]['flag3'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Введите <b><i>место рождения</i></b> 🏳️\nНапример: <code>Россия, Москва</code>', reply_markup=kb, parse_mode = "HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите дату смерти ещё раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>30.12.2000</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag4']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn48 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn49 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn50 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn49, btn48)
        kb.add(btn50)
        if prov(message.text, 'МР', chat_id) or message.text == 'Следующий вопрос▶️':
            session[chat_id]['mr'] = message.text
            session[chat_id]['flag5'] = True
            message.text = ''
            session[chat_id]['flag4'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Введите <b><i>место смерти</i></b> 🪦\nНапример: <code>Россия, Москва</code>', reply_markup=kb, parse_mode = "HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите место рождения ещё раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Россия, Москва</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag5']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn51 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn52 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn53 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn52, btn51)
        kb.add(btn53)
        if prov(message.text, 'МС', chat_id) or message.text == 'Следующий вопрос▶️':
            session[chat_id]['ms'] = message.text
            session[chat_id]['flag6'] = True
            message.text = ''
            session[chat_id]['flag5'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Введите <b><i>ФИО супруга(ги)</i></b> 👫\nНапример: <code>Иванов Иван Иванович</code>', reply_markup=kb, parse_mode = "HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите место смерти ещё раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Россия, Москва</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag6']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn54 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn55 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn56 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn55, btn54)
        kb.add(btn56)
        if prov(message.text, 'Супруг', chat_id) or message.text == 'Следующий вопрос▶️':
            session[chat_id]['supr'] = message.text
            session[chat_id]['flag7'] = True
            message.text = ''
            session[chat_id]['flag6'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Укажите <b><i>образование (учебное заведение), которое есть у человека</i></b> 🎓\nНапример: <code>КФУ им. Вернадского, информатика и вычислительная техника</code>', reply_markup=kb, parse_mode = "HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите ФИО супруга(ги) ещё раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Иванов Иван Иванович</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag7']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn57 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn58 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn59 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn58, btn57)
        kb.add(btn59)
        if prov(message.text, 'обр', chat_id) or message.text == 'Следующий вопрос▶️':
            session[chat_id]['obr'] = message.text
            session[chat_id]['flag8'] = True
            message.text = ''
            session[chat_id]['flag7'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Укажите <b><i>род деятельности человека</i></b> 👨🏻‍🔧\nНапример: <code>Учёный-математик</code>', reply_markup=kb, parse_mode = "HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите образование (учебное заведение), которое есть у человека ещё раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>КФУ им. Вернадского, информатика и вычислительная техника</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag8']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn60 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn61 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn62 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn61, btn60)
        kb.add(btn62)
        if prov(message.text, 'РД', chat_id) or message.text == 'Следующий вопрос▶️':
            session[chat_id]['rd'] = message.text
            session[chat_id]['flag9'] = True
            message.text = ''
            session[chat_id]['flag8'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Укажите <b><i>гражданство человека</i></b> 👳🏽‍♀️\nНапример: <code>Российская Федерация</code>', reply_markup=kb, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите род деятельности человека еще раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Учёный-математик</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag9']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn63 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn64 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn65 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn64, btn63)
        kb.add(btn65)
        if prov(message.text, 'ГРАЖ', chat_id) or message.text == 'Следующий вопрос▶️':
            session[chat_id]['graj'] = message.text
            session[chat_id]['flag10'] = True
            message.text = ''
            session[chat_id]['flag9'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Укажите <b><i>ФИО детей</i></b> 👨‍👩‍👧‍👦\nНапример: <code>Иванов Иван Иванович</code>', reply_markup=kb, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите гражданство человека еще раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Российская Федерация</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag10']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn66 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn67 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn68 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn67, btn66)
        kb.add(btn68)
        if prov(message.text, 'Дети', chat_id) or message.text == 'Следующий вопрос▶️':
            session[chat_id]['deti'] = message.text
            session[chat_id]['flag11'] = True
            message.text = ''
            session[chat_id]['flag10'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Укажите <b><i>ФИО внуков</i></b> 👨‍👧‍👦\nНапример: <code>Иванов Иван Иванович</code>', reply_markup=kb, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите ФИО детей еще раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Иванов Иван Иванович</code>', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag11']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn69 = types.KeyboardButton(text = 'Следующий вопрос▶️')
        btn70 = types.KeyboardButton(text = '◀️Прошлый вопрос')
        btn71 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn70, btn69)
        kb.add(btn71)
        if prov(message.text, 'Внуки', chat_id) or message.text == 'Следующий вопрос▶️':
            session[chat_id]['vnuki'] = message.text
            session[chat_id]['flag12'] = True
            message.text = ''
            session[chat_id]['flag11'] = False
            save_session(session)
            bot.send_message(message.chat.id, 'Введите <b><i>награды, премии или достижения, которые есть у человека</i></b> 🏅\nНапример: <code>Знак Почета 1954</code>', reply_markup=kb, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите ФИО внуков еще раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Иванов Иван Иванович</code>''', reply_markup=kb, parse_mode = "HTML")
    elif session[chat_id]['flag12']:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn72 = types.KeyboardButton(text = 'Другая страница🔄')
        btn73 = types.KeyboardButton(text = 'Начать заново↩️')
        kb.add(btn72)
        kb.add(btn73)
        if prov(message.text, 'дост', chat_id):
            session[chat_id]['dost'] = message.text
            session[chat_id]['flag12'] = False
            save_session(session)
            MESS_MAX_LENGTH = 4096
            otv_ne = main(session[chat_id]['fio'], session[chat_id]['dr'], session[chat_id]['ds'], session[chat_id]['mr'], session[chat_id]['ms'], session[chat_id]['supr'], session[chat_id]['obr'], session[chat_id]['rd'], session[chat_id]['graj'], session[chat_id]['deti'], session[chat_id]['vnuki'], session[chat_id]['dost'])
            for x in range(0, len(otv_ne), MESS_MAX_LENGTH):
                mess = otv_ne[x: x + MESS_MAX_LENGTH]
                bot.send_message(message.chat.id, mess, reply_markup = kb)
        else:
            bot.send_message(message.chat.id, 'Что то пошло не так... 😵‍💫\n<i>Введите награды, премии или достижения, которые есть у человека, еще раз, проверьте правильность и логику написанного.</i> ✅\nНапример: <code>Знак Почета 1954</code>''', reply_markup=kb, parse_mode = "HTML")
    else:
        kb = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn74 = types.KeyboardButton(text = 'Эпитафия')
        btn75 = types.KeyboardButton(text = 'Биография')
        kb.add(btn74)
        kb.add(btn75)
        bot.send_message(message.chat.id, 'Извините, я вас не понимаю... 😔')
        bot.send_message(message.chat.id, 'Что вас интересует?', reply_markup=kb)

bot.polling()

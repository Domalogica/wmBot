# -*- coding: utf-8 -*-
import telebot
from menu import menu, generator_menu, generator_stop
from db import connect_mysql
import requests, json
from settings import *
import cherrypy
import time

token = "533495913:AAHG-ssiGLwQMCPVBSDG-WVUA8M3aUYzo-0"
WEBHOOK_HOST = '194.67.204.153'
WEBHOOK_PORT = 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)

SERVER_URL = "api.domalogica.com/"
SERVER_PATH = "app/"

bot = telebot.TeleBot(token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


def transfer(method, **kwargs):
    url = 'http://%s%s%s/' % (SERVER_URL, SERVER_PATH, method)
    response = requests.get(url, params=kwargs)
    try:
        return json.loads(response.content.decode("utf-8"))
    except Exception:
        pass


@bot.message_handler(commands=['start'])
def handle_start(message):
    result = transfer("add_user", telegram=message.from_user.id, first_name=message.chat.first_name)
    if result['return'] == "USER_ADDED":
        try:
            del_message_db(message.chat.id)
        except Exception as e:
            pass
        menu_list = get_branch_db(message.from_user.id)
        send = bot.send_message(message.from_user.id, text_start, reply_markup=generator_menu(menu_list))
        add_message_db(message.chat.id, send.message_id)
    else:
        message_id = get_message_db(message.chat.id)
        if not message_id:
            menu_list = get_branch_db(message.from_user.id)
            send = bot.send_message(message.from_user.id, "Выберите один из пунктов меню", reply_markup=generator_menu(menu_list))
            add_message_db(message.chat.id, send.message_id)
        else:
            try:
                del_msgmenu(message_id, message.chat.id)
            except Exception as e:
                pass
            del_message_db(message.chat.id)
            menu_list = get_branch_db(message.from_user.id)
            send = bot.send_message(message.from_user.id, "Выберите один из пунктов меню", reply_markup=generator_menu(menu_list))
            add_message_db(message.chat.id, send.message_id)

@bot.callback_query_handler(func=lambda message: True)
def message_handler(message):
    if message.data == "Подключиться к водомату":
        transfer("get_score", telegram=message.from_user.id)
        transition(text_id, message.data, message.message.chat.id)
    elif message.data == "Назад":
        go_back(text_get, message.data, message.message.chat.id)
    elif message.data  == "Остановить":
        result = transfer("disconnect/wm", telegram=message.from_user.id)
        print(result)
        if result['return'] == "SUCCESSFUL":
            result = transfer("get_score", telegram=message.from_user.id)
            print(result['return'])
            R = str(result['return']/100) + " ₽"
            L = str(result['return']/400) + " литров / "
            score = L + R
            go_back(text_1 + score, message.data, message.message.chat.id)
    elif message.data == "Баланс":
        result = transfer("get_score", telegram=message.from_user.id)
        print(result['return'])
        R = str(result['return']/100) + " ₽"
        L = str(result['return']/400) + " литров / "
        entrance(L + R, message.message.chat.id)
    elif message.data == "Адреса водоматов":
        result = transfer("get_location", telegram=message.from_user.id)
        print(result)
    elif message.data == "Текущее состояние":
        result = transfer("sales_statistics", telegram=message.from_user.id)
        print(result)
    elif message.data == "Активные водоматы":
        result = transfer("get_active_wms", telegram=message.from_user.id)
        print(result)
        message_id = get_message_db(message.message.chat.id)
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message_id, text="0000000000000000000")
    elif message.data == "За сутки":
        pass
    elif message.data == "За неделю":
        pass
    elif message.data == "Оставить отзыв":
        result = transfer("active_water", telegram=message.from_user.id)
        print(result)
    elif message.data:
        transition(text_get, message.data, message.message.chat.id)


@bot.message_handler(content_types=['location'])
def handle_start(message):
    recommends = {
        "telegram": message.chat.id,
        "username": message.chat.first_name,
        "place_x": message.location.latitude,
        "place_y": message.location.longitude
    }
    result = transfer("active_water", **recommends)
    print(result)

@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text.isdigit():
        menu_list = get_branch_db(message.from_user.id)
        if menu_list[-1] == "Подключиться к водомату":
            result = transfer("connect/wm", telegram=message.from_user.id, wm=message.text)
            print(result)
            try:
                message_id = get_message_db(message.chat.id)
                del_msgmenu(message_id, message.chat.id)
            except Exception as e:
                pass
            del_message_db(message.chat.id)
            menu_list = get_branch_db(message.from_user.id)
            res = result["return"]

            result = transfer("get_score", telegram=message.from_user.id)
            print(result['return'])
            R = str(result['return']/100) + " ₽"
            L = str(result['return']/400) + " литров / "
            score = L + R
            wm = int(message.text)

            text_on = """
            Вы успешно подключились к %d водомату\n\n1. Установите тару в водомат\n\n2. Нажмите кноку "Старт" на аппарате.\n\nЦена за 1 литр 4₽\n\nЧтобы пополнить баланс используйте купюроприемник и монетоприемник.\n\nВаш баланс: %s"""%(wm, score)

            send = bot.send_message(message.from_user.id, text_on, reply_markup=generator_stop())
            add_message_db(message.chat.id, send.message_id)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    bot.send_voice(chat_id=message.chat.id, voice=file.content)


def entrance(text, chat_id):
    message_id = get_message_db(chat_id)
    menu_list = get_branch_db(chat_id)
    upt_msgmenu(text, menu_list, message_id, chat_id)

def transition(menu_text, text, chat_id):
    message_id = get_message_db(chat_id)
    # del_message_db(chat_id)
    add_branches_db(chat_id, text)
    menu_list = get_branch_db(chat_id)
    upt_msgmenu(menu_text, text, menu_list, message_id, chat_id)

def go_back(menu_text, text, chat_id):
    message_id = get_message_db(chat_id)
    # del_message_db(chat_id)
    del_branch_db(chat_id)
    menu_list = get_branch_db(chat_id)
    upt_msgmenu(menu_text, text, menu_list, message_id, chat_id)

def distributor():
    pass


def upt_msgmenu(menu_text, text, menu_list, message_id, chat_id):
    send = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=menu_text, reply_markup=generator_menu(menu_list))
    # add_message_db(chat_id, send.message_id)


def del_msgmenu(message_id, chat_id):
    bot.delete_message(chat_id=chat_id, message_id=message_id)




























def add_branches_db(telegram, branch):
    result = connect_mysql.insert('branches', *["telegram", "branch"], **{'telegram': telegram, 'branch': branch})
    return result

def get_branch_db(telegram):
    conditional_query = "telegram = %s"
    result = connect_mysql.select("branches", conditional_query, *["branch"], **{'telegram': telegram})
    return result

def del_branch_db(telegram):
    result = connect_mysql.delete_branch(telegram)
    return result

def get_message_db(telegram):
    conditional_query = "telegram = %s"
    result = connect_mysql.select("message", conditional_query, *["message_id"], **{'telegram': telegram})
    return result

def add_message_db(telegram, message_id):
    result = connect_mysql.insert('message', *["telegram", "branch"], **{'telegram': telegram, 'message_id': message_id})
    return result

def del_message_db(telegram):
    conditional_query = 'telegram = %s'
    result = connect_mysql.delete('message', conditional_query, *[telegram])
    return result



# bot.polling(none_stop=True, interval = 0)



bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})


cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})



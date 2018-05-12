# -*- coding: utf-8 -*-
import telebot
from menu import menu, generator_menu, generator_stop
from db import connect_mysql
import requests, json
from settings import *

token = "533495913:AAHG-ssiGLwQMCPVBSDG-WVUA8M3aUYzo-0"

bot = telebot.TeleBot(token)


class MethodGet:
    def __init__(self, method):
        self.request = {"method": "", "param": {}}
        self.request.update({"method": method})

    def transfer(self):
        response = requests.get('http://194.67.217.180:8484/app/%s/' % self.request["method"], params=self.request["param"])
        try:
            response = json.loads(response.content.decode("utf-8"))
        except Exception as e:
            pass
        return response

    def param(self, **kwargs):
        self.request["param"] = kwargs
        return True

@bot.message_handler(commands=['start'])
def handle_start(message):
    a = MethodGet("add_user")
    add_user = {
        "telegram": message.from_user.id,
        "first_name": message.chat.first_name
    }
    a.param(**add_user)
    result = a.transfer()
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
        a = MethodGet("get_score")
        add_user = {
            "telegram": message.from_user.id
        }
        a.param(**add_user)
        result = a.transfer()
        print(result['return'])
        R = str(result['return']/100) + " ₽"
        L = str(result['return']/400) + " литров / "
        score = L + R
        transition(text_water + score, message.data, message.message.chat.id)
    elif message.data == "Назад":
        go_back(text_get, message.data, message.message.chat.id)
    elif message.data  == "Остановить":
        a = MethodGet("disconnect/wm")
        add_user = {
            "telegram": message.from_user.id
        }
        a.param(**add_user)
        result = a.transfer()
        print(result)
        if result['return'] == "SUCCESSFUL":
            go_back(message.data, message.message.chat.id)
    elif message.data == "Баланс":
        a = MethodGet("get_score")
        add_user = {
            "telegram": message.from_user.id
        }
        a.param(**add_user)
        result = a.transfer()
        print(result['return'])
        R = str(result['return']/100) + " ₽"
        L = str(result['return']/400) + " литров / "
        entrance(L + R, message.message.chat.id)
    elif message.data == "Адреса водоматов":
        a = MethodGet("get_location")
        add_user = {
            "telegram": message.from_user.id
        }
        a.param(**add_user)
        result = a.transfer()
        print(result)
    elif message.data == "Текущее состояние":
        a = MethodGet("sales_statistics")
        add_user = {
            "telegram": message.from_user.id
        }
        a.param(**add_user)
        result = a.transfer()
        print(result)
    elif message.data == "Активные водоматы":
        a = MethodGet("get_active_wms")
        add_user = {
            "telegram": message.from_user.id
        }
        a.param(**add_user)
        result = a.transfer()
        print(result)
        message_id = get_message_db(message.message.chat.id)
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message_id, text="0000000000000000000")
    elif message.data == "За сутки":
        pass
    elif message.data == "За неделю":
        pass
    elif message.data == "Оставить отзыв":
        a = MethodGet("active_water")
        add_user = {
            "telegram": message.from_user.id
        }
        a.param(**add_user)
        result = a.transfer()
        print(result)
    elif message.data:
        transition(message.data, message.message.chat.id)


@bot.message_handler(content_types=['location'])
def handle_start(message):
    a = MethodGet("active_water")
    recommends = {
    "telegram": message.chat.id,
    "username": message.chat.first_name,
    "place_x": message.location.latitude,
    "place_y": message.location.longitude
    }
    a.param(**recommends)
    result = a.transfer()
    print(result)

@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text.isdigit():
        menu_list = get_branch_db(message.from_user.id)
        if menu_list[-1] == "Подключиться к водомату":
            a = MethodGet("connect/wm")
            add_user = {
                "telegram": message.from_user.id,
                "wm": message.text
            }
            a.param(**add_user)
            result = a.transfer()
            print(result)
            try:
                message_id = get_message_db(message.chat.id)
                del_msgmenu(message_id, message.chat.id)
            except Exception as e:
                pass
            del_message_db(message.chat.id)
            menu_list = get_branch_db(message.from_user.id)
            res = result["return"]


            a = MethodGet("get_score")
            add_user = {
                "telegram": message.from_user.id
            }
            a.param(**add_user)
            result = a.transfer()
            print(result['return'])
            R = str(result['return']/100) + " ₽"
            L = str(result['return']/400) + " литров / "
            score = L + R
            wm = int(message.text)

            # text_on = """
            # Вы успешно подключились к %d водомату

            # 1. Установите тару в водомат

            # 2. Нажмите кноку "Старт" на аппарате.

            #  Цена за 1 литр 4₽

            # Чтобы пополнить баланс используйте купюроприемник и монетоприемник.

            # Ваш баланс: %s
            # """(wm, score)
            print(type(wm))
            print(type(score))

            # send = bot.send_message(message.from_user.id, text_on, reply_markup=generator_stop())
            add_message_db(message.chat.id, send.message_id)




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






bot.polling(none_stop=True, interval=0)
# -*- coding: utf-8 -*-
import telebot
from menu import menu, generator_menu
from db import connect_mysql
import requests, json

token = "533495913:AAHG-ssiGLwQMCPVBSDG-WVUA8M3aUYzo-0"

bot = telebot.TeleBot(token)


class MethodGet:
    def __init__(self, method):
        self.request = {"method": "", "param": {}}
        self.request.update({"method": method})

    def transfer(self):
        response = requests.get('http://194.67.217.180:8484/app/%s/' % self.request["method"], params=self.request["param"])
        response = json.loads(response.content.decode("utf-8"))
        return response

    def param(self, **kwargs):
        self.request["param"] = kwargs
        return True


@bot.message_handler(commands=['start'])
def handle_start(message):
    message_id = get_message_db(message.chat.id)
    del_msgmenu(message_id, message.chat.id)
    del_message_db(message.chat.id)
    menu_list = get_branch_db(message.from_user.id)
    send = bot.send_message(message.from_user.id, "Выберите один из пунктов меню", reply_markup=generator_menu(menu_list))
    add_message_db(message.chat.id, message.message_id)


# URL:8485/app/connect/wm methods=['GET']) args (user:id, wm:id)


@bot.callback_query_handler(func=lambda message: True)
def message_handler(message):
    if message.data == "Подключиться к водомату":
        transition(message.data, message.message.chat.id)
    # elif isdigit(message.data):
    #     menu_list = get_branch_db(message.from_user.id)
    #     if menu_list[-1] == == "Подключиться к водомату":
    #         a = MethodGet("connect/wm")
    #         add_user = {
    #             "telegram": message.from_user.id,
    #             "first_name": message.chat.first_name
    #         }
    #         a.param(**add_user)
    #         result = a.transfer()
    #     else:


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
            bot.send_message(message.from_user.id, result)




# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     del_message_db(message.chat.id)
#     menu_list = get_branch_db(message.from_user.id)
#     send = bot.send_message(message.from_user.id, "Выберите один из пунктов меню", reply_markup=generator_menu(menu_list))
#     add_message_db(message.chat.id, send.message_id)

@bot.callback_query_handler(func=lambda message: True)
def determinant(message):
    if message.data == "Назад":
        go_back(message.data, message.message.chat.id)
    elif message.data:
        transition(message.data, message.message.chat.id)
    else:
        if message.data == "Подключиться к водомату":
            pass



def transition(text, chat_id):
    message_id = get_message_db(chat_id)
    # del_message_db(chat_id)
    add_branches_db(chat_id, text)
    menu_list = get_branch_db(chat_id)
    upt_msgmenu(text, menu_list, message_id, chat_id)

def go_back(text, chat_id):
    message_id = get_message_db(chat_id)
    # del_message_db(chat_id)
    del_branch_db(chat_id)
    menu_list = get_branch_db(chat_id)
    upt_msgmenu(text, menu_list, message_id, chat_id)
    
def distributor():
    pass


def upt_msgmenu(text, menu_list, message_id, chat_id):
    send = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=generator_menu(menu_list))
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
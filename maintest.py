# -*- coding: utf-8 -*-
import telebot
from menu import menu
from db import connect_mysql
from generator_menu import  generator_menu
import requests, json

token = "533495913:AAHG-ssiGLwQMCPVBSDG-WVUA8M3aUYzo-0"

bot = telebot.TeleBot(token)



@bot.callback_query_handler(func=lambda c: True)
def handle_start(c):


@bot.callback_query_handler(func=lambda c: True)
def handle_start(c):
    if menu[c.data]:
        message_id = get_message_db(call.message.chat.id)
        del_message_db(call.message.chat.id)

        # bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        add_branches_db(call.message.chat.id, call.data)
        menu_list = get_branch_db(call.message.chat.id)
        # send = bot.send_message(call.message.chat.id, "Выберите один из пунктов меню", reply_markup=generator_menu(menu_list))

        send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text="Выберите один из пунктов меню",
            parse_mode='Markdown',
            reply_markup=generator_menu(menu_list))
        add_message_db(call.message.chat.id, send.message_id)
    elif c.data == "Назад":
        message_id = get_message_db(call.message.chat.id)
        del_message_db(call.message.chat.id)


        del_branch_db(call.message.chat.id)
        menu_list = get_branch_db(call.message.chat.id)

        
        # bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        # send = bot.send_message(call.message.chat.id, "Выберите один из пунктов меню", reply_markup=generator_menu(menu_list))
        send = bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text="Выберите один из пунктов меню",
            parse_mode='Markdown',
            reply_markup=generator_menu(menu_list))
        add_message_db(call.message.chat.id, send.message_id)
    else:


















@bot.message_handler(commands=['start']) 
def handle_start(message):
    start = {
        "telegram": message.chat.id
    }
    res = adduser(start)
    bot.send_message(message.from_user.id, res)

    # menu_list = get_branch_db(message.from_user.id)
    # send = bot.send_message(message.from_user.id, "Выберите один из пунктов меню", reply_markup=generator_menu(menu_list))
    # add_message_db(message.chat.id, send.message_id)


def adduser(start):
    response = requests.get('http://194.67.217.180:8181/app/add_user/', params=start)
    return response

@bot.callback_query_handler(func=lambda c: True)
def handle_start(c):

    liss = menu.copy()

    for item in menu_list:
        liss = liss[item]
    try:
        
    if liss:
        return True
    else:
        return False






    dtr = determinant(c.data, menu_list)
    if dtr:
        upt_msgmenu("Выберите один из пунктов меню", menu_list, message_id, c.message.chat.id)
    else:
        del_msgmenu(menu_list, message_id, c.message.chat.id)

        send = bot.send_message(message.from_user.id, "Выберите один из пунктов меню", reply_markup=generator_menu(menu_list))
        add_message_db(message.chat.id, send.message_id)

    add_branches_db(c.message.chat.id, c.data)
    message_id = get_message_db(c.message.chat.id)
    del_message_db(c.message.chat.id)
    menu_list = get_branch_db(c.message.chat.id)




def distributor(message):
    pass




def upt_msgmenu(text, menu_list, message_id, chat_id):
    send = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=generator_menu(menu_list))
    add_message_db(chat_id, send.message_id)

def del_msgmenu(text, menu_list, message_id, chat_id):
    bot.delete_message(chat_id=c.message.chat.id, message_id=message_id)


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

import telebot
from menu import menu

def generator_menu(menu_list):
	if menu_list:
		liss = menu.copy()
		for item in menu_list:
			liss = liss[item]
		menu_list = list(liss)
		menu_list.append("Назад")
		user_markup = telebot.types.InlineKeyboardMarkup()
		for item in menu_list:
			item = telebot.types.InlineKeyboardButton(text=item, callback_data=item)
			user_markup.add(item)
		return user_markup
	else:
		liss = list(menu)
		user_markup = telebot.types.InlineKeyboardMarkup()
		for item in liss:
			item = telebot.types.InlineKeyboardButton(text=item, callback_data=item)
			user_markup.add(item)
		return user_markup
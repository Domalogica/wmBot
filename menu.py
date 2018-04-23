import telebot

ID0 = ("Назад")
ID1 = ("Подключиться к водомату")
ID2 = ("Личный кабинет")
ID3 = ("Обратная связь")
ID4 = ("Баланс")
ID5 = ("Адреса водоматов")
ID6 = ("Админ панель")
ID7 = ("Оставить отзыв")
ID8 = ("Рекомендовать место")
ID9 = ("Статистика")
ID10 = ("Текущее состояние")
ID11 = ("Активные водоматы")
ID12 = ("За сутки")
ID13 = ("За неделю")
ID14 = ("Остановить")

menu = {
    "MAIN": [ID1, ID2, ID3],
    ID0: False,
    ID1: [ID0],
    ID2: [ID4, ID5, ID6, ID0],
    ID3: [ID7, ID8, ID0],
    ID4: False,
    ID5: False,
    ID6: [ID9, ID10, ID11, ID0],
    ID7: [ID0],
    ID8: False,
    ID9: [ID12, ID13, ID0],
    ID10: False,
    ID11: False,
    ID12: False,
    ID13: False,
    ID14: False
}


def generator_menu(menu_list):
    print(menu_list)
    if menu_list:
        menu_list = menu[menu_list[-1]]
        print(type(menu_list))
        user_markup = telebot.types.InlineKeyboardMarkup()
        for item in menu_list:
            if item == "Рекомендовать место":
                item = telebot.types.InlineKeyboardButton(text=item, request_location=True)
            else:
                item = telebot.types.InlineKeyboardButton(text=item, callback_data=item)
            user_markup.add(item)
        return user_markup
    else:
        menu_list = menu["MAIN"]
        user_markup = telebot.types.InlineKeyboardMarkup()
        for item in menu_list:
            item = telebot.types.InlineKeyboardButton(text=item, callback_data=item)
            user_markup.add(item)
        return user_markup



def generator_stop():
    user_markup = telebot.types.InlineKeyboardMarkup()
    item = telebot.types.InlineKeyboardButton(text='Остановить', callback_data='Остановить')
    user_markup.add(item)
    return user_markup









    
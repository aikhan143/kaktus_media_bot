import telebot
from decouple import config
from parsing import main

token = config('TOKEN')

bot = telebot.TeleBot(token)

first_keyboard = telebot.types.InlineKeyboardMarkup()
parsing_button = telebot.types.InlineKeyboardButton('Получить новости', callback_data='parsing_news')
first_keyboard.add(parsing_button)

news_nums_keyboard = telebot.types.InlineKeyboardMarkup()
for i in range(1, 21):
    news_nums = telebot.types.InlineKeyboardButton(str(i),callback_data=f'news_{i}')
    news_nums_keyboard.add(news_nums)

desc_photo_keyboard = telebot.types.InlineKeyboardMarkup()
desc = telebot.types.InlineKeyboardButton('Описание', callback_data='desc')
photo = telebot.types.InlineKeyboardButton('Фото', callback_data='photo')
quit = telebot.types.InlineKeyboardButton('Выход', callback_data='quit')
desc_photo_keyboard.add(desc, photo, quit)

all_news = []
index_in_all_news = 0

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Я - бот, который находит новости с Кактус Медиа. Чтобы получить новости нажмите "Получить новости"', reply_markup=first_keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'parsing_news')
def handler_callback_parsing(call):
    global all_news
    all_news = main()
    pars = bot.send_message(call.message.chat.id, 'Новости найдены. Отправьте любое слово, чтобы получить новости.')
    bot.register_next_step_handler(pars, titles)

@bot.message_handler(content_types=['text'])
def titles(message):
    news_in_text = ''
    for num, news in enumerate(all_news, 1):
        news_in_text += f'{num}. {news[0]}\n'
    bot.send_message(message.chat.id, news_in_text)
    
    bot.send_message(message.chat.id, 'Выберите новость, о который хотите узнать подробнее: ', reply_markup=news_nums_keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('news_'))
def handler_callback_news(call):
    try:
        global index_in_all_news
        index_in_all_news = int(call.data.split('_')[1]) - 1

        if 0 <= index_in_all_news < len(all_news):
            news_index = all_news[index_in_all_news]
            bot.send_message(call.message.chat.id, f'Ваша новость: {news_index[0]}. Вы можете посмотреть описание и фото', reply_markup=desc_photo_keyboard)
        else:
            print("Invalid index")

    except Exception as e:
        print(f'Ошибка: {e}')

@bot.callback_query_handler(func=lambda call: call.data == 'desc' or call.data == 'photo' or call.data == 'quit')
def info(call):
    try:
        if all_news and 0 <= index_in_all_news < len(all_news):
            if call.data == 'desc':
                bot.send_message(call.message.chat.id, all_news[index_in_all_news][1])
                bot.send_message(call.message.chat.id, 'Хотите ли Вы посмотреть что-либо еще?', reply_markup=desc_photo_keyboard)
            elif call.data == 'photo':
                bot.send_photo(call.message.chat.id, all_news[index_in_all_news][2])
                bot.send_message(call.message.chat.id, 'Хотите ли Вы посмотреть что-либо еще?', reply_markup=desc_photo_keyboard)
            elif call.data == 'quit':
                bot.send_message(call.message.chat.id, 'До свидания')
        else:
            print("Нет новостей")

    except Exception as e:
        print(f"Ошибка: {e}")

bot.polling()
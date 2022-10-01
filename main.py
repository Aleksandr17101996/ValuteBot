"""
+Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
+При написании бота необходимо использовать библиотеку pytelegrambotapi.
+Человек должен отправить сообщение боту в виде <имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>.
+При вводе команды /start или /help пользователю выводятся инструкции по применению бота.
+При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде.
+Для взятия курса валют необходимо использовать API (https://www.cryptocompare.com/) и отправлять к нему запросы с помощью библиотеки Requests.
+Для парсинга полученных ответов использовать библиотеку JSON.
-При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено число) вызывать собственно написанное исключение APIException с текстом пояснения ошибки.
-Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения.
+Для отправки запросов к API описать класс со статическим методом get_price(), который принимает три аргумента: имя валюты, цену на которую надо узнать, — base, имя валюты, цену в которой надо узнать, — quote, количество переводимой валюты — amount и возвращает нужную сумму в валюте.
+Токен telegramm-бота хранить в специальном конфиге (можно использовать .py файл).
+Все классы спрятать в файле extensions.py.
"""

import telebot
import extensions
from tkn_config import token, list_valute

mybot=telebot.TeleBot(token)
@mybot.message_handler(commands=['start'])
def start_message(message):
  mybot.send_message(message.chat.id,"Привет ✌️\nПришлите запрос для конвертации.\n\n*👍 Пример запроса:*\nUSD RUB 100", parse_mode='Markdown')


@mybot.message_handler(commands=['help'])
def start_message(message):
  mybot.send_message(message.chat.id,"Данный бот предназначен для *конвертации валюты*.\nЗапрос необходимо присылать в следующем виде:\n<имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>\n\n*👍 Пример запроса:*\nUSD RUB 100", parse_mode='Markdown')


@mybot.message_handler(commands=['values'])
def start_message(message):
  mybot.send_message(message.chat.id,"💰 На данный момент между собой можно конвертировать следующие валюты:\n\n🔷*USD* - американский доллар\n🔷*EUR* - евро\n🔷*RUB* - российский рубль\n", parse_mode='Markdown')


@mybot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        list_of_value = message.text.split()
        if len(list_of_value) != 3:
            raise extensions.APIExtension('❌ Введено неверное число аргументов!')
        if list_of_value[0].upper() not in list_valute:
            raise extensions.APIExtension('❌ Конвертация валюты {} невозможна!\nДоступный перечень валют можете узнать при помощи команды /values'.format(list_of_value[0]))
        if list_of_value[1].upper() not in list_valute:
            raise extensions.APIExtension('❌ Конвертация валюты {} невозможна!\nДоступный перечень валют можете узнать при помощи команды /values'.format(list_of_value[1]))
        if not list_of_value[2].isdigit():
            raise extensions.APIExtension('❌ {} не является целым числом!'.format(list_of_value[2]))
        cur_price = extensions.CryptoComp.get_prices(list_of_value[0].upper(), list_of_value[1].upper(), int(list_of_value[2]))
        text_for_msg = 'Для приобретения *' + list_of_value[2] + ' ' + list_of_value[0].upper() + '*\nВам понадобится *' + str(cur_price) + ' ' + list_of_value[1].upper() + '*'
        mybot.send_message(message.chat.id, text=text_for_msg, parse_mode='MarkDown')
        mybot.send_message(message.chat.id, text='Пришлите запрос для конвертации.\n\n*👍 Пример запроса:*\nUSD RUB 100', parse_mode='MarkDown')
    except extensions.APIExtension as ae:
        mybot.send_message(message.chat.id, text=ae, parse_mode='MarkDown')
        mybot.send_message(message.chat.id, text='Пришлите запрос для конвертации.\n\n*👍 Пример запроса:*\nUSD RUB 100', parse_mode='MarkDown')

    


if __name__ == '__main__':
    mybot.infinity_polling()
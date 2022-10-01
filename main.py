
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
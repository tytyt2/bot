import telebot, json, requests
from config import TOKEN
from extensions import CConverter, ConvertionException


bot=telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def function_command(messege: telebot.types.Message):
    text = 'Этот бот может переводить большинство мировых валют и некоторые крипто-монеты' \
           '\n Для начала работы введите комманду боту в следубщем формате:\n<имя валюты(RUB), ' \
           'в какую валюту перевести(USD)>' \
           '<количество переводимой валюты>' \
           '\n Пример: RUB USD 1000 \n Увидеть список всех доступных валют: /values'
    bot.reply_to(messege, text)

@bot.message_handler(commands=['values'])
def value(messege: telebot.types.Message):
    currency_list = requests.get('https://currate.ru/api/?get=currency_list&key=26361c7ae9627554919bec896f67b31e')
    Object = json.loads(currency_list.content)

    text ='Доступные валютные пары:'
    for key in Object['data']:
        text ='\n'.join((text, key))
    bot.reply_to(messege, text)

@bot.message_handler(content_types=['text', ])
def convert(messege: telebot.types.Message):
    try:
        values = messege.text.split(' ')

        if len(values) !=3:
            raise ConvertionException('Слишком много или мало значений.')

        quote, base, amount = values

        count=CConverter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(messege, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(messege, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {count}'
        bot.send_message(messege.chat.id, text)

bot.polling()





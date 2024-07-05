import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Добро пожаловать! Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
        "<имя валюты> <имя валюты для конвертации> <количество>\n"
        "Например: USD EUR 100\n"
        "Доступные команды:\n"
        "/start или /help - показать это сообщение\n"
        "/values - показать доступные валюты"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def send_values(message):
    text = "Доступные валюты:\nUSD, EUR, RUB"
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        base, quote, amount = message.text.split()
        total = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
        bot.reply_to(message, f"Цена {amount} {base.upper()} в {quote.upper()} - {total}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду. Пожалуйста, проверьте правильность ввода.")

if __name__ == '__main__':
    bot.polling()
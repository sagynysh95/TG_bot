from loader import bot
from handlers import handlers


if __name__ == '__main__':
    handlers.TelegramBot()
    bot.polling(none_stop=True)

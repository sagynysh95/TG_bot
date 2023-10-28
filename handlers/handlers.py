from loader import bot, request_search, request_players, request_transfers
from telebot import types


team_id = ''


class TelegramBot:
    def __init__(self):

        @bot.message_handler(commands=['start'])
        def start(message):
            bot.send_message(message.chat.id, 'Приветствую. Напишите какую команду ищем на английском:')
            bot.register_next_step_handler(message, search)

        def search(message):
            response = request_search(message.text)
            data = response.json()
            i = 0
            try:
                while True:
                    id = data['results'][i]['entity']['id']
                    if data['results'][i]['type'] == 'team' and data['results'][i]['entity']['gender'] == 'M':
                        bot.send_message(message.chat.id, '{0}|{1}'.format(data['results'][i]['entity']['name'], id))
                    i += 1
            except (IndexError, KeyError):
                bot.send_message(message.chat.id,
                                 'Это весь список по вашему запросу. '
                                 'Для вывода информации по нужной команды обратитесь по ID этой команды')
                bot.send_message(message.chat.id, 'Если нет нужной команды в списке, введите слово "Назад"')
                bot.register_next_step_handler(message, choose)
            except TypeError:
                bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуйте заново ввести название команды')
                bot.register_next_step_handler(message, search)

        def choose(message):
            try:
                global team_id
                team_id = int(message.text)
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Список игроков', callback_data='team_players'))
                markup.add(types.InlineKeyboardButton('Последние трансферы на вход', callback_data='In'))
                markup.add(types.InlineKeyboardButton('Последние трансферы на выход', callback_data='Out'))
                bot.send_message(message.chat.id, 'Выберите какую информацию хотите вывести', reply_markup=markup)
            except Exception:
                bot.send_message(message.chat.id, 'Введите название команды по другому')
                bot.register_next_step_handler(message, search)

        @bot.callback_query_handler(func=lambda callback: True)
        def callback_message(callback):
            if callback.data == 'team_players':
                response = request_players(str(team_id))
                data = response.json()
                i = 0
                bot.send_message(callback.message.chat.id, "*Имя | Национальность | Игровой номер*", parse_mode='Markdown')
                try:
                    while True:
                        bot.send_message(callback.message.chat.id,
                                         f"{data['players'][i]['player']['name']} | "
                                         f"{data['players'][i]['player']['country']['name']} | "
                                         f"{data['players'][i]['player']['jerseyNumber']}")
                        i += 1
                except (IndexError, KeyError):
                    bot.send_message(callback.message.chat.id, '_Это все игроки в этой команде_', parse_mode='Markdown')
                    bot.send_message(callback.message.chat.id, 'Напишите название команды для нового поиска')
                    bot.register_next_step_handler(callback.message, search)
            elif callback.data == 'In':
                response = request_transfers(str(team_id))
                data = response.json()
                i = 0
                bot.send_message(callback.message.chat.id, "*Имя | Предыдущая команда | Стоимость трансфера*",
                                 parse_mode='Markdown')
                try:
                    while True:
                        if 'transferFee' in data['transfersIn'][i].keys():
                            bot.send_message(callback.message.chat.id, f"{data['transfersIn'][i]['player']['name']} | "
                                                                       f"{data['transfersIn'][i]['fromTeamName']} | "
                                                                       f"{data['transfersIn'][i]['transferFee']:,} €")
                        i += 1
                except IndexError:
                    bot.send_message(callback.message.chat.id, '_Это все трансферы на вход в этой команде_',
                                     parse_mode='Markdown')
                    bot.send_message(callback.message.chat.id, 'Напишите название команды для нового поиска')
                    bot.register_next_step_handler(callback.message, search)
            elif callback.data == 'Out':
                response = request_transfers(str(team_id))
                data = response.json()
                i = 0
                bot.send_message(callback.message.chat.id, "*Имя | Новая команда | Стоимость трансфера*",
                                 parse_mode='Markdown')
                try:
                    while True:
                        bot.send_message(callback.message.chat.id, f"{data['transfersOut'][i]['player']['name']} | "
                                                                   f"{data['transfersOut'][i]['toTeamName']} | "
                                                                   f"{data['transfersOut'][i]['transferFee']:,} €")
                        i += 1
                except (IndexError, KeyError):
                    bot.send_message(callback.message.chat.id, '_Это все трансферы на выход в этой команде_',
                                     parse_mode='Markdown')
                    bot.send_message(callback.message.chat.id, 'Напишите название команды для нового поиска')
                    bot.register_next_step_handler(callback.message, search)
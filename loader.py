import telebot
from config_data import config
import requests


bot = telebot.TeleBot(token=config.BOT_TOKEN)


def request_search(message):
    return requests.get(config.URL+'search/'+message, headers=config.HEADERS)


def request_players(message):
    return requests.get(config.URL+'team/'+message+'/players', headers=config.HEADERS)


def request_transfers(message):
    return requests.get(config.URL+'team/'+message+'/transfers', headers=config.HEADERS)


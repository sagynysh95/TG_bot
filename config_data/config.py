import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
HEADERS = {
    "X-RapidAPI-Key": os.getenv('RAPID_TOKEN'),
    "X-RapidAPI-Host": "footapi7.p.rapidapi.com"
}
URL = os.getenv('URL')

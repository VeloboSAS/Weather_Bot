import pyowm
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
import telebot


config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('Api_key', config_dict)

city = input('Введите название города:')
mgr = owm.weather_manager()

bot = telebot.TeleBot("Your_Token")


@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        wind = w.wind()['speed']
        status = w.detailed_status
        hum = w.humidity
        cloud = w.clouds

        answer = f"В городе {message.text} сейчас {status}\n"
        answer += "Температура сейчас в районе " + str(temp) + "\n"
        answer += 'Скорость ветра: ' + str(wind) + ' м/с' + "\n"
        answer += 'Относительная влажность: ' + str(hum) + ' %' + "\n"
        answer += 'Облачность: ' + str(cloud) + ' %' + "\n\n"

        if temp < -10:
            answer += "Сейчас жестко холодно"
        elif temp < 0:
            answer += "Сейчас холодно, оденься потеплее"
        else:
            answer += "Температура найс, одевайся как хош"

        bot.send_message(message.chat.id, answer)
    except:
        bot.send_message(message.chat.id,'Ошибка! Город не найден.')

bot.polling(none_stop=True)

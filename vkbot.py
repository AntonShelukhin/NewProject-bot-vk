import random
import pyowm
from pyowm import OWM
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

def write_msg(user_id, message):
	vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

# API-ключb созданные ранее
owm = pyowm.OWM('ff6b560049d6c96e62037ce30febce4e', language='ru')
token = "1fa4b605de1af0c135cb60af293ed0f34f35dc9ab950ac4f452c1cb2c8994d6d88ae105db5b8bc2b9e21f"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Бот запущен")
# Основной цикл
while True:
	for event in longpoll.listen():
    # Если пришло новое сообщение
		if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня (то есть бота)
			if event.to_me:
            # Сообщение от пользователя
				request = event.text
				# Исключение для ошибок
				try:	
					# Запрос погоды	
					observation = owm.weather_at_place(event.text)
					w = observation.get_weather()
					temp = w.get_temperature('celsius')["temp"]
					
					answer = 'В городе ' + event.text + ' сейчас ' + w.get_detailed_status() + '.' + '\n'
					answer += 'Температура в районе ' + str(temp) + '.' + '\n\n'

					if temp < 10:
						answer += 'Сейчас холодно! Ты что, хочешь маму расстроить?'
					elif temp < 20:
						answer += 'Погода более менее, можешь одевать кросы!'
					else:
						answer += 'Наслаждаемся летом!'

		            # Каменная логика ответа
					if request == event.text:
						write_msg(event.user_id, answer)

				except Exception:
					write_msg(event.user_id, 'Введите корректное название города.')
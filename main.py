import random
import pyowm
from pyowm import OWM
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

def write_msg(user_id, message):
	vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

# API-keys
owm = pyowm.OWM('OWM Token...', language='ru')
token = "VK group Token..."

# Authorization as a community
vk = vk_api.VkApi(token=token)

# Messaging
longpoll = VkLongPoll(vk)

# Main cycle
while True:
	for event in longpoll.listen():
    		# If a new message arrives
		if event.type == VkEventType.MESSAGE_NEW:
        		# If it has a label for me (i.e. bot)
			if event.to_me:
            			# Message from user
				request = event.text
				# Error exception
				try:	
					# Weather request
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

					# Response logic
					if request == event.text:
						write_msg(event.user_id, answer)

				except Exception:
					write_msg(event.user_id, 'Введите корректное название города.')

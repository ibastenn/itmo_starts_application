from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnProfile = KeyboardButton('Личный кабинет')

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
mainMenu.add(btnProfile)
#
btnEvent = KeyboardButton('Мероприятия')
#btnSetProfile = KeyboardButton('Редактировать личную информацию')

mainLK = ReplyKeyboardMarkup(resize_keyboard = True)
mainLK.add(btnEvent)
#mainLK.add(btnSetProfile)
#
btnCreateEvent = KeyboardButton('Создать мероприятие')
btnChoouse = KeyboardButton('Отбор на активные мероприятия')
btnCNback = KeyboardButton('Вернуться в личный кабинет')

mainEvent = ReplyKeyboardMarkup(resize_keyboard = True)
mainEvent.add(btnCreateEvent)
mainEvent.add(btnChoouse)
mainEvent.add(btnCNback)
#
btnSendEventback = KeyboardButton('Вернуться к мероприятиям')

mainSendEvent = ReplyKeyboardMarkup(resize_keyboard = True)
mainSendEvent.add(btnSendEventback)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnProfile = KeyboardButton('Личный кабинет волонтера')

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
mainMenu.add(btnProfile)
#
btnActiveEvent = KeyboardButton('Активные мероприятия')
btnPersonProfile = KeyboardButton('Мой профиль')

mainLK = ReplyKeyboardMarkup(resize_keyboard = True)
mainLK.add(btnActiveEvent)
mainLK.add(btnPersonProfile)
#
btnBacktoLK = KeyboardButton('Вернуться назад')
btnSetProfile = KeyboardButton('Редактировать личную информацию')

mainMyProfile = ReplyKeyboardMarkup(resize_keyboard = True)
mainMyProfile.add(btnSetProfile)
mainMyProfile.add(btnBacktoLK)
#
btnEditName = KeyboardButton('Фамилия, имя, отчество')
btnEditAge = KeyboardButton('Возраст')
btnEditMail = KeyboardButton('Почта')
btnEditVK = KeyboardButton('ВКонтакте')
btnEditTG = KeyboardButton('Телеграм')
btnEditBack = KeyboardButton('Завершить редактирование')

mainEditProfile = ReplyKeyboardMarkup(resize_keyboard = True)
mainEditProfile.add(btnEditName)
mainEditProfile.add(btnEditAge)
mainEditProfile.add(btnEditMail)
mainEditProfile.add(btnEditVK)
mainEditProfile.add(btnEditTG)
mainEditProfile.add(btnEditBack)
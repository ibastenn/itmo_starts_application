import telebot
import time
import logging
from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
import markups as vol
import adm_mark as adm
from db import DB
from admincase import adminkeys
from db_admins import DBA
from db_event import DBE
from db_vol import DBV
from choose import Choose

TOKEN = 
bot = Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)
db = DB('users.db')
dba = DBA('users.db')
dbe = DBE('users.db')
dbv = DBV('users.db')
chs = Choose('users.db')

status = ['creator', 'administrator', 'member', 'owner']
event_statuses = ['setcreate', 'setlimit', 'setbasic', 'setreversed', 'setminage']
profile_statuses = ['setname', 'setage', 'setemail', 'setvk']
profile_edit_statuses = ['editprofile', 'editname', 'editage', 'editmail', 'editvk', 'edittg']


# регистрация пользователя
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        member = await bot.get_chat_member(chat_id='@testchanelvl', user_id=message.from_user.id)
        print(member)
        if isinstance(member, types.ChatMember):
            if member.status in status:
                db.add_user(message.from_user.id)
                print(message.from_user)
                for keys in adminkeys:
                    if message.from_user.id == keys:
                        if dba.get_admin(message.from_user.id) is None:
                            dba.add_admin(message.from_user.id)
                        await bot.send_message(message.from_user.id,
                                               'Добро пожаловать, ' + message.from_user.first_name + '!',
                                               reply_markup=adm.mainMenu)
                        db.set_signup(message.from_user.id, 'done')
                        break
                else:
                    await bot.send_message(message.from_user.id, 'Приветствую! 👋 \nЯ - бот, который помогает волонтерам в огранизации их деятельности :). \nЧтобы в дальнейшем принимать участие в мероприятиях, Вам необходимо пройти предварительную регистрацию. Это нужно сделать 1 раз, чтобы после подавать заявки на участие было гораздо проще! ☺️\nПожалуйста, укажите Ваши фамилию, имя и отчество: ')
            else:
                await bot.send_message(message.from_user.id, 'Извините, проверка на идентификацию не пройдена. Если вы считаете, что произошла ошибка, обратитесь к @hellteenz')


    else:
        for keys in adminkeys:
            if message.from_user.id == keys:
                await bot.send_message(message.from_user.id, 'Вы уже зарегистрированны!', reply_markup=adm.mainMenu)
                break
        else:
            await bot.send_message(message.from_user.id, 'Вы уже зарегистрированны!', reply_markup=vol.mainMenu)


#рассылка сообщений
@dp.message_handler(commands=['new'])
async def newpost(message: types.Message):
    text_of_new_event = message.text[5:]
    user_id = message.from_user.id
    dba.set_full_text_of_new_event(user_id, text_of_new_event)
    volunteers = db.get_mess_for_vol()
    for vol in volunteers:
        try:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Подать заявку", callback_data="supply"))
            await bot.send_message(vol[0], text_of_new_event, reply_markup=keyboard)
            await bot.send_message(vol[0], 'Помните, если Вы не можете подать заявку - это может быть связано с возрастными ограничениями или с временем подачи заявки. Будьте внимательны!')
            if int(vol[1]) != 1:
                db.set_active(vol[0], 1)
        except:
            db.set_active(vol[0], 0)
    dba.set_active_done(user_id)
    await bot.send_message(user_id, 'Успешная рассылка', reply_markup=adm.mainEvent)


# кнопка к посту
@dp.callback_query_handler(text="supply")
async def send_a_supply(call: types.CallbackQuery):
    user_id = call.from_user.id
    event_name = call.values.get('message').text
    if dbe.get_supply(user_id, event_name) is None:
        timepress = round(time.time() * 1000)
        try:
            user_age = dbe.get_supply_userage(user_id)
            if user_age is None:
                await call.answer(text="Не указан Ваш возраст! Пожалуйста, отредактируйте свой профиль.", show_alert=True)
            else:
                if (user_age >= dbe.get_minage(event_name)) and (timepress <= dbe.get_end_times(event_name)):
                    dbe.create_supply(user_id,
                                      event_name,
                                      dbe.get_supply_username(user_id),
                                      dbe.get_supply_userage(user_id),
                                      dbe.get_supply_usermail(user_id),
                                      dbe.get_supply_uservk(user_id),
                                      dbe.get_supply_usertg(user_id),
                                      round(time.time() * 1000))
                    await call.answer(text="Ваша заявка успешно подана!", show_alert=True)
        except:
            await call.answer(text="Извините, что-то пошло не так!", show_alert=True)
    else:
        await call.answer(text="Вы уже подали заявку!", show_alert=True)


def clean_previous_actions(id):
    dba.clean_empty_events(id)
    dba.delete_all_active(id)
    db.set_signup(id, 'done')


# обработка сообщений
@dp.message_handler()
async def bot_message(message: types.Message):
    ak = [keys for keys in adminkeys]
    if message.chat.type == 'private':
        if message.text == 'Личный кабинет':
            clean_previous_actions(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Функции личного кабинета ☀️', reply_markup=adm.mainLK)

        elif message.text == 'Мероприятия':
            clean_previous_actions(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Управление мероприятиями 🕹', reply_markup=adm.mainEvent)

        elif message.text == 'Создать мероприятие':
            if message.text == 'Создать мероприятие':
                clean_previous_actions(message.from_user.id)
            if dba.get_signup(message.from_user.id) == '':
                dba.add_admin_to_events(message.from_user.id)
                tconv = round(time.time() * 1000)
                dba.set_PostTime(message.from_user.id, tconv)
                await bot.send_message(message.from_user.id, 'Пожалуйста, введите краткое название мероприятия: ')

        elif message.text == 'Личный кабинет волонтера':
            clean_previous_actions(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Функции личного кабинета 🌏', reply_markup=vol.mainLK)

        elif message.text == 'Мой профиль':
            clean_previous_actions(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Ваши данные', reply_markup=vol.mainMyProfile)
            await bot.send_message(message.from_user.id, 'ФИО: ' + dbv.select_user_name(message.from_user.id)
                                   + '\nВозраст: ' + str(dbv.select_user_age(message.from_user.id))
                                   + '\nПочта: ' + dbv.select_user_mail(message.from_user.id)
                                   + '\nВКонтакте: ' + dbv.select_user_vk(message.from_user.id)
                                   + '\nТелеграм: @' + dbv.select_user_tg(message.from_user.id))

        elif message.text == 'Редактировать личную информацию':
            clean_previous_actions(message.from_user.id)
            dbv.set_edit_signup(message.from_user.id, 'editprofile')
            await bot.send_message(message.from_user.id, 'Выберите позицию, которую Вы хотите отредактировать. \nЕсли изменения внесены, выберите кнопку "Завершить редактирование"', reply_markup=vol.mainEditProfile)

        elif message.text == 'Активные мероприятия':
            await bot.send_message(message.from_user.id,
                                   'Мероприятия, на участие в которых Вы подали заявку: ')
            a = dbv.active_events(message.from_user.id)
            for ev in a:
                await bot.send_message(message.from_user.id, ev[0])
            await bot.send_message(message.from_user.id, 'Организаторы скоро уведомят Вас по почте или через мессенджеры, ожидайте', reply_markup=vol.mainLK)

        elif message.text == 'Отбор на активные мероприятия':
            await bot.send_message(message.from_user.id, 'Мероприятия:')
            b = chs.get_all_events(message.from_user.id)
            for ot in b:
                await bot.send_message(message.from_user.id, ot[0])

                base_volunteers_list = chs.get_base_volunteers(ot[0], ot[1])
                if base_volunteers_list is not None and len(base_volunteers_list) > 0:
                    await bot.send_message(message.from_user.id, '    Волонтеры в основе:')
                    for volunteer in base_volunteers_list:
                        if isinstance(volunteer, tuple):
                            strvolunteer = ''
                            for element in volunteer:
                                strvolunteer += str(element)
                                strvolunteer += ', '
                            await bot.send_message(message.from_user.id, strvolunteer[:-2])

                reserve_volunteers_list = chs.get_reserve_volunteers(ot[0], ot[1])
                if reserve_volunteers_list is not None and len(reserve_volunteers_list) > 0:
                    await bot.send_message(message.from_user.id, '    Волонтеры в резерве:')
                    for volunteer in reserve_volunteers_list:
                        if isinstance(volunteer, tuple):
                            strvolunteerR = ''
                            for element in volunteer:
                                strvolunteerR += str(element)
                                strvolunteerR += ', '
                            await bot.send_message(message.from_user.id, strvolunteerR[:-2])

                await bot.send_message(message.from_user.id, 'Следующее мероприятие \n🔽')

        elif message.text == 'Вернуться назад':
            clean_previous_actions(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Функции личного кабинета 🌏', reply_markup=vol.mainLK)
        elif message.text == 'Вернуться в личный кабинет':
            clean_previous_actions(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Функции личного кабинета ☀️', reply_markup=adm.mainLK)
        elif message.text == 'Вернуться к мероприятиям':
            clean_previous_actions(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Управление мероприятиями 🕹', reply_markup=adm.mainEvent)

        elif dba.get_signup(message.from_user.id) in event_statuses and (message.from_user.id in ak):
            signup = dba.get_signup(message.from_user.id)
            if signup == 'setcreate':
                dba.set_shortname(message.from_user.id, message.text)
                dba.set_signup(message.from_user.id, 'setlimit')
                await bot.send_message(message.from_user.id,
                                       'Укажите сколько по времени будет длиться набор в формате D.H.M.C')

            elif signup == 'setlimit':
                dba.set_limit(message.from_user.id, message.text)
                dba.ending_time(message.from_user.id)
                dba.set_signup(message.from_user.id, 'setbasic')
                await bot.send_message(message.from_user.id, 'Укажите сколько волонтеров набираются в основной состав')

            elif signup == 'setbasic':
                dba.set_basic(message.from_user.id, message.text)
                dba.set_signup(message.from_user.id, 'setreversed')
                await bot.send_message(message.from_user.id, 'Укажите сколько волонтеров набираются в резервный состав')

            elif signup == 'setreversed':
                dba.set_reversed(message.from_user.id, message.text)
                dba.set_signup(message.from_user.id, 'setminage')
                await bot.send_message(message.from_user.id, 'Укажите минимальный возраст волонтера')

            elif signup == 'setminage':
                dba.set_min_age(message.from_user.id, message.text)
                dba.set_signup(message.from_user.id, 'done')
                await bot.send_message(message.from_user.id, 'Введите информацию по мероприятию через /new',
                                       reply_markup=adm.mainSendEvent)

        elif db.get_signup(message.from_user.id) in profile_edit_statuses:
            signup = dbv.get_edit_signup(message.from_user.id)
            if message.text == 'Фамилия, имя, отчество':
                dbv.set_edit_signup(message.from_user.id, 'editname')
                await bot.send_message(message.from_user.id, 'Введите актуальную информацию для поля "Фамилия, имя, отчество"',
                                       reply_markup=vol.mainEditProfile)

            elif signup == 'editname':
                dbv.edit_user_name(message.from_user.id, message.text)
                dbv.set_edit_signup(message.from_user.id, 'editprofile')
                await bot.send_message(message.from_user.id, 'Поле "Фамилия, имя, отчество" обновлено', reply_markup=vol.mainEditProfile)

            elif message.text == 'Возраст':
                dbv.set_edit_signup(message.from_user.id, 'editage')
                await bot.send_message(message.from_user.id, 'Введите актуальную информацию для поля "Возраст"',
                                       reply_markup=vol.mainEditProfile)
            elif signup == 'editage':
                dbv.edit_user_age(message.from_user.id, message.text)
                dbv.set_edit_signup(message.from_user.id, 'editprofile')
                await bot.send_message(message.from_user.id, 'Поле "Возраст" обновлено', reply_markup=vol.mainEditProfile)

            elif message.text == 'Почта':
                dbv.set_edit_signup(message.from_user.id, 'editmail')
                await bot.send_message(message.from_user.id, 'Введите актуальную информацию для поля "Почта"',
                                       reply_markup=vol.mainEditProfile)
            elif signup == 'editmail':
                dbv.edit_user_email(message.from_user.id, message.text)
                dbv.set_edit_signup(message.from_user.id, 'editprofile')
                await bot.send_message(message.from_user.id, 'Поле "Почта" обновлено', reply_markup=vol.mainEditProfile)

            elif message.text == 'ВКонтакте':
                dbv.set_edit_signup(message.from_user.id, 'editvk')
                await bot.send_message(message.from_user.id, 'Введите актуальную информацию для поля "ВКонтакте". ' +
                                       '\nНе забывайте, что данное поле подразумевает под собой ссылку на страницу в социальной сети',
                                       reply_markup=vol.mainEditProfile)
            elif signup == 'editvk':
                dbv.edit_user_vk(message.from_user.id, message.text)
                dbv.set_edit_signup(message.from_user.id, 'editprofile')
                await bot.send_message(message.from_user.id, 'Поле "ВКонтакте" обновлено', reply_markup=vol.mainEditProfile)

            elif message.text == 'Телеграм':
                dbv.set_edit_signup(message.from_user.id, 'edittg')
                dbv.edit_user_tg(message.from_user.id, message.from_user.username)
                dbv.set_edit_signup(message.from_user.id, 'editprofile')
                await bot.send_message(message.from_user.id, 'Данное поле обновлено автоматически, спасибо',
                                       reply_markup=vol.mainEditProfile)

            elif message.text == 'Завершить редактирование':
                dbv.set_edit_signup(message.from_user.id, 'done')
                await bot.send_message(message.from_user.id, 'Изменения успешно внесены! \nВаши актуальные данные:',
                                       reply_markup=vol.mainMyProfile)
                await bot.send_message(message.from_user.id, 'ФИО: ' + dbv.select_user_name(message.from_user.id)
                                       + '\nВозраст: ' + str(dbv.select_user_age(message.from_user.id))
                                       + '\nПочта: ' + dbv.select_user_mail(message.from_user.id)
                                       + '\nВКонтакте: ' + dbv.select_user_vk(message.from_user.id)
                                       + '\nТелеграм: @' + dbv.select_user_tg(message.from_user.id))

        elif db.get_signup(message.from_user.id) in profile_statuses and message.from_user.id not in ak:
            signup = db.get_signup(message.from_user.id)
            if signup == 'setname':
                db.set_user_name(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, 'setage')
                await bot.send_message(message.from_user.id, 'Укажите Ваш полный возраст')

            elif signup == 'setage':
                db.set_user_age(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, 'setemail')
                await bot.send_message(message.from_user.id, 'Укажите Вашу почту')

            elif signup == 'setemail':
                db.set_user_email(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, 'setvk')
                await bot.send_message(message.from_user.id, 'Укажите ссылку на ваш ВК')

            elif signup == 'setvk':
                db.set_user_vk(message.from_user.id, message.text)
                db.set_user_tg(message.from_user.id, message.from_user.username)
                db.set_signup(message.from_user.id, 'done')
                await bot.send_message(message.from_user.id, 'Регистрация успешно завершена', reply_markup=vol.mainMenu)

        else:
            clean_previous_actions(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Произошла ошибка')

# Запускаем бота, чтобы работал 24/7
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import datetime

import database as db
from classs import Sessions


bot = Bot('5889581464:AAFBzA97vPaDKVA0z42uKdd86z_lYI6wh7k')

dp = Dispatcher(bot,storage=MemoryStorage())

user = {'goal': 0,'username': ''}
sessions_bot = {'why': ''}

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
  username = str(m.from_user.id)
  
  if username not in [x.id_user for x in db.session.query(db.User.id_user).distinct()]:
    ln = m.from_user.language_code
    co = 0
    cr = str(datetime.datetime.now())

    user['username'] = username
    
    users = db.User(language=ln,count_offers=co,created=cr,id_user=username)
    db.session.add(users)
    db.session.commit()
    db.session.close()

  user['username'] = username
  bilder = ReplyKeyboardMarkup(resize_keyboard=True)
  bilder.add(types.KeyboardButton(text='Предложение'))
  
  await m.reply('Добро пожаловать в бота для Предложений.\nЧтобы продолжить нажмите кнопку "Предложение"',reply_markup=bilder)

@dp.message_handler(text='Предложение',state=None)
async def pred(m: types.Message):
  await m.reply('Напишите Ваше предложение')
  await Sessions.why.set()

@dp.message_handler(state=Sessions.why)
async def pred_2(m: types.Message,state: FSMContext):
  sessions_bot['why'] = m.text
  user['goal'] = [i.count_offers for i in db.session.query(db.User).filter(db.User.id_user == user['username'])][0]
  user['goal'] += 1
  db.User.update_count_offers(user['username'],user['goal'])
  await m.reply('Ваше предложение отправлено')
  await bot.send_message(-819572767,
                         f'Новое предложение от пользователя {m.from_user.username}:\n{sessions_bot["why"]}')
  await state.finish()

@dp.message_handler(commands=['admin'])
async def admin(m: types.Message):
  if m.chat.id == -819572767:
    bilder = ReplyKeyboardMarkup(resize_keyboard=True)
    bilder.add(types.KeyboardButton(text='/stat'))
  
    await m.reply('Админ панель вкл.',reply_markup=bilder)

@dp.message_handler(commands=['stat'])
async def admin_stat(m: types.Message):
  if m.chat.id == -819572767:
    id = [x.id for x in db.session.query(db.User.id).distinct()]
    count_offers = [x.count_offers for x in db.session.query(db.User.count_offers).distinct()]
    
    await bot.send_message(-819572767,f'общие кол. всех пользователей {len(id)}\nобщая сумма всех счетчиков {sum(count_offers)}')

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)

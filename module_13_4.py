from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


"""
Задание выполнялось на:
Phiton 3.9
aiogram 2.25
"""

user_token = input('Введите ваш токен: ')
bot = Bot(token=user_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    genders = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["help"])
async def greeting(message):
    text = ('Домашнее задание по теме "Машина состояний".'
            '\nЦель: получить навык работы с состояниями в телеграм-боте.'
            '\nЗадача "Цепочка вопросов":'
            '\nСтудент Крылов Эдуард Васильевич.'
            '\nДата работы над заданием: 17.10.2024г.')
    await message.answer(text)


@dp.message_handler(text="Calories")
async def set_genders(message):
    await message.answer('Введите ваш пол " М ", "Ж":')
    await UserState.genders.set()


@dp.message_handler(state=UserState.genders)
async def set_age(message, state):
    keyw = types.ReplyKeyboardRemove()
    await state.update_data(genders=message.text)
    counting = await state.get_data()
    list_gender = str(counting['genders'])
    if list_gender == 'Мужской':
        await state.update_data(genders=float(5))
    elif list_gender == 'Женский':
        await state.update_data(genders=float(-161))
    else:
        await state.update_data(genders=float(5))
    await message.answer('Введите ваш возраст, лет', reply_markup=keyw)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост, см.')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес, кг.')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    counting = await state.get_data()
    list_gender = float(counting['genders'])
    rep_weight = str(counting['weight']).replace(",", ".")
    set_weights = float(rep_weight)
    rep_growth = str(counting['growth']).replace(",", ".")
    set_growths = float(rep_growth)
    rep_age = str(counting['age']).replace(",", ".")
    set_ages = float(rep_age)
    calories = float(10 * set_weights + 6.25 * set_growths - 5 * set_ages + list_gender)
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start_message(messeage):
    await messeage.answer('Привет! Я бот помогающий твоему здоровью, напишите "Calories", для расчета.')


@dp.message_handler()
async def all_message(message):
    await message.answer('module_13_4: упрощенная формула\nНажмите кнопку "/start", или "/help" чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

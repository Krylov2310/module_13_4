from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


user_token = input('Введите ваш токен: ')
bot = Bot(token=user_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    genders = State()
    age = State()
    growth = State()
    weight = State()
    actives = State()


@dp.message_handler(commands=["help"])
async def greeting(message):
    text = ('Домашнее задание по теме "Машина состояний".'
            '\nЦель: получить навык работы с состояниями в телеграм-боте.'
            '\nЗадача "Цепочка вопросов":'
            '\nРасширенная формула'
            '\nСтудент Крылов Эдуард Васильевич.'
            '\nДата работы над заданием: 17.10.2024г.')
    await message.answer(text)


@dp.message_handler(text="Calories")
async def set_genders(message):
    await message.answer('Введите ваш пол " М ", " Ж "')
    await UserState.genders.set()


@dp.message_handler(state=UserState.genders)
async def set_age(message, state):
    await state.update_data(genders=message.text)
    counting = await state.get_data()
    list_gender = str(counting['genders'])
    if list_gender == 'М' or list_gender == 'м' or list_gender == 'M' or list_gender == 'm':
        await state.update_data(genders=float(5))
    elif list_gender == 'Ж' or list_gender == 'ж' or list_gender == 'W' or list_gender == 'w':
        await state.update_data(genders=float(-161))
    else:
        await state.update_data(genders=float(5))
    await message.answer('Введите ваш возраст, лет')
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
    print()


@dp.message_handler(state=UserState.weight)
async def set_activ(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите одну из степеней вашей активности:'
                         '\n\n1 - минимальная активность, сидячая работа, не требующая '
                         'значительных физических нагрузок;'
                         '\n\n2 – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза '
                         'в неделю.Это может быть езда на велосипеде, бег трусцой, баскетбол, плавание, катание '
                         'на коньках и т. д. Если вы не тренируетесь регулярно, но сохраняете занятый стиль жизни, '
                         'который требует частой ходьбы в течение длительного времени, то выберите этот коэффициент;'
                         '\n\n3 – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин '
                         'три-четыре раза в неделю (любой из перечисленных выше видов спорта);'
                         '\n\n4 – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом '
                         ' работы (кирпичная кладка, столярное дело и т. д.), занятость в сельском хозяйстве и т. п.;'
                         '\n\n5 – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные '
                         'виды деятельности: занятия спортом с почти ежедневным графиком и несколькими тренировками '
                         'в течение дня; очень трудоемкая работа, например, сгребание угля или длительный рабочий день '
                         'на сборочной линии. Зачастую этого уровня активности очень трудно достичь.')
    await UserState.actives.set()


@dp.message_handler(state=UserState.actives)
async def set_calories(message, state):
    await state.update_data(actives=message.text)
    counting = await state.get_data()
    list_active = str(counting['actives'])
    rep_weight = str(counting['weight']).replace(",", ".")
    set_weights = float(rep_weight)
    rep_growth = str(counting['growth']).replace(",", ".")
    set_growths = float(rep_growth)
    rep_age = str(counting['age']).replace(",", ".")
    set_ages = float(rep_age)
    list_gender = float(counting['genders'])
    if list_active == '1':
        set_actives = float(1.2)
    elif list_active == '2':
        set_actives = float(1.375)
    elif list_active == 3:
        set_actives = float(1.55)
    elif list_active == '4':
        set_actives = float(1.7)
    elif list_active == '5':
        set_actives = float(1.9)
    else:
        set_actives = float(1.55)
    calories = float((10 * set_weights + 6.25 * set_growths - 5 * set_ages + list_gender) * set_actives)
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start_message(messeage):
    await messeage.answer('Привет! Я бот помогающий твоему здоровью, наберите "Calories" для подсчета калорий')


@dp.message_handler()
async def all_message(message):
    await message.answer('module_13_4_1: полная формула\nВведите команду /start, или /help чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

from typing_extensions import ParamSpec
import aioschedule as schedule
import time
import config
import logging
import main
import bs4 as bs
import urllib.request

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['fractions'])
async def show(message: types.Message):
    args = message.text[11:]
    if len(args) <= 0:
        answer = "Фракции: \n"
        for fraction in set(parlament.fractions):
            answer += f'{fraction}\n'
        await message.answer(answer)
    else:
        if args == "СДПК":
            frac = ("Парламентская фракция " + args)
        else:
            frac = ("Парламентская фракция «" + args + "»")

        if (frac) not in set(parlament.fractions):
            await message.answer(f'Нету фракции с названием: {args}')
        else:
            answer = f'Депутаты относящиеся к фракции {args}: \n'
            for deputy in parlament.deputies:
                if args in deputy.fraction:
                    answer += (deputy.name + f'\n {deputy.deputyLink} \n')
            await message.answer(answer)


@dp.message_handler(commands=['deputy'])
async def show(message: types.Message):
    args = message.text[8:]
    if args not in set(parlament.names):
        await message.answer(f'Нету депутата с именем: {args}')
    else:
        answer = ""
        for deputy in parlament.deputies:
            if deputy.name == args:
                url = deputy.deputyLink
                source = urllib.request.urlopen(url)
                soup = bs.BeautifulSoup(source, 'html.parser')
                biographySoup = soup.find("div", {"id": "biography"})
                ps = biographySoup.findAll(
                    "p", {"style": "text-align:justify"})
                for p in ps:
                    answer += p.text + "\n"

        await message.answer(answer)


@dp.message_handler(commands=['deputies'])
async def show(message: types.Message):
    answer = "Депутаты: \n"
    for name in set(parlament.names):
        answer += f'{name}\n'
    await message.answer(answer)


@ dp.message_handler(commands=['help'])
async def show(message: types.Message):

    help_text = '''
/fractions - для получения списка фракций
/deputies - для получения списка депутатов
/fractions {Название Фракции} - для вывода участников фракций. 
Пример: /fractions Ата Мекен
/deputy {ФИО} - для получения информации о депутате.
Пример: /deputy Абдылдаев Шералы Итибаевич
/update - Чтобы обновить базу данных о депутатах.
'''

    await message.answer(help_text)


@ dp.message_handler(commands=['update'])
async def show(message: types.Message):
    global parlament
    parlament = main.Parlament(main.fetchDeputies())
    await message.answer("База данных успешно обновлена.")

if __name__ == '__main__':
    parlament = main.Parlament(main.fetchDeputies())
    executor.start_polling(dp, skip_updates=True)

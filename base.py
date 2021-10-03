import logging
import config as cfg
from parser_classes import RbcParse, RiaParse

from aiogram import Bot, Dispatcher, executor, types

# log level
logging.basicConfig(level=logging.INFO)

# Bot initialisation
bot = Bot(token=cfg.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_msg(message: types.Message):
    await message.answer("Hey, what news are you looking for? Choose a resource)")


@dp.message_handler(commands='rbk')
async def get_rbk(message: types.Message):
    await message.answer("What is your key word?")

    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def get_rbk_news(message: types.Message):
        k_word = message.text

        rbc = RbcParse(k_word=k_word).rbc_parse()
        if isinstance(rbc, dict):
            for title in rbc:
                await message.answer(f'{title}. \n --> Read more: {rbc[title]}')

        elif isinstance(rbc, str):
            await message.answer(rbc)


@dp.message_handler(commands='ria')
async def get_ria(message: types.Message):
    await message.answer("What is your key word?")

    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def get_ria_news(message: types.Message):
        k_word = message.text

        ria = RiaParse(k_word=k_word).ria_parse()
        if isinstance(ria, dict):
            for title in ria:
                await message.answer(f'{title}. \n --> Read more: {ria[title]}')

        elif isinstance(ria, str):
            await message.answer(ria)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

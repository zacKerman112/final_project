import os
import sys
import django
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from configuration.models import Item, Category

BOT_TOKEN = '8814381174:AAEPdfe5rBPlZsDJCBhUO40xbzdsJ9Uly4k'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

COMMANDS_TEXT = (
    'Available commands:\n\n'
    '/start - start the bot\n\n'
    '/items - show all items and deeper information about them\n\n'
    '/help - show available commands\n\n'
    '/become_a_part_of_the_team - become a part of the team'
)


@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer(COMMANDS_TEXT)


@dp.message(Command('become_a_part_of_the_team'))
async def become_a_part_of_the_team(message: types.Message):
    await message.answer(
        'To become a part of the team, please contact us at @shopbox_team'
    )


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        'Welcome to ShopBox! Use /help command to see avaliable commands\n'
    )


@sync_to_async
def get_all_items():
    return list(Item.objects.all())


@dp.message(Command('items'))
async def show_items(message: types.Message):
    items = await get_all_items()
    if not items:
        await message.answer('Our shop is empty at the moment')
        return
    
    response_text = '===== Our current items =====: \n\n'
    for item in items:
        response_text += f'{item.name}\n'
        response_text += f'{item.description}\n'
        response_text += f'Price: UAH {item.price}\n'
        response_text += '-'*15+'\n'
    await message.answer(response_text, parse_mode='Markdown')    


@dp.message()
async def unknown_message(message: types.Message):
    await message.answer(
        'I do not understand this command yet.\n\n'
        f'{COMMANDS_TEXT}'
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    print('Bot is starting...')
    print(f'Loaded bot file: {__file__}')
    await dp.start_polling(bot)
    

if __name__=='__main__':
    asyncio.run(main())
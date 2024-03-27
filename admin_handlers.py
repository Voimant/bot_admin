import asyncio
from asyncio import sleep

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher, Router, F
from aiogram.types import ContentType
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.types import FSInputFile, BufferedInputFile

from DB import conn
from func_db import invite_user, you_invite, db_update_invate, db_select_users, db_add_group, db_group_invites, \
    db_group_inv_update

router = Router()


@router.message(Command('add_group'))
async def get_add_group(mess: Message):
    if mess.from_user.id in [423947942, 5805441535]:
        print(mess.from_user.id)
        group_id = mess.chat.id
        db_add_group(str(group_id))
    else:
        await mess.delete()


@router.message(Command('add'))
async def get_add(mess: Message, command: CommandObject):
    if mess.from_user.id in [423947942, 5805441535]:
        group_id = mess.chat.id
        result = int(command.args)
        db_group_inv_update(group_id, result)
        await asyncio.sleep(5)
        await mess.delete()
        print(group_id)
        print(result)
    else:
        await mess.delete()

# @router.message(Command('edit'))
# async def bot_settings(mess: Message):
#     if mess.chat.type == 'private':
#         await mess.answer('да этот чат приватный')
#     else:
#         await mess.delete()
#         new_msg = await mess.answer('команда только для администратора')
#         await asyncio.sleep(10)
#         await new_msg.delete()


@router.message(F.content_type == types.ContentType.NEW_CHAT_MEMBERS)
async def new_members(mess: Message):
    print(mess.from_user.id)
    my_db = db_select_users()
    if str(mess.from_user.id) in my_db:
        pass
    else:
        inv = 0
        invite_user(mess.from_user.id, inv)
    for user in mess.new_chat_members:
        inviter = None
        if user.id:
            inviter = user.id
        elif user.sender_chat:
            inviter = user.sender_chat.user.id
        print(f"Пользователь {user.full_name} был приглашен {inviter}\n"
              f"Пригласивший: {mess.from_user.id}\n")
        inv = 0
        invite_user(inviter, inv)
        db_update_invate(mess.from_user.id)
        conn.commit()


@router.message()
async def members(mess: Message):
    """Функция не пропускает текстовое сообщения пока не будет 10 приглашенных участников"""
    if int(mess.chat.id) < 0:
        user_id = mess.from_user.id
        group_id = mess.chat.id
        threshold = db_group_invites(str(group_id))
        invites = you_invite(user_id)
        print(threshold[0])
        print(mess.from_user.id)
        for inv in invites:
            print(inv)
            if inv < threshold[0] and int(mess.from_user.id) not in [423947942, 5805441535]:
                await mess.delete()
                button_1 = [[InlineKeyboardButton(text='Опубликовать объявления', url='https://t.me/OMKS312_bot')]]
                markup = InlineKeyboardMarkup(inline_keyboard=button_1)
                new_msg = await mess.answer(f'{mess.from_user.username} Пожалуйста добавьте {str(threshold[0])} пользователей,'
                                            f' после этого сможете публиковать объявления. Для публикации объявлений без добавления участников\n'
                                            f'нажмите кнопку ниже\n\n'
                                            f' НА ДАННЫЙ МОМЕНТ ВЫ ДОБАВИЛИ: 👉🏻 {inv} пользователей\n'
                                            f'А если вам понравился бот и хочешь такого же жми сюда 👉🏻', reply_markup=markup)
                print(mess.from_user.id)
                await asyncio.sleep(10)
                try:
                    await new_msg.delete()
                except Exception as e:
                    print(e)
            elif inv >= threshold[0] or mess.from_user.id in [423947942, 5805441535]:
                pass
    else:
        await mess.answer('Чат бот предназначен для использования в группах, обратитесь к разработчикам или администратору')

import asyncio
from asyncio import sleep
from pprint import pprint

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher, Router, F
from aiogram.types import ContentType
from aiogram.filters import CommandStart, Command, CommandObject, ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import Message, ChatMember
from aiogram.types import FSInputFile, BufferedInputFile

from DB import conn
from func_db import invite_user, you_invite, db_update_invate, db_select_users, db_add_group, db_group_invites, \
    db_group_inv_update, save_user, db_update

router = Router()


@router.message(Command('open'))
async def get_open_chat(mess: Message, command: CommandObject):
    """Принудительно установить инвайты пользователя"""
    if mess.chat.id < 0:
        if mess.from_user.id in [5805441535, 423947942]:
            try:
                result = command.args
                result_list = result.split(' ')
                db_update(result_list[0], int(result_list[1]))
                print(result_list)

            except Exception as e:
                print(e)
                await mess.answer('Введите число')
                await asyncio.sleep(20)
        else:
            await mess.delete()
            await mess.answer('Команды только для администратора')
            await asyncio.sleep(20)


@router.message(Command('add_group'))
async def get_add_group(mess: Message):
    """Добавление группы в отслеживаемые у бота"""
    print(mess.from_user.id)
    if mess.chat.id < 0:
        if mess.from_user.id in [5805441535, 423947942]:
            print(mess.from_user.id)
            group_id = mess.chat.id
            db_add_group(str(group_id))
        else:
            await mess.delete()
            await mess.answer('Команды может использовать только администратор')
    else:
        pass


@router.message(Command('add'))
async def get_add(mess: Message, command: CommandObject):
    """Установить порог добавления участников в группу, для возможности написания сообщений"""
    if mess.chat.id < 0:
        if mess.from_user.id in [5805441535, 423947942]:
            group_id = mess.chat.id
            result = int(command.args)
            db_group_inv_update(group_id, result)
            await asyncio.sleep(5)
            await mess.delete()
            print(group_id)
            print(result)
        else:
            await mess.delete()
            await mess.answer('Команды может использовать только администратор')
    else:
        pass


# @router.message(Command('edit'))
# async def bot_settings(mess: Message):
#     if mess.chat.type == 'private':
#         await mess.answer('да этот чат приватный')
#     else:
#         await mess.delete()
#         new_msg = await mess.answer('команда только для администратора')
#         await asyncio.sleep(10)
#         await new_msg.delete()


# @router.message(F.content_type == types.ContentType.NEW_CHAT_MEMBERS)ChatMemberUpdatedFilter  .new_chat_members
@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def new_members(mem: ChatMember):
    """При событии добавления нового учасника, добавляем в базу
    -- Добавляет в базу нового участника, ставит inv = 0
    -- + 1 человек, узеру которойй добавил пользователя"""
    print(mem.from_user.id)
    my_db = db_select_users()
    if str(mem.from_user.id) in my_db:
        pass
    else:
        inv = 0
        username = mem.from_user.username
        invite_user(mem.from_user.id, inv, username)
    invited = mem.new_chat_member.user.id
    inviter = mem.from_user.id
    print(f"Пользователь {mem.new_chat_member.user.username} был приглашен {invited}\n"
          f"Пригласивший: {inviter}\n")
    inv = 0
    you_username = mem.new_chat_member.user.username
    invite_user(invited, inv, you_username)
    db_update_invate(mem.from_user.id)
    conn.commit()
    print(mem)


@router.message()
async def members(mess: Message):
    """Функция не пропускает текстовое сообщения пока не будет 10 приглашенных участников"""

    if int(mess.chat.id) < 0:
        user_id = mess.from_user.id
        group_id = mess.chat.id
        username = mess.from_user.username
        save_user(str(user_id), username)

        try:
            threshold = db_group_invites(str(group_id))
            invites = you_invite(user_id)
            print(mess)
            for inv in invites:
                if inv < threshold[0] and int(mess.from_user.id) not in [5805441535] and mess.from_user.is_bot is False and mess.forward_origin is None:
                    print('отработало первое условие')
                    await mess.delete()
                    button_1 = [[InlineKeyboardButton(text='Опубликовать объявления', url='https://t.me/OMKS312_bot')]]
                    markup = InlineKeyboardMarkup(inline_keyboard=button_1)
                    new_msg = await mess.answer(f'{mess.from_user.username} Пожалуйста добавьте {str(threshold[0])} пользователей,'
                                                f' после этого сможете публиковать объявления. Для публикации объявлений без добавления участников\n'
                                                f'Или напишите администратору https://t.me/kronus16 '
                                                f'нажмите кнопку ниже\n\n'
                                                f' НА ДАННЫЙ МОМЕНТ ВЫ ДОБАВИЛИ: 👉🏻 {inv} пользователей\n'
                                                f'А если вам понравился бот и хочешь такого же жми сюда 👉🏻 https://t.me/nbchatbot_bot', reply_markup=markup)
                    await asyncio.sleep(30)

                    try:
                        await new_msg.delete()
                    except Exception as e:
                        print(e)

                elif int(mess.from_user.id) < 0:
                    await mess.delete()
                    new_msg = await mess.answer('Нельзя пересылать сообщения из групп и каналов, а так же публиковать от имени групп')
                    await asyncio.sleep(30)
                    try:
                        await new_msg.delete()
                    except Exception as e:
                        print(e)

                elif mess.forward_origin is not None:
                    try:
                        if mess.forward_origin.chat.id < 0 and mess.from_user.id not in [5805441535]:
                            await mess.delete()
                            new_msg = await mess.answer('Нельзя пересылать сообщения из групп и каналов')
                            await asyncio.sleep(30)
                            try:
                                await new_msg.delete()
                            except Exception as e:
                                print(e)
                    except AttributeError:
                        pass

                elif inv >= threshold[0] or mess.from_user.id in [423947942, 5805441535]:
                    pass

        except TypeError:
            await mess.answer('Группа не добавлена в базу, напишите разработчикам что бы начать пользоваться ботом\n https://t.me/nbchatbot_bot')
    else:
        await mess.answer('Чат бот предназначен для использования в группах, обратитесь к разработчикам или администратору')

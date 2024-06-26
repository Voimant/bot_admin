import pandas as pd
import psycopg2.extras
# from psycopg2.errors import UniqueViolation
import psycopg2.errors
from DB import conn


def db_update(username, inv: int):
    with conn.cursor() as cur:
        update_query = '''UPDATE users_invtes SET invites = {}  WHERE username = '{}';'''.format(inv, username )
        cur.execute(update_query)
        conn.commit()


def invite_user(user_id, invite: int, username):
    """Добавляет нового человека в базу  ставит изначальное значение 0"""
    with conn.cursor() as cur:
        insert_query = """INSERT INTO users_invtes(user_id, invites, username) VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING;"""
        try:
            cur.execute(insert_query, (user_id, invite, username))
        except (Exception, psycopg2.errors) as e:
            cur.close()
            print(e)
            return f'пока что то'
        finally:
            cur.close()


def save_user(user_id, username):
    with conn.cursor() as cur:
        insert_query = """INSERT INTO users_invtes(user_id, invites, username) VALUES (%s, 0, %s)
        ON CONFLICT (user_id) DO NOTHING;"""
        try:
            cur.execute(insert_query, (user_id, username))
            conn.commit()
        except (Exception, psycopg2.errors) as e:
            cur.close()
            print(e)
        finally:
            cur.close()



def you_invite(user_id):
    with conn.cursor() as cur:
        select_query = '''SELECT invites fROM users_invtes WHERE user_id = '%s';'''
        cur.execute(select_query, (user_id,))
        return cur.fetchone()


def db_update_invate(user_id):
    with conn.cursor() as cur:
        update_query = '''UPDATE users_invtes SET invites = invites + 1 WHERE user_id = '%s';'''
        cur.execute(update_query, (user_id,))


def db_select_users():
    with conn.cursor() as cur:
        select_query = '''SELECT user_id fROM users_invtes;'''
        cur.execute(select_query)
        res = cur.fetchall()
        res_list = []
        for row in res:
            for r in row:
                res_list.append(r)
        return res_list


def db_add_group(group_id: str):
    with conn.cursor() as cur:
        insert_query = "INSERT INTO groups(group_id, inv) VALUES ('{}', 10) ON CONFLICT (group_id) DO NOTHING;".format(
            group_id)
        cur.execute(insert_query, )
        conn.commit()


def db_group_invites(group_id: str):
    with conn.cursor() as cur:
        select_query = '''SELECT inv FROM groups WHERE group_id = %s;'''
        cur.execute(select_query, (group_id,))
        res = cur.fetchone()
        res_list = []
        for row in res:
            res_list.append(row)
        return res_list


def db_group_inv_update(group_id, inv):
    with conn.cursor() as cur:
        update_query = ("UPDATE groups SET inv = {} WHERE group_id = '{}'").format(inv, str(group_id))
        cur.execute(update_query)
        conn.commit()

# print(db_select_users())

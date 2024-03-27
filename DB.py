import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

with psycopg2.connect(user=USER,
                      password=PASSWORD,
                      port=PORT,
                      database=DATABASE) as conn:
    def create_db():
        """
        Функция, создающая структуру БД (таблицы)
        :return: База данных создана
        """
        with conn.cursor() as cur:
            create_query = """ CREATE TABLE IF NOT EXISTS users_invtes(
                                user_id VARCHAR(150) PRIMARY KEY,
                                invites INTEGER);
                                CREATE TABLE IF NOT EXISTS groups(
                                group_id VARCHAR(150) PRIMARY KEY,
                                inv INTEGER);"""
            cur.execute(create_query)
            return 'База данных создана'


    #print(create_db())
    conn.commit()


    def delete_db():
        """
        Функция, удаляющая таблицы базы данных
        :return: База данных удалена
        """
        with conn.cursor() as cur:
            delete_query = """DROP TABLE users;"""
            cur.execute(delete_query)
            return 'База данных удалена'


    #print(delete_db())
    conn.commit()
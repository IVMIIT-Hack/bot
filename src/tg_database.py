#!seperaokeq/bin/python
import sqlite3 as sql

class DatabaseStorageTelegramUsersData:
    
    """
        Данный класс отвечает за создание базы данных пользователей Telegram, работу с ней по средству авторизации и регистрации.
        Используется для обновления данных о местоположении человека в рейтинге и вывод в Telegram посредством записи в БД.
    """
    def __init__(self, db_file: str):
        self.connection = sql.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS base (
                    uuid STRING,
                    tg_user_id INTEGER,
                    rating_json STRING,
                    tg_sub_status BOOl
                    )""")
        self.connection.commit()

    """
        Добавление пользователя в базу данных.
        
        Принимает tg_user_id, UUID(Снилс или Уникальный индифекатор, присвоенный самим вузом), Рейтинги как аргумент.
    """
    def add_user_db(self, tg_user_id: id, id: str, rating_json: str):
        with self.connection:
            return self.cursor.execute("INSERT INTO base VALUES (?, ?, ?, ?)", (id, tg_user_id, rating_json, False,))

    """
        Проверка, на то, если пользователь в базе.
        
        Принимает tg_user_id как аргумент.
    """
    def exists_user_db(self, tg_user_id: int) -> bool:
        result = self.cursor.execute("SELECT tg_user_id FROM base WHERE tg_user_id = ?", (tg_user_id,))
        return bool(len(result.fetchall()))
    
    """
        Получить текущую информацию о подписке.
    """ 
    def get_subsriptions_db(self, status: bool = True) -> list:
        with self.connection:
            return self.cursor.execute("SELECT * FROM base WHERE tg_sub_status = ?", (status,)).fetchall()

    """
        Обновление статуса подписки для пользователя.
    """ 
    def update_subsriptions_db(self, tg_user_id: int, status: bool = True):
        with self.connection:
            return self.cursor.execute("UPDATE base SET tg_sub_status = ? WHERE tg_user_id = ?", (status, tg_user_id,))
    
    """
        Получить полную информацию о пользователе.
    """
    def get_full_info_user_db(self, tg_user_id: int) -> list:
        result = self.cursor.execute("SELECT * FROM base WHERE tg_user_id = ?", (tg_user_id,))
        return result.fetchall()
    
    """
        Удалить информацию о рейтингах у пользователя.
    """
    def delete_rating_data_user_db(self, tg_user_id: int, spec: str):
        with self.connection:
            return self.cursor.execute("DELETE FROM base WHERE (tg_user_id, rating_json) = (?,?)", (tg_user_id, spec,))

    """
        Закрыть базу данных.
    """
    def close_db(self):
        self.connection.close_db()
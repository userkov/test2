from mysql.connector import MySQLConnection, Error
import os

config_heroku = {
    "user": os.environ["db_user"],
    "password": os.environ["db_password"],
    "host": os.environ["db_host"]
}


def connect_to_db():
    """ Подключение к БД """
    print("[method: Connect_to_db]: ", end="")
    cnx = MySQLConnection(**config_heroku)

    if cnx.is_connected():
        print("Succesfull")
        return cnx
    else:
        print("Failed")


def Querying_data(table):
    """Сбор всей информации из таблицы в dict"""
    cnx = connect_to_db()
    print("[method: Querying_data]: ", end="")
    try:
        db_day_arr = []

        cursor = cnx.cursor()
        cursor.execute("USE heroku_3d84c9c6e24e707")
        cursor.execute(f"SELECT * FROM {table}")
        rows_turple = cursor.fetchall()

        for item in rows_turple:  # Преобразование turple в dict
            day_dict = {"FullDate": item[0], "Link": item[1]}
            db_day_arr.append(day_dict)

        cnx.commit()
        print("Successful")
        return db_day_arr
    except Error as e:
        print("Failed\n", e)
    finally:
        cnx.close()


def Update_data(web_day_arr):
    """Удаление всех данных из таблицы и последующие заполнение новой информации"""
    print("[method: Update_data]")
    cnx = connect_to_db()
    try:
        cursor = cnx.cursor()
        cursor.execute("USE heroku_3d84c9c6e24e707")
        cursor.execute("DELETE FROM table_days")
        for web_day_dict in web_day_arr:
            args = f"INSERT INTO table_days(FullDate, Link) VALUES('{web_day_dict['FullDate']}', '{web_day_dict['Link']}')"
            print(args)
            cursor.execute(args)
            cnx.commit()
    except Error as e:
        print(e)
    finally:
        cnx.close()

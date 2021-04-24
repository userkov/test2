from mysql.connector import MySQLConnection, Error
import os

config_heroku = {
    "user": os.environ["db_user"],
    "password": os.environ["db_password"],
    "host": os.environ["db_host"]
}


def connect_to_db():
    """ Подключение к БД """
    print("Connecting to MySQL datebase...", end="")
    cnx = MySQLConnection(**config_heroku)

    if cnx.is_connected():
        print(" Succesfull")
        return cnx
    else:
        print(" Failed")


def Querying_data(table):
    """Сбор всей информации из таблицы в dict"""
    print("[func: Querying_data]")
    cnx = connect_to_db()
    try:
        days_from_db = []

        cursor = cnx.cursor()
        cursor.execute("USE heroku_3d84c9c6e24e707")
        cursor.execute(f"SELECT * FROM {table}")
        rows_turple = cursor.fetchall()

        for item in rows_turple:  # Преобразование turple в dict
            day_dict = {"FullDate": item[0], "Date": item[1], "StatusDay": item[2], "Link": item[3]}
            days_from_db.append(day_dict)

        cnx.commit()
        return days_from_db
    except Error as e:
        print(e)
    finally:
        cnx.close()


def Update_data(var_arr):
    """Удаление всех данных из таблицы и последующие заполнение новой информации"""
    print("[func: Update_data]")
    cnx = connect_to_db()
    try:
        cursor = cnx.cursor()
        cursor.execute("USE heroku_3d84c9c6e24e707")
        cursor.execute("DELETE FROM table_days")
        for day_dict in var_arr:
            args = f"INSERT INTO table_days(FullDate, Date, StatusDay, Link) VALUES('{day_dict['FullDate']}', '{day_dict['Date']}', '{day_dict['StatusDay']}', '{day_dict['Link']}')"
            print(args)
            cursor.execute(args)
            cnx.commit()
    except Error as e:
        print(e)
    finally:
        cnx.close()

import get_keys
from parstb import parstb
import database
import vk
from datetime import datetime


def check_new_day(web_day_arr, db_day_arr):
    """Сравнение двух словарей web_dict и db_dict для поиска нового дня"""
    new_day_arr = []
    for day_web_dict in web_day_arr:
        print(day_web_dict)
        bool_new_day = True
        for day_db_dict in db_day_arr:
            print(f"\t{day_db_dict}")
            if day_web_dict["FullDate"] == day_db_dict["FullDate"]:
                bool_new_day = False
                break

        print("\t[Result - ", end="")
        if bool_new_day:
            print(f"{day_web_dict['FullDate']}: New day]")
            new_day_arr.append({"FullDate": day_web_dict["FullDate"], "Link": day_web_dict["Link"]})
        else:
            print(f"{day_web_dict['FullDate']}: Old day]")

    if new_day_arr:# Если есть новое расписание
        database.Update_data(web_day_arr)
    return new_day_arr


kbt = parstb("ИБ31-18")
while True:
    now = datetime.now()
    print(f"\n[ ——— {now} ——— ]")
    if now.hour in range(10, 23):
        web_day_arr = kbt.get_blogs()  # Создание словаря web_dict (записи из сайта кбт)
        db_day_arr = database.Querying_data("table_days")  # Создание словаря db_dict (записи из БД)

        new_day_arr = check_new_day(web_day_arr, db_day_arr)  # Сравнение словарей на наличие новой записи

        if new_day_arr:
            for new_day_dict in new_day_arr:
                status_png = kbt.get_img(new_day_dict["Link"])
                if status_png:
                    msg = f"{new_day_dict['FullDate']}.\nСсылка на расписание {new_day_dict['Link']} "
                    status_send = vk.send_photo(2000000001, msg)  # Отправка скриншота

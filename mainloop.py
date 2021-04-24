import get_keys
from parstb import parstb
import database
import vk
from datetime import datetime



def check_new_day(web_arr, db_arr):
    """Сравнение двух словарей web_dict и db_dict для поиска нового дня"""
    var_arr = []
    new_day = False
    for day_web_dict in web_arr:
        print(f"[{day_web_dict}]")
        local_new_day = True
        for day_db_dict in db_arr:
            print(f"    {day_db_dict} [{day_web_dict['Date']} == {day_db_dict['Date']}] :  ", end="")
            if day_web_dict['Date'] == day_db_dict['Date']:
                print("True")
                local_new_day = False
            else:
                print("False")

        if local_new_day:
            status = "new"
            new_day = True
        elif not local_new_day:
            status = "old"
        print(f"Status - {status}")
        var_arr.append({"FullDate": day_web_dict['FullDate'], "Date": day_web_dict['Date'], "StatusDay": status,
                        "Link": day_web_dict["Link"]})  # {
    if new_day:
        database.Update_data(var_arr)

    return new_day, var_arr


kbt = parstb("ИБ31-18")
while True:
    now = datetime.now()
    print(" ")
    web_arr = kbt.get_blogs()  # Создание словаря web_dict (записи из сайта кбт)
    db_arr = database.Querying_data("table_days")  # Создание словаря db_dict (записи из базы)

    new_day, var_arr = check_new_day(web_arr, db_arr)  # Сравнение словарей на наличие новой записи
    print(f"{var_arr} \n[New day - {new_day}]")

    if new_day:
        for day in var_arr:
            if day['StatusDay'] == "new":
                status_png = kbt.get_img_day(day['Date'])
                if status_png:
                    status_send = vk.send_photo(2000000001, "Расписание")  # Отправка скриншота

from selenium import webdriver
import png_crop
import time


class parstb():
    def __init__(self, group):
        self.group = group

    def __get_driver(self):
        """Запуск webdriver Chrome"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def get_blogs(self):
        """Создание web_day_arr."""
        print("[method: get_blogs]: ", end="")
        driver = self.__get_driver()
        driver.get("https://cbcol.mskobr.ru/elektronnye_servisy/blog/")
        try:
            web_day_arr = []
            time.sleep(10)
            blogs_arr = driver.find_elements_by_class_name("item-body-h")
            for blog in blogs_arr:
                blog_txt = blog.text  # FullDate
                if "Расписание" in blog_txt:
                    link_el = blog.find_element_by_tag_name('a')
                    link = link_el.get_attribute('href')  # Link
                    web_day_arr.append({"FullDate": blog_txt, "Link": link})
            print("Successful")
            return web_day_arr
        except:
            print("Failed")
        finally:
            driver.quit()

    def get_img(self, link):
        """Создание скришнтоа расписания."""
        print("[method: get_img]")
        driver = self.__get_driver()
        driver.get(link)
        time.sleep(10)
        table_arr = driver.find_elements_by_tag_name("tbody")
        for table in table_arr:
            group_arr = table.find_elements_by_tag_name("td")
            for item in group_arr:
                item_txt = item.text
                item_txt = item_txt.replace(" ", "")
                item_txt = item_txt.replace("\n", " ")
                print(f"    group ({self.group}) in {item_txt}:", end=" ")
                if self.group in item_txt:
                    print("True")
                    size_table = table.size
                    location_table = table.location
                    size_group = item.size
                    location_group = item.location

                    width = size_table["width"]
                    height = int(size_table["width"]) / 2
                    driver.set_window_size(width, height)
                    time.sleep(5)
                    driver.execute_script("arguments[0].scrollIntoView();", table)
                    time.sleep(3)
                    table.screenshot("table.png")
                    png_crop.crop(location_table, size_table, location_group, size_group)
                    driver.quit()
                    return True
                else:
                    print("False")
        print(f"Error: [{self.group} — не найден]")
        driver.quit()



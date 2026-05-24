import csv
import time
from csv import writer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('chromedriver')

field_names = ['Space', 'Age', 'Bedrooms',
               'Elevator', 'Parking', "WareHouse", "Price", "Price Per Meter"]


def fetchData(urls):
    driver.get('https://divar.ir/v/' + urls)
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "kt-group-row-item__value")))  # This is a dummy element
    except:
        return False
    finally:
        el = driver.find_elements(by=By.CLASS_NAME, value='kt-group-row-item__value')
        if el:

            space = el[0].text

            if 'قبل از ۱۳۷۰' in el[1].text:
                age = el[1].text.replace('قبل از ۱۳۷۰', '70')
            else:
                age = el[1].text

            if 'بدون اتاق' in el[2].text:
                bedrooms = el[2].text.replace('بدون اتاق', '0')
            else:
                bedrooms = el[2].text

            elevator = 0 if 'ندارد' in el[3].text else 1
            parking = 0 if 'ندارد' in el[4].text else 1
            warehouse = 0 if 'ندارد' in el[5].text else 1
            # قسمت قیمت
            pel = driver.find_elements(by=By.CLASS_NAME, value="kt-unexpandable-row__value")
            # قیمت کل
            price = pel[0].text.replace("٬", "")
            price = price.replace(' تومان', '')
            # قیمت به ازای هر متر
            price_per_meter = pel[1].text.replace("٬", "")
            price_per_meter = price_per_meter.replace(' تومان', '')
            # طبقه یا شخصی

            level = pel[len(pel) - 1].text
            if ' از ' in level:
                if 'همکف' in level:
                    level = level.replace('همکف', '1')
                elif 'زیر همکف' in level:
                    level = level.replace('زیر همکف', '0')
                else:
                    level = int(float(level.replace(' از ', '.')))

            elif 'همکف' in level:
                if 'زیرهمکف' in level:
                    level = level.replace('زیرهمکف', '0')
                level = int(level.replace('همکف', '1'))
            else:
                level = int(level)

            #         level = level1[0]
            # if 'شخصی' or 'املاک' in pel[2].text:
            #     if 'همکف' in pel[3].text:
            #         level = '0'
            #     elif ' از ' in pel[3].text:
            #         level1 = pel[3].text.replace(' از ', '')
            #         level = level1[0]
            #     else:
            #         level = pel[3].text
            # else:
            #     if 'همکف' in pel[2].text:
            #         level = '0'
            #     elif ' از ' in pel[2].text:
            #         level1 = pel[2].text.replace(' از ', '')
            #         level = level1[0]
            #     else:
            #         level = pel[2].text

            mylist = [int(space), int(age), int(bedrooms), level, elevator, parking, warehouse, int(price),
                      int(price_per_meter), 'https://divar.ir/v/' + urls]

            with open('Houses.csv', 'a', encoding='utf-8', newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(mylist)
                f_object.close()

            with open('URL.csv', 'a', encoding="utf-8", newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow([urls])
                f_object.close()


urls = []
with open('Remained Tokens.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        urls.append(row)

for i in urls[0]:
    fetchData(i)
    time.sleep(5)
# بستن مرورگر
driver.quit()

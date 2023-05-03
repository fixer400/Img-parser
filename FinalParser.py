import json
import time
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import freeze_support
from multiprocessing import Pool
import re

f = open('data.json', encoding="utf8")
dataArr = json.load(f)
f.close()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def appendJson(entry):
    filename = 'sample.json'
    listObj = []

    # Read JSON file
    with open(filename, "r", encoding='utf8') as outfile:
         listObj = json.load(outfile)

    # Verify existing list
    print(type(listObj))

    listObj.append(entry)
    
    # Verify updated list
 
    with open(filename, 'w', encoding='utf8') as json_file:
        json.dump(listObj, json_file, 
                            indent=2,
                            ensure_ascii=False,
                            separators=(',',': '))

    print('Successfully appended to the JSON file')

def findImgByName(name, array):
    for i, value in enumerate(array):
        if value['Наименование'] == name:
            return i
    return False

def verificateFile():
    foundImg = []
    with open('sample.json', "r", encoding='utf8') as outfile:
        foundImg = json.load(outfile)
    for i in foundImg:
        result = findImgByName(i['Наименование'], dataArr)
        if result != -1:
            del dataArr[result]

def LoadImg():
    for count in range (1,10):
        count = str(count)
        imgList = driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div['+count+']')
        imgList.click()
        time.sleep(4)
        path = driver.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')
        if (path.get_attribute('src').startswith("data") == False):
            return path.get_attribute('src')

def main(i):
    url = 'https://www.google.com/search?q=+'+i['Наименование'].replace(" ","+")+'&hl=ru&prmd=ivmn&sxsrf=AJOqlzVHmngGsZrz__M8PHnLQWxQhXtFhQ:1675148751745&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiOsqyyn_H8AhUqiv0HHUmfB0EQ_AUoAXoECAEQAQ&biw=1018&bih=850&dpr=2'
    driver.get(url=url)
    time.sleep(1)
    imgSrc = LoadImg()
    dictionary = {
        "Наименование":i["Наименование"],
        "Ссылка":imgSrc
    }
    appendJson(dictionary)

if __name__ == '__main__':
    freeze_support()
    verificateFile()
    print('Введите сколько браузеров открыть для парсинга (от 1 до 5)')
    #p = Pool(processes = 1)
    #p.map(main, dataArr)
    x = input()
    if int(x) <= 5:
        p = Pool(processes = int(x))
        p.map(main, dataArr)
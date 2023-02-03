import json
import time
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#from multiprocessing import Pool

f = open('data.json', encoding="utf8")
dataArr = json.load(f)
f.close()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com")
driver.maximize_window()

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
        if value['Название'] == name:
            return i
    return False

def verificateFile():
    foundImg = []
    with open('sample.json', "r", encoding='utf8') as outfile:
        foundImg = json.load(outfile)
    for i in foundImg:
        result = findImgByName(i['Название'], dataArr)
        if result != -1:
            del dataArr[result]

def main():
    verificateFile()
    try:
        for i in dataArr:
            url = 'https://www.google.com/search?q=+'+i['Название'].replace(" ","+")+'&hl=ru&prmd=ivmn&sxsrf=AJOqlzVHmngGsZrz__M8PHnLQWxQhXtFhQ:1675148751745&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiOsqyyn_H8AhUqiv0HHUmfB0EQ_AUoAXoECAEQAQ&biw=1018&bih=850&dpr=2'
            driver.get(url=url)
            time.sleep(2)
            img = driver.find_element(By.XPATH, '//div[@jsname="r5xl4"]/div[1]')
            img.click()
            time.sleep(4)
            result = driver.find_element(By.CLASS_NAME,'zjoqD')
            imgSrc = result.find_element(By.TAG_NAME,'img')
            dictionary = {
                "Название":i["Название"],
                "Ссылка":imgSrc.get_attribute('src')
            }
            appendJson(dictionary)
    except:
            (print('Произошла ошибка'))

if __name__ == '__main__':
    main()
    
    

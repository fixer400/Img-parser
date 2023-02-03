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


def main():
    currentPos = 0
    with open('options.json', "r", encoding='utf8') as outfile:
         currentPos = json.load(outfile)
         currentPos = currentPos["currentPos"]

    for i in dataArr[currentPos:]:
        try:
            url = 'https://www.google.com/search?q=+'+i['Название'].replace(" ","+")+'&hl=ru&prmd=ivmn&sxsrf=AJOqlzVHmngGsZrz__M8PHnLQWxQhXtFhQ:1675148751745&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiOsqyyn_H8AhUqiv0HHUmfB0EQ_AUoAXoECAEQAQ&biw=1018&bih=850&dpr=2'
            driver.get(url=url)
            time.sleep(2)
            img = driver.find_element(By.XPATH, '//div[@jsname="r5xl4"]/div[1]')
            img.click()
            time.sleep(3)
            result = driver.find_element(By.CLASS_NAME,'zjoqD')
            imgSrc = result.find_element(By.TAG_NAME,'img')
            dictionary = {
                "Название":i["Название"],
                "Ссылка":imgSrc.get_attribute('src')
            }
            appendJson(dictionary)
            currentPos +=1
        except:
            option = {"currentPos":currentPos}
            with open('options.json', "w", encoding='utf8') as outfile:
                json.dump(option, outfile, 
                            indent=1,
                            ensure_ascii=False,
                            separators=(',',': '))

        


if __name__ == '__main__':
    main()
    
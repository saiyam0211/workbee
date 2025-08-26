from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import requests
from bs4 import BeautifulSoup
import time


firefox_options = Options()
#firefox_options.add_argument("--headless")
driver = webdriver.Chrome(options=firefox_options)
url = "https://jobs.apple.com/en-in/search"
driver.get(url)
L=[]
driver.implicitly_wait(20)
time.sleep(3)
ns = ""
while ns =="":
    try:
        num_str = driver.find_element(By.XPATH,"//h2[@id='resultCount']").text#get_attribute("innerHTML")
        #print(num_str)
        for i in num_str:
            if i not in "0123456789":
                break
            else:
                ns+=i
    except:
        #print("error")
        pass
    

int_num = int(ns)
count = 0
print(int_num)
while True:
    
    soup = BeautifulSoup(driver.page_source,"html.parser")
    total = soup.find_all("td",class_='table-col-1')
    total1 =  soup.find_all("td",class_='table-col-2')
    # print(len(total))
    # print(total)
    for i,j in zip(total,total1):
        soup2 = BeautifulSoup(str(i),"html.parser")
        soup3 = BeautifulSoup(str(j),"html.parser")
        #print(str(j))
        job_title = soup2.find("a").text
        job_link = "https://jobs.apple.com"+soup2.find("a",class_='table--advanced-search__title')["href"]
        job_location = j.text.replace("\n","")
        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        # print({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    # total = soup.find_all("li",class_='css-3hlofn')
    # for i in total:
    #     soup2 = BeautifulSoup(str(i),"html.parser")
    #     job_title = soup2.find("h3").text
    #     job_link = "https://nvidia.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
    #     job_location = soup2.find("dd",class_='css-129m7dg').text
    #     L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    time.sleep(3)
    try:
        elem = driver.find_element(By.XPATH,"//span[@class='next']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(3)
    except:
        break

    
json_data = json.dumps(L)
# json_data = json.dumps({"company":"nvidia","data":L})
print(len(L))
print(int_num)
print(json_data)
driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.chrome.options import Options
import json
import requests
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://jobs.netflix.com/search?team=Client%20and%20UI%20Engineering~Core%20Engineering~Data%20Platform~Data%20Science%20and%20Engineering~Netflix%20Technology%20Services~Production%20Services%20and%20Technology~Security~Studio%20Technologies~Video%20Encoding%20and%20Streaming'
driver.get(url)
L = []
driver.implicitly_wait(20)
time.sleep(2)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("section", class_="css-gf7hb5 e1rpdjew3")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("a", class_='css-2y5mtm essqqm81').text   
        job_link = 'https://jobs.netflix.com'+ soup2.find("a", class_="css-2y5mtm essqqm81")["href"]
        job_department = soup2.find("div", class_="teams-list").text
        job_location_multi = soup2.find("div", class_="locations-list")
        if job_location_multi != None:
            job_location=[]
            job_location_multi = job_location_multi.find_all("span")
            for j in job_location_multi:
                loc = j.text.strip()
                job_location.append(loc) 

        else:
            job_location=soup2.find("span", class_="css-ipl420 e13jx43x2").text
            
        L.append({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        #print({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        #print(len(L))
    try:
        exists = driver.find_element(By.XPATH,"//button[@aria-label='Next Page']").get_attribute('disabled')
        #print(exists)
        #print(type(exists))
        if exists=='true':
            #print("done")
            driver.quit()
            break

        elem=driver.find_element(By.XPATH,"//button[@aria-label='Next Page']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)

    except:
        #print("no button?")
        driver.quit()
        break
        

#print(len(L))
#print(L)

json_data=json.dumps({'company':'netflix','data':L})
print(json_data)
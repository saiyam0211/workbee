from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

from selenium.webdriver.chrome.options import Options
import json
import requests
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
url = "https://careers.mcafee.com/global/en/search-results"
driver.get(url)
L = []

driver.implicitly_wait(20)
time.sleep(2)

category = ['Engineering', 'Information Technology']


for i in category:

    team = driver.find_element(By.XPATH, "//input[@type='checkbox' and @data-ph-at-text='%s']"%i)
    driver.execute_script('arguments[0].scrollIntoView();', team)
    driver.execute_script('arguments[0].click();', team)
    time.sleep(2)
    
num_str = driver.find_element(By.XPATH, "//span[@class='result-count']").get_attribute('innerHTML')
int_num=int(num_str)
print(int_num)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="jobs-list-item")
    print(total)
    print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("div", class_= 'job-title').text.strip()   
        job_link = soup2.find("a")["href"]
        job_location = soup2.find('span', class_= 'au-target externalLocation').text.strip()             
        job_category = soup2.find('span', class_= 'job-category').text[9:].strip()                    
        job_created = soup2.find('span', class_='job-postdate').text[12:].strip()
        L.append({"job_title":job_title, 'job_category':job_category, "job_link": job_link, "job_created":job_created, "job_location": job_location})
        print({"job_title":job_title, 'job_category':job_category, "job_link": job_link, "job_created":job_created, "job_location": job_location})
        print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//a[@aria-label='View next page']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except:
        print("no button?")
        driver.quit()
        break

    if len(L)>=int_num:
        print('done')
        driver.quit()
        break

print(len(L))

json_data=json.dumps({'company':'adobe','data':L})
print(json_data)


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
url = "https://www.yelp.careers/us/en/search-results"
driver.get(url)
L = []

driver.implicitly_wait(20)
time.sleep(2)

cookies = driver.find_element(By.XPATH,"//button[@class='btn primary-button au-target' and @click.delegate='acceptAndClose()']")
driver.execute_script('arguments[0].click();', cookies)

time.sleep(2)

elem = driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='Engineering']")
driver.execute_script('arguments[0].scrollIntoView();', elem)
driver.execute_script('arguments[0].click();', elem)
time.sleep(2)

int_num = int(driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='Engineering']").get_attribute('data-ph-at-count'))

#print(int_num)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="jobs-list-item")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("div", class_= 'job-title').text.strip()   
        job_category = 'Engineering'
        job_link = soup2.find("a", class_="au-target")["href"]
        try:
            job_location = soup2.find('span', class_= 'job-location').text[9:].strip()             
        except:
            job_location = []
            job_location_multi = soup2.find_all(attrs={'data-ph-at-id':"job-multi-location-item"})
            for j in job_location_multi:
                loc = j.get('data-ph-at-job-location-text').strip()
                job_location.append(loc)
            # print(job_location_multi)
            # print(job_location)

        
        job_type = soup2.find("a")['data-ph-at-job-type-text'].strip()
        L.append({"job_title":job_title,'job_category':job_category, "job_link":job_link, "job_type":job_type, "job_location":job_location})
        # print({"job_title":job_title, 'job_category':job_category, "job_link": job_link, "job_type": job_type, "job_location":job_location})
        # print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//a[@aria-label='View next page']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except:
        #print("no button?")
        driver.quit()
        break

    if len(L)>=int_num:
        #print('done')
        driver.quit()
        break

#print(L)

json_data=json.dumps({'company':'yelp','data':L})
print(json_data)

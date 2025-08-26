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
url = "https://jobs.ebayinc.com/us/en/search-results"
driver.get(url)
L = []

cookies=driver.find_element(By.XPATH,"//button[@class='btn primary-button au-target' and @click.delegate='acceptAndClose()']")
driver.execute_script('arguments[0].click();', cookies)

time.sleep(2)

category1=driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='Data Science']")
num1=driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='Data Science']").get_attribute('data-ph-at-count')
driver.execute_script('arguments[0].click();', category1)

time.sleep(2)

category2=driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='Engineering']")
num2=driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='Engineering']").get_attribute('data-ph-at-count')
driver.execute_script('arguments[0].click();', category2)

time.sleep(2)

category3=driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='IT & Technical Operations']")
num3=driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='IT & Technical Operations']").get_attribute('data-ph-at-count')
driver.execute_script('arguments[0].click();', category3)

num=int(num1)+int(num2)+int(num3)
#print(num)

driver.implicitly_wait(20)
time.sleep(2)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="jobs-list-item")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("div", class_="job-title").text.strip()  
        job_link = soup2.find("a", class_="au-target")["href"]
        job_category = soup2.find("span", class_="job-category").text.strip()[8:].strip()
        try:
            job_location = soup2.find('span', class_="au-target dual-location dual-category").text.strip()[8:].strip()
        except:
            # job_location='Multiple'
            job_location=[]
            button_class=soup2.find("button", attrs={'data-ph-at-id':"job-multi-locations-button"})["class"]
            #print(button_class)
            button_str = ' '.join([str(elem) for elem in button_class])
            #print(button_str)
            job_location_button=driver.find_element(By.XPATH,'//button[@class="%s"]'%button_str)
            driver.execute_script('arguments[0].click();', job_location_button)
            time.sleep(2)
            soup3 = BeautifulSoup(driver.page_source, "html.parser")
            job_location_multi=soup3.find_all("li", class_="au-target each-location")
            #print(job_location_multi)
            for j in job_location_multi:
                loc = j.text.strip()
                job_location.append(loc) 
            close_button = driver.find_element(By.XPATH, "//button[@class='close ph-a11y-close-multi-location au-target']")
            driver.execute_script('arguments[0].click();', close_button)

       
        L.append({"job_title":job_title, "job_link": job_link, "job_location":job_location, "job_category":job_category})
        #print({"job_title":job_title, "job_link": job_link, "job_location":job_location, "job_category":job_category})
        #print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//a[@aria-label='View next page']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except:
        #print("no button?")
        driver.quit()
        break
    if len(L)>=num:
        #print('done')
        driver.quit()
        break

#print(len(L))

json_data=json.dumps({'company':'ebay','data':L})
print(json_data)

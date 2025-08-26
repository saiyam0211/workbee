#import webdriver
import os
os.environ['PATH'] += r"C:/Users/ANUBHAB/Downloads/geckodriver-v0.33.0-win-aarch64"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import By method to find the elements
from selenium.webdriver.common.by import By
#import time library to give sleep time to load data(bcz if we try to extract the data before getting loaded then we may get errros)
import time
import csv
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time

chrome_options = Options()
#setting the --headless argument to stop the browser window from opening as selenium is a type of automated browser software it opens browser window when we run code
#chrome_options.add_argument("--headless")
driver = webdriver.Firefox(options=chrome_options)
#take the url of website
url = "https://razorpay.com/jobs/department/creators/"
#this code gets the info from the url given
driver.get(url)

#this code is to wait till the data gets loaded from url
driver.implicitly_wait(20)
s = BeautifulSoup(driver.page_source,"html.parser")
driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
time.sleep(1)
driver.execute_script("arguments[0].click()",driver.find_element(By.XPATH,"//button[@class='styles_viewAllButton__PB96t']"))
time.sleep(3)
driver.find_element(By.XPATH,"//input[@id='DevOps']").click()
time.sleep(3)
driver.find_element(By.XPATH,"//input[@id='Product Support Engineering']").click()
time.sleep(3)
driver.find_element(By.XPATH,"//input[@id='Product Engineering']").click()
time.sleep(3)
s2 = BeautifulSoup(driver.page_source,"html.parser")
sp = s2.find_all("span",class_="styles_jobTitle__ZewFx")

job_loc = s2.find_all("span",class_="styles_jobDept__cpd2J")

link = s2.find_all("a",class_="row styles_container__LrNWu")
c=1
data =[]
for i in range(len(sp)):
    job_data ={
        "job":sp[i].text,
        "loc/role":job_loc[c].text,
        "job-link":"https://razorpay.com"+link[i]["href"]
    }
    data.append(job_data)
    c+=2
print(data)
json_data = json.dumps(data)
print(json_data)

# driver.execute_script("arguments[0].click()",driver.find_element(By.XPATH,"//li[@class='styles_viewAllButton__PB96t']"))


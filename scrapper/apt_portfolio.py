from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
import json
import requests
from bs4 import BeautifulSoup
import time

firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Chrome(options=firefox_options)
url = "https://boards.greenhouse.io/aptportfolio"
driver.get(url)
L=[]
driver.implicitly_wait(20)
time.sleep(3)

# num_str = driver.find_element(By.XPATH,"//p[@class='css-12psxof']").get_attribute("innerHTML")
# ns = ""
# for i in num_str:
#     if i not in "0123456789":
#         break
#     else:
#         ns+=i
# int_num = int(ns)
# count = 0
soup = BeautifulSoup(driver.page_source,"html.parser")
total = soup.find_all("section",class_='level-0')
    
for i in total:
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_title = soup2.find("a").text
    print(job_title)
    job_link = "https://boards.greenhouse.io"+soup2.find("a",attrs={"data-mapped": "true"})["href"]
    print(job_link)
    job_location = soup2.find("span",class_='location').text
    print(job_location)
    L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    #print({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        
time.sleep(3)
exit

    
json_data = json.dumps(L)
# json_data = json.dumps({"company":"nvidia","data":L})
#print(len(L))
#print(int_num)
print(json_data)
driver.quit()





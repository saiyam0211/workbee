from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

website = "https://www.binance.com/en/careers/job-openings"

driver = webdriver.Chrome()

driver.get(website)

time.sleep(3)


select_element = driver.find_element(By.XPATH, '//input[@placeholder="Team"]').click()

eng = driver.find_element(By.XPATH, '//div[text()="Engineering"]')

eng.click()

soup = BeautifulSoup(driver.page_source, 'html.parser')

buttons = soup.find_all('a', class_='css-1bx3lzi')

job_data = []

for button in buttons:
    link = 'https://www.binance.com' + button['href']
    driver.get(link)
    time.sleep(5)
    try:
        title = driver.find_element(By.XPATH, '//div[@class="css-1an4z5t"]')
        location = driver.find_element(By.XPATH, '//div[@class="css-19c62a5"]').text.split('/')[0]
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        about = soup2.find('div', class_='css-15om9hc').get_text()
        job_data.append({'job_title' : str(title), 'job_location' : str(location), 'job_link' : str(link), 'job_desc' : str(about)})
    except:
        continue

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, sys
from bs4 import BeautifulSoup

website = 'https://jobs.citi.com/category/technology-jobs/287/19627/1'

driver = webdriver.Chrome()

driver.get(website)

time.sleep(5)

job_set = set()

pages = int(driver.find_element(By.XPATH, '//div[@class="pagination-page-count"]').text.split()[1].split("G")[0])

print(pages)



page_input = driver.find_element(By.XPATH, '//input[@class="pagination-current"]')

soup = BeautifulSoup(driver.page_source, 'html.parser')

job_section = soup.find('section', id="search-results-list")

jobs = job_section.find_all('a')

for job in jobs:
    job_set.add(job)


i = 0

while i < pages-1:
    driver.execute_script('arguments[0].click()', driver.find_element(By.XPATH, '//a[@class="next"]'))
    time.sleep(3)
    job_section = soup.find('section', id="search-results-list")

    jobs = job_section.find_all('a')

    for job in jobs:
        job_set.add(job)

    i+=1

job_data = []

for job in job_set:
    try:
        link = 'https://jobs.citi.com' + job['href']
        driver.get(link)
        time.sleep(3)
        title = driver.find_element(By.XPATH, '//h1[@class="ajd_header__job-title"]').text
        location = driver.find_element(By.XPATH, '//p[@class="ajd_header__location"]').text
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        about = soup.find('section', id='anchor-overview').get_text()
        job_data.append({'job_title' : str(title), 'job_location' : str(location), 'job_link' : str(link), 'job_desc' : str(about)})
    except:
        continue


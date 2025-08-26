from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

website = "https://optiver.com/working-at-optiver/career-opportunities"

driver = webdriver.Chrome()

driver.get(website)

time.sleep(3)

select_element = driver.find_element(by=By.XPATH, value='//select[@data-placeholder="Departments"]')

select = Select(select_element)

select.select_by_visible_text('Technology')
time.sleep(2)

links_set = set()


while driver.find_element(By.XPATH, '//div[@class="row loadmore"]').find_element(By.TAG_NAME, 'a').is_displayed():
    
    links = driver.find_elements(By.CLASS_NAME, 'h5')

    for li in links:
        links_set.add(li)

    driver.execute_script('arguments[0].click()', driver.find_element(By.XPATH, '//div[@class="row loadmore"]').find_element(By.TAG_NAME, 'a'))
    time.sleep(3)

job_data = []

for li in links_set:
    try:
        link = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(link)
        time.sleep(3)
        title = driver.find_element(By.TAG_NAME, 'h1').text
        location = driver.find_element(By.XPATH, '//div[@class="bottom"]').find_element(By.TAG_NAME, 'p').text
        about = driver.find_element(By.TAG_NAME, 'section').text
        job_data.append({'job_title' : str(title), 'job_location' : str(location), 'job_link' : str(link), 'job_desc' : str(about)})
    except:
        continue

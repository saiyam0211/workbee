from bs4 import BeautifulSoup
import requests

page = requests.get("https://careers.media.net/")
page_content = page.content

soup = BeautifulSoup(page_content, 'html.parser')

roles = soup.find_all('a', class_ = 'flex-btn-link')

job_data = []

for role in roles:
    role_page_link = "https://careers.media.net/" + role['href']
    role_page = requests.get(role_page_link)
    soup2 = BeautifulSoup(role_page.content, 'html.parser')
    list_elements = soup2.find_all('li')
    for li in list_elements:
        try:
            link = li.contents[0]['href']
            title = li.string
            job_page = requests.get(  link)
            soup3 = BeautifulSoup(job_page.content, 'html.parser')
            about = soup3.find('div', class_ = 'post-body')
            jpb_data.append({'job_title' : str(title), 'job_link' : str(link), 'job_desc' : about})
        except:
            continue

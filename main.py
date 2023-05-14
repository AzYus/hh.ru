import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from requests import get
if __name__ == "__main__":
        headers = Headers(browser='googlechrome', os="mac", headers=True).generate()
import time
import json
def get_links (text, text2, text3):
    data = requests.get(
        url = f"https://hh.ru/search/vacancy?text={text+text2+text3}&from=suggest_post&salary=&area=1&area=2&ored_clusters=true&page=1",
        headers=headers
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup (data.content, "lxml")
    try:
        page_count = int(soup.find("div", attrs={"class":"pager"}).find_all("span",recursive=False)[-1].find("a").find("span").text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(
                url = f"https://hh.ru/search/vacancy?text={text+text2+text3}&from=suggest_post&salary=&area=1&area=2&ored_clusters=true&page={page}",
                headers=headers
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"class":"serp-item__title"}):
                yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        time.sleep(1)
    pass

def get_vacancy(link):
    data = requests.get(
        url=link,
        headers=headers
    )
    if data.status_code !=200:
        return
    soup = BeautifulSoup(data.content,"lxml")
    try:
        name = soup.find(attrs={"class":"bloko-header-section-1"}).text
    except:
        name = ""
    try:
        salary = soup.find(attrs={"class":"bloko-header-section-2 bloko-header-section-2_lite"}).text.replace("\u2009","").replace("\xa0","")
    except:
        salary = ""
    try:
        company_name = soup.find(attrs={"class":"vacancy-company-name"}).text
    except:
        company_name = ""
    try:
        city = soup.find(attrs={"class":"bloko-text bloko-text_large"}).text
    except:
        city = ""
    vacancy = {
        "name":name,
        "salary": salary,
        "company_name": company_name
    }
    return vacancy
    pass

if __name__ == "__main__":
    for a in get_links ("python", "django", "flask"):
        print(a)
        time.sleep(1)
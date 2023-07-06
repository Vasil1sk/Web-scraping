import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint

headers = Headers(browser="firefox", os="win")

hh_main_html = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers.generate()).text

hh_main_soup = BeautifulSoup(hh_main_html, "lxml")

vacancy_serp_results = hh_main_soup.find("div", id="a11y-main-content")

vacancys = vacancy_serp_results.find_all(class_="serp-item")

parsed_data = []

for vacancy in vacancys:
    h3_tag = vacancy.find("h3")
    span = h3_tag.find("span")
    a_tag = span.find("a")
    link = a_tag["href"]
    title = a_tag.text
    address = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).text
    salary = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
    if salary != None:
        salary = salary.text
    else:
        salary = "Заработная плата не указана"
    company_name = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).text

    vacancy_page_soup = BeautifulSoup(requests.get(link, headers=headers.generate()).text, "lxml")
    vacancy_description = vacancy_page_soup.find("div", class_="vacancy-description").text
    match_1 = re.findall(".*Django.*", vacancy_description, flags=re.MULTILINE)
    match_2 = re.findall(".*Flask.*", vacancy_description, flags=re.MULTILINE)
    if match_1 or match_2 != []:
        parsed_data.append(
            {"link": link,
             "salary": salary,
             "company_name": company_name,
             "address": address}
        )
with open("Vacancys.json", "w", encoding="utf-8") as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=4)
pprint(parsed_data)

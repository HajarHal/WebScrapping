import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

result = requests.get("https://www.gohitv.com/")
src = result.content
soup = BeautifulSoup(src, "lxml")

headers = ["RECOMMEND", "UPDATING", "THE LATEST", "UPCOMING"]

with open("/Users/PcPack/series2.csv", "w", newline='', encoding='utf-8') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Header", "Series Name", "Episodes", "Episode Link", "Description"])

    for header in headers:
        recommend_header = soup.find("h2", {"class": "title", "data-v-50cbb81f": ""}, string=header)

        if recommend_header:
            parent_div = recommend_header.find_next('div')

            recommended_series = parent_div.find_all("div", {"class": "series-name"})
            episodes_numb = parent_div.find_all("div", {"class": "update-info", "data-v-2fcc5114": ""})
            episode_lien = parent_div.find_all("a", class_="thumbnail", href=True)

            recommended_series_names = [element.get_text(strip=True) for element in recommended_series]
            episodes_numb1 = [element.get_text(strip=True) for element in episodes_numb]
            episode_lien1 = [element.get('href') for element in episode_lien]

            for series_name, episodes, episode_link in zip(recommended_series_names, episodes_numb1, episode_lien1):
                series_page = requests.get(episode_link)
                series_soup = BeautifulSoup(series_page.content, 'lxml')

                description_span = series_soup.find("span", {"aria-label": True})
                description = description_span.get_text(strip=True) if description_span else "No description available"

                data = [header, series_name, episodes, episode_link, description]
                wr.writerow(data)
        else:
            print(f"The <h2> tag with '{header}' not found.")

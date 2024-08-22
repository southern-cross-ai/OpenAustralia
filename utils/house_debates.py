import os
import re

import requests
from bs4 import BeautifulSoup


def retrieve_house_debates(start_year, end_year, save_root):
    prefix = 'https://www.openaustralia.org.au'

    for year in range(start_year, end_year+1):
        print(f"Searching for dates in year {year}")
        year_url = 'https://www.openaustralia.org.au/debates/?y=' + str(year)
        response = requests.get(year_url)
        # print(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        date_pattern = re.compile(r'/debates/\?d=([0-9]{4}-[0-9]{2}-[0-9]{2})')
        date_affixes = [anchor.get('href')
                        for anchor in soup.find_all('a',  href=date_pattern)]
        date_urls = [prefix + date_affix for date_affix in date_affixes]
        # print(date_urls)
        print(f"Found {len(date_urls)} dates in year {year}")

        for date_url in date_urls:
            response = requests.get(date_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # print(response.content)
            post_pattern = re.compile(
                r'/debates/\?id=[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+\.[0-9]+')
            post_affixes = [anchor.get('href') for anchor in soup.find_all(
                'a',  href=post_pattern)]
            post_urls = [prefix + post_affix for post_affix in post_affixes]
            print(f"Found {len(post_urls)} posts in date {
                  date_url.split('=')[1]}")
            print(f"Searching for posts in date {date_url.split('=')[1]}")

            for post_url in post_urls:
                try:
                    print(post_url)
                    response = requests.get(post_url)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    name = post_url.split('=')[1] + '.html'
                    path = os.path.join(save_root, name)
                    with open(path, 'w') as f:
                        f.write(f"<!--{post_url}-->\n")
                        f.write(soup.prettify())
                    print(f"Saved the post as {path}")
                except:
                    print(f"Failed to retrieve from {post_url}")

        print('\n\n')


if __name__ == '__main__':
    # last time updated on 22 Aug 2024
    start_year = 2006
    end_year = 2024
    save_root = '/Users/yifan/Documents/GitHub/datasets/Gale-Literature-Criticism/house_debates'
    retrieve_house_debates(start_year, end_year, save_root)

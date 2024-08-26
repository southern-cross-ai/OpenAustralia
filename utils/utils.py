"""
Download comments, house debates or senate debates data from OpenAustralia (https://www.openaustralia.org.au).
"""

import argparse
import re
import os
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help="Show all help messages.")
    parser.add_argument("-s", "--start_date", type=str, default="2006-01-01",
                        help="The start of your search range (YYYY-MM-DD).\n"
                        "The default date is 2006-01-01.")
    parser.add_argument("-e", "--end_date", type=str, default=date.today().strftime("%Y-%m-%d"),
                        help="The end of your search range (YYYY-MM-DD).\n"
                        "The default date is set to your current date.")
    parser.add_argument("-t", "--data_type", type=str, required=True,
                        help="Which data you want to download.\n"
                        "Choose between 'comments', 'house' or 'senate'.")
    parser.add_argument("-p", "--save_path", type=str, default="OpenAustralia",
                        help="The path to save the data.\n"
                        "Default path is 'OpenAustralia'.")
    args = parser.parse_args()
    return args


class OpenAustralia(object):
    __prefix = 'https://www.openaustralia.org.au'
    __recent_comments = 'comments/recent'
    __house_debates = 'debates'
    __senate_debates = 'senate'

    def __init__(self, start_date, end_date, data_type, save_path) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.data_type = data_type
        self.save_path = save_path

    def search_dates(self) -> list[str]:
        if not self.start_date or not self.end_date:
            raise ValueError("Start date and end date must be set in the format YYYY-MM-DD.")
        else:
            try:
                datetime.strptime(self.start_date, '%Y-%m-%d')
                datetime.strptime(self.end_date, '%Y-%m-%d')
            except:
                raise ValueError("Invalid date format. Set dates in the format YYYY-MM-DD.")
            try:
                self.end_date < self.start_date
            except:
                raise ValueError("End date must be a date after start date.")
        
        if self.data_type == 'comments':
            pass  # TODO
        elif self.data_type == 'house':
            date_prefix = self.__prefix + '/' + self.__house_debates + '/?y='
            date_pattern = re.compile(r'/debates/\?d=([0-9]{4}-[0-9]{2}-[0-9]{2})')
        elif self.data_type == 'senate':
            date_prefix = self.__prefix + '/' + self.__senate_debates + '/?y='
            date_pattern = re.compile(r'/senate/\?d=([0-9]{4}-[0-9]{2}-[0-9]{2})')
        else:
            raise TypeError("Invalid data type\n."\
                            "Choose between 'comments', 'house_debates' or 'senate_debates'.")
        
        start_year = int(self.start_date.split('-')[0])  # suppose format is YYYY-MM-DD
        end_year = int(self.start_date.split('-')[0])

        all_dates = []
        
        for year in range(start_year, end_year+1):
            response = requests.get(date_prefix + str(year))
            soup = BeautifulSoup(response.content, 'html.parser')
            if year == start_year:  # get rid of any dates before the start date
                dates = [anchor.get('href').split('=')[1] 
                         for anchor in soup.find_all('a',  href=date_pattern)
                         if anchor.get('href').split('=')[1] >= self.start_date]
            elif year == end_year:  # get rid of any dates after the end date
                dates = [anchor.get('href').split('=')[1] 
                         for anchor in soup.find_all('a',  href=date_pattern)
                         if anchor.get('href').split('=')[1] <= self.start_date]
            else:
                dates = [anchor.get('href').split('=')[1] 
                         for anchor in soup.find_all('a',  href=date_pattern)]
            
            all_dates.extend(dates)

        print(f"Found {len(all_dates)} entries in the range {self.start_date} - {self.end_date}.")
        
        return all_dates
    
    def build_urls(self) -> list[str]:
        all_dates = self.search_dates()
        if len(all_dates) == 0:
            raise ValueError("No entry found in the range {self.start_date} - {self.end_date}.")
        
        if self.data_type == 'comments':
            pass
        elif self.data_type == 'house':
            date_prefix = self.__prefix + '/' + self.__house_debates + '/?d='
            post_prefix = self.__prefix + '/' + self.__house_debates + '/?id='
            post_pattern = re.compile(r'/debates/\?id=[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+\.[0-9]+')
        elif self.data_type == 'senate':
            date_prefix = self.__prefix + '/' + self.__senate_debates + '/?d='
            post_prefix = self.__prefix + '/' + self.__senate_debates + '/?id='
            post_pattern = re.compile(r'/senate/\?id=[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+\.[0-9]+')
        else:
            raise TypeError("Invalid data type\n."\
                            "Choose between 'comments', 'house_debates' or 'senate_debates'")
        all_urls = []    
        
        for date in all_dates:
            url = date_prefix + date
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            affixes = [anchor.get('href') for anchor in soup.find_all('a',  href=post_pattern)]
            urls = [self.__prefix + affix for affix in affixes]
            all_urls.extend(urls)
            
        return all_urls
    
    def retrieve_data(self) -> None:
        all_urls = self.build_urls()
        if len(all_urls) == 0:
            raise ValueError("No URL found in the range {self.start_date} - {self.end_date}.")
        
        root = os.path.join(self.save_path, self.data_type)
        if not os.path.exists(root):
            os.makedirs(root, exist_ok=True)
            
        for url in all_urls:
            response = requests.get(url)
            response.raise_for_status()   
            soup = BeautifulSoup(response.content, 'html.parser')
            path = os.path.join(root, url.split('=')[1] + '.html')
            with open(path, 'w') as f:
                f.write(f"<!--{url}-->\n")
                f.write(soup.prettify())
            print(f"Saved as {path}")
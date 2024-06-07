# (c) 2024 CapCrawlington Inc.

from typing import List, Dict, Any, Union, Optional

import os
import requests
from bs4 import BeautifulSoup

from tabulate import tabulate


COIN_MARKET_CAP_URL = 'https://coinmarketcap.com'
COIN_MARKET_CAP_ROBOTS_URL = 'https://coinmarketcap.com/robots.txt'
API_ENDPOINT = ''
CAP_UA = ''

'''valid as of 6/7/24'''
TABLE_ROW_SELECTOR = 'table.cmc-table > tbody > tr'


def execute_request(method: str, url: str, params: Optional[Dict[str, Union[str, List[str]]]] = None, headers: Dict[str, str] = {}, json_data: Optional[Dict[str, Any]] = None) -> requests.Response:
    return requests.request(method, url, params=params, headers=headers, json=json_data)

class CapCrawlington:
    """
    CapCrawlington scrapes CMC and extracts Top 10 cryptocurrency data.
    Scraped data includes the rank, name, price, 1hr % change, 24-hour % change, 7-day % change, market cap, trading volume, and circulating supply.
    """
    def _is_allowed(self) -> bool:
        '''
        Be good, check if allowed.
        '''
        try:
            headers = {'User-Agent': CAP_UA}
            response = execute_request('GET', COIN_MARKET_CAP_ROBOTS_URL, headers=headers)
            if response.status_code == 200:
                robots_txt_content: str = response.text
                return 'User-agent: *\nDisallow: /' not in robots_txt_content
            else:
                print(f"Failed fetch - {COIN_MARKET_CAP_ROBOTS_URL}. Http status code: {response.status_code}")
                return False
        except Exception as e:
            print("Error fetching robots.txt: ", e)
            return False

    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape CMC
        
        :return: List of scraped Top 10 cryptocurrency data.
        """
        try:
            if not self._is_allowed():
                return []

            headers = {'User-Agent': CAP_UA}
            response = execute_request('GET', COIN_MARKET_CAP_URL, headers=headers)
            if response.status_code == 200:
                soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
                scraped_crypto_list: List[Dict[str, Any]] = []

                for idx, elem in enumerate(soup.select(TABLE_ROW_SELECTOR)):
                    table_data = elem.find_all('td')
                    crypto: Dict[str, Any] = {}
                    if table_data and idx < 10:
                        crypto['rank'] = idx + 1
                        crypto['name'] = table_data[2].get_text().strip()
                        crypto['price'] = table_data[3].get_text().strip()
                        crypto['1h'] = table_data[4].get_text().strip()
                        crypto['24h'] = table_data[5].get_text().strip()
                        crypto['7d'] = table_data[6].get_text().strip()
                        crypto['marketCap'] = table_data[7].get_text().strip()
                        crypto['volume'] = table_data[8].get_text().strip()
                        crypto['circulatingSupply'] = table_data[9].get_text().strip()
                        scraped_crypto_list.append(crypto)
                return scraped_crypto_list
            else:
                print(f"Failed to retrieve data from {COIN_MARKET_CAP_URL}. Status code: {response.status_code}")
                return []
        except Exception as e:
            print("Error scraping CoinMarketCap: ", e)
            return []


def send(data: List[dict]):
    """stream"""
    # payload = create_and_fmt_payload(data)
    # response = execute_request('POST', ...)
    pass

def create_and_fmt_payload(data: List[dict]):
    '''fmt payload'''
    pass

def run_scrape():
    pass

def taskify():
    # dae & sch
    pass


if __name__ == "__main__":
    cap_crawler = CapCrawlington()
    extracted_data: List[Dict[str, Any]] = cap_crawler.scrape()
    if extracted_data:  print(tabulate(extracted_data, headers="keys", tablefmt="pretty"))

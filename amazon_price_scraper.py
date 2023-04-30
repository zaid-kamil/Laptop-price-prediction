from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from dputils.scrape import Scraper, Tag

BASE_URL = 'https://www.amazon.in'
def get_links_from_page(page=1):
    SEARCH_PAGE_URL = f'https://www.amazon.in/s?k=laptops&page={page}'
    scraper = Scraper(SEARCH_PAGE_URL)
    target = Tag(cls='s-main-slot s-result-list s-search-results sg-row')
    items = Tag(cls='s-result-item')
    link = Tag('a', cls='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal', output='href')

    all_links = scraper.get_all(target, items, link=link)
    return all_links

def get_laptop_details(link):
    '''
    collect the following details from the link
    1.Manufacturer ✔️
    2.Model Name ✔️
    4.Screen Size ✔️
    6.CPU ✔️
    7.RAM ✔️
    8.Storage   ✔️
    9.GPU ✔️
    10.Operating System     ✔️
    13.Price ✔️
    '''
    scraper = Scraper(link, clean=True)
    manufacturer = Tag('tr', cls='po-brand')
    model_name = Tag('tr', cls='po-model_name')
    screen_size = Tag('tr', cls='po-display.size')
    color = Tag('tr', cls='po-color')
    cpu = Tag('tr', cls='po-cpu_model.family')
    storage = Tag('tr', cls='po-hard_disk.size')
    ram = Tag('tr', cls='po-ram_memory.installed_size')
    os = Tag('tr', cls='po-operating_system')
    gpu = Tag('tr', cls='po-graphics_coprocessor')
    price =Tag('span', cls='a-price-whole')

    result =  scraper.get(brand=manufacturer, 
                       model=model_name, 
                       screen_size=screen_size, 
                       color=color, 
                       cpu=cpu,
                       storage=storage,
                       ram=ram,
                       os=os,
                       gpu=gpu,
                       price=price)
    result['link'] = link
    return result

def main():
    page = 1    
    while True:
        print(f'Extracting links from page {page}')
        links = [f"{BASE_URL}{link['link']}" for link in get_links_from_page(page) if link['link'] !=None]
        laptops = []
        if len(links) > 0:
            print(f'Found {len(links)} links')
            for link in links[:3]:
                print(f'Extracting details from {link}')
                details = get_laptop_details(link)
                laptops.append(details)
            page += 1
            if page > 2 :
                break
        else:
            break
        print(f'Extracted details for {len(laptops)} laptops')
    if len(laptops) > 0:
        print('Saving to laptops.csv')
        df = pd.DataFrame(laptops)
        df.to_csv('laptops.csv', index=False)
        print('Saved to laptops.csv')

if __name__ == '__main__':
    main()






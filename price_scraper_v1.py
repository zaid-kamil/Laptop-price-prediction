from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
# Function to extract Product Title
def get_title(soup):

  try:
    # Outer Tag Object
    title = soup.find("span", attrs={"id": 'productTitle'})

    # Inner NavigatableString Object
    title_value =title.text

    #Title as a string value
    title_string = title_value.strip()

  except AttributeError:
    title_string = " "

  return title_string

# Function to extract Product Price
def get_price(soup):

  try:
    price = soup.find("span", attrs={"class":'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span", attrs={"class": "a-offscreen"}).text

  except AttributeError:
    price = " "

  return price

# Function to extract product rating
def get_rating(soup):

  try:
    rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-icon-4-5'}).string.strip()

  except AttributeError:
    try:
      rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
    except:
      rating = " "

  return rating

# Function to extract number of user reviews
def get_review_count(soup):
  try:
    review_count = soup.find("span", attrs={'class':'a-size-base s-underline-text'}).string.strip()

  except AttributeError:
    review_count = " "

  return review_count

# Function to extract avalability status
def get_availability(soup):
  try:
    available = soup.find("div", attrs={'id':'availability'})
    available = available.find("span").string.strip()

  except AttributeError:
    available = "Not Available"

  return available

# The webpage URL
def get_amazon_data(url, HEADERS): 
    # HTTP Request
    webpage = requests.get(url, headers=HEADERS)
    print(f'webpage status code: {webpage.status_code}')
    # Soup object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    # Store the links
    links_list = []

    # Loop for extracting links from tag objects
    for link in links:
        links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[], "availability":[]}

    # Loop for extracting product details from each link
    for link in links_list:
        print(f'=> visiting {link}')
        try:
            new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to display all necessary product information
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['availability'].append(get_availability(new_soup))
        except:
            print('=> error occured')
            pass
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    return amazon_df

def collect_all(q='laptop', pos=1):
  # Headers for request
  HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
  results = []
  while True:
    print(f'Collecting data from amazon for {q} from page {pos}')
    amazon_url = f"https://www.amazon.in/s?k={q}&page={pos}"
    print(amazon_url)
    out = get_amazon_data(amazon_url, HEADERS)
    print(out.shape)
    if len(out) > 0:
      pos+=1
      results.append(out)
      print('results updated')
    else:
      print(len(out), 'items found')
      break
  return results

def save_data(data, filename):
  df = pd.concat(data)
  df.to_csv(filename, header=True, index=False)


if __name__ == '__main__':
    data = collect_all()
    filename = f'laptop_{time.strftime("_%Y%m%d_%H%M")}.csv'
    save_data(data, filename)

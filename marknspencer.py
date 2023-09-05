import requests
from bs4 import BeautifulSoup
import pandas as pd
import gzip
import zlib
import re
import os
from requests.exceptions import RequestException


def extract_href_values(url, headers, max_retries=3):
    for _ in range(max_retries):
        try:
            # Send a GET request to the URL with the headers
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except RequestException as e:
            print(f"An error occurred: {e}")
            print("Retrying...")
    return None  # Return None if all retries fail


def extract_number_of_pages(soup):
    pagination_span = soup.find('span', class_='css-82gmvi e1ytuwls1')
    if pagination_span:
        text = pagination_span.get_text()
        parts = text.split(' of ')
        if len(parts) == 2:
            return int(parts[1])
    return None

def extract_product_url(pageUrls):
    for pages in pageUrls:
        soup =  extract_href_values (pages, headers)
        product = soup.find_all('a', class_='css-g65o95 eenyued10')
        for link in product:
            urlextension = link.get('href')
            producturl= baseUrl + urlextension
            productUrl.append(producturl)

    return productUrl


def extract_company(soup):
    company_element = soup.find('p', class_='css-m5y22d eand5hi23')
    if company_element:
        return company_element.text.strip()
    else:
        company_element = soup.find('a', class_='eand5hi23 css-z0abg7 epzkrr00')
        if company_element:
            return company_element.get_text()
        else:
            return None

def extract_product_name(soup):
    return soup.find('h1', class_='css-vvorhm eand5hi26').text

def extract_product_code(soup):
    product_code_element = soup.find('p', class_='css-1jx4yjs e1b0kgj0')
    if product_code_element:
        product_code_text = product_code_element.text
    
        # Extract the product code
        product_code = product_code_text.split(': ')[-1]
    return product_code

def extract_avg_rating(soup):
    avg_rating_element = soup.find('div', class_='css-w44v8g e1tr9ty71')
    avg_rating = float(avg_rating_element['aria-label'].split(':')[1].split(' out')[0])
    return avg_rating

def extract_reviews(soup):
    review_element = soup.find('button', class_='e1kxsblz1 css-yvs3kk e2ucisq0')
    if review_element:
        reviews_text = review_element.get_text(strip=True)
        reviews_match = re.search(r'(\d+)', reviews_text)
        if reviews_match:
            return int(reviews_match.group(1))
    return None

def extract_selling_price(soup):
    # Check if "css-1v802j0 e1b0kgj0" class exists
    selling_price_element_v802j0 = soup.find('p', class_='css-1v802j0 e1b0kgj0')
    if selling_price_element_v802j0:
        selling_price_text = selling_price_element_v802j0.text.strip()
        selling_price = float(selling_price_text[1:])
    else:
        # Use "css-ktq1e4 e1b0kgj0" class as fallback
        selling_price_element_ktq1e4 = soup.find('p', class_='css-ktq1e4 e1b0kgj0')
        if selling_price_element_ktq1e4:
            selling_price_text = selling_price_element_ktq1e4.text.strip()
            selling_price = float(selling_price_text[1:])
        else:
            selling_price = 0
    return selling_price

def extract_original_price(soup):
    original_price_element = soup.find('p', class_='css-1bb4dcr e1b0kgj0')
    if original_price_element:
        original_price_text = original_price_element.text.strip()
        original_price = float(original_price_text[1:])
    else:
        # If original price is not found, use selling price as fallback
        original_price = extract_selling_price(soup)
    return original_price

def extract_saved_price(soup):
    saved_price_element = soup.find('p', class_='css-opziqa e1b0kgj0')
    if saved_price_element:
        saved_price_text = saved_price_element.text.strip()
        saved_price_start = saved_price_text.find('£') + 1
        saved_price_value = saved_price_text[saved_price_start:]
        try:
            saved_price = float(saved_price_value)
        except ValueError:
            saved_price = 0.0
    else:
        saved_price = 0.0
    return saved_price

def extract_color(soup):
    return soup.find('span', class_='css-1jtzzxv ecsh60z7').text

def extract_sales_status(soup):
    sales_status_element = soup.find('span', class_='css-1jjg44c ecsh60z6')
    if sales_status_element:
        return sales_status_element.text.strip()
    return None

def extract_composition(soup):
    div_element = soup.find('div', class_='css-14hvavs eohri893')
    if div_element:
        p_element = div_element.find('p', class_='css-z5zkuw e1b0kgj0')
        if p_element:
            return p_element.text
    return "No composition found"

def fetch_product_details(productUrl):
    x = 1
    for page in productUrl:
        soup = extract_href_values(page, headers)
        print(page)
        print(f"Product count :{x}")
        x += 1
        
        company = extract_company(soup)
        product_name = extract_product_name(soup)
        product_code = extract_product_code(soup)
        avg_rating = extract_avg_rating(soup)
        reviews = extract_reviews(soup)
        selling_price = extract_selling_price(soup)
        original_price = extract_original_price(soup)
        saved_price = extract_saved_price(soup)
        color = extract_color(soup)
        sales_status = extract_sales_status(soup)
        composition = extract_composition(soup)
        
        Company.append(company)
        Product_Name.append(product_name)
        Product_Code.append(product_code)
        Avg_Rating.append(avg_rating)
        Reviews.append(reviews)
        Selling_Price.append(selling_price)
        Original_Price.append(original_price)
        Saved_Price.append(saved_price)
        Color.append(color)
        Sales_Status.append(sales_status)
        Composition.append(composition)


# Define variables
productUrl = []
pageUrls = []
# Extract company
Company = []
# Extract product name
Product_Name = []
# Extract product code
Product_Code = []
# Extract average rating
Avg_Rating = []
# Extract reviews
Reviews = []
# Extract selling price
Selling_Price = []
# Extract original price
Original_Price = []
# Extract saved price
Saved_Price = []
# Extract color and sales status
Color = []
Sales_Status = []
# Extract style details
Styles = []
# Extract composition
Composition = []

# Define the URLs
baseUrl = 'https://www.marksandspencer.com'
mainUrl = baseUrl + '/l/lingerie/nightwear#intid=gnav_Lingerie_Nightwear_All-Nightwear'

# Define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate'
}

# Extract href values from the first page
soup = extract_href_values (mainUrl, headers)


# Extract the number of pages
numberOfPages = extract_number_of_pages(soup)
if numberOfPages is not None:
    print(f"Number of Pages: {numberOfPages}")

href_elements = soup.find_all('a', class_='css-jeyzxy e8trdjq0')
for page in range(1, numberOfPages + 1):
    href = href_elements[0]['href']
    page_number = href[-1]  # Get the last character of href
    href = href[:-1]  # Remove the last character from href
    page_url = f"{baseUrl}{href}{page}"
    pageUrls.append(page_url)


# Exact product URL from each page
productUrl = extract_product_url (pageUrls)

print("Number of products:", len(productUrl))

fetch_product_details (productUrl)

data = {'Brand': Company, 
        'Title': Product_Name, 
        'Product_Url' : productUrl,
        'Average_rating': Avg_Rating, 
        'Product_Code' : Product_Code,
        'Reviews' : Reviews,
        'Selling_Price': Selling_Price,
        'Orginal_Price' : Original_Price,
        'Discount' : Saved_Price,
        'Sales_Status' : Sales_Status,
        'Composition' : Composition
        }

df = pd.DataFrame(data)

# Check if the file already exists
if os.path.exists('mas.csv'):
    # Replace the file if it already exists
    df.to_csv('mas.csv', index=False, mode='w')
else:
    # Export the DataFrame to an Excel file
# Export the DataFrame to an Excel file
    df.to_csv('mas.csv', index=False)

    
 


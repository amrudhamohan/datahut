import requests
from bs4 import BeautifulSoup
import pandas as pd
import gzip
import zlib
import re
import os


def extract_href_values(url, headers):
    # Send a GET request to the URL with the headers
    response = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_number_of_pages(soup):
    pagination_span = soup.find('span', class_='css-82gmvi e1ytuwls1')
    if pagination_span:
        text = pagination_span.get_text()
        parts = text.split(' of ')
        if len(parts) == 2:
            return int(parts[1])
    return None

# def generate_page_urls(base_url, num_pages):
#     page_urls = []
#     for page in range(1, num_pages + 1):
#         page_url = f"{base_url}?page={page}"
#         page_urls.append(page_url)
#     return page_urls

def extract_product_url(pageUrls):
    for pages in pageUrls:
        soup =  extract_href_values (pages, headers)
        product = soup.find_all('a', class_='css-g65o95 eenyued10')
        for link in product:
            urlextension = link.get('href')
            producturl= baseUrl + urlextension
            productUrl.append(producturl)

    return productUrl

def fetch_product_details(productUrl):
    for pages in productUrl:
        soup =  extract_href_values (pages, headers)
        print(pages)
        # Extract company
        company_element = soup.find('p', class_='css-m5y22d eand5hi23')
        if company_element:
            company = company_element.text.strip()
        else:
            company_element = soup.find('a', class_='eand5hi23 css-z0abg7 epzkrr00')
            if company_element:
                company = company_element.get_text()
            else:
                company = None

        # Extract product name
        product_name = soup.find('h1', class_='css-vvorhm eand5hi26').text
        # Extract product code
        product_code = soup.find('p', class_='css-1jx4yjs e1b0kgj0').text
        # Extract average rating
        avg_rating_element = soup.find('div', class_='css-w44v8g e1tr9ty71')
        avg_rating = float(avg_rating_element['aria-label'].split(':')[1].split(' out')[0])
        # Extract reviews
        review_element = soup.find('button', class_='e1kxsblz1 css-yvs3kk e2ucisq0')
        if review_element:
            reviews_text = review_element.get_text(strip=True)

        # Use regular expression to extract the numeric value
            reviews_match = re.search(r'(\d+)', reviews_text)
            if reviews_match:
                reviews = int(reviews_match.group(1))
            else:
                reviews = None
        else:
            reviews = None

        # Extracting price


        # Extract selling price
        # selling_price_element = soup.find('p', class_='css-1v802j0 e1b0kgj0')
        # if selling_price_element:
        #     selling_price_text = selling_price_element.text.strip()
        #     selling_price = float(selling_price_text[1:])
        # else:
        #     selling_price = 0.0

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
        # Extract original price
        original_price_element = soup.find('p', class_='css-1bb4dcr e1b0kgj0')
        if original_price_element:
            original_price_text = original_price_element.text.strip()
            original_price = float(original_price_text[1:])
        else:
            original_price = selling_price

        # Extract saved price
        #saved_price_element = soup.find('p', class_='css-opziqa e1b0kgj0')
        #if saved_price_element:
        #    saved_price_text = saved_price_element.text.strip()
        #    saved_price = float(saved_price_text[1:])
        #else:
        #    saved_price= 0
        # Extract color and sales status
        color = soup.find('span', class_='css-1jtzzxv ecsh60z7').text

        # Sale status
        sales_status_element = soup.find('span', class_='css-1jjg44c ecsh60z6')
        if sales_status_element:
            sales_status= sales_status_element.text.strip()
        else:
            sales_status = None

        # Extract style details
        # style_div = soup.find('div', class_='css-17obbps e2gxgh90')
        # style_elements = style_div.find_all('p', class_='css-fger60 eohri892')
        # styles = [element.text for element in style_elements]
        # Extract composition
        #composition = soup.find('div', class_='css-14hvavs eohri893').find('p', class_='css-z5zkuw e1b0kgj0').text
        div_element = soup.find('div', class_='css-14hvavs eohri893')
        if div_element:
            p_element = div_element.find('p', class_='css-z5zkuw e1b0kgj0')
            if p_element:
                composition = p_element.text
            else:
                composition = "No composition found"
        else:
            composition = "No composition found"

       
        Company.append(company)
        Product_Name.append(product_name)
        Product_Code.append(product_code)
        Avg_Rating.append(avg_rating)
        Reviews.append(reviews)
        Selling_Price.append(selling_price)
        Original_Price.append(original_price)
        #Saved_Price.append(saved_price)
        Color.append(color)
        Sales_Status.append(sales_status)
        # Styles.append(styles)
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

# # Extract href values from class "css-jeyzxy e8trdjq0"
# href_elements = soup.find_all(class_="css-jeyzxy e8trdjq0")
# href_values = [element.get('href') for element in href_elements]

# # Extract the "number of pages" value from class "css-82gmvi e1ytuwls1"
# number_of_pages_element = soup.find(class_="css-82gmvi e1ytuwls1")
# number_of_pages_text = number_of_pages_element.get_text()
# number_of_pages = int(number_of_pages_text.split()[-1])  # Extracting the number after "of"

# # Generate and print href values for all numberOfPages
# for page_number in range(1, number_of_pages + 1):
#     href = f"/l/lingerie/nightwear?page={page_number}"
#     print(href)


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

data = {'Company': Company, 
        'Title': Product_Name, 
        'Average rating': Avg_Rating, 
        'Product Code' : Product_Code,
        'Reviews' : Reviews,
        'Selling Price': Selling_Price,
        'Orginal Price' : Original_Price,
        'Sales Status' : Sales_Status,
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

    
 


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import openpyxl

# Define the URL of the Flipkart microwave category page you want to scrape
url = 'https://www.flipkart.com/microwave-ovens/pr?sid=j9e,m38,o49'

# Define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Create lists to store the data
page_url = []
titles = [] 
oprices = [] 
ratings = [] 
producturls = []
brands = [] 
ratings_counts = []
reviews_counts = [] 
mrpprice = []
dimenstions =[]
general = []
capacity = []
type =[]
model = []
sellername = []
offerperc = []

# Send a GET request to the URL with the headers
response = requests.get(url, headers=headers, verify=False, timeout=30)

# Create a BeautifulSoup object from the response text
soup = BeautifulSoup(response.text, 'html.parser')

# Get all the pages
page_url = soup.find_all('a', class_='ge-49M')

# Get all product in the page
for page in page_url:
    link = page.get('href')
    ind_page_url = "https://www.flipkart.com" + link
    page_response = requests.get(ind_page_url, headers=headers, verify=False, timeout=30)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')
    product_urllists = page_soup.find_all('a', class_='_1fQZEK')

# For reach product extract the required details
    for product in product_urllists:
        link = product.get('href')
        product_url = "https://www.flipkart.com" + link
        product_response = requests.get(product_url, headers=headers, verify=False, timeout=30)
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        # Find the elements containing the data you want to extract
        # Title
        product_title = product_soup.find('span', class_='B_NuCI') 
        product_price_element = product_soup.find('div', class_='_30jeq3 _16Jk6d') 
        if product_price_element is not None:
            product_price = product_price_element.text
        else:
            product_price = None

        # Rating
        product_rating_element = product_soup.find('div', class_='_3LWZlK') 
        if product_rating_element is not None:
            product_rating = product_rating_element.text
        else:
            product_rating = None

        # MRP
        product_mrpprice_element = product_soup.find('div', class_='_3I9_wc _2p6lqe') 
        if product_mrpprice_element is not None:
            product_mrpprice = product_mrpprice_element.text
        else:
            product_mrpprice = None

        # Offer percentage
        product_off_element = product_soup.find('div', class_='_3Ay6Sb _31Dcoz')
        if product_off_element is not None:
         # If the element exists, extract the text
            product_off = product_off_element.text
        else:
            # If the element doesn't exist, set the value as null
            product_off = None
        
        #Finding Brand
        brand_element = product_soup.find('td', text='Brand')
        brand_name = None
        if brand_element:
            value_element = brand_element.find_next_sibling('td')
            if value_element:
                brand_li = value_element.find('li', class_='_21lJbe')
                brand_name = brand_li.text.strip() if brand_li else None
    
        # Rating and review count
        rating_span = product_soup.find('span', class_='_1lRcqv')
        rating_count = None
        review_count = None
        if rating_span:
            noof_rating = rating_span.find_next_sibling('span').text.strip()
            rating_match = re.search(r'(\d+(?:,\d+)*)\s+Ratings', noof_rating)
            review_match = re.search(r'(\d+(?:,\d+)*)\s+Reviews', noof_rating)

            rating_count = rating_match.group(1).replace(',', '') if rating_match else None
            review_count = review_match.group(1).replace(',', '') if review_match else None

        # Product dimension
        dimensions_element = product_soup.find('div', class_='flxcaE', text='Dimensions')
        ldimensions = []
        if dimensions_element:
            table = dimensions_element.find_next_sibling('table')
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    dimension_name = cols[0].text.strip()
                    dimension_value = cols[1].find('li', class_='_21lJbe').text.strip()
                    dimension = f"{dimension_name}: {dimension_value}"
                    ldimensions.append(dimension)
            ldimensions = ', '.join(ldimensions)
        else:
            ldimensions = None

        # Box Content
        box_element = product_soup.find('td', text='In The Box')
        box_content = None
        if box_element:
            value_element = box_element.find_next_sibling('td')
            if value_element:
                brand_li = value_element.find('li', class_='_21lJbe')
                box_content = brand_li.text.strip() if brand_li else None
        
        # Product capacity
        capcity_element = product_soup.find('td', text='Capacity')
        cap = None
        if capcity_element:
            value_element = capcity_element.find_next_sibling('td')
            if value_element:
                brand_li = value_element.find('li', class_='_21lJbe')
                cap = brand_li.text.strip() if brand_li else None 

        # Product Type 
        type_element = product_soup.find('td', text='Type')
        type_name = None
        if type_element:
            value_element = type_element.find_next_sibling('td')
            if value_element:
                brand_li = value_element.find('li', class_='_21lJbe')
                type_name = brand_li.text.strip() if brand_li else None 

        #Find model
        model_element = product_soup.find('td', text='Model Name')
        model_name = None
        if model_element:
            value_element = model_element.find_next_sibling('td')
            if value_element:
                brand_li = value_element.find('li', class_='_21lJbe')
                model_name = brand_li.text.strip() if brand_li else None   

        # seller name
        seller_element = product_soup.find('div', id='sellerName')
        if seller_element:
            seller_name = seller_element.find('span').text.strip()
        else:
            seller_name = None


        # Append the data to the list
        if product_title:
            titles.append(product_title.text)
            oprices.append(product_price)
            ratings.append(product_rating)
            producturls.append(product_url)
            brands.append(brand_name)
            ratings_counts.append(rating_count)
            reviews_counts.append(review_count)
            mrpprice.append(product_mrpprice)
            dimenstions.append(ldimensions)
            general.append(box_content)
            capacity.append(cap)
            type.append(type_name)
            model.append(model_name)
            sellername.append(seller_name)
            offerperc.append(product_off)

# Create a pandas DataFrame from the extracted data
data = {'URL': producturls, 
        'Title': titles, 
        'Offer Price': oprices, 
        'MRP' : mrpprice,
        'Off' : offerperc,
        'Rating': ratings,
        'In the Box' : general,
        'Capacity' : capacity,
        'Type' : type,
        'Model' : model,
        'Seller Name' : sellername,
        'Brand': brands,
        'No of Ratings': ratings_counts, 
        'No of Reviews': reviews_counts, 
        'Dimensions' : dimenstions
        }

df = pd.DataFrame(data)

# Export the DataFrame to an CSV file
df.to_csv('microwave_flipkart_16_Juneee.csv', index=False)

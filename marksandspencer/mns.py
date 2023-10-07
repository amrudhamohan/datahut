import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from requests.exceptions import RequestException
'''
I have used below libraries for scraping, cleanup and exporting the data.
requests, BeautifulSoup, pandas, regular expressions, os and exceptions

'''

# Function to extract HTML and pass it using BeautifulSoup
def extract_href_values(url, headers, max_retries=3):
    """
    For any URL request we are using this function to get the html response and parse it with beautiful soup
    Incase of any failure response because of connectivity issue or any other network issues it will do retry 3 times.
    The function returns the parsed soup data.

    """
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

# Function to extract the number of pages
def extract_number_of_pages(soup):
    """
    From the main URL we find the number of pages using this function
    It finds the max number of pages and returns the number. 
    """
    try:
        pagination_span = soup.find('span', class_='css-82gmvi e1ytuwls1')
        if pagination_span:
            text = pagination_span.get_text()
            parts = text.split(' of ')
            if len(parts) == 2:
                return int(parts[1])
    except:
        return "No pages avalible"

# Function to scrape the product URL
def extract_product_url(baseUrl, pageUrls, headers):
    """
    Fuction itrates through each page URL and extract the product URL for each product.
    Returns all product URL's for the respective product
    """
    productUrl = []  # Initialize an empty list here
    for pages in pageUrls:
        soup = extract_href_values(pages, headers)
        try:
            product = soup.find_all('a', class_='css-mr86mw eenyued10')
            for link in product:
                urlextension = link.get('href')
                producturl = baseUrl + urlextension
                productUrl.append(producturl)
        except:
            productUrl = "Not avalible"

    return productUrl

# Function to scrape brand name
def extract_company(soup):
    try:
        company_element = soup.find('p', class_='css-m5y22d eand5hi23')
        if company_element:
            return company_element.text.strip()
    except Exception as e:
        print(f"An error occurred while extracting the company: {e}")
    
    try:
        company_element = soup.find('a', class_='eand5hi22 css-1lbjlfl epzkrr00')
        if company_element:
            return company_element.get_text()
    except Exception as e:
        print(f"An error occurred while extracting the company: {e}")

    return "Not avalible"

# Function to scrape product name
def extract_product_name(soup):
    try:
        product_name_element= soup.find('h1', class_='css-1rlzoae eand5hi25')
        if product_name_element:
            return product_name_element.get_text()
    except:
        return "Not avalible"

# Function to scrape product code
def extract_product_code(soup):
    try:
        product_code_element = soup.find('p', class_='css-1jx4yjs e1b0kgj0')
        if product_code_element:
            product_code_text = product_code_element.text
            # Scrape the product code
            product_code = product_code_text.split(': ')[-1]
            return product_code
    except:
        return "Not avalible"

# Function to scrape avg rating
def extract_avg_rating(soup):
    try:
        avg_rating_element = soup.find('div', class_='css-w44v8g e1tr9ty71')
        avg_rating = float(avg_rating_element['aria-label'].split(':')[1].split(' out')[0])
        return avg_rating
    except:
        return None

# Function to scrape reviews
def extract_reviews(soup):
    try:
        review_element = soup.find('button', class_='e1kxsblz1 css-yvs3kk e2ucisq0')
        if review_element:
            reviews_text = review_element.get_text(strip=True)
            reviews_match = re.search(r'(\d+)', reviews_text)
            if reviews_match:
                return int(reviews_match.group(1))
    except:
        return None

# Function to scrape selling price
def extract_selling_price(soup):
    """
    Price is having '£' symbol in it, aftr extracting the text the code will strip of £.
    Function returns float value 
    """
    try:
        # Check if "css-1l2oq8c ezee3i61" class exists
        selling_price_element = soup.find('p', class_='css-1l2oq8c ezee3i61')
        if selling_price_element:
            selling_price_text = selling_price_element.text.strip()
            selling_price = float(selling_price_text[1:])
            return selling_price
    except Exception as e:
        print(f"An error occurred while extracting selling price: {e}")

    try:
        # Use "css-ktq1e4 e1b0kgj0" class as fallback
        selling_price_element_fallback = soup.find('p', class_='css-1v802j0 e1b0kgj0')
        if selling_price_element_fallback:
            selling_price_text = selling_price_element_fallback.text.strip()
            selling_price = float(selling_price_text[1:])
            return selling_price
    except:
        return None

# Function to scrape original price
def extract_original_price(soup):
    """
    Price is having '£' symbol in it, aftr extracting the text the code will strip of £.
    Function returns float value 
    """
    try:
        original_price_element = soup.find('p', class_='css-ydfpcm ezee3i61')
        if original_price_element:
            original_price_text = original_price_element.text.strip()
            original_price = float(original_price_text[1:])
            return original_price
    except Exception as e:
        print(f"An error occurred while extracting original price: {e}")

    # If original price is not found, use selling price as fallback
    try:
        selling_price = extract_selling_price(soup)
        if selling_price is not None:
            return selling_price
    except:
        return None

# Function to scrape discount price
def extract_saved_price(soup):
    """
    Price is having '£' symbol in it, aftr extracting the text the code will strip of £.
    Function returns float value 
    """
    try:
        saved_price_element = soup.find('p', class_='css-opziqa e1b0kgj0')
        if saved_price_element:
            saved_price_text = saved_price_element.text.strip()
            saved_price_start = saved_price_text.find('£') + 1
            saved_price_value = saved_price_text[saved_price_start:]
            saved_price = float(saved_price_value)
            return saved_price
    except:
        return None

# Function to scrape product color
def extract_color(soup):
    try:
        return soup.find('span', class_='css-1jtzzxv ecsh60z7').text
    except:
        return "Not avalible"

# Function to scrape sales status
def extract_sales_status(soup):
    try:
        sales_status_element = soup.find('span', class_='css-1jjg44c ecsh60z6')
        if sales_status_element:
            return sales_status_element.text.strip()
    except:
        return "Not avalible"

# Function to scrape product composition
def extract_composition(soup):
    try:
        div_element = soup.find('div', class_='css-14hvavs eohri893')
        if div_element:
            p_element = div_element.find('p', class_='css-z5zkuw e1b0kgj0')
            if p_element:
                return p_element.text
    except:
        return "Not avalible"

# Scraping main function
def fetch_product_details(productUrls, headers):
    Company = []  # Define the Company list here
    Product_Name = []  # Define the Product_Name list here
    Product_Code = []  # Define the Product_Code list here
    Avg_Rating = []  # Define the Avg_Rating list here
    Reviews = []  # Define the Reviews list here
    Selling_Price = []  # Define the Selling_Price list here
    Original_Price = []  # Define the Original_Price list here
    Saved_Price = []  # Define the Saved_Price list here
    Color = []  # Define the Color list here
    Sales_Status = []  # Define the Sales_Status list here
    Composition = []  # Define the Composition list here

    for index, page in enumerate(productUrls, start=1):
        soup = extract_href_values(page, headers)
        print(page)
        print(f"Product count: {index}")
        
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

    return Company, Product_Name, Product_Code, Avg_Rating, Reviews, Selling_Price, Original_Price, Saved_Price, Color, Sales_Status, Composition

# Main function
def main():
    '''
    The code begins extracting the number of pages and the extract the next page URL from the main page.
    With this information it itrate through each page and extact all the product URL and store it in the list.
    To get the product details html is fetched for each product URL and parsed the output using beautiful soup.
    After extracting all the details the data is converted to dataframe and saved CSV using pandas
    '''
    ################### URL and header definition ###################

    # Define the URLs
    baseUrl = 'https://www.marksandspencer.com'
    mainUrl = f'{baseUrl}/l/lingerie/nightwear#intid=gnav_Lingerie_Nightwear_All-Nightwear'

    # Define the headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate'
    }

    ################# Extraction of page and product URLs ########################
    soup = extract_href_values(mainUrl, headers)  # function call

    numberOfPages = extract_number_of_pages(soup)  # function call
    if numberOfPages is not None:
        print(f"Number of Pages: {numberOfPages}")

    # Function to extract Page URLs
    href_elements = soup.find_all('a', class_='css-1vfr0rg e1is2euj0')
    pageUrls = []
    for page in range(1, numberOfPages + 1):
        href = href_elements[0]['href']
        page_number = href[-1]  # Get the last character of href
        href = href[:-1]  # Remove the last character from href
        page_url = f"{baseUrl}{href}{page}"
        pageUrls.append(page_url)

    # Extract product URLs from each page
    productUrls = extract_product_url(baseUrl, pageUrls, headers)  # function call
    print("Number of products:", len(productUrls))

    ################# Scrape product details ####################
    Company, Product_Name, Product_Code, Avg_Rating, Reviews, Selling_Price, Original_Price, Saved_Price, Color, Sales_Status, Composition = fetch_product_details(productUrls, headers)  # function call

    ############## Print the data to CSV ######################
    # Update the name of the items
    data = {
        'Brand': Company,
        'Title': Product_Name,
        'Product_Url': productUrls,
        'Average_rating': Avg_Rating,
        'Product_Code': Product_Code,
        'Reviews': Reviews,
        'Selling_Price': Selling_Price,
        'Orginal_Price': Original_Price,
        'Discount': Saved_Price,
        'Sales_Status': Sales_Status,
        'Composition': Composition
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Check if the file already exists
    if os.path.exists('mas.csv'):
        # Replace the file if it already exists
        df.to_csv('mas.csv', index=False, mode='w')
    else:
        # Export the DataFrame to a CSV file
        df.to_csv('mas.csv', index=False)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()

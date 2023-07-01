import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from fake_useragent import UserAgent

def get_headers():
    headers = {
        'User-Agent': user_agent.random,
        'Accept-Language': 'en-US,en;q=0.9',
    }
    return headers

def extract_href_values(url):
    max_retries = 10  # Maximum number of retries
    retry_count = 0
    headers = get_headers()
    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=30)
            if response.status_code == 503:
                # 503 error, retry the request
                retry_count += 1
                continue

            # Process the response here
            # ...
            break  # Break the loop if the request is successful

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print("Error:", e)
            break

    if retry_count == max_retries:
        print("Maximum retries reached. Request unsuccessful.")

    # Create a BeautifulSoup object from the response text
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Finding the Number of pages
    disabled_value = soup.find(class_='s-pagination-item s-pagination-disabled').text

    # Extracting the href value of the "Next" anchor element
    href = soup.find(class_='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator').get('href')

    disabled_value = int(disabled_value)  # Converting the disabled value to an integer

    for i in range(1, disabled_value + 1):
        modified_href = href.split('&')[0] + '&page=' + str(i)
        if 'sspa' not in modified_href:
            page_href.append(modified_href)

    time.sleep(1)

    # Extract href value for all Microwaves
    for page in page_href:
        ind_page_url = "https://www.amazon.in" + page
        headers = get_headers() 
        page_response = requests.get(ind_page_url, headers=headers, verify=False, timeout=30)
        page_soup = BeautifulSoup(page_response.text, 'html.parser')
        ind_product_urls = page_soup.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        for div in ind_product_urls:
            link = div['href']
            if 'amazon' not in link :
                href_values.append(link)
    time.sleep(1)

    # Scrapping the data
    for product in href_values:
        product_url = "https://www.amazon.in" + product
        headers = get_headers() 
        retry_count = 0
        product_title = None
        
        while product_title is None and retry_count < 5:
            product_response = requests.get(product_url, headers=headers, verify=False, timeout=30)
            product_soup = BeautifulSoup(product_response.text, 'html.parser')
            product_title = product_soup.find('span', class_='a-size-large product-title-word-break')
            
            if product_title is None:
                retry_count += 1
        
        if product_title is not None:
            product_price = product_soup.find('span', class_='a-price-whole')
            price_element = product_soup.find('span', class_='a-price a-text-price')
            if price_element:
                product_mrpprice = price_element.find('span', class_='a-offscreen')
                if product_mrpprice:
                    mrps.append(product_mrpprice.text.strip() if product_mrpprice else None)
            else:
                mrps.append('null')

            offer_percentage = product_soup.find('span', class_='a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage')

            product_titles.append(product_title.text.strip() if product_title else None)
            wholeprice.append(product_price.text.strip() if product_price else None)

            product_urls.append(product_url)
            discount_percentages.append(offer_percentage.text.strip() if offer_percentage else None )

            #Product details table
            table = product_soup.find('table', id='productDetails_detailBullets_sections1')
            if table:
                rows = table.find_all('tr')

                data = {}
                for row in rows:
                    heading = row.find('th', class_='a-color-secondary').text.strip()
                    td = row.find('td')
                    value = td.text.strip() if td else None
                    data[heading] = value

                best_sellers_rank = data.get('Best Sellers Rank', 'null')
                date_first_available = data.get('Date First Available', 'null')
                packer = data.get('Packer', 'null')
                importer = data.get('Importer', 'null')
                asian = data.get('ASIN', 'null')
                customer_review = data.get('Customer Reviews', 'null')
                item_weight = data.get('Item Weight', 'null')
                item_dimension = data.get('Item Dimensions LxWxH', 'null')
                net_quality = data.get('Net Quantity', 'null')
                generic_name = data.get('Generic Name', 'null')
            else:
                best_sellers_rank = "null"
                date_first_available = "null"
                packer = "null"
                importer = "null"
                asian = "null"
                customer_review = "null"
                item_weight = "null"
                item_dimension = "null"
                net_quality = "null"
                generic_name = "null"

            # Append product details to the lists
            best_sellers_ranks.append(best_sellers_rank)
            date_first_availables.append(date_first_available)
            packers.append(packer)
            importers.append(importer)
            asians.append(asian)
            customer_reviews.append(customer_review)
            item_weights.append(item_weight)
            item_dimensions.append(item_dimension)
            net_qualitys.append(net_quality)
            generic_names.append(generic_name)

                # Product technical Specs table
            table = product_soup.find('table', id='productDetails_techSpec_section_1')
            if table:
                rows = table.find_all('tr')

                details = {}

                for row in rows:
                    heading = row.find('th').text.strip()
                    value = row.find('td').text.strip()
                    details[heading] = value

                brand = details.get('Brand', 'null')
                model = details.get('Model', 'null')
                capacity = details.get('Capacity', 'null')
                installation_type = details.get('Installation Type', 'null')
                part_number = details.get('Part Number', 'null')
                special_features = details.get('Special Features', 'null')
                oven_cooking_mode = details.get('Oven Cooking Mode', 'null')
                burner_type = details.get('Burner Type', 'null')
                colour = details.get('Colour', 'null')
                voltage = details.get('Voltage', 'null')
                wattage = details.get('Wattage', 'null')
                fuel_type = details.get('Fuel Type', 'null')
                door_orientation = details.get('Door Orientation', 'null')
                material = details.get('Material', 'null')
                included_components = details.get('Included Components', 'null')
                batteries_included = details.get('Batteries Included', 'null')
                batteries_required = details.get('Batteries Required', 'null')
                country_of_origin = details.get('Country of Origin', 'null')
            else:
                brand = "null"
                model = "null"
                capacity = "null"
                installation_type = "null"
                part_number = "null"
                special_features = "null"
                oven_cooking_mode = "null"
                burner_type = "null"
                colour = "null"
                voltage = "null"
                wattage = "null"
                fuel_type = "null"
                door_orientation = "null"
                material = "null"
                included_components = "null"
                batteries_included = "null"
                batteries_required = "null"
                country_of_origin = "null"
                # Append values to the lists
            brands.append(brand)
            models.append(model)
            capacitys.append(capacity)
            installation_types.append(installation_type)
            part_numbers.append(part_number)
            special_featuress.append(special_features)
            oven_cooking_modes.append(oven_cooking_mode)
            burner_types.append(burner_type)
            colours.append(colour)
            voltages.append(voltage)
            wattages.append(wattage)
            fuel_types.append(fuel_type)
            door_orientations.append(door_orientation)
            materials.append(material)
            included_componentss.append(included_components)
            batteries_includeds.append(batteries_included)
            batteries_requireds.append(batteries_required)
            country_of_origins.append(country_of_origin)

# Define the URLs
url = 'https://www.amazon.in/s?k=microwaves&rh=n%3A1380263031%2Cn%3A1380072031&dc&ds=v1%3AX0XSk4IZYj7dvTovmuPLULgNH2iJf1kyEz%2BRbPZRUV4&crid=310PRPGXV0PB9&qid=1687783381&rnid=3576079031&sprefix=microwaves%2Caps%2C712&ref=sr_nr_n_2'

user_agent = UserAgent()
# Define the headers

# Create lists to store the extracted data
# lists for General details
page_href = []
href_values = []
product_urls = []
product_titles = []
wholeprice = []
mrps = []
discount_percentages = []

# lists for product details
best_sellers_ranks = []
date_first_availables = []
manufacturers = []
packers = []
importers = []
asians = []
customer_reviews = []
item_weights = []
item_dimensions = []
net_qualitys = []
generic_names = []

# lists for  technical details
brands = []
models = []
capacitys = []
installation_types = []
part_numbers = []
special_featuress = []
oven_cooking_modes = []
burner_types = []
colours = []
voltages = []
wattages = []
fuel_types = []
door_orientations = []
materials = []
included_componentss = []
batteries_includeds = []
batteries_requireds = []
manufacturers = []
country_of_origins = []

# Extract href values from the first page
extract_href_values(url)

# Extract href values from the second page
#extract_href_values(url2)

#Scraping data from Iduvidual product URl's



# Create a DataFrame to store the extracted data
data = {
    'Product URL': product_urls,
    'Product Title': product_titles,
    'Product Price': wholeprice,
    'MRP Price': mrps,
    'Discount Percentage' : discount_percentages,
    'Best Sellers Rank': best_sellers_ranks,
    'Date First Available': date_first_availables,
    'Packer': packers,
    'Importer': importers,
    'ASIN': asians,
    'Customer Reviews': customer_reviews,
    'Item Weight': item_weights,
    'Item Dimensions': item_dimensions,
    'Net Quantity': net_qualitys,
    'Generic Name': generic_names,
    'Brand': brands,
    'Model': models,
    'Capacity': capacitys,
    'Installation Type': installation_types,
    'Part Number': part_numbers,
    'Special Features': special_featuress,
    'Oven Cooking Mode': oven_cooking_modes,
    'Burner Type': burner_types,
    'Colour': colours,
    'Voltage': voltages,
    'Wattage': wattages,
    'Fuel Type': fuel_types,
    'Door Orientation': door_orientations,
    'Material': materials,
    'Included Components': included_componentss,
    'Batteries Included': batteries_includeds,
    'Batteries Required': batteries_requireds,
    'Country of Origin': country_of_origins
}

df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_csv('amazon_data_last3.csv', index=False)

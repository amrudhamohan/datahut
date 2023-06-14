import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_href_values(url):
    # Send a GET request to the URL with the headers
    response = requests.get(url, headers=headers, verify=False, timeout=30)

    # Create a BeautifulSoup object from the response text
    soup = BeautifulSoup(response.text, 'html.parser')

    divs = soup.find_all('div', class_=lambda value: value and 'sg-col-4-of-24' in value and 'sg-col-4-of-12' in value)

    for div in divs:
        link = div.find('a', class_='a-link-normal s-no-outline')
        if link:
            href = link['href']
            if 'wrong' not in href:
                href_values.append(href)

# Define the URLs
url1 = 'https://www.amazon.in/s?rh=n%3A84514739031&fs=true&ref=lp_84514739031_sar'
url2 = 'https://www.amazon.in/s?i=kitchen&rh=n%3A84514739031&fs=true&page=2&qid=1686482966&ref=sr_pg_2'

# Define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Create lists to store the extracted data
# lists for General details
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

# Extract href values from the first URL
extract_href_values(url1)

# Extract href values from the second URL
extract_href_values(url2)

#Scraping data from Iduvidual product URl's
for product in href_values:
    product_url = "https://www.amazon.in" + product
    product_response = requests.get(product_url, headers=headers, verify=False, timeout=30)
    product_soup = BeautifulSoup(product_response.text, 'html.parser')

    product_title = product_soup.find('span', class_='a-size-large product-title-word-break')
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
df.to_excel('amazon_data_last.xlsx', index=False)

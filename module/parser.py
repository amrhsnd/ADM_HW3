from bs4 import BeautifulSoup
import os
import csv

def extract_info_from_html(file_path, index):
    """
    Extracts the required information from an HTML file.

    Args:
        file_path (str): The path to the HTML file.
        index (int): The index for the restaurant entry.

    Returns:
        dict: A dictionary containing the extracted information.
        
    """
    with open(file_path, 'r', encoding='utf-8') as file:

        soup = BeautifulSoup(file, 'lxml')  # or use 'html.parser'
        
        # Prepare a dictionary to hold the extracted information
        extracted_info = {
            "index": index,
            "restaurantName": "",
            "address": "",
            "city": "",
            "postalCode": "",
            "country": "",
            "priceRange": "",
            "cuisineType": "",
            "description": "",
            "creditCards": "",
            "facilitiesServices": "",
            "phoneNumber": "",
            "website": "",
        }

        # Extract the restaurant name
        title = soup.find('h1', class_='data-sheet__title')
        extracted_info["restaurantName"] = title.text.strip()
        
        info_div = soup.findAll('div', class_='data-sheet__block--text')
        # Extract the address, city, postal code, country
        address = info_div[0].text.strip().split(',')

        # Reverse the address list and split it into 4 parts (Country, Postal Code, City, Address)
        address = (','.join(address[::-1])).split(',',3)
        extracted_info["address"] = ','.join((address[3].split(','))[::-1])
        extracted_info["city"] = address[2]
        extracted_info["postalCode"] = address[1]
        extracted_info["country"] = address[0]


        # Extract price range and cuisine type
        price_and_type = info_div[1].text.strip().split('·')
        extracted_info["priceRange"] = price_and_type[0].strip()
        extracted_info["cuisineType"] = price_and_type[1].strip()

        # Extract description
        description_div = soup.find('div', class_='data-sheet__description')
        extracted_info["description"] = description_div.text.strip()

        # Extract facilities and services
        extracted_info["facilitiesServices"] = []
        services_div = soup.find_all('div', class_='restaurant-details__services')
        if services_div:
            list_of_services = services_div[0].find_all('li') # Get all list items
            for item in list_of_services:
                extracted_info["facilitiesServices"] += [item.text.strip()]

        # Extract phone number and website
        extra_info = soup.find_all('a', class_='link js-dtm-link')
        extracted_info["website"] = extra_info[-1].get('href')
        extracted_info["phoneNumber"] = extra_info[-2].get('href').replace('tel:', '')
        

        # Extract credit cards
        extracted_info["creditCards"] = []
        credit_cards_div = soup.findAll('div', class_='list--card')
        if credit_cards_div:
            imgs = (credit_cards_div)[0].find_all('img')
            for img in imgs:
                name = img.get('data-src')
                extracted_info["creditCards"] += [name.split('/')[-1].split('-')[0].capitalize()]

        return extracted_info


def tsv_extractor(start_dir, dest_dir, start_index, keys):
    """
    Extracts the required information from all HTML files in a directory and writes it to TSV files.

    Args:
        start_dir (str): The directory containing the HTML files.
        dest_dir (str): The directory where the TSV files will be written.
        start_index (int): The starting index for the restaurant entries.
        keys (list): The keys for the TSV file.
    
    Returns:
        None

    """
   
    for index, filename in enumerate(os.listdir(start_dir), start=1):
        if filename.endswith('.html'):
            file_path = os.path.join(start_dir, filename)
            new_file_path = os.path.join(dest_dir, f'restaurant_{start_index+index}.tsv')
            
            info = [extract_info_from_html(file_path, start_index+index)]

            with open(new_file_path, 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, keys, delimiter='\t')
                dict_writer.writeheader()
                dict_writer.writerows(info)

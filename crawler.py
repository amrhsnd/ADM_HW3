import scrapy
import os
import requests

class UrlMichelin(scrapy.Spider):
    '''
    A spider to crawl the URLs of the restaurants from the Michelin Guide website
    
    Attributes:
        name (str): The name of the spider
        start_urls (list): The start URLs for the spider to crawl
    
    Methods:
        parse(self, response): Parse the response from the start URLs and write the URLs to a .txt file
    
    '''
    name = 'url_michelin_spider'

    # Define the start URLs for the spider to crawl
    start_urls = [f'https://guide.michelin.com/en/it/restaurants/page/{i}' for i in range(1, 103)] # The range is 1 to 102 because there are 102 pages of restaurants

    def parse(self, response):
        #The selector "div.col-md-6 > div:nth-child(1) > a:nth-child(3)" is used to select the anchor element that contain the URL of the restaurants
        restaurants = response.css('div.col-md-6 > div:nth-child(1) > a:nth-child(3)')

        # Write the URLs to a .txt file
        with open('urls.txt', 'a') as f:     
            for restaurant in restaurants:
                # Get the full URL, joining the relative URL, stored in the href attribute of the anchor element, with the base URL of the website
                url = response.urljoin(restaurant.attrib['href'])  
                page_num = response.url.split("/")[-1]  # Get the page number from the URL
                f.write(f'{url}|{page_num}\n')  # Write the URL to the file with the page number


def make_folders(last_page):
    '''
    Create folders to store the HTML files, numebered from 1 to last_page

    Parameters:
        last_page (int): The number of the last page of the website

    Returns:
        None
    '''
    for i in range(1, last_page+1):
        os.makedirs(f'page_{i}', exist_ok=True)


def HTML_downloader(url, page_num):
    '''
    Download the HTML files from the URLs and store them in the corresponding folder
    
    Parameters:
        page_num (int): The number of the page of the website
        url (str): The URL of the website
    
    Returns:
        None
    '''
   
    # Send a GET request to the URL
    response = requests.get(url)

    # Get the name of the HTML file from the URL
    html_name = url.split("/")[-1]

    # Create the path of the file
    file_path = os.path.join('page_' + str(page_num), f'{html_name}.html')

    # Write the HTML content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response.text)





     


import os
import django
import random
import time
import re
import requests


# Set up Django environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from server.services import ProductService
from server.models import Product
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())

# Initialize Selenium WebDriver
chromedriver_path = r'C:\Users\amish\Documents\btp_api\chromedriver-win64\chromedriver.exe'

# chromedriver_path = 'C:\\Users\\amish\\Documents\\btp_api\\chromedriver-win64\\chromedriver.exe'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Scrape data
#from robu.in
def scrape_all_pages(driver, url):
    driver.get(url)
    all_product_data = []

    # while True:
    #     # Wait until the products are loaded
    #     WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//h2[@class="woocommerce-loop-product__title"]')))

        # Extract data on the current page
    prices = driver.find_elements(By.XPATH, '//span[@class="price"]')
    # images = driver.find_elements(By.XPATH, '//div[@class="product-thumbnail product-item__thumbnail"]')
    titles = driver.find_elements(By.XPATH, '//h2[@class="woocommerce-loop-product__title"]')
    links = driver.find_elements(By.XPATH, '//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')

    # Collect data
    for i in range(len(prices)):
        price_text = prices[i].text.strip()
        # image_url = images[i].find_element(By.TAG_NAME, 'img').get_attribute('src')
        title_text = titles[2*i+1].text.strip()
        link_href = links[2*i].get_attribute('href')
        
        all_product_data.append([price_text, title_text, link_href])

        # Check if there is a next page button and click it
        # try:
        #     next_button = driver.find_element(By.XPATH, '//a[@class="page-numbers"]')
        #     print('moving to next page')
        #     next_button.click()
        # except:
        #     # If there is no next button, break the loop
        #     print('no next page')
        #     break

    return all_product_data

url = 'https://robu.in/product-category/electronic-components/inductor/fixed-value-inductors/'

    # Call the function to scrape all pages
# prices_list = scrape_all_pages(driver, url)

# Print or process the scraped data
# for item in prices_list:
#     print(item)

##from digi-key
def digikey(driver):
    prices_list2=[]

    driver.get('https://www.digikey.in/en/products/filter/fixed-inductors/71?s=N4IgTCBcDaIJYDsAmBXAxgFwPYCcDOIAugDQgCsUoADlAIylU2S0AMLAvu0A')
    title_ex = driver.find_elements(By.XPATH, '//div[@class="tss-css-7dp38y-productColExpandedDescription"]')
    # images1 = driver.find_element(By.ID, 'image_id')


# Extract the text inside the <div> within the <td> element
    inductor_value_ex = driver.find_elements(By.ID, "2087")
    # inductor_value_ex=driver.find_element(By.ID, "2087")
    curr_rating_ex = driver.find_elements(By.ID, '2088')
    core_ex=driver.find_elements(By.ID, '1221')
    link_href_ex= driver.find_elements(By.XPATH, '//a[@class="tss-css-41s5xv-productColExpandedPartNumber-anchor"]')
    price_ex=driver.find_elements(By.ID, '-101')
    for i in range(len(title_ex)):
        title=title_ex[i].text
        price=price_ex[i].text
        inductor_value=inductor_value_ex[i].text
        curr_rating=curr_rating_ex[i].text
        core=core_ex[i].text
        link_href = link_href_ex[i].get_attribute("href")

        prices_list2.append([title, price, inductor_value, curr_rating,core,link_href])

    return prices_list2

##from mouser.in
def mouser():
   
    import requests

    url = "https://api.mouser.com/api/v1/search/keyword"
    headers = {
        "Content-Type": "application/json",
        "apiKey": "f5058d4b-a63d-4314-ac9f-09e0418624fc"  
    }

    payload = {
        "SearchByKeywordRequest": {
            "keyword": "inductor",
            "records": 50,
            "startingRecord": 0,
            "searchOptions": "",
            "searchWithYourSignUpLanguage": "en"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        parts = data.get("SearchResults", {}).get("Parts", [])
        for part in parts:
            print(f"Manufacturer: {part['Manufacturer']}")
            print(f"Part Number: {part['ManufacturerPartNumber']}")
            print(f"Description: {part['Description']}")
            print(f"Availability: {part['Availability']}")
            print(f"DataSheetUrl: {part['DataSheetUrl']}")
            print("-" * 20)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


#from element-14
def element14(driver):
    prices_list3 = []
    driver.get('https://in.element14.com/c/passive-components/inductors/fixed-value-inductors')

    # Locate all product containers (adjust the div class if necessary)
    product_containers = driver.find_elements(By.XPATH, '//div[@class="ProductListerPageMobileElementstyles__ListerTableMobileElement-sc-gbb7ol-0 juoHcf"]')

    for product in product_containers:
        # Extract the title
        title = product.find_element(By.XPATH, './/div[@class="ProductListerPageMobileElementstyles__Description-sc-gbb7ol-14 jnppqh"]').text.strip()

        # Extract the first price
        try:
            # Find all price elements, then extract the first one
            prices = product.find_elements(By.XPATH, './/span[@class="PriceBreakupTableCellstyles__TaxAmount-sc-ylr3xn-2 yKzyS"]')
            price = prices[0].text.strip() if prices else "N/A"
        except:
            price = "N/A"

        # Extract the inductor value
        
        try:
            inductor_value1 = product.find_element(By.CSS_SELECTOR, '[data-testid="catalog.listerTable.extended-attrs-dropdown__Inductance"]').text.split('\n')
            inductor_value=inductor_value1[1]
        except:
            inductor_value = "N/A"

        # Extract the current rating
        try:
            curr_rating1 = product.find_element(By.CSS_SELECTOR, '[data-testid="catalog.listerTable.extended-attrs-dropdown__DC Current Rating"]').text.split('\n')
            curr_rating=curr_rating1[1]
        except:
            curr_rating = "N/A"

        try:
            # link_element = product.find_element(By.CSS_SELECTOR, '[data-testid="catalog.listerTable.product-link"]')
            link_element = product.find_element(By.CLASS_NAME, "ProductListerPageMobileElementstyles__ManNumberLink-sc-gbb7ol-8.cFxLGD")
    
    # Get the href attribute to retrieve the link
            relative_link = link_element.get_attribute('href')
            print(relative_link)
            link = relative_link
            #https://in.element14.com"+
        except Exception as e:
            print(f"Error occurred: {e}")
            link = "N/A"

        # Other details
        core = "NA"
        # catalog.listerTable.product-link
        link_href = link

        # Append to the list
        prices_list3.append([title, price, inductor_value, curr_rating, core, link_href])
    
    return prices_list3


def func():
    Product.objects.all().delete()
    # mouser()
    # prices_list4=[]
    # prices_list4.append(['Power Inductors - SMD 47UH 1.7A 177 MOHM SMD', '₹36.70', ['47UH'], ['1.7A'], 'ferrite', 'https://www.mouser.in/ProductDetail/Vishay-Dale/IFSC3232DBER470M02?qs=iLKYxzqNS743NLwMxrLEwQ%3D%3D'])
    # print(prices_list4[0])
    # ProductService.create_products4(prices_list4)
    prices_list3=element14(driver)
    print(prices_list3)
    
    ProductService.create_products3(prices_list3)
    
    prices_list = scrape_all_pages(driver, url)
    print(prices_list[0])
    
    prices_list2=digikey(driver)
    print(prices_list2[0])
    
    ProductService.create_products(prices_list)
    ProductService.create_products2(prices_list2)
    

    # delay = random.uniform(60, 180)  # Random delay between 60 to 120 seconds
    # time.sleep(delay)
    
    ##add this line laterrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    
func()
scheduler = BlockingScheduler()
scheduler.add_job(func, 'interval', seconds=3600)  # Execute my_task every 1 hr
scheduler.start()

# driver.quit()


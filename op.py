import os
import django
import random
import time



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


# Initialize Selenium WebDriver
chromedriver_path = r'C:\Users\amish\Documents\btp_api\chromedriver-win64\chromedriver.exe'
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
def mouser(driver):
    prices_list3=[]
    driver.get('https://www.mouser.in/c/passive-components/inductors-chokes-coils/power-inductors-smd/?q=inductors&core%20material=Ferrite&inductance=10%20nH~~120%20mH&rp=passive-components%2Finductors-chokes-coils%2Fpower-inductors-smd%7C~Inductance%7C~Core%20Material')
    title_ex = driver.find_elements(By.XPATH, '//td[@class="column desc-column hide-xsmall"]')
    ##tss-css-7dp38y-productColExpandedDescription
    inductor_value_ex = driver.find_elements(By.ID, "2087")
    curr_rating_ex = driver.find_elements(By.ID, '2088')
    # core_ex=driver.find_elements(By.ID, '1221')
    link_href_ex= driver.find_elements(By.ID, 'lnkMfrPartNumber_1')
    price_ex=driver.find_elements(By.ID, '-101')
    for i in range(len(price_ex)):
        title=title_ex[i].text
        price=price_ex[i].text
        inductor_value=inductor_value_ex[i].text
        curr_rating=curr_rating_ex[i].text
        core="ferrite"
        link_href = link_href_ex[i].get_attribute("href")

        prices_list3.append([title, price, inductor_value, curr_rating,core,link_href])

    return prices_list3

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
            inductor_value = product.find_element(By.CSS_SELECTOR, '[data-testid="catalog.listerTable.extended-attrs-dropdown__Inductance"]').text.strip()
        except:
            inductor_value = "N/A"

        # Extract the current rating
        try:
            curr_rating = product.find_element(By.CSS_SELECTOR, '[data-testid="catalog.listerTable.extended-attrs-dropdown__DC Current Rating"]').text.strip()
        except:
            curr_rating = "N/A"

        # Other details
        core = "NA"
        link_href = 'https://in.element14.com/c/passive-components/inductors/fixed-value-inductors'

        # Append to the list
        prices_list3.append([title, price, inductor_value, curr_rating, core, link_href])
    
    return prices_list3


def func():
    prices_list3=element14(driver)
    print(prices_list3)
    # Product.objects.all().delete()
    # prices_list = scrape_all_pages(driver, url)
    # print(prices_list[0])
    
    # prices_list2=digikey(driver)
    # print(prices_list2[0])
    
    # ProductService.create_products(prices_list)
    # ProductService.create_products2(prices_list2)

    # delay = random.uniform(60, 180)  # Random delay between 60 to 120 seconds
    # time.sleep(delay)
    
    ##add this line laterrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    
func()
scheduler = BlockingScheduler()
scheduler.add_job(func, 'interval', seconds=120)  # Execute my_task every 1 hr
scheduler.start()

# driver.quit()


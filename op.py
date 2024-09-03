import os
import django

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

    while True:
        # Wait until the products are loaded
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//h2[@class="woocommerce-loop-product__title"]')))

        # Extract data on the current page
        prices = driver.find_elements(By.XPATH, '//span[@class="price"]')
        images = driver.find_elements(By.XPATH, '//div[@class="product-thumbnail product-item__thumbnail"]')
        titles = driver.find_elements(By.XPATH, '//h2[@class="woocommerce-loop-product__title"]')
        links = driver.find_elements(By.XPATH, '//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')

        # Collect data
        for i in range(len(prices)):
            price_text = prices[i].text.strip()
            image_url = images[i].find_element(By.TAG_NAME, 'img').get_attribute('src')
            title_text = titles[2*i+1].text.strip()
            link_href = links[2*i].get_attribute('href')
            
            all_product_data.append([price_text, title_text, link_href, image_url])

        # Check if there is a next page button and click it
        try:
            next_button = driver.find_element(By.XPATH, '//a[@class="page-numbers"]')
            print('moving to next page')
            next_button.click()
        except:
            # If there is no next button, break the loop
            print('no next page')
            break

    return all_product_data

url = 'https://robu.in/product-category/electronic-components/inductor/fixed-value-inductors/'

    # Call the function to scrape all pages
prices_list = scrape_all_pages(driver, url)

# Print or process the scraped data
for item in prices_list:
    print(item)
##from element-14


# driver.get('https://in.element14.com/c/passive-components/inductors/fixed-value-inductors')
# prices1 = driver.find_elements(By.XPATH, '//span[@class="PriceBreakupTableCellstyles__TaxAmount-sc-ylr3xn-2 yKzyS"]')
# images1 = driver.find_elements(By.XPATH, '//img[@class="ProductImagestyles__Image-sc-1mj07db-1 bFOYXT product_image__plpMobile"]')
# titles1 = driver.find_elements(By.XPATH, '//div[@class="ProductListerPageMobileElementstyles__Description-sc-gbb7ol-14 jnppqh"]')
# # links = driver.find_elements(By.XPATH, '//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')


# for i in range(len(titles1)):
#     price_text = prices1[i].text.strip()
#     image_url = ''
#     title_text = titles1[i].text.strip()
#     link_href = 'https://in.element14.com/c/passive-components/inductors/fixed-value-inductors'
    
#     prices_list.append([price_text, title_text, link_href, image_url])
# Store data in the Django database
# print(prices_list[0])
def func():
    print(prices_list[0])
    Product.objects.all().delete()
    ProductService.create_products(prices_list)
    

scheduler = BlockingScheduler()
scheduler.add_job(func, 'interval', seconds=180)  # Execute my_task every 5 seconds
scheduler.start()

# driver.quit()


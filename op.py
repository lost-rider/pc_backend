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


# Initialize Selenium WebDriver
chromedriver_path = r'C:\Users\amish\Documents\btp_api\chromedriver-win64\chromedriver.exe'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Scrape data
driver.get('https://robu.in/product-category/electronic-components/inductor/fixed-value-inductors/')
prices = driver.find_elements(By.XPATH, '//span[@class="price"]')
images = driver.find_elements(By.XPATH, '//div[@class="product-thumbnail product-item__thumbnail"]')
titles = driver.find_elements(By.XPATH, '//h2[@class="woocommerce-loop-product__title"]')
links = driver.find_elements(By.XPATH, '//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')

prices_list = []

for i in range(len(prices)):
    price_text = prices[i].text.strip()
    image_url = images[i].get_attribute('src')
    title_text = titles[i].text.strip()
    link_href = links[i].get_attribute('href')
    
    prices_list.append([price_text, title_text, link_href, image_url])

# Store data in the Django database
print(prices_list[0])
Product.objects.all().delete()
ProductService.create_products(prices_list)
driver.quit()

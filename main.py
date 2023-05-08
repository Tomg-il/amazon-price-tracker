""" Amazon price tracker , check if the price is under the requested price and sent alert email
if the price is lower """
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
from twilio.rest import Client

PRODUCT_URL = "https://www.amazon.com/dp/B09NPTDXD1?pd_rd_i=B09NPTDXD1&pf_rd_p=b000e0a0-9" \
              "e93-480f-bf78-a83c8136dfcb&pf_rd_r=VS9MEX605FW93YXAFECY&pd_rd_wg=4CvCK&pd_rd_w" \
              "=lQ7VD&pd_rd_r=449ff2f8-bee1-4109-abda-0d5b39dd98fc"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/112.0.0.0 Safari/537.36"
ACCEPT = "text/html,application/xhtml+xml,application/xml;" \
         "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
PRODUCT_TARGET_PRICE = 40
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')


# get product page
def check_product_page_price():
    """ scribe the amazon page of the product to check if price is lower, if yes return the price"""
    # headers = {
    #     "user-agent": USER_AGENT,
    #     "accept": ACCEPT,
    # }
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(PRODUCT_URL)
    product_price = driver.find_element(By.CLASS_NAME, value="a-price-whole")
    product_price_fraction = driver.find_element(By.CLASS_NAME, value="a-price-fraction")

    last_price: float = int(product_price.text) + int(product_price_fraction.text) / 100
    print(last_price)
    return last_price


def send_price_alert(price):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                           to=os.environ.get('CELL_PHONE_NUMBER'),
                           body=f'The price for the surfe hat on Amazon dropped to {price} Go get '
                                f'it now!')
    print("SMS sent")


current_price = check_product_page_price()
if current_price < PRODUCT_TARGET_PRICE:
    send_price_alert(current_price)

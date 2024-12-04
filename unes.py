import random
import time
import logging
import csv

# import third party modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


""" Module documentation
"""


def chrome(mode='h'):
    '''A function to instantiate chrome driver with settings like that of a normal browser to improve stealth.

        :arguments: 
            mode: representing either headless (preferred) or browser mode.

        :returns: 
            driver: the driver instantiated.
    '''
    chrome_options = Options()
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # bypass OS security
    chrome_options.add_argument('--no-sandbox')
    # overcome limited resources
    chrome_options.add_argument('--disable-dev-shm-usage')
    # don't tell chrome that it is automated
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # select random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    if mode == 'h':
        #  Headless mode
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        
    elif mode == 'b':
        # Browser mode
        chrome_options.add_argument("start-maximized")
        driver = webdriver.Chrome(options=chrome_options)

    else:
        print("Mode is invalid")
        exit(0)
    
    logging.info('Instantiating a browser instance')
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


class Browser:
    """ Class to represent all browser actions
    """

    def __init__(self, driver, zip_code) -> None:
        """ Initializes the browser

            args:
                driver: an instantiated driver object
                zip_code: zip code of the city to scrape
        """
        self.driver = driver
        self.zip_code = zip_code
        self.action = ActionChains(driver)
        self.stores = []
        self.products = []
        self.current_store_name = ''
        self.number_of_stores = 0
        self.stores_counter = 0         # to keep track of the store currently being scrapped

        
    def navigate_to_stores(self) -> None:
        """ Navigates to page where stores are available for the provided zip code.
            Expected to run before scrape_stores
        """
        
        logging.info('Navigating to stores page')

        self.driver.get('https://www.spesaonline.unes.it/')
        time.sleep(2)

        # click accept cookies button
        self.driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
        logging.info('Clicked Accep all cookies button')

        # fill in the zip code
        self.driver.find_element(By.ID, "onboarding--bodySearchCap").send_keys(self.zip_code)
        time.sleep(2)
        logging.info('Filled in the zip code')

        # select location pop up
        self.action.send_keys(Keys.ARROW_DOWN)
        self.action.perform()
        self.action.send_keys(Keys.ENTER)
        self.action.perform()
        logging.info('Selected location pop up')
        time.sleep(2)

        self.driver.find_element(By.XPATH, '//*[@id="offcanvas__content--first"]/div/div[2]/div/div').click()
        time.sleep(2)

        self.stores = self.driver.find_elements(By.XPATH, '//div[@id="offcanvas__content--first"]/div/div[2]/div/div[2]/div')
        self.number_of_stores = len(self.stores)
        logging.info(f'There are {len(self.stores)} number of stores')


    def scrape_stores(self) -> None:
        """ Scrapes all stores available. Expected to run after navigate_to_stores
        """
        with open('stores.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Address', 'Withdrawal', 'Hours'])
            for store in self.stores:
                self.action.move_to_element(store).click().perform()
                name = store.find_element(By.XPATH, 'div/div/span').text.strip()
                address = store.find_element(By.XPATH, 'div/div[2]/span').text.strip()
                withdrawal = store.find_element(By.XPATH, 'div/div[3]/div/span/div').text.strip()
                hours = store.find_elements(By.XPATH, 'div[2]/div/div[1]/div/div[2]/div[2]/ul/li')
                if len(hours) > 1: hours = ', '.join([i.text.strip() for i in hours])
                writer.writerow([name, address, withdrawal, hours])
        time.sleep(2)


    def navigate_to_products_page(self) -> None:
        """ Navigates to page where all products are available. This is expected to run after scrape_stores
        """
        logging.info("Navigating to products' page")

        # click the first store
        first_store = self.stores[0]
        self.action.move_to_element(first_store).click().perform()
        
        self.current_store_name = first_store.find_element(By.XPATH, 'div/div/span').text.strip()
        self.stores_counter += 1

        # click "Conferma"
        self.driver.find_element(By.ID, 'onboarding__confirm').click()
        time.sleep(2)

        try:
            # click start shopping
            self.driver.find_element(By.XPATH, '//*[@id="firsttime__onboarding--modal"]/div/div/div/button[1]').click()
        except:
            # click proceed to change collection point
            self.driver.find_element(By.ID, 'confirm__storecc--sm').click()
        time.sleep(3)
        
        try:
            # press enter on the search bar to display all products 
            self.driver.find_element(By.XPATH, '//header/div[2]/div[2]/div[1]/div[2]/div[1]/div/input').click()
            time.sleep(2)
            self.action.send_keys(Keys.ENTER)
            self.action.perform()
        except Exception:
            logging.exception('Could not click the search bar: ')
            # visit the product category site instead
            self.driver.get('https://www.spesaonline.unes.it/search?query=')
        time.sleep(5)   # sleep to slow down requests so as to not trigger anti bot actions


    def return_to_stores_page(self) -> None:
        """ Returns to stores page. This is meant to run after scraping products for a zip code instance
        """
        # click on "Modifica"
        self.driver.find_element(By.XPATH, '//*[@id="onboarding__subheader"]/div/a[2]').click()
        time.sleep(3)

        # click on next store
        next_store = self.driver.find_elements(By.XPATH, '//main/div[2]/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div')[self.stores_counter]
        self.action.move_to_element(next_store).click().perform()
        self.current_store_name = next_store.find_element(By.XPATH, 'div/div/span').text.strip()
        self.stores_counter += 1

        # click "Conferma"
        self.driver.find_element(By.ID, 'onboarding__confirm').click()
        time.sleep(2)

        try:
            # click start shopping
            self.driver.find_element(By.XPATH, '//*[@id="firsttime__onboarding--modal"]/div/div/div/button[1]').click()
        except:
            # click proceed to change collection point
            self.driver.find_element(By.ID, 'confirm__storecc--sm').click()
        time.sleep(2)
        
        try:
            # press enter on the search bar to display all products
            # self.driver.find_element(By.XPATH, '//div[@id="smartAppBanner"]/div[2]/div/div[2]/div/div/input').click()
            self.driver.find_element(By.XPATH, '//header/div[2]/div[2]/div[1]/div[2]/div[1]/div/input').click()
            time.sleep(2)
            self.action.send_keys(Keys.ENTER)
            self.action.perform()
        except Exception:
            logging.exception('Could not click the search bar: ')
            # visit the product category site instead
            self.driver.get('https://www.spesaonline.unes.it/search?query=')
        time.sleep(5)   # sleep to slow down requests so as to not trigger anti bot actions


    def scrape_products(self) -> None:
        """
        """
        product_csv = csv.writer(open(f'{self.current_store_name} products.csv', 'w'))
        product_csv.writerow(['Name', 'Weight', 'Id', 'Details', 'Price', 'Price per Kg', 'Promotion Discount', 'Promotion End Date', 'Image Url'])

        x = 1
        while True:
            self.products = self.driver.find_elements(By.XPATH, '//*[@id="hits"]/div/div/ol/li')

            for product in self.products:
                logging.info(f'Scraping products {x} - {x + 23}')
                self.action.move_to_element(product).perform()
                id = product.find_element(By.XPATH, 'article/div/div[2]/div/div/a').get_attribute('href')
                image_url = product.find_element(By.XPATH, 'article/div/div[2]/div/div/a/img').get_attribute('src')
                
                name_and_weight = [i.strip() for i in product.find_element(By.XPATH, 'article/div/div[2]/div[2]/div[2]/a').text.strip().split(',')]
                name = name_and_weight[0]
                try: weight = name_and_weight[1]
                except: weight = ''
                
                details = product.find_element(By.XPATH, 'article/div/div[2]/div[2]/div[4]').text.strip()
                price = product.find_element(By.XPATH, 'article/div/div[2]/div[2]/div[5]/span[2]').text.strip()
                price_per_kg = [i.strip() for i in product.find_element(By.XPATH, 'article/div/div[2]/div[2]/div[4]').text.strip().split()][-2]
                try: 
                    promotion_discount = product.find_element(By.XPATH, 'article/div/div/div/span').text.strip()[1:]
                    promotion_end_date = product.find_element(By.XPATH, 'article/div/div/p').text.strip().split()[-1]
                except Exception: promotion_discount, promotion_end_date = '', ''
                product_csv.writerow([name, weight, id, details, price, price_per_kg, promotion_discount, promotion_end_date, image_url])
                x += 1

            try: 
                next_button  = self.driver.find_elements(By.XPATH, '//*[@id="pagination"]/div/ul/li')[-2].find_element(By.TAG_NAME, 'a')
                self.action.move_to_element(next_button).click().perform()
            except Exception:
                logging.exception('Could not click on the next buutton')
                break
            time.sleep(2)   # sleep to slow down requests so as to not trigger anti bot actions


def main():
    """ Main method
    """
    logging.basicConfig(filename='logfile.log', filemode='w', format='%(asctime)s - %(message)s',\
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
    driver = chrome()
    Unes = Browser(driver, '20121')
    Unes.navigate_to_stores()
    Unes.scrape_stores()
    for i in range(Unes.number_of_stores):
        if i == 0: Unes.navigate_to_products_page()
        else: Unes.return_to_stores_page()
        Unes.scrape_products()


if __name__ == "__main__":
    main()
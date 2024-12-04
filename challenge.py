import re
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

    def __init__(self, driver) -> None:
        """ Initializes the browser

            args:
                driver - an instantiated driver object
        """
        self.driver = driver
        self.zip_code = '20121'
        self.action = ActionChains(driver)
            

    def scrape_stores(self) -> None:
        """ Scrapes all stores available
        """
        self.driver.get('https://www.spesaonline.unes.it/')

        # click accept cookies button
        self.driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()

        # fill in the zip code
        self.driver.find_element(By.ID, "onboarding--bodySearchCap").send_keys(self.zip_code)

        # select location pop up
        self.action.send_keys(Keys.DOWN, Keys.ENTER).perform()

        stores = self.driver.find_elements(By.XPATH, '//div[@id="offcanvas__content--first"]/div/div[2]/div/div[2]/div')

        with open('stores.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Address', 'Withdrawal'])
            for store in stores:
                name = store.find_element(By.XPATH, 'div/div/span').text.strip()
                address = store.find_element(By.XPATH, 'div/div[2]/span').text.strip()
                withdrawal = store.find_element(By.XPATH, 'div/div[3]/div/span/div').text.strip()
                self.action.move_to_element(store).click().perform()
                hours = ', '.join([i.strip() for i in store.find_elements(By.XPATH, '/div[2]/div/div[1]/div/div[2]/div[2]/ul/li')])
                writer.writerow([name, address, withdrawal, hours])


    def scrape_products(self) -> None:
        """
        """
        # click the first store
        self.action.move_to_element(self.stores[0]).click().perform()

        # click "He confirms"
        self.driver.find_element(By.ID, 'onboarding__confirm').click()

        try:
            # click start shopping
            self.driver.find_element(By.XPATH, '//*[@id="firsttime__onboarding--modal"]/div/div/div/button[1]').click()
        except:
            # click proceed to change collection point
            self.driver.find_element(By.ID, 'confirm__storecc--sm').click()
        
        






def main():
    pass


if __name__ == "__main__":
    main()
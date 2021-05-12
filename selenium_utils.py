from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def make_driver(profile=2, version='Windows'):
    chromeOptions = Options()
    #chromeOptions.add_argument('window-size=1920x1080')
    #chromeOptions.add_argument("disable-gpu")
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("'--disable-setuid-sandbox'")
    #chromeOptions.add_argument('headless')
    chromeOptions.add_argument('--no-proxy-server')
    chromeOptions.add_argument("--proxy-server='direct://'")
    chromeOptions.add_argument("--proxy-bypass-list=*")
    chromeOptions.add_argument('--ignore-certificate-errors')
    chromeOptions.add_argument('--ignore-certificate-errors-spki-list')
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument("--start-maximized")
    chromeOptions.add_argument('--ignore-ssl-errors')
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(executable_path='chromedriver', options=chromeOptions, service_log_path='NUL')

def load(driver):  
    def _load(token, options='xpath', duration=2):
        waiter = WebDriverWait(driver, duration)
        if options == 'xpath':
            
            return waiter.until(EC.visibility_of_element_located((By.XPATH, token)))
        if options == 'tag':
            return waiter.until(EC.presence_of_element_located((By.TAG_NAME, token)))
        if options == 'text':
            return waiter.until(EC.presence_of_element_located((By.LINK_TEXT, token)))
        if options == 'class':
            return waiter.until(EC.presence_of_element_located((By.CLASS_NAME, token)))
        if options == 'css':
            return waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, token)))
    return _load

def load_all(driver):
    waiter = WebDriverWait(driver, 10)
    def _load_all(token, options='class'):
        if options == 'class':
            return waiter.until(EC.presence_of_all_elements_located((By.CLASS_NAME, token)))
        if options == 'xpath':
            return waiter.until(EC.presence_of_all_elements_located((By.XPATH, token)))
        if options == 'tag':
            return waiter.until(EC.presence_of_all_elements_located((By.TAG_NAME, token)))  
        if options == 'css':
            return waiter.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, token)))      
    return _load_all

def click(driver):
    waiter = WebDriverWait(driver, 10)
    def _click(token, options='xpath'):
        if options == 'xpath':
            return waiter.until(EC.element_to_be_clickable((By.XPATH, token))).click
        if options == 'tag':
            return waiter.until(EC.element_to_be_clickable((By.TAG_NAME, token))).click
        if options == 'text':
            return waiter.until(EC.element_to_be_clickable((By.LINK_TEXT, token))).click
        if options == 'class':
            return waiter.until(EC.element_to_be_clickable((By.CLASS_NAME, token))).click
        if options == 'css':
            return waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, token))).click
    return _click

def select(token, driver, options='xpath'):
    if options == 'xpath':
        return Select(driver.find_element_by_xpath(token))
    if options == 'tag':
        return Select(driver.find_element_by_tag(token))
    if options == 'class':
        return Select(driver.find_element_by_class_name(token))
    if options == 'css':
        return Select(driver.find_element_by_css_selector(token))

def wait_for_url(driver):
    
    def _wait_for_url(new_url, duration):
        waiter = WebDriverWait(driver, duration)
        waiter.until(EC.url_matches(new_url))
    return _wait_for_url
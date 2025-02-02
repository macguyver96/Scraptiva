# Uses selenium chrome driver to perform actions on Factiva web pages.

import src.config as config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By


# initiate a new chrome driver
def get_chrome_driver():
    options = webdriver.ChromeOptions()
    # the following two options are added so that headless can work on mac
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    #options.headless = True if config.headless else False
    driver = webdriver.Chrome(executable_path=config.chrome_webdriver_location, chrome_options=options)
    driver.implicitly_wait(config.implicit_wait_time)
    return driver


# based on the search criteria specified in config, enter the search information into Factiva.
def enter_search_criteria(driver):

    # Enter elements in search box
    #driver.find_element_by_class_name('ace_text-input').send_keys(role)

    # Enter the date range
    driver.find_element(By.XPATH, "//select[@name='dr']/option[@value='Custom']").click()
    for key, value in config.search_criteria['time'].items():
        driver.find_element(By.NAME, key).send_keys(value)

    # Choose the Duplicate (Identical)
    driver.find_element(By.XPATH, "//select[@name='isrd']/option[@value='High']").click()

    # Enter the Source
    # The default is the first option that appears on the list, except for Fortune, which is the 5th
    driver.find_element(By.XPATH, "//td[@id = 'scTab']/div[@class = 'pnlTabArrow']").click()
    for source in config.search_criteria['sources']:
        sleep(0.1)
        element = driver.find_element(By.ID, 'scTxt')
        element.send_keys(source)
        sleep(2)
        element.send_keys(Keys.ARROW_DOWN)

        # based on the choice of article source, the source we want does not necessary
        # be the first one on the dropdown list. So when adding additional sources, check it on Factiva first
        if source == "Fortune":
            for i in range(4):
                element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)


    # Enter the Subject
    # The default is the first option that appears on the list
    driver.find_element(By.XPATH, "//td[@id = 'nsTab']/div[@class = 'pnlTabArrow']").click()
    for source in config.search_criteria['subjects']:
        sleep(0.1)
        element = driver.find_element(By.ID, 'nsTxt')
        element.send_keys(source)
        sleep(2)
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

    # Languages
    # Remove English
    try:
        driver.find_element(By.XPATH, "//td[@id = 'laLst']/div/ul/li/div[@companyid = 'la_en']").click()
    except:
        print("No English Found!")
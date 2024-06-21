from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller
import time
import pandas as pd

companies_df = pd.read_csv('companies.csv') # replace with the path to your file
companies = companies_df['Companies'].tolist()

def main():
    company_dict: {str, str} = {}
    driver = webdriver.Chrome()
    for c in companies:
        driver.get(f"https://www.bing.com/search?q={c}")
        driver.implicitly_wait(5)
        try:
            first_result = driver.find_element(By.XPATH, '(//h2/a)[1]')

            # checks to see if the company name appears in the bulk of the url and not wikipedia.com/said_company
            if c.split()[0].lower() in first_result.get_attribute('href').split('.')[1].lower() or \
                c.split()[1].lower() in first_result.get_attribute('href').split('.')[1].lower():
                company_dict[c] = first_result.get_attribute('href')
            else:
                company_dict[c] = "NA"
            
        except NoSuchElementException:
            company_dict[c] = "NA"
        #print(f"{c} : {first_result}")
    print(company_dict)
    new_companies = pd.DataFrame({'Companies': company_dict.keys(), 'Links': company_dict.values()})
    new_companies.to_csv('companies_with_Links.csv', index= False)
    
        
main()


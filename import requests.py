from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

website = 'https://www.amazon.com/'
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(25)
driver.get(website)
captcha_link = driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute('src')
captcha = AmazonCaptcha.fromlink(captcha_link)
captcha_value = AmazonCaptcha.solve(captcha)
input_field = driver.find_element(By.ID, 'captchacharacters').send_keys(captcha_value)
driver.find_element(By.CLASS_NAME, 'a-button-text').click()
driver.find_element(By.ID, 'twotabsearchtextbox').send_keys('books')
driver.find_element(By.ID, 'nav-search-submit-button').click()

English_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'English').click()
German_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'German').click()
French_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'French').click()
Spanish_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'Spanish').click()
ASINs = []

def paperback():
    paperback_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'Paperback').click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 's-main-slot')))

    # Get all result blocks
    results = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    # Print first 5 titles
    current_page = driver.current_url
    titles = []
    

    for result in results:
                title = result.find_element(By.TAG_NAME, "h2").text
                titles.append(title)
    print(titles)
    for i in range(len(results)+1):
        results = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
        try:
            href = results[i].find_element(By.LINK_TEXT, titles[i]).get_attribute("href")
            driver.execute_script(f"window.open('{href}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            ASIN = ""
            try:
                ASIN_parent = driver.find_element(By.CLASS_NAME, 'detail-bullets-wrapper').find_elements(By.TAG_NAME, 'li') #.find_element(By.CLASS_NAME, 'a-list-item').find_elements(By.TAG_NAME, 'span')
                for li in ASIN_parent:
                    spans = li.find_element(By.CLASS_NAME, 'a-list-item').find_elements(By.TAG_NAME, 'span')
                    if spans[0].text == "ASIN :" :
                        ASIN = spans[1].text
                        ISBN = ""
                        ASINs.append({"Book Name":titles[i] ,"ASIN" : spans[1].text, "ISBN": ISBN})
                        break
                    elif spans[0].text == "ISBN-13 :" :
                        ISBN = spans[1].text
                        ASIN = ""
                        ASINs.append({"Book Name":titles[i] ,"ASIN" : ASIN, "ISBN": ISBN})
                        break
            except:
                try:
                    ASIN = driver.find_element(By.CLASS_NAME, 'a-keyvalue').find_element(By.ID, 'detailsAsin').find_element(By.TAG_NAME, 'td').find_element(By.TAG_NAME, 'span').text
                    ISBN = ""
                    ASINs.append({"Book Name":titles[i] ,"ASIN" : ASIN, "ISBN": ISBN})
                except:
                    print(f"..............ASIN not found...........")
                
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            print("No title found in this result.")
    next_page_li = driver.find_element(By.CLASS_NAME, "s-pagination-container").find_elements(By.TAG_NAME, "li")
    print(ASINs)
    next_page_li[-1].find_element(By.LINK_TEXT,"Next").click()
    for li in next_page_li :
        try:
            li.find_element(By.LINK_TEXT,"Next").click()
            break
        except:
            continue
paperback()

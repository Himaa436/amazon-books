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
    next_found = True
    paperback_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'Paperback').click()
    #while(1):
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
    results = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    for i in range(len(results)+1):
        try:
            link_element = results[i].find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")

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
        except Exception as e:
            print(f"No title found or another error at index {i}: {e}")
            driver.switch_to.window(driver.window_handles[0])  # Always go back to main tab
            continue
#    next_page_li = driver.find_element(By.CLASS_NAME, "s-pagination-container").find_elements(By.TAG_NAME, "li")
#    for li in next_page_li :
#        try:
#            link = li.find_element(By.LINK_TEXT,"Next")
#            #if "disabled" in li.get_attribute("class") or link.get_attribute("aria-disabled") == "true":
#                #   print("Reached last page.")
#                #  next_found = False
#                # break
#            link.click()
#            break
#       except:
#            continue
    #if next_found == False:
        #   break     
paperback()
keys = ASINs[0].keys()
with open('C:/Users/PC/Desktop/hima/matches/matches_details.csv','w', newline='', encoding='utf-8-sig') as output_file:
    dict_writer = csv.DictWriter(output_file,keys)
    dict_writer.writeheader()
    dict_writer.writerows(ASINs)
    print("file created")

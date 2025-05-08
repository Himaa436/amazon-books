from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time
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
WebDriverWait(driver, 25)
driver.find_element(By.ID, 'twotabsearchtextbox').send_keys('books')
driver.find_element(By.ID, 'nav-search-submit-button').click()

def apply_language_filter(language):
    try:
        see_more_language = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="See more, Language"]'))
            )
        is_expanded = see_more_language.get_attribute("aria-expanded")
        if is_expanded == "false":
            see_more_language.click()
    except:
        print("languages toggle expended")
    wait = WebDriverWait(driver, 10)
    try:
        filter_element = wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, language))
        )
        filter_element.click()
    except:
        print(f"Filter for {language} not found or not clickable.")

apply_language_filter('English')
apply_language_filter('French')
apply_language_filter('German')
apply_language_filter('Spanish')

ASINs = []

def paperback():
    paperback_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'Paperback').click()
    while 1:
        prev_count = 0
        # Get all result listitem
        try:
            search_result = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
            )
        except TimeoutException:
            print("Timed out waiting for search results to load.")
            break
            
            # Handle fallback or exit
        main_message = search_result.find_element(By.XPATH, "//div[@cel_widget_id='MAIN-MESSAGING-0']").find_element(By.TAG_NAME, "h2").text
        if main_message != "Results":
            break
        results = search_result.find_elements(By.XPATH, ".//div[@role='listitem']")
        while True:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Let content load

            results = driver.find_elements(By.XPATH, ".//div[@role='listitem']")
            if len(results) == prev_count:
                break
            prev_count = len(results)
        
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 's-main-slot')))

        
        # Then find all list items within it
        if(len(results) == 0):
            break

        titles = []
        
        for result in results:
                    title = result.find_element(By.TAG_NAME, "h2").text
                    titles.append(title)
        i = 0
        
        for result in results:
            
            try:
                link_element = result.find_element(By.TAG_NAME, "a")
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
                        print(f"ASIN not found")
                    
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except:
                print("No title found in this result.")
            i += 1
        next_page_li = driver.find_element(By.CLASS_NAME, "s-pagination-container").find_elements(By.CLASS_NAME, "s-list-item-margin-right-adjustment")
        print(ASINs)
        next_element = next_page_li[-1].find_element(By.TAG_NAME, "a")
        href = next_element.get_attribute("href")
        driver.get(href)
paperback()
print(ASINs)
keys = ASINs[0].keys()
with open('C:/Users/PC/Desktop/amazon_books/books_details.csv','w', newline='', encoding='utf-8-sig') as output_file:
    dict_writer = csv.DictWriter(output_file,keys)
    dict_writer.writeheader()
    dict_writer.writerows(ASINs)
    print("file created")
    
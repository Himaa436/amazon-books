from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
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

def extract_asin_from_page():
    """Try multiple methods to extract ASIN or ISBN from the product page."""
    try:
        # Check table layout
        table = driver.find_element(By.ID, 'productDetails_detailBullets_sections1')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            key = row.find_element(By.TAG_NAME, 'th').text.strip()
            value = row.find_element(By.TAG_NAME, 'td').text.strip()
            if "ASIN" in key or "ISBN-13" in key:
                return value
    except:
        pass

    try:
        # Check bullet layout
        ul = driver.find_element(By.ID, 'detailBullets_feature_div')
        items = ul.find_elements(By.TAG_NAME, 'li')
        for item in items:
            text = item.text
            if "ASIN" in text or "ISBN-13" in text:
                return text.split(":")[-1].strip()
    except:
        pass

    try:
        # Fallback: regex from page source
        asin_match = re.search(r'"ASIN"\s*:\s*"(\w+)"', driver.page_source)
        if asin_match:
            return asin_match.group(1)
    except:
        pass

    return None

def paperback():
    ASINs.clear()
    try:
        paperback_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'Paperback').click()
    except:
        print("Could not apply paperback filter.")
        return

    while True:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 's-main-slot')))
        results = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
        titles = []

        for result in results:
            try:
                title = result.find_element(By.TAG_NAME, "h2").text
                titles.append(title)
            except:
                titles.append("")

        for i, result in enumerate(results):
            if not titles[i]:
                continue

            try:
                link_element = result.find_element(By.TAG_NAME, "a")
                href = link_element.get_attribute("href")

                driver.execute_script(f"window.open('{href}', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'body'))
                    )
                except TimeoutException:
                    print(f"Timeout loading page for: {titles[i]}")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                asin_or_isbn = extract_asin_from_page()
                if asin_or_isbn:
                    ASINs.append({"Book Name": titles[i], "ASIN": asin_or_isbn, "ISBN": ""})
                else:
                    print(f"..............ASIN not found for book: {titles[i]}")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Error processing book at index {i}: {e}")
                try:
                    driver.close()
                except:
                    pass
                driver.switch_to.window(driver.window_handles[0])
                continue

        # Try to go to the next page
        try:
            next_page = driver.find_element(By.CLASS_NAME, "s-pagination-container").find_element(By.LINK_TEXT, "Next")
            if "disabled" in next_page.get_attribute("class") or next_page.get_attribute("aria-disabled") == "true":
                print("Reached last page.")
                break
            next_page.click()
        except NoSuchElementException:
            print("No next page button found. Ending loop.")
            break
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            break
 
paperback()
keys = ASINs[0].keys()
with open('C:/Users/PC/Desktop/hima/asin/asin_details.csv','w', newline='', encoding='utf-8-sig') as output_file:
    dict_writer = csv.DictWriter(output_file,keys)
    dict_writer.writeheader()
    dict_writer.writerows(ASINs)
    print("file created")

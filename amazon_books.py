from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time
import threading
from tkinter import *
from selenium.common.exceptions import WebDriverException

root = Tk()
root.geometry('600x600')
root.title("Amazon Books scraping")

# Create a frame to hold the widgets
frame = Frame(root)
frame.pack(expand=True, fill='both')

# Create a label
main_label = Label(frame, text="Click the start button to start",padx=100,pady=50,font=20)
main_label.pack(pady=100)

page_label = Label(frame)
page_label.pack()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

website = 'https://www.amazon.com/'
driver = None
pages = None
ASINs = []
f = 0
stop_scraping = False
scraping_thread = None
scraping_state = False

def driver_is_alive(drv):
    try:
        return drv is not None and drv.session_id and len(drv.window_handles) > 0
    except WebDriverException:
        return False

def start_scraping_thread():
    global f
    global scraping_thread, stop_scraping, ASINs,scraping_state
    if(stop_scraping or not driver_is_alive(driver)) and f == 0:
        
        ASINs = []
        stop_scraping = False
        wait_label.config(text="")
        page_label.config(text="")
        f = 0
        scraping_state = True
        scraping_thread = threading.Thread(target=scraping)
        scraping_thread.start()

def scraping ():

    global driver
    global ASINs
    global f

    main_label.config(text="Scraping started")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(25)
    driver.get(website)
    print(f"...............{len(driver.window_handles)}.............")
    captcha_link = driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute('src')
    captcha = AmazonCaptcha.fromlink(captcha_link)
    captcha_value = AmazonCaptcha.solve(captcha)
    input_field = driver.find_element(By.ID, 'captchacharacters').send_keys(captcha_value)
    driver.find_element(By.CLASS_NAME, 'a-button-text').click()
    WebDriverWait(driver, 25)
    driver.find_element(By.ID, 'twotabsearchtextbox').send_keys('books')
    driver.find_element(By.ID, 'nav-search-submit-button').click()

    def apply_language_filter(language):
        if (stop_scraping or not driver_is_alive(driver)) and f == 0:
                wait_label.config(text="Please wait...")
                page_label.config(text="")
                f = 1
                print("🛑 Scraping stopped by user.")
                driver.quit()
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
    if (stop_scraping or not driver_is_alive(driver)) and f == 0:
                    f = 1
                    wait_label.config(text="Please wait...")
                    page_label.config(text="")

                    stop_and_export()
                    print(f".............{1}🛑 Scraping stopped by user.")
    if(f == 0):
        apply_language_filter('English')
        apply_language_filter('French')
        apply_language_filter('German')
        apply_language_filter('Spanish')

    
    
    
    
    def paperback():
        global pages
        global driver
        f = 0
        pages = 1
        paperback_filter = driver.find_element(By.ID, 's-refinements').find_element(By.PARTIAL_LINK_TEXT, 'Paperback').click()
        while 1:
            global stop_scraping
            if (stop_scraping or not driver_is_alive(driver)) and f == 0:
                f = 1
                wait_label.config(text="Please wait...")
                page_label.config(text="")
                print(f"...........{2}🛑 Scraping stopped by user.")
                stop_and_export()
                break
            prev_count = 0
            # Get all result listitem
            try:
                search_result = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
                )
            except TimeoutException:
                print("Timed out waiting for search results to load.")
                break

            page_label.config(text=f"Extracting data from page {pages} ...",font=8)    
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
                if (stop_scraping or not driver_is_alive(driver)) and f == 0:
                    f = 1
                    wait_label.config(text="Please wait...")
                    page_label.config(text="")
                    print("..........3🛑 Scraping stopped by user.")
                    break
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
            if f == 1:
                stop_and_export()
                break
            else:
                next_page_li = driver.find_element(By.CLASS_NAME, "s-pagination-container").find_elements(By.CLASS_NAME, "s-list-item-margin-right-adjustment")
                print(ASINs)
                next_element = next_page_li[-1].find_element(By.TAG_NAME, "a")
                href = next_element.get_attribute("href")
                driver.get(href)
                pages += 1
        
    paperback()
    print(ASINs)
    
    if(f == 0):
        stop_and_export()


wait_label = Label(frame)
wait_label.pack()
def stop_and_export():
    global driver  # make sure this is declared if you're modifying it

    keys = ASINs[0].keys()
    with open('C:/Users/PC/Desktop/amazon_books/books_details.csv','w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file,keys)
        dict_writer.writeheader()
        dict_writer.writerows(ASINs)
        print("file created")

    try:
        if driver_is_alive(driver):
            driver.quit()
    finally:
        driver = None  # <-- Important reset
        wait_label.config(text="")
        page_label.config(text="")
        main_label.config(text="Click the start button to start")
# Create a button
start_button = Button(frame, text="Start Scraping",padx=50,font=10,command=start_scraping_thread)
start_button.pack(pady=10)

end_button = Button(frame, text="End scraping and give the csv file",padx=50,font=10,command=stop_and_export)
end_button.pack(pady=10)

root.mainloop()

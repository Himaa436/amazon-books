# Amazon Book Details Scraper

This Python script uses Selenium to automate the process of searching for books on Amazon.com, applying various filters (language, format), navigating through product pages, and extracting details like Book Title, ASIN, and ISBN-13. The collected data is then saved into a CSV file.

## Features

*   **Automated Browsing**: Navigates Amazon.com.
*   **CAPTCHA Handling**: Attempts to solve Amazon's image CAPTCHA using the `amazoncaptcha` library.
*   **Search Functionality**: Searches for a predefined term (currently "books").
*   **Filter Application**:
    *   Applies language filters (English, French, German, Spanish).
    *   Applies format filter (Paperback).
*   **Data Extraction**:
    *   Extracts book titles from search result pages.
    *   Opens each book's product page in a new tab.
    *   Scrapes ASIN and/or ISBN-13 from the product details section.
*   **Pagination**: Navigates through multiple pages of search results.
*   **Infinite Scroll Handling**: Attempts to load all items on a search results page by scrolling down.
*   **CSV Export**: Saves the scraped data (Book Name, ASIN, ISBN) into a `books_details.csv` file.

## Prerequisites

*   Python 3.x
*   Google Chrome browser installed.
*   ChromeDriver:
    *   Ensure you have ChromeDriver installed and that its version matches your Google Chrome browser version.
    *   You can check your Chrome version by typing `chrome://version` in the Chrome address bar.
    *   Download ChromeDriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
    *   Make sure ChromeDriver is in your system's PATH, or place the `chromedriver.exe` (or `chromedriver` for Linux/macOS) in the same directory as the script.

## Setup

1.  **Clone the repository (or download the script):**
    ```bash
    git clone <https://github.com/Himaa436/amazon-books/>
    cd <Himaa436/amazon-books>
    ```
    Or simply save the Python script to a local directory.

2.  **Install required Python libraries:**
    Create a `requirements.txt` file with the following content:
    ```
    selenium
    amazoncaptcha
    ```
    Then install them using pip:
    ```bash
    pip install -r requirements.txt
    ```
    Or install them individually:
    ```bash
    pip install selenium amazoncaptcha
    ```

## Configuration

Before running the script, you might want to adjust:

1.  **Search Term**:
    Currently, the script searches for "books". You can change this line:
    ```python
    driver.find_element(By.ID, 'twotabsearchtextbox').send_keys('books')
    ```
    to search for a different term.

2.  **Output File Path**:
    The script saves the CSV file to a hardcoded path:
    ```python
    with open('C:/Users/PC/Desktop/amazon_books/books_details.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
    ```
    **Important:** Change `'C:/Users/PC/Desktop/amazon_books/books_details.csv'` to your desired path and filename. Make sure the directory exists, or the script might fail.

3.  **Language Filters**:
    The `apply_language_filter` function is called for specific languages. You can modify these calls:
    ```python
    apply_language_filter('English')
    apply_language_filter('French')
    apply_language_filter('German')
    apply_language_filter('Spanish')
    ```
    Note that applying multiple language filters like this will usually result in products that are tagged with *all* these languages, which might yield very few or no results. You might want to apply only one, or modify the logic to select one from a list.

## Usage

1.  Ensure ChromeDriver is accessible (in PATH or same directory).
2.  Modify the configuration parameters in the script as needed (especially the output file path).
3.  Run the script from your terminal:
    ```bash
    amazon_books.py
    ```
    (Replace `amazon_books.py` with the actual name of your Python file).

The script will open a Chrome browser window, navigate to Amazon, attempt to solve any CAPTCHA, perform the search, apply filters, and then start scraping. You will see progress printed to the console, and a `books_details.csv` file will be created at the specified location upon completion.

## Important Notes & Limitations

*   **CAPTCHA Reliability**: The `amazoncaptcha` library's success rate can vary. Amazon frequently updates its CAPTCHA mechanisms, which might break the solver.
*   **Website Structure Changes**: Web scraping scripts are sensitive to changes in the target website's HTML structure. If Amazon changes its layout, the XPaths and element selectors in this script might break and require updates.
*   **Rate Limiting/IP Bans**: Amazon employs measures to prevent aggressive scraping. Running the script too frequently or for too long might lead to temporary IP blocks or more persistent CAPTCHA challenges. Use responsibly and consider adding more significant delays (`time.sleep()`) if you encounter issues.
*   **Error Handling**: The script includes some `try-except` blocks, but it might not cover all possible edge cases or errors.
*   **"See More" for Languages**: The script tries to click "See more" for language filters. If this element's structure changes or if it's already expanded, it might not behave as expected.
*   **Dynamic Content Loading**: The script uses scrolling and `WebDriverWait` to handle dynamically loaded content, but complex loading scenarios might still pose challenges.
*   **Ethical Considerations**: Always respect Amazon's Terms of Service and `robots.txt` file. This script is provided for educational purposes.

## Contributing

Feel free to fork this project, make improvements, and submit pull requests. If you find any bugs or have suggestions, please open an issue.

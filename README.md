# Amazon Book ASIN Scraper

This Python script uses Selenium to automate the process of browsing Amazon.com, searching for books, applying specific language and format filters, and extracting ASIN/ISBN numbers along with book titles. The extracted data is then saved to a CSV file.

## Features

*   **Automated Captcha Solving**: Utilizes the `amazoncaptcha` library to attempt to solve Amazon's CAPTCHAs.
*   **Book Search**: Initiates a search for "books" on Amazon.
*   **Language Filtering**: Applies filters for English, German, French, and Spanish language books.
*   **Format Filtering**: Applies a filter for "Paperback" format books.
*   **ASIN/ISBN Extraction**:
    *   Navigates to individual product pages.
    *   Employs multiple strategies to find ASIN or ISBN-13 numbers (checking product details table, bullet points, and regex on page source).
*   **Pagination Handling**: Navigates through multiple pages of search results.
*   **Data Export**: Saves the scraped book titles and their corresponding ASINs/ISBNs to a CSV file.
*   **Robustness**: Includes error handling for page loading timeouts and issues processing individual books.

## Prerequisites

*   Python 3.x
*   Google Chrome browser installed.
*   ChromeDriver:
    *   Must match your installed Google Chrome version.
    *   Download from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
    *   Ensure ChromeDriver is in your system's PATH, or specify its path when initializing the `webdriver.Chrome()`. (Alternatively, you can use `webdriver-manager` to handle this automatically - see "Potential Improvements").

## Installation

1.  **Clone the repository (or download the script):**
    ```bash
    git clone <https://github.com/Himaa436/amazon-books>
    cd <Himaa436/amazon-books>
    ```

2.  **Install required Python libraries:**
    ```bash
    pip install selenium amazoncaptcha
    ```
    *(Consider adding `webdriver-manager` if you want to automate ChromeDriver setup: `pip install webdriver-manager`)*

3.  **Setup ChromeDriver:**
    *   Download the correct ChromeDriver version for your Chrome browser.
    *   Place it in a directory included in your system's PATH (e.g., `/usr/local/bin` on Linux/macOS) or in the same directory as the script.
    *   Alternatively, you can modify the script to explicitly point to the ChromeDriver executable:
        ```python
        # from selenium import webdriver
        # service = webdriver.chrome.service.Service('/path/to/your/chromedriver')
        # driver = webdriver.Chrome(service=service, options=options)
        ```
        Or, if using `webdriver-manager`:
        ```python
        # from selenium import webdriver
        # from webdriver_manager.chrome import ChromeDriverManager
        # from selenium.webdriver.chrome.service import Service as ChromeService

        # options = webdriver.ChromeOptions()
        # options.add_experimental_option("detach", True)
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        ```

## Usage

1.  **Modify Output Path (Optional):**
    By default, the script saves the CSV file to `C:/Users/PC/Desktop/amazon_books/asin_details.csv`. You might want to change this path in the script:
    ```python
    # Near the end of the script
    with open('your/desired/path/asin_details.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
        # ...
    ```

2.  **Run the script:**
    ```bash
    python amazon_books.py
    ```

3.  The script will:
    *   Open Amazon.com.
    *   Attempt to solve any CAPTCHA presented.
    *   Search for "books".
    *   Apply language and paperback filters.
    *   Iterate through search results, opening each book in a new tab to extract its ASIN/ISBN.
    *   Navigate to subsequent pages of search results.
    *   Once completed or if no more pages are found, it will create an `asin_details.csv` file with the columns: "Book Name", "ASIN", "ISBN".

## Configuration Points in the Code

*   **`website`**: The Amazon domain to target (default: `https://www.amazon.com/`).
*   **Search Term**: Hardcoded as `'books'` in `driver.find_element(By.ID, 'twotabsearchtextbox').send_keys('books')`.
*   **Language Filters**: Hardcoded partial link texts: 'English', 'German', 'French', 'Spanish'.
*   **Format Filter**: Hardcoded partial link text: 'Paperback'.
*   **Output File Path**: Hardcoded as `C:/Users/PC/Desktop/amazon_books/asin_details.csv`.
*   **`options.add_experimental_option("detach", True)`**: This keeps the Chrome browser window open after the script finishes, which can be useful for debugging. You can remove or comment it out if you want the browser to close automatically.

## Output

The script generates a CSV file (e.g., `asin_details.csv`) with the following columns:
*   `Book Name`: The title of the book.
*   `ASIN`: The ASIN or ISBN-13 of the book. If an ISBN-13 is found, it's placed here.
*   `ISBN`: This column is currently always an empty string as the `extract_asin_from_page` function returns a single value which is assigned to the "ASIN" key in the dictionary.

## Important Notes & Limitations

*   **CAPTCHAs**: Amazon's CAPTCHA mechanisms can change, potentially breaking the `amazoncaptcha` library's effectiveness.
*   **Website Structure**: This script relies on specific HTML element IDs, classes, and structures. Amazon frequently updates its website, which can break the selectors and require script updates.
*   **Rate Limiting/IP Blocking**: Extensive or rapid scraping can lead to Amazon temporarily or permanently blocking your IP address. Use responsibly.
*   **Resource Intensive**: Opening many tabs can be resource-intensive on your system.
*   **Error Handling**: While some error handling is present, complex scenarios or unexpected page structures might still cause issues.
*   **ISBN Field**: The current implementation populates the "ASIN" field with either the ASIN or ISBN-13 if found, leaving the dedicated "ISBN" field in the CSV empty. This could be refined if separate storage is strictly needed.

## Potential Improvements

*   Make search terms, filters, and output paths configurable via command-line arguments or a configuration file.
*   Implement IP rotation using proxies to reduce the risk of blocking.
*   Add random delays between requests to mimic human behavior.
*   Use `webdriver-manager` for automatic ChromeDriver downloading and management.
*   Add an option to run in headless mode (browser runs in the background).
*   More sophisticated logging for debugging and tracking progress.
*   Refine ASIN/ISBN extraction to clearly distinguish and store both if available.
*   Allow selection of different book formats or other filter types.

## License

This project is open-source. Please specify a license if you intend to distribute it (e.g., MIT License).

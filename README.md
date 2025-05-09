# Amazon Book Scraper with GUI

This Python script uses Selenium and Tkinter to scrape book details (Title, ASIN, ISBN) from Amazon.com. It automates the process of searching for "books," applying language filters, selecting the "Paperback" format, and navigating through search result pages. The scraped data is then exported to a CSV file.

## Features

*   **Graphical User Interface (GUI):** Built with Tkinter for easy interaction (Start/Stop).
*   **Automated CAPTCHA Solving:** Utilizes the `amazoncaptcha` library to attempt to solve Amazon's CAPTCHAs.
*   **Language Filtering:** Applies filters for English, French, German, and Spanish.
*   **Format Filtering:** Specifically targets "Paperback" books.
*   **Pagination:** Automatically navigates to the next page of search results.
*   **Data Extraction:** Scrapes Book Title, ASIN, and ISBN for each relevant product.
*   **CSV Export:** Saves the collected data into a `books_details.csv` file.
*   **Responsive GUI:** Uses threading to keep the GUI responsive while scraping.
*   **Graceful Stop:** Allows the user to stop the scraping process and export the currently collected data.

## Prerequisites

1.  **Python 3.x:** Download from [python.org](https://www.python.org/downloads/)
2.  **Google Chrome:** The script is configured to use Chrome.
3.  **ChromeDriver:**
    *   Download the ChromeDriver version that **matches your installed Google Chrome version** from [here](https://chromedriver.chromium.org/downloads).
    *   Place `chromedriver.exe` (Windows) or `chromedriver` (Linux/macOS) in your system's PATH, or in the same directory as the Python script.
4.  **Python Libraries:** Install the required libraries using pip:
    ```bash
    pip install selenium amazoncaptcha
    ```
    (Tkinter is usually included with standard Python installations.)

## How to Use

1.  **Clone or Download:** Get the script file (`amazon_books.py`).
2.  **Install Prerequisites:** Ensure Python, Chrome, ChromeDriver, and the necessary Python libraries are installed and configured.
3.  **Configure CSV Output Path (Optional):**
    The script saves the CSV file to a hardcoded path:
    `C:/Users/PC/Desktop/amazon_books/books_details.csv`
    If you want to save it elsewhere, modify this line in the `stop_and_export` function:
    ```python
    with open('YOUR_DESIRED_PATH/books_details.csv','w', newline='', encoding='utf-8-sig') as output_file:
    ```
4.  **Run the Script:**
    Open a terminal or command prompt, navigate to the directory where you saved the script, and run:
    ```bash
    python amazon_books.py
    ```
5.  **Interact with the GUI:**
    *   A window titled "Amazon Books scraping" will appear.
    *   Click the **"Start Scraping"** button.
        *   A new Chrome browser window will open and navigate to Amazon.com.
        *   The script will attempt to solve any initial CAPTCHA.
        *   It will then search for "books," apply language and format filters, and begin scraping.
        *   The GUI will update with messages like "Scraping started" and "Extracting data from page X...".
    *   To stop scraping and save the data:
        *   Click the **"End scraping and give the csv file"** button.
        *   The script will stop, close the browser, and save all data collected up to that point into the CSV file. The GUI will reset to its initial state.

## Output

The script generates a CSV file (default: `books_details.csv`) with the following columns:

*   `Book Name`: The title of the book.
*   `ASIN`: The Amazon Standard Identification Number.
*   `ISBN`: The International Standard Book Number (usually ISBN-13).

## Important Notes & Limitations

*   **CAPTCHAs:** Amazon's CAPTCHA system is designed to prevent automated access. While this script uses the `amazoncaptcha` library, frequent scraping or changes by Amazon can lead to CAPTCHAs that the library cannot solve. Manual intervention might be required if the script gets stuck on a CAPTCHA.
*   **Website Structure Changes:** Web scraping scripts are sensitive to changes in the target website's HTML structure. If Amazon updates its website layout, the Selenium selectors (XPaths, IDs, class names) in this script might break, requiring updates to the code.
*   **Rate Limiting & IP Blocking:** Amazon may implement rate limiting or IP blocking if it detects excessive automated requests. Use this script responsibly and consider adding delays if you encounter issues.
*   **Error Handling:** The script includes some error handling, but it might not cover all possible scenarios (e.g., network interruptions, unexpected pop-ups on Amazon).
*   **Single Threaded Scraping Logic:** While the GUI is responsive due to threading, the core scraping logic runs sequentially.
*   **Driver Management:** The script re-initializes the WebDriver if "Start Scraping" is clicked after a previous run (or stop). Ensure that previous browser windows controlled by Selenium are closed if you manually stop the Python script execution without using the GUI's stop button.

## Troubleshooting

*   **`WebDriverException: Message: 'chromedriver' executable needs to be in PATH`**:
    Ensure `chromedriver.exe` (or `chromedriver`) is either in your system's PATH environment variable or in the same directory as your Python script. Also, verify the ChromeDriver version matches your Chrome browser version.
*   **CAPTCHA solving fails repeatedly**:
    The `amazoncaptcha` library might be outdated, or Amazon has significantly changed its CAPTCHA. Check for updates to the library or consider alternative CAPTCHA solving services/methods (which might involve costs).
*   **Elements not found (`NoSuchElementException`, `TimeoutException`)**:
    This usually means Amazon has changed its website HTML structure. You will need to inspect the Amazon page and update the XPaths or other selectors (e.g., `By.ID`, `By.CLASS_NAME`) in the script.
*   **Script stops without error message / GUI hangs:**
    Check the console output where you ran the script for any Python errors that might not be caught or displayed in the GUI.

## Disclaimer

This script is intended for educational purposes. Be mindful of Amazon's terms of service regarding web scraping. Scraping too aggressively can put a strain on their servers. Always scrape responsibly.

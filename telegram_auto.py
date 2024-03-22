import os
import time
import traceback
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService

CUR_DIR = Path(__file__).parent.absolute()
USER_DATA_DIR = os.path.join(CUR_DIR, "profile")

HOME_URL = "https://web.telegram.org"

os.chdir(CUR_DIR)


def create_browser() -> Chrome:
    browser = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")

        driver = webdriver.Chrome(
            options=options,
        )
        driver.get(HOME_URL)
        browser = driver
    except:
        traceback.print_exc()
    return browser


def main():
    try:
        browser = create_browser()
        time.sleep(10)
        browser.quit()
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()

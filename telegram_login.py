import os
import time
import traceback
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import Chrome

CUR_DIR = Path(__file__).parent.absolute()
USER_DATA_DIR = os.path.join(CUR_DIR, "profile")

HOME_URL = "https://web.telegram.org/k"

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
        while True:
            time.sleep(1)
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()

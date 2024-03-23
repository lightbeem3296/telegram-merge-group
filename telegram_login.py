import os
import traceback
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import Chrome

CUR_DIR = Path(__file__).parent.absolute()
USER_DATA_DIR = os.path.join(CUR_DIR, "profile")


os.chdir(CUR_DIR)


def create_browser() -> Chrome:
    browser = None
    try:
        print(f"[*] open browser with user data directory: {USER_DATA_DIR}")
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")

        driver = webdriver.Chrome(
            options=options,
        )
        print(f"[*] visit telegram web page")
        driver.get(HOME_URL)
        browser = driver
    except:
        traceback.print_exc()
    return browser


async def main():
    try:
        browser = create_browser()
        print(f"[*] please login to https://web.telegram.org")
        while True:
            str = input("[*] login finished? then exit me.[y]")
            if str.lower() == "y":
                break
        browser.quit()
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()

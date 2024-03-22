import os
import traceback
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

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


def copy_members(browser: Chrome, from_group_name: str, to_group_name: str):
    try:
        # click group
        group_list = browser.find_elements(by=By.CLASS_NAME, value=from_group_name)
        for group in group_list:
            group_name = group.find_element(
                by=By.CSS_SELECTOR,
                value="div.row-row.row-title-row.dialog-title > div.row-title.no-wrap.user-title > span.peer-title",
            )
            print(group_name.text)

        pass
    except:
        traceback.print_exc()


def main():
    try:
        browser = create_browser()
        copy_members(
            browser=browser,
            from_group_name="Django Community",
            to_group_name="dev-test",
        )
        browser.quit()
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()

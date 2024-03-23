# disable animations

import argparse
import asyncio
import os
import time
import traceback
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

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
        go2url(driver, HOME_URL)
        browser = driver
    except:
        traceback.print_exc()
    return browser


def go2url(browser: Chrome, url: str, timeout: float = 0.5):
    try:
        browser.get(url)
        time.sleep(timeout)
    except:
        traceback.print_exc()


def go2group(browser: Chrome, group_id: str):
    try:
        print(f"[*] group_id: {group_id}")
        chat_link = f"{HOME_URL}/#{group_id}"
        go2url(browser, chat_link)
    except:
        traceback.print_exc()


def wait_for_clickable(browser: Chrome, by: str, value: str, timeout: float = 10):
    try:
        return WebDriverWait(browser, timeout).until(EC.element_to_be_clickable((by, value)))
    except:
        traceback.print_exc()


def click_elem(browser: Chrome, selector: str, timeout: float = 10):
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        browser.execute_script(f'document.querySelector("{selector}").click()')
    except:
        traceback.print_exc()


async def merge_members(browser: Chrome, src_group_id: str, dst_group_id: str):
    try:
        print(f"[*] from_group_id: {src_group_id}")

        # find and click source group
        print(f"[*] open source group page")
        go2group(browser, src_group_id)
        time.sleep(3)

        # click chat information
        print(f"[*] click chat information")
        click_elem(
            browser=browser,
            selector="#column-center > div > div > div.sidebar-header.topbar.has-avatar > div.chat-info-container > div.chat-info",
        )
        time.sleep(1)

        # fetch all group member information
        member_count = int(
            browser.find_element(
                by=By.CSS_SELECTOR,
                value="#column-right > div > div > div.sidebar-content > div > div.profile-content > div.profile-avatars-container.is-single > div.profile-avatars-info > div.profile-subtitle > span > span:nth-child(1)",
            )
            .text.strip()
            .replace(" ", "")
            .replace("members", "")
        )
        members = {}
        print(f"[*] {member_count} members")
        print(f"[*] list all members")

        # while False:
        while True:
            member_list = browser.find_elements(
                by=By.CLASS_NAME,
                value="chatlist",
            )[2].find_elements(
                by=By.TAG_NAME,
                value="a",
            )
            new_member_found = False
            # for member_item in member_list[:5]:
            for member_item in member_list:
                member_id = member_item.get_attribute("data-peer-id")
                if member_id in members:
                    continue
                new_member_found = True
                member_name = member_item.find_elements(
                    by=By.TAG_NAME,
                    value="span",
                )[1].text
                members[member_id] = member_name
                print(f"{len(members.keys())}\t{member_id}\t{member_name}")

                ActionChains(browser).scroll_to_element(member_item).perform()
            if not new_member_found:
                print("[*] no more new members found")
                break

        # add members to contact
        print(f"[*] add members to contact")
        for member_id in members:
            # go to member page
            print(f"[*] go to member page: {member_id} {members[member_id]}")
            member_link = f"{HOME_URL}/#{member_id}"
            go2url(browser, member_link)

            # click ... button
            print(f"[*] click ... button")
            click_elem(
                browser=browser,
                selector="#column-center > div > div.chat.tabs-tab.can-click-date.active > div.sidebar-header.topbar.has-avatar > div.chat-info-container > div.chat-utils > button:nth-child(9)",
            )
            time.sleep(0.5)

            # click add to contact button
            print(f"[*] click add to contact button")
            submenu_items = browser.find_elements(
                by=By.CSS_SELECTOR,
                value="#column-center > div > div.chat.tabs-tab.can-click-date.active > div.sidebar-header.topbar.has-avatar > div.chat-info-container > div.chat-utils > button.btn-icon.rp.btn-menu-toggle.menu-open > div.btn-menu.bottom-left.active.was-open > div",
            )
            for submenu_item in submenu_items:
                if "Add to contacts" in submenu_item.text:
                    submenu_item.click()

                    # click conform button
                    print(f"[*] click confirm button")
                    click_elem(
                        browser=browser,
                        selector="#column-right > div > div.tabs-tab.sidebar-slider-item.scrolled-top.scrolled-bottom.scrollable-y-bordered.edit-peer-container.edit-contact-container.active > div.sidebar-content > button",
                    )
                    break

        # add members to destination group
        print(f"[*] open destination group page")
        go2group(browser, dst_group_id)
        time.sleep(3)

        # click chat info
        print(f"[*] click chat information")
        click_elem(
            browser=browser,
            selector="#column-center > div > div > div.sidebar-header.topbar.has-avatar > div.chat-info-container > div.chat-info",
        )

        for member_id in members:
            try:
                member_name = members[member_id]

                # click add to group button
                print(f"[*] click add to group button")
                click_elem(
                    browser=browser,
                    selector="#column-right > div > div > div.sidebar-content > button",
                )

                # input username
                print(f"[*] input username: {member_name}")
                search_user = wait_for_clickable(
                    browser=browser,
                    by=By.CSS_SELECTOR,
                    value="body > div.popup.popup-forward.active > div > div.popup-header > div > input",
                )
                search_user.clear()
                search_user.send_keys(member_name)

                # wait for search result
                time.sleep(1)

                # click matching result
                search_results = browser.find_element(
                    by=By.CSS_SELECTOR,
                    value="body > div.popup.popup-forward.active > div > div.popup-body > div > div > div > div > div.sidebar-left-section-container.selector-list-section-container > div > div > ul",
                )
                search_result_items = search_results.find_elements(
                    by=By.TAG_NAME,
                    value="a",
                )
                for search_result in search_result_items:
                    if member_id == search_result.get_attribute("data-peer-id"):
                        time.sleep(0.5)
                        search_result.click()
                        time.sleep(0.5)

                        # click add button
                        print(f"[*] click add button")
                        click_elem(
                            browser=browser,
                            selector="body > div.popup.popup-peer.popup-add-members.active > div > div.popup-buttons > button:nth-child(1)",
                        )
                        time.sleep(0.5)
                        browser.execute_script("document.body.click()")
                        time.sleep(1)
                        break

            except:
                traceback.print_exc()
    except:
        traceback.print_exc()


async def main():
    try:
        parser = argparse.ArgumentParser()
        args = parser.parse_args()

        browser = create_browser()
        await merge_members(
            browser=browser,
            src_group_id=args.src_group_id,
            dst_group_id=args.dst_group_id,
        )

        while True:
            in_str = input("[*] work finished? exit me.[y]")
            if in_str.lower() == "y":
                break
        browser.quit()
    except:
        traceback.print_exc()


async def test():
    try:
        browser = create_browser()
        await merge_members(
            browser=browser,
            src_group_id="@irflask",
            dst_group_id="-4109507158",
        )

        while True:
            in_str = input("[*] work finished? exit me.[y]")
            if in_str.lower() == "y":
                break
        browser.quit()
    except:
        traceback.print_exc()


if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.run(test())

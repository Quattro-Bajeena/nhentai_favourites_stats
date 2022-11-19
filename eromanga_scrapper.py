import re
import json
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from undetected_chromedriver import Chrome

options = ChromiumOptions()

def get_favourites(driver: Chrome):
    favourites_urls = []

    last_page_url = driver.find_element(By.CLASS_NAME, "last").get_attribute('href')
    last_page = int(re.search(r"page=(\d+)", last_page_url).group(1))

    for page_num in range(1, last_page+1):
        driver.get(f"https://nhentai.net/favorites/?page={page_num}")
 
        page_favourites = driver.find_element(By.ID, "favcontainer").find_elements(By.XPATH, "div")
        for favourite in page_favourites:
            url = favourite.find_element(By.CLASS_NAME, "gallery").find_element(By.TAG_NAME, "a").get_attribute('href')
            favourites_urls.append(url)

    return favourites_urls

def get_tags(url, driver: Chrome):
    driver.get(url)
    tags = []
    tag_counts = {}
    TAG_CATEGORIES = ("parody", "character", "tag", "artist", "group", "language", "category", "pages")
    tag_divs = driver.find_element(By.ID, "tags").find_elements(By.XPATH, "div")
    for i, div in enumerate(tag_divs):
        tag_urls = div.find_element(By.CLASS_NAME, "tags").find_elements(By.TAG_NAME, "a")
        for url in tag_urls:
            tag_name = url.find_element(By.CLASS_NAME, "name").text

            tag_count_element = url.find_elements(By.CLASS_NAME, "count")
            
            if tag_count_element:
                tag_count = tag_count_element[0].text
                if tag_count[-1] == "K":
                    tag_count = 1000 * int(tag_count[:-1])
                else:
                    tag_count = int(tag_count)

                if tag_name in tag_counts:
                    tag_counts[tag_name] = (tag_counts[tag_name] + tag_count)/2
                else:
                    tag_counts[tag_name] = tag_count

            tags.append((TAG_CATEGORIES[i], tag_name))
    return tags, tag_counts

if __name__ == '__main__':
    driver = uc.Chrome(options=options)
    driver.get("https://nhentai.net/")
    tags_dict = {
        "tags" : [],
        "tag_counts" : {}
    }
    favourites_wait = WebDriverWait(driver, 120).until(EC.url_contains("nhentai.net/favorites"))
    favourites_urls = get_favourites(driver)
    for favourite_url in favourites_urls:
        doujin_tags, doujin_tag_counts = get_tags(favourite_url, driver)
        tags_dict["tags"].extend(doujin_tags)
        tags_dict["tag_counts"].update(doujin_tag_counts)

    with open("favourites_tags.json", 'w') as fp:
        json.dump(tags_dict, fp)





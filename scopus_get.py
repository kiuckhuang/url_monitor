#!/usr/bin/python3

# https://playwright.dev/python/docs/intro
# pip install pytest-playwright
# playwright install

from time import sleep
from random import randint
from playwright.sync_api import sync_playwright


playwright = sync_playwright().start()

browser = playwright.chromium.launch(channel="chrome", headless=False)
context = browser.new_context(
    viewport={ 'width': 1280, 'height': 1024 },
    locale='en-US',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
)
page = browser.new_page()

url_prefix = 'https://www.scopus.com/authid/detail.uri?authorId='
author_ids = ['14063470600', '9042311600', '6507012293']

metrics = {
    'name': '#scopus-author-profile-page-control-microui__general-information-content > section > div > h2',
    'documents': '#scopus-author-profile-page-control-microui__ScopusAuthorProfilePageControlMicroui > div:nth-child(2) > div > section > div > div.col-lg-6.col-24 > els-stack > div:nth-child(1) > h3',
    'citations': '#scopus-author-profile-page-control-microui__ScopusAuthorProfilePageControlMicroui > div:nth-child(2) > div > section > div > div.col-lg-6.col-24 > els-stack > div:nth-child(2) > h3',
    'hindex': '#scopus-author-profile-page-control-microui__ScopusAuthorProfilePageControlMicroui > div:nth-child(2) > div > section > div > div.col-lg-6.col-24 > els-stack > div:nth-child(3) > h3'
}


print('","'.join(metrics.keys()))

for author_id in author_ids:
    page.goto( url_prefix + author_id )

    lst = [] # Declares an empty list named lst
    for m_key, m_selector in metrics.items():
        page.wait_for_selector(m_selector)
        lst.append(page.inner_text(m_selector))
    print('","'.join(lst))
    sleep(randint(100,200)/100)
browser.close()

playwright.stop()
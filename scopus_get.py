#!/usr/bin/python3

# https://playwright.dev/python/docs/intro
# pip install pytest-playwright
# playwright install


from playwright.sync_api import sync_playwright

url = 'https://www.scopus.com/authid/detail.uri?authorId=7006328373'

playwright = sync_playwright().start()

browser = playwright.chromium.launch(channel="chrome", headless=False)
context = browser.new_context(
    viewport={ 'width': 1280, 'height': 1024 },
    locale='en-US',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
)
page = browser.new_page()
page.goto( url )


locator_documents = '#scopus-author-profile-page-control-microui__ScopusAuthorProfilePageControlMicroui > div:nth-child(2) > div > section > div > div.col-lg-6.col-24 > els-stack > div:nth-child(1) > h3'
locator_citations = '#scopus-author-profile-page-control-microui__ScopusAuthorProfilePageControlMicroui > div:nth-child(2) > div > section > div > div.col-lg-6.col-24 > els-stack > div:nth-child(2) > h3'
locator_hindex    = '#scopus-author-profile-page-control-microui__ScopusAuthorProfilePageControlMicroui > div:nth-child(2) > div > section > div > div.col-lg-6.col-24 > els-stack > div:nth-child(3) > h3'

page.wait_for_selector(locator_documents)

docs = page.inner_text(locator_documents)
cits = page.inner_text(locator_citations)
hind = page.inner_text(locator_hindex)

print(docs, cits, hind)

browser.close()

playwright.stop()
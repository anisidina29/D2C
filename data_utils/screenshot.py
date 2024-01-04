from playwright.sync_api import sync_playwright
import os

def take_screenshot(url, output_file="screenshot.png"):
    # Convert local path to file:// URL if it's a file
    if os.path.exists(url):
        url = "file://" + os.path.abspath(url)

    with sync_playwright() as p:
        # Choose a browser, e.g., Chromium, Firefox, or WebKit
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the URL
        page.goto(url)

        # Take the screenshot
        page.screenshot(path=output_file, full_page=True)

        browser.close()

# for name in ["aryaman", "danqi", "diyi", "tatsu", "yanzhe"]:
#     take_screenshot("/Users/clsi/Desktop/Pix2Code/trial_dataset/" + "{}.html".format(name), "trial_dataset/" + "{}.png".format(name))

if __name__ == "__main__":
    take_screenshot("testset_anonymized/" + "{}.html".format("1438"), "testset_anonymized/" + "{}.png".format("1438"))
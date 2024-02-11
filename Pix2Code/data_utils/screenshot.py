from playwright.sync_api import sync_playwright
import os
from tqdm import tqdm

def take_screenshot(url, output_file="screenshot.png"):
    # Convert local path to file:// URL if it's a file
    if os.path.exists(url):
        url = "file://" + os.path.abspath(url)

    with sync_playwright() as p:
        # Choose a browser, e.g., Chromium, Firefox, or WebKit
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the URL
        page.goto(url, timeout=60000)

        # Take the screenshot
        page.screenshot(path=output_file, full_page=True, animations="disabled", timeout=60000)

        browser.close()

# for name in ["aryaman", "danqi", "diyi", "tatsu", "yanzhe"]:
#     take_screenshot("/Users/clsi/Desktop/Pix2Code/trial_dataset/" + "{}.html".format(name), "trial_dataset/" + "{}.png".format(name))

if __name__ == "__main__":
    predictions_dirs = ["../../gemini_ultra_predictions_full/direct_prompting", "../../gemini_ultra_predictions_full/text_augmented_prompting", "../../gemini_ultra_predictions_full/visual_revision_prompting"]
    for predictions_dir in predictions_dirs:
        for filename in tqdm(os.listdir(predictions_dir)):
            if filename.endswith(".html"):
                take_screenshot(os.path.join(predictions_dir, filename), os.path.join(predictions_dir, filename.replace(".html", ".png")))

    # take_screenshot("/Users/clsi/Desktop/Pix2Code/predictions_full/gemini_direct_prompting/348.html", "/Users/clsi/Desktop/Pix2Code/predictions_full/gemini_direct_prompting/348.png")

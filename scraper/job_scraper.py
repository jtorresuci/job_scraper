from scraper.browser import get_driver
from scraper.search import search_jobs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_jobs(keyword, location):
    driver = get_driver(headless=False)
    search_jobs(driver, keyword, location)

    time.sleep(3)

    input("Press Enter after solving captcha")
    job_cards = driver.find_elements(By.CSS_SELECTOR, "a.jcs-JobTitle")

    jobs = []

    for idx, card in enumerate(job_cards, 1):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(0.5)
            card.click()

            # Wait for the job title to appear or update
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h2[data-testid='simpler-jobTitle']"))
                )
                title_element = driver.find_element(By.CSS_SELECTOR, "h2[data-testid='simpler-jobTitle']")
                title = title_element.text
                print("Title: ", title)
            except Exception as e:
                print(f"Error getting title: {e}")
                title = ""

            # Extract salary
            try:
                salary_element = driver.find_element(By.CSS_SELECTOR, "span.js-match-insights-provider-1vjtffa")
                salary = salary_element.text
            except Exception:
                salary = ""

            # Extract job description
            try:
                description_element = driver.find_element(By.ID, "jobDescriptionText")
                description = description_element.text
            except Exception:
                description = ""

            print(f"Scraped: {title} | {salary}")

            jobs.append({
                "title": title,
                "salary": salary,
                "description": description,
            })

        except Exception as e:
            print(f"Failed to scrape job {idx}: {e}")
            continue

    driver.quit()

    # Save to CSV
    save_to_csv(jobs, keyword, location)

def save_to_csv(jobs, keyword, location):
    filename = f"data/{keyword}_{location}_jobs.csv".replace(" ", "_").replace(",", "")
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "salary", "description"])
        writer.writeheader()
        writer.writerows(jobs)

    print(f"\n✅ Saved {len(jobs)} jobs to {filename}")

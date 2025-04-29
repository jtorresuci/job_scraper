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
        title = ""
        company = ""
        salary = ""
        address = ""
        work_location = ""
        description = ""

        try:
            driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(0.5)
            card.click()


            # Extract job title
            try:
                try:
                    # Try first selector
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h2[data-testid='simpler-jobTitle']"))
                    )
                    title_element = driver.find_element(By.CSS_SELECTOR, "h2[data-testid='simpler-jobTitle']")
                except Exception:
                    # If first fails, try the second
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h2[data-testid='jobsearch-JobInfoHeader-title']"))
                    )
                    title_element = driver.find_element(By.CSS_SELECTOR, "h2[data-testid='jobsearch-JobInfoHeader-title']")
                
                title = title_element.text
            except Exception as e:
                print(f"Error getting title: {e}")
                title = ""


            # Extract company name
            try:
                try:
                    # Try span with wait
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "span.jobsearch-JobInfoHeader-companyNameSimple"))
                    )
                    company_element = driver.find_element(By.CSS_SELECTOR, "span.jobsearch-JobInfoHeader-companyNameSimple")
                except Exception:
                    try:
                        # Try a known linked company name
                        company_element = driver.find_element(By.CSS_SELECTOR, "a.jobsearch-JobInfoHeader-companyNameLink")
                    except Exception:
                        # Try a generic link if necessary
                        company_element = driver.find_element(By.CSS_SELECTOR, "a.css-1ytmynw.e19afand0")
                
                company = company_element.text
            except Exception as e:
                print(f"Error getting company: {e}")
                company = ""


            # Extract salary
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.js-match-insights-provider-1vjtffa"))
                )
                salary_element = driver.find_element(By.CSS_SELECTOR, "span.js-match-insights-provider-1vjtffa")
                salary = salary_element.text
            except Exception:
                input("Salary not found Press enter to continue")
                salary = ""



            # Extract address
            try:
                try:
                    # Try original address first
                    address_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='job-location']")
                    address = address_element.text
                except Exception:
                    try:
                        # Try new address layout
                        address_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='inlineHeader-companyLocation'] div")
                        address_text = address_element.text
                        # Split by "•" if Hybrid or Remote is present
                        if "•" in address_text:
                            address = address_text.split("•")[0].strip()
                        else:
                            address = address_text.strip()
                    except Exception:
                        address = ""
            except Exception:
                address = ""


            # Extract work location
            try:
                try:
                    # Try old method (Work Location: In person)
                    work_location_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Work Location')]")
                    work_location = work_location_element.text.replace("Work Location: ", "").strip()
                except Exception:
                    try:
                        # Try new method (span with Hybrid/Remote text)
                        work_location_element = driver.find_element(By.CSS_SELECTOR, "span.js-match-insights-provider-1vjtffa.e1wnkr790")
                        possible_text = work_location_element.text.strip()
                        # Only use it if it matches typical work location patterns
                        if any(word in possible_text.lower() for word in ["remote", "in person", "hybrid"]):
                            work_location = possible_text
                        else:
                            work_location = ""
                    except Exception:
                        work_location = ""
            except Exception:
                work_location = ""


            # Extract job description
            try:
                description_element = driver.find_element(By.ID, "jobDescriptionText")
                description = description_element.text
            except Exception:
                input("Description not foundPress enter to continue")
                description = ""

            print(f"Scraped: {title} | {company} | {salary}")

            jobs.append({
                "title": title,
                "company": company,
                "salary": salary,
                "address": address,
                "work_location": work_location,
                "description": description,
            })

        except Exception as e:
            input("Press enter to continue")
            print(f"Failed to scrape job {idx}: {e}")
            continue

    driver.quit()

    # Save to CSV
    save_to_csv(jobs, keyword, location)

def save_to_csv(jobs, keyword, location):
    filename = f"data/{keyword}_{location}_jobs.csv".replace(" ", "_").replace(",", "")
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "company", "salary", "address", "work_location", "description"])
        writer.writeheader()
        writer.writerows(jobs)

    print(f"\n✅ Saved {len(jobs)} jobs to {filename}")

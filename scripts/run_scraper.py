# scripts/run_scraper.py

from scraper.job_scraper import scrape_jobs

def main():
    keyword = "accountant"
    location = "Anaheim, CA"
    scrape_jobs(keyword=keyword, location=location)

if __name__ == "__main__":
    main()

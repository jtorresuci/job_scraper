# 📄 README.md

# Indeed Job Scraper

This project is an automated job scraper built using **Selenium**.  
It searches for jobs on **Indeed**, clicks on each job card, extracts detailed job information, and saves it into a **CSV file**.

---

## 🚀 Features
- Dynamic keyword and location search
- Captcha support (manual pause if encountered)
- Clicks into each job listing to extract:
  - **Job Title**
  - **Company Name**
  - **Salary** (if available)
  - **Address**
  - **Work Location** (Remote, Hybrid, In-person)
  - **Full Job Description**
- Auto-scrolls to each listing for stability
- Saves extracted job listings into a structured CSV file
- Handles page changes in layout automatically (fallbacks included)

---

## 📂 Project Structure

```
job_scraper/
├── scraper/
│   ├── browser.py       # Launches and configures Selenium WebDriver
│   ├── job_scraper.py    # Main scraping logic
│   ├── search.py         # Searching for job listings
│   ├── utils.py          # Helper functions (optional for splitting duties, waits, etc.)
├── scripts/
│   └── run_scraper.py    # Entry point to run the scraper
├── data/                 # Folder where CSV output files are saved
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/job_scraper.git
   cd job_scraper
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # (on Windows: venv\Scripts\activate)
   ```

3. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper**
   ```bash
   python scripts/run_scraper.py
   ```

---

## 🖥️ Usage

When you run the scraper:
- You will be prompted to **solve any captcha manually** if it appears.
- After solving, **press Enter** to continue scraping.
- Extracted jobs will be saved automatically to a CSV file under the `/data/` folder, named based on your search keyword and location (e.g., `software_engineer_New_York_jobs.csv`).

---

## 📦 Example Output (CSV Columns)

| title | company | salary | address | work_location | description |
|:------|:--------|:-------|:--------|:--------------|:------------|

---

## 🛠️ Requirements
- Python 3.8+
- Google Chrome installed
- ChromeDriver (managed automatically via `webdriver-manager`)

Python packages used:
- `selenium`
- `webdriver-manager`
- `pandas` (optional if you expand for data cleaning)
- `python-dotenv` (optional if adding .env configs)

---

## ⚡ Future Improvements
- Automatic handling of pagination (scraping multiple pages)
- Parallel scraping (for faster results)
- Detect and skip sponsored ads
- Handle missing data even more gracefully
- Export into databases (like SQLite) instead of just CSV
- Integrate a **local AI model** to classify job descriptions, duties, and requirements (e.g., categorize seniority level, job type, industry sector)

---

## ⚠️ Disclaimer
This project is for educational purposes only.  
Please respect Indeed's [Terms of Service](https://www.indeed.com/legal) when scraping public data.

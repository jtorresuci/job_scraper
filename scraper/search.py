from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_jobs(driver, keyword, location):
    driver.get("https://www.indeed.com/")

    # Find and fill in the job title
    what_input = driver.find_element(By.ID, "text-input-what")
    what_input.clear()
    what_input.send_keys(Keys.CONTROL + "a")  # select all
    what_input.send_keys(Keys.DELETE)         # delete
    what_input.send_keys(keyword)
    

    # Find and fill in the location
    where_input = driver.find_element(By.ID, "text-input-where")
    where_input.click()
    time.sleep(2)                            # tiny wait (optional)
    where_input.send_keys(Keys.CONTROL + "a")  # select all
    where_input.send_keys(Keys.BACK_SPACE)         # delete
    where_input.send_keys(Keys.COMMAND + "a")  # select all
    where_input.send_keys(Keys.BACK_SPACE)         # delete
    time.sleep(0.5)                            # tiny wait (optional)
    where_input.send_keys(location)

    # Press Enter to search
    where_input.send_keys(Keys.RETURN)

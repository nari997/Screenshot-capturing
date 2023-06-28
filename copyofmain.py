from fastapi import FastAPI, BackgroundTasks
import requests
from bs4 import BeautifulSoup
import validators
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from PIL import Image
import io
import csv
import time

app = FastAPI()

# Configure the database connection
DATABASE_URL = 'mysql+mysqlconnector://root:Vijay$555@localhost:3306/rubixe_emp'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))



@app.get("/extract_urls")
async def extract_urls(url: str, background_tasks: BackgroundTasks):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all anchor tags and extract the href attribute (URLs)
        urls = [a['href'] for a in soup.find_all('a', href=True)]

        # Validate URLs
        validated_urls = []
        for url in urls:
            if validators.url(url):
                validated_urls.append(url)

        # Create a session to access the database
        db = SessionLocal()
        db.commit()

        # Delete existing records from the URLs table
        db.query(URL).delete()
        db.commit()

        # Save validated URLs to the database
        for url in validated_urls:
            url = URL(url=url)
            db.add(url)

        db.commit()

        # Save URLs to CSV file
        save_urls_to_csv(validated_urls)

        # Queue the task to capture screenshots
        background_tasks.add_task(capture_screenshots)

        return {"urls": validated_urls, "message": "URLs saved to CSV file and capturing screenshots has been scheduled"}

    except Exception as e:
        return {"error": str(e)}

def save_urls_to_csv(urls):
    with open("urls.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URLs'])
        writer.writerows([[url] for url in urls])

# Setting up selenium options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless") # Headless mode to capture full page screenshot
# Setting up selenium webdriver
driver = webdriver.Chrome(options=chrome_options)

def capture_screenshots():
    try:
        # Create a session to access the database
        db = SessionLocal()

        # Retrieve the URLs from the database
        urls = [result[0] for result in db.query(URL.url).all()]

        # Capture screenshots for each URL
        for index, url in enumerate(urls):
            try:
                # Navigate to the webpages of the stored URLs
                driver.get(url)
                width = 1920
                # Setting height of the webpage to capture fully
                height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

                driver.set_window_size(width,height)
                page_body = driver.find_element(By.TAG_NAME, "body")


                # Saving the screenshots
                filename = f"E:\Vijay\Python_exps\Screenshot\Screenshots\screenshot_{index}.png" # To be saved folder
                page_body.screenshot(filename) # defining file name
                print(f"Screenshot captured for URL:{url} - Saved as: {filename}") # printing output progress

            except Exception as e:
                print(f"Error capturing screenshot for URL:{url}. Error message: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        driver.quit()
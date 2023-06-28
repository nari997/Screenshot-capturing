from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from PIL import Image
import io

# Configure the database connection
DATABASE_URL = 'mysql+mysqlconnector://root:Vijay$555@localhost:3306/rubixe_emp'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
#driver.maximize_window()

# # Set up Selenium options
# options = webdriver.ChromeOptions()
# options.headless = True
# #driver = webdriver.Chrome(ChromeDriverManager().install(),options = options)
# # Set up Selenium WebDriver
# webdriver_manager = ChromeDriverManager()
# driver = webdriver_manager.install()
# driver = webdriver.Chrome(options=options)
# driver.implicitly_wait(10)
# #driver.set_window_size(1920, 1080)

def capture_screenshots():
    try:
        # Create a session to access the database
        db = SessionLocal()

        # Retrieve the URLs from the database
        urls = [result[0] for result in db.query(URL.url).all()]

        # Capture screenshots for each URL
        for index, url in enumerate(urls):
            try:
                # Navigate to the webpage
                driver.get(url)
                width = 1920
                height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

                driver.set_window_size(width,height)
                page_body = driver.find_element(By.TAG_NAME, "body")
                              
                # Capture the screenshot
                filename = f"E:\Vijay\Python_exps\Screenshot\Screenshots\screenshot_{index}.png"
                page_body.screenshot(filename)
                print(f"Screenshot captured for URL: {url} - Saved as: {filename}")

            except Exception as e:
                print(f"Error capturing screenshot for URL: {url}. Error message: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        driver.quit()

# Call the function to capture screenshots
capture_screenshots()

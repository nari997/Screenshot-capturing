import tkinter as tk
from tkinter import ttk
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from PIL import Image, ImageTk
from fastapi import FastAPI
from fastapi.responses import FileResponse
from io import BytesIO

app = FastAPI()

# Function to capture the full-page screenshot
def capture_screenshot(url):

    # Open the webpage
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)  # Wait for the webpage to load
    
    # Capture the full-page screenshot
    width = driver.execute_script("return document.body.scrollWidth")
    height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
    driver.set_window_size(width, height)
    # page_body = driver.find_element(By.TAG_NAME, "body")

    screenshot_file = f"E:\\Vijay\\Python_exps\\Screenshot\\Screenshots\\screenshot.png"
    driver.save_screenshot(screenshot_file)
    driver.quit()

    return screenshot_file

# Define a route to capture screenshot
@app.get("/Capture Screenshot")
async def run_screenshot(url: str):
    screenshot_file = capture_screenshot(url)

    # open the screenshot file
    img = Image.open(screenshot_file)

    # Convert the image to the bytes to open in a response in fastapi server
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    return FileResponse(screenshot_file, media_type = 'image/png')
    

if __name__ == "__uiapi__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
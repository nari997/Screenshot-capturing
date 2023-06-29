import tkinter as tk
from tkinter import ttk
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from PIL import Image, ImageTk

# Function to capture the full-page screenshot
def capture_screenshot():
    url = url_entry.get()
    # screenshot_format = format_combobox.get()

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

    # Displaying the screenshot
    img = Image.open(screenshot_file)
    # img_width, img_height = img.size
    cropped_image = img.crop((0, 0, img.width, img.height))
    resized_image = cropped_image.resize((width, height), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(resized_image)

    # Calculate the canvas width and img height
    canvas_width = resized_image.width
    img_height = resized_image.height

    canvas.image = img_tk # Stores a reference to the PhotoImage object
    canvas.create_image(canvas_width / 2, img_height /2, anchor="center", image=img_tk)
    
    result_label.config(text=f"Screenshot captured successfully!")

# Create the main window
window = tk.Tk()
window.title("Capturing Screenshot")


# URL entry
url_label = tk.Label(window, text="URL:")
url_label.pack()
url_entry = tk.Entry(window)
url_entry.pack()

# # Screenshot format dropdown
# format_label = tk.Label(window, text="Screenshot Format:")
# format_label.pack()
# format_combobox = ttk.Combobox(window, values=["png", "jpg"])
# format_combobox.pack()

# Capture screenshot button
capture_button = tk.Button(window, text="Capture Screenshot", command=capture_screenshot)
capture_button.pack()

# Scrollable region to display the screenshot.
canvas_frame = tk.Frame(window)
canvas_frame.pack(fill='both', expand=True)

canvas = tk.Canvas(canvas_frame)
canvas.pack(side='left', fill='both', expand=True)

scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side='right', fill='y')

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0,0), anchor="nw")


# Result label
result_label = tk.Label(window, text="")
result_label.pack()

# Run the GUI
window.mainloop()
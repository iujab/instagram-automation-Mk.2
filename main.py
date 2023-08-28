from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
import pyperclip
import pyautogui
import os
import time
import pandas as pd
from PIL import Image

# SETTINGS: ONLY THIS NEEDS TO BE EDITED FOR USE
username = "[ACCOUNT USERNAME]"
password = "[ACCOUNT PASSWORD]"
directory = r"C:[POSTS DIRECTORY]"
caption = "[CAPTION]"
start_date = "2023-08-27"  # year-month-day format
end_date = "2023-9-2"  # year-month-day format
hour = "8"  # post hour as string
ampm = "a"  # a for am, p for pm
prepped = True  # whether posts are prepped


# START
dpath = directory + r"\\"
dirs = os.listdir(dpath)
daterange = pd.date_range(start_date, end_date)


def removeLatest(d):
    for item in d[:1]:
        print(item + " posted and removed")
        os.remove(dpath + item)


def moveAndClick(x, y):
    pyautogui.moveTo(x, y)
    time.sleep(1)
    pyautogui.click(x, y)
    time.sleep(1)


def rename():
    count = 1
    for i, f in enumerate(dirs):
        src = os.path.join(dpath, f)
        dst = os.path.join(dpath, (f'{count:04}' + ".jpg"))
        os.rename(src, dst)
        count += 1


def resize():
    for item in dirs:
        print(item)
        if os.path.isfile(dpath+item):
            im = Image.open(dpath+item)
            f, e = os.path.splitext(dpath+item)
            imResize = im.resize((800, 1000))
            imResize.save(f + '.jpg', 'JPEG', quality=100)


if not prepped:
    resize()
    rename()
    print("Files Prepped")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://instagram.com")
wait = WebDriverWait(driver, 10)
driver.set_window_size(800, 600)
driver.set_window_position(0, 0, windowHandle='current')
pyperclip.copy(caption)
keyboard = Controller()


# LOGIN
sdf = ("xpath", '//*[@id="loginForm"]/div/div[1]/div/label/input')
last = wait.until(EC.element_to_be_clickable(sdf))
last.click()
last.send_keys(username)
last = driver.find_element("xpath", '//*[@id="loginForm"]/div/div[2]/div/label/input')
last.click()
last.send_keys(password)
last = driver.find_element("xpath", '//*[@id="loginForm"]/div/div[3]')
last.click()
time.sleep(8)  # gives time to load if running slow, edit at your own volition

# META BUSINESS SUITE
driver.get("https://business.facebook.com/business/loginpage/?next=latest%3Fnav_ref%3Dig_web_return_path_button&login_options%5B0%5D=IG")
sdf = ("xpath", '//*[@id="globalContainer"]/div/div/div[1]/div/div/div/div/div[1]/div[3]/div/div[1]/div/div/span/div/div/div[2]')
last = wait.until(EC.element_to_be_clickable(sdf))
last.click()
driver.get("https://business.facebook.com/latest/content_calendar")

# POSTING CYCLE
for single_date in daterange:
    dirs = os.listdir(dpath)

    sdf = ("xpath", '//*[text()="Create"]')
    last = wait.until(EC.element_to_be_clickable(sdf))
    last.click()

    sdf = ("xpath", '//*[contains(text(), "Add photo")]')
    last = wait.until(EC.element_to_be_clickable(sdf))
    last.click()

    time.sleep(1)  # needed to load in button, edit at your own volition
    sdf = ("xpath", '//*[text()="Upload from desktop"]')
    last = wait.until(EC.element_to_be_clickable(sdf))
    last.click()

    time.sleep(3)  # needed to load if running slow, edit at your own volition
    keyboard.type(directory + "\\" + dirs[0])
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    pyautogui.moveTo(681, 204)
    for x in range(10):
        pyautogui.scroll(-100)
    time.sleep(3)  # needed to load if running slow, edit at your own volition
    moveAndClick(370, 236)
    pyautogui.hotkey("ctrl", "v")

    element = driver.find_element("xpath", '//*[text()="Schedule"]')
    driver.execute_script("arguments[0].click();", element)

    pyautogui.moveTo(681, 204)
    for x in range(10):
        pyautogui.scroll(-100)
    moveAndClick(270, 366)

    pyautogui.hotkey("ctrl", "a")
    for k in range(10):
        pyautogui.press("backspace")
    pyautogui.typewrite(single_date.strftime("%m/%d/%y"))
    moveAndClick(433, 366)
    for x in range(5):  # needed to register click if running slow, edit at your own volition
        pyautogui.click(433, 366)
    pyautogui.typewrite(hour)
    moveAndClick(458, 366)
    pyautogui.typewrite("0")
    moveAndClick(481, 366)
    pyautogui.typewrite(ampm)

    moveAndClick(625, 500)
    removeLatest(dirs)

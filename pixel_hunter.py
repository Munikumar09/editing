from pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pyautogui

image_path=Path("/home/munikumar-17774/Music/kia/p14/images/original")
root_path=image_path.parent

all_images=list(image_path.glob("*.jpeg"))



def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully and saved at {save_path}")
    else:
        print("Failed to download image")
        


driver = webdriver.Chrome()
wait = driver.implicitly_wait(20)
driver.get("https://pixelhunter.io/")
upload_button = driver.find_element(
    By.XPATH, "/html/body/div/div[1]/div/div[1]/div[2]/div[1]/div/button[1]"
)
result = driver.execute_script("arguments[0].click();", upload_button)
driver.maximize_window()

for i,image_file in enumerate(all_images):
    choose_file = driver.find_element(
        By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div[2]/div/button"
    ).click()

    sleep(1)
    pyautogui.click(1200, 400)

    sleep(1)

    pyautogui.hotkey("ctrl", "l")
    pyautogui.write(str(image_file))
    pyautogui.hotkey("alt", "o")
    sleep(1)
    pyautogui.press("enter")
    image_xpaths = {
        "square": "/html/body/div[1]/div[2]/div[1]/article[2]/div/div[2]/div[2]/div/img",
        "youtube": "/html/body/div[1]/div[2]/div[1]/article[4]/div/div[2]/div[2]/div/img",
        "short": "/html/body/div[1]/div[2]/div[1]/article[5]/div/div[1]/div[2]/div/img",
    }
    for key in image_xpaths.keys():
        (root_path/key).mkdir(parents=True, exist_ok=True)
    sleep(13)
    for image_type, img_xpath in image_xpaths.items():
        image = driver.find_element(By.XPATH, img_xpath)
        img_url=image.get_attribute("src")
        download_image(img_url, f"{root_path}/{image_type}/{image_type}_{i}.jpg")
    remove_ele=driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div[3]/div[1]")
    remove_ele.click()
    cancel_ele=driver.find_element(By.XPATH,"/html/body/div[3]/div[1]/div/div[2]/div[1]/div[3]/button[1]")
    cancel_ele.click()
driver.quit()
    


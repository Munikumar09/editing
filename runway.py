from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path
import requests
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import List, Any

image_path = Path("/home/munikumar-17774/Music/kia/p14/images/square")

video_path = image_path.parent.parent / "videos"
video_path.mkdir(exist_ok=True)

all_images_list = sorted(list(image_path.glob("*")))

driver = webdriver.Chrome()
wait = driver.implicitly_wait(20)
driver.get("https://app.runwayml.com/login/")
driver.maximize_window()

driver.implicitly_wait(30)

user_name = driver.find_element(By.XPATH, "//input[@name='usernameOrEmail']").send_keys(
    "catheri"
)
password = driver.find_element(By.XPATH, "//input[@name='password']").send_keys(
    "Test@3214"
)


submit_button = driver.find_element(
    By.XPATH,
    "/html/body/div[1]/div/div[5]/div[1]/div/div/div/div/div/div/div[2]/div[2]/form/button",
).click()

img_vid = driver.find_element(
    By.XPATH,
    "/html/body/div[1]/div/div[4]/div[1]/div[2]/div[2]/section/div/div/div[3]/div[2]/div[2]/button",
).click()


def download_video(url: str, file_path: Path):
    """
    Download video from url and save it to file_path

    Parameters:
    ----------
    url: ``str``
        url of video to download
    file_path: ``Path``
        path to save video
    """
    print(f"download url : {url}")
    response = requests.get(url, stream=True, timeout=60)
    print(f"download response : {response}")
    response.raise_for_status()
    
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)


# def get_video_containers(driver: WebDriver) -> List[Any]:
#     """
#     Get all video containers from the page and return them as a list

#     Parameters:
#     ----------
#     driver: ``WebDriver``
#         Selenium webdriver instance

#     Returns:
#     -------
#     ``List[Any]``
#         list of video containers
#     """
#     all_video_divs = []
#     for div in driver.find_element(
#         By.CLASS_NAME, "History__HistoryItemsContainer-sc-k9w32x-2"
#     ).find_elements(By.TAG_NAME, "div"):
#         if div.get_attribute("data-gen2-item-id") != None:
#             all_video_divs.append(div)

#     return all_video_divs


# def upload_images_and_generate_videos(
#     driver: WebDriver, all_images_list: list, video_path: Path
# ):
#     """
#     Convert images to videos and download them

#     Parameters:
#     ----------
#     driver: ``WebDriver``
#         Selenium webdriver instance
#     all_images_list: ``list``
#         list of images to convert to videos
#     video_path: ``Path``
#         path to save videos
#     """
#     j = 1

#     for i in range(len(all_images_list)):
#         wait = WebDriverWait(driver, 500)
#         driver.find_element(By.XPATH, "//input[@type='file']").send_keys(
#             str(all_images_list[i])
#         )
#         generate_video = driver.find_element(
#             By.CLASS_NAME, "GenerateButtonForNonUnlimitedPlans__Button-sc-uwwfm9-0"
#         )
#         wait.until(
#             lambda driver: driver.find_element(
#                 By.CLASS_NAME, "GenerateButtonForNonUnlimitedPlans__Button-sc-uwwfm9-0"
#             ).is_enabled()
#         )
#         generate_video.click()

#         def check_link_available(driver):
#             try:
#                 all_video_divs = get_video_containers(driver)

#                 if len(all_video_divs) < j:
#                     return False

#                 last_div = all_video_divs[-1]
#                 video_tag = last_div.find_element(By.TAG_NAME, "video")
#                 video_url = video_tag.get_attribute("src")

#                 if not video_url or video_url == "":
#                     return False

#                 return True
#             except:
#                 return False

#         wait.until(check_link_available)

#         all_video_elements = get_video_containers(driver)
#         all_video_urls = [
#             container.find_element(By.TAG_NAME, "video").get_attribute("src")
#             for container in all_video_elements
#         ]
#         download_video(all_video_urls[-1], video_path / f"{i}.mp4")
#         driver.find_element(By.CLASS_NAME, "dqZQKX").click()
#         j += 1


# upload_images_and_generate_videos(driver, all_images_list, video_path)


def get_video_containers(driver):
    all_video_divs = []
    for div in driver.find_element(By.CLASS_NAME, "History__HistoryItemsContainer-sc-k9w32x-2").find_elements(By.TAG_NAME, "div"):
        if div.get_attribute("data-gen2-item-id") != None:
            all_video_divs.append(div)
    return all_video_divs

def upload_images_and_generate_videos(driver:WebDriver, all_images_list:list, video_path:Path):
    j = 1
    print(f"all images list : {len(all_images_list)}")
    for i in range(10):
        wait = WebDriverWait(driver, 180)
        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(
            str(all_images_list[i])
        )
        generate_video = driver.find_element(
            By.CLASS_NAME, "GenerateButtonForNonUnlimitedPlans__Button-sc-uwwfm9-0"
        )
        wait.until(
            lambda driver: driver.find_element(
                By.CLASS_NAME, "GenerateButtonForNonUnlimitedPlans__Button-sc-uwwfm9-0"
            ).is_enabled()
        )
        generate_video.click()

        def check_link_available(driver):
            try:
                all_video_divs = get_video_containers(driver)
                print(f"all video urls : {len(all_video_divs)}")
                print(f"j value : {j}")
                
                if len(all_video_divs) < j:
                    return False
                
                last_div = all_video_divs[-1]
                video_tag = last_div.find_element(By.TAG_NAME, "video")
                video_url=video_tag.get_attribute("src")
                print(f"Video src : {video_url}")
                
                if not video_url or video_url=="":
                    print(f"Video url is empty {video_url}")
                    return False
                
                return True
            except: 
                return False

        wait.until(check_link_available)
        
        all_video_elements = get_video_containers(driver)
        all_video_urls = [
            container.find_element(By.TAG_NAME, "video").get_attribute("src")
            for container in all_video_elements
        ]
        print(f"all_video_urls:{len(all_video_urls)}")
        print(f"last video url : {all_video_urls[-1]}")
        download_video(all_video_urls[-1], video_path / f"{i}.mp4")
        driver.find_element(By.CLASS_NAME, "dqZQKX").click()
        j += 1


upload_images_and_generate_videos(driver, all_images_list, video_path)

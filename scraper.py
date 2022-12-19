from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

YOUTUBE_URL='https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_URL)
  time.sleep(5)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

if __name__ == "__main__":
  driver = get_driver()

  print('Fetching page')
  videos = get_videos(driver)
  
  print(f'Found {len(videos)}')



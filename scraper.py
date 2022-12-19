from selenium import webdriver
import json
from email.message import EmailMessage
import ssl
import os
import smtplib
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

YOUTUBE_URL='https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D'

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
  time.sleep(10)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

def parse_video(video):
  title_tag=video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')

  thumbnail_tag=video.find_element(By.TAG_NAME, 'img')
  thumbnail_url=thumbnail_tag.get_attribute('src')

  channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel_name = channel_div.text

  description = video.find_element(By.ID, 'description-text').text

  return {
    'title': title,
    'url': url,
    'thumbnail_url': thumbnail_url,
    'channel': channel_name,
    'description': description
  }

def send_email(body): 
  FROM_EMAIL= 'habibiahmedmohamed6@gmail.com'
  FROM_PASSWORD = os.environ["GMAIL_PASSWORD"]
  TO_EMAIL='habibiahmedmohamed6@gmail.com'
  
  subject = 'Youtube trending videos'

  em = EmailMessage()
  em['From'] = FROM_EMAIL
  em['To'] = TO_EMAIL
  em['Subject'] = subject
  em.set_content(body)

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(FROM_EMAIL, FROM_PASSWORD)
    smtp.sendmail(FROM_EMAIL, TO_EMAIL, em.as_string())


if __name__ == "__main__":
  driver = get_driver()

  print('Fetching page')
  videos = get_videos(driver)
  
  print(f'Found {len(videos)} no of videos')

  print('Parsing top 10 videos')
  videos_data = [parse_video(video) for video in videos[:10]]

  print('Save data to CSV')
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('yt_trending.csv')

  print("Send email")
  body = json.dumps(videos_data, indent=2)
  send_email(body)

  print('Finishh')
  
  


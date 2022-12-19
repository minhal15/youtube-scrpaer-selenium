"""This file runs on AWS Lambda"""

import smtplib
import time
from email.message import EmailMessage
import ssl
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_URL='https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D'


def get_driver():
  options = Options()
  options.binary_location = '/opt/headless-chromium'
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--single-process')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome('/opt/chromedriver',chrome_options=options)
  return driver

def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_URL)
  time.sleep(10)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')
  
  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

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

def lambda_handler(event, context):
    # Create the browser
    driver = get_driver()
    
    # Get the videos
    videos = get_videos(driver)
    
    # Parse the top 10 videos
    videos_data = [parse_video(video) for video in videos[:10]]
    
    # Send the data over email
    body = json.dumps(videos_data, indent=2)
    send_email(body)

    driver.close();
    driver.quit();

    response = {
        "statusCode": 200,
        "body": videos_data
    }

    return response


if __name__ == "__main__":
  lambda_handler(None, None)

    

import requests

YOUTUBE_URL='https://www.youtube.com/feed/trending'

response = requests.get(YOUTUBE_URL)

print("Status code ", response.status_code)
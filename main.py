import os
import requests
from dotenv import load_dotenv
import argparse

load_dotenv()

TOKEN = os.getenv('BITLY_TOKEN')
BITLINK_URL = 'https://api-ssl.bitly.com/v4/bitlinks'
COUNTER_URL = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'

HEADERS = {
  'Authorization': 'Bearer {}'.format(TOKEN)
}

def shorten_link(token, url):

  payload = {
  'long_url' : url
}

  response = requests.post(BITLINK_URL, headers=HEADERS, json=payload)
  short_link = response.json()['link']
  return short_link

def count_clicks(token, url):

  base_link = COUNTER_URL.format(url[7:])
  response = requests.get(base_link, headers=HEADERS)
  clicks = response.json()['total_clicks']
  return clicks


if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument('link', help='Введите ссылку для сокращения или Ваш битлинк')
  args = parser.parse_args() 
  
  user_link = args.link

  if user_link.startswith('bit.ly', 7):
    try:
      clicks = count_clicks(TOKEN, user_link)
      print('По вашей ссылке прошли {} раз(а)'.format(clicks))
    except KeyError:
      print('Указан неверный битлинк')
  else:
    try:
      bitlink = shorten_link(TOKEN, user_link)
      print('Короткая ссылка: {}'.format(bitlink))
      print('По вашей ссылке прошли {} раз(а)'.format(count_clicks(TOKEN, bitlink)))
    except KeyError:
      print('Указана невереная ссылка')

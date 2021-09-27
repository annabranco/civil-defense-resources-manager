from flask import jsonify, request
import requests
from dotenv import load_dotenv, find_dotenv
from os import environ as env

AUTH0_USER_API_BEARER_TOKEN = env.get('AUTH0_USER_API_BEARER_TOKEN')
AUTH0_DOMAIN  = env.get('AUTH0_DOMAIN')

def get_user_info(user_id):
    url = f'https://{AUTH0_DOMAIN}/api/v2/users/{user_id}'
    headers = {
      'Content-Type': "application/json",
      'Authorization': f"Bearer {AUTH0_USER_API_BEARER_TOKEN}"
    }

    response = requests.request("GET", url, headers=headers)
    return response.json()
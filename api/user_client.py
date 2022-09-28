import requests as requests
from . import USER_API_URL
from flask import session


class UserClient:
    @staticmethod
    def login(form):
        api_key = None
        payload = {
            "username": form.username.data,
            "password": form.password.data,
        }

        url = f"{USER_API_URL}/login"

        response = requests.post(url, data=payload)
        if response:
            api_key = response.json().get("api_key")

        return api_key

    @staticmethod
    def get_user():
        headers = {
            "Authorization": session['user_api_key']
        }

        url = f"{USER_API_URL}/me"
        response = requests.get(url, headers=headers)
        user = response.json().get("user")
        return user

    @staticmethod
    def create_user(form):
        user = None
        payload = {
            "password": form.password.data,
            "username": form.username.data,
        }

        response = requests.post(USER_API_URL, data=payload)
        if response:
            user = response.json().get("user")

        return user

    @staticmethod
    def user_exists(username):
        url = f"{USER_API_URL}/{username}/exists"

        response = requests.get(url)
        return response.status_code == 200

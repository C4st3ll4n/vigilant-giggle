import requests
from flask import session

from api import ORDER_API_URL


class OrderClient:
    @staticmethod
    def get_order():
        header = {
            "Authorization": session['user_api_key']
        }

        response = requests.get(ORDER_API_URL, headers=header)
        return response.json().get("order")

    @staticmethod
    def add_to_cart(book_id, quantity=1):
        payload = {
            "book": book_id,
            "quantity": quantity
        }

        header = {
            "Authorization": session["user_api_key"]
        }

        response = requests.post(ORDER_API_URL, headers=header, data=payload)
        return response.json().get("order")

    @staticmethod
    def checkout():
        header = {
            "Authorization": session["user_api_key"]
        }
        response = requests.post(f"{ORDER_API_URL}/checkout", headers=header)
        return response.json()

    def get_order_from_session(self):
        default_order = {
            "items": {}
        }
        return session.get('order', default_order)


import requests

from api import BOOK_API_URL


class BookClient:
    @staticmethod
    def get_books():
        response = requests.get(BOOK_API_URL)
        print(f"\nResponse: {response.json()}\n")
        return response.json()

    @staticmethod
    def get_book(slug):
        response = requests.get(f"{BOOK_API_URL}/{slug}")
        return response.json().get("book")

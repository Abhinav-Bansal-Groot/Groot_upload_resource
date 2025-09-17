# app/services/url_service.py
import requests
from bs4 import BeautifulSoup

class URLService:
    def extract_text(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        texts = soup.stripped_strings
        return "\n".join(texts)

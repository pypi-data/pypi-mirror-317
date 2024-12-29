import requests
import random
import re

class HadithSearcher:
    API_URL = "https://hadith-py.vercel.app/search"
    
    def __init__(self, *file_names):
        self.file_names = file_names

    def search(self, keyword):
        results = []

        for file_name in self.file_names:
            params = {
                "keyword": keyword,
                "books": [file_name]
            }
            response = requests.get(self.API_URL, params=params)
            data = response.json()

            if response.status_code == 200:
                if data.get("status", False):
                    for hadith in data['data']:
                        results.append({
                            "arabic": hadith['arabic'],
                            "english": hadith.get('english', {}),
                            "book_owner": hadith.get('book_owner', None)
                        })
            else:
                return data

        random.shuffle(results)
        return results

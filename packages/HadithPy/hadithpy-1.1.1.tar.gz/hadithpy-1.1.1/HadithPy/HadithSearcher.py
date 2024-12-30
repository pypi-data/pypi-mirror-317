import requests
import random
import re

class HadithSearcher:
    API_URL = "https://hadith-py.vercel.app/"
    
    def __init__(self, *file_names):
        self.file_names = file_names

    def search(self, keyword):
        results = []

        for file_name in self.file_names:
            params = {
                "keyword": keyword,
                "books": [file_name]
            }
            response = requests.get(f"{self.API_URL}/search", params=params)
            data = response.json()

            if response.status_code == 200:
                if data.get("status", False):
                    for hadith in data['data']:
                        
                        source = hadith.get('source', None)
                        del source['id']
                        del source['length']
                        
                        results.append({
                            "arabic": hadith['arabic'],
                            "english": hadith.get('english', {}),
                            "source": source
                        })
            else:
                return data

        random.shuffle(results)
        return results
    
    def get_books(self):
        response = requests.get(f"{self.API_URL}/books")
        data = response.json()
        return data

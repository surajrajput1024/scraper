import json
import os
from typing import List

class StorageService:
    def save_to_json(self, data: List[dict], filename: str = "scraped_products.json") -> str:
        """
        Saves the scraped data to a local JSON file.
        """
        if os.path.exists(filename):
            with open(filename, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Avoiding updating products if price has not changed
        existing_titles = [item['product_title'] for item in existing_data]

        for item in data:
            if item['product_title'] not in existing_titles:
                existing_data.append(item)

        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)

        return filename

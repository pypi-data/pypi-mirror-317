import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

class CloneUI:
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filenames to avoid illegal characters."""
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    @staticmethod
    def download_and_save(file_url, folder_name, headers):
        """Download and save files locally."""
        try:
            file_extension = file_url.split('.')[-1].lower()
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'webm', 'avi', 'css', 'js']
            if file_extension not in allowed_extensions:
                return None

            parsed_url = urlparse(file_url)
            file_path = CloneUI.sanitize_filename(parsed_url.path.lstrip("/"))
            save_path = os.path.join(folder_name, file_path)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            response = requests.get(file_url, headers=headers, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            return os.path.relpath(save_path, folder_name)
        except Exception as e:
            print(f"Failed to download {file_url}: {e}")
            return None

    @staticmethod
    def update_links(soup, base_url, folder_name, headers):
        """Update resource links in the HTML to local paths."""
        for tag in soup.find_all(["link", "script", "img", "video"]):
            attr = "href" if tag.name == "link" else "src"
            if tag.has_attr(attr):
                file_url = urljoin(base_url, tag[attr])
                local_path = CloneUI.download_and_save(file_url, folder_name, headers)
                if local_path:
                    tag[attr] = local_path

        for tag in soup.find_all("video"):
            for source_tag in tag.find_all("source"):
                if source_tag.has_attr("src"):
                    file_url = urljoin(base_url, source_tag["src"])
                    local_path = CloneUI.download_and_save(file_url, folder_name, headers)
                    if local_path:
                        source_tag["src"] = local_path

    @staticmethod
    def download_webpage(url):
        """Download a webpage and save its contents locally."""
        try:
            folder_name = f"CloneUI_{urlparse(url).hostname.replace('www.', '')}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Update links and download resources
            CloneUI.update_links(soup, url, folder_name, headers)

            # Create directory and save the HTML file
            os.makedirs(folder_name, exist_ok=True)
            with open(os.path.join(folder_name, "index.html"), "w", encoding="utf-8") as file:
                file.write(str(soup))
            print(f"Website saved in folder: {folder_name}")
        except Exception as e:
            print(f"Error: {e}")

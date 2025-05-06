import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError, NameResolutionError
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_html_links(url):
    try:
        if not url or '//' not in url:
            return []

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=5, verify=False)
        r.raise_for_status()
        html_content = r.text

        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a')

        return [link.get('href') for link in links if link.get('href')]
    
    except (requests.RequestException, MaxRetryError, NameResolutionError) as e:
        return []
    except Exception as e:
        return []
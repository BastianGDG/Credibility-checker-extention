import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError, NameResolutionError

def get_html_links(url):
    try:
        r = requests.get(url, timeout=1)
        r.raise_for_status()
        html_content = r.text

        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a')

        return [link.get('href') for link in links]
    
    except (requests.RequestException, MaxRetryError, NameResolutionError) as e:
        #print(f"Failed to fetch {url}: {str(e)}")
        return []
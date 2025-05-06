from googlesearch import search
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
import reliable_site_scraper as rsc
from dotenv import load_dotenv
import os
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

system_prompt = (
    "You are a fact checking AI. You will receive a statement and a website content. "
    "Return only one word: 'true', 'false', or 'unclear'. No explanations, no extra text."
)

def sentence_reword(STATEMENT):
    words = STATEMENT.split()
    if "is" in words:
        words.remove("is")
        words.insert(0, "is")
    elif "are" in words:
        words.remove("are")
        words.insert(0, "are")
    elif "were" in words:
        words.remove("were")
        words.insert(0, "were")
    return " ".join(words)

def google_search(query, num_results=5):
    return list(search(query, num_results=num_results))

def fetch_page_content(url):
    try:
        # If URL is empty or invalid, return early
        if not url or '//' not in url:
            print(f"Invalid URL format: {url}")
            return ""

        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # Disable SSL verification but add a warning
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        response.raise_for_status()
        
        # Parse content with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text content
        content = ' '.join([p.text.strip() for p in soup.find_all("p") if p.text.strip()])
        
        # If no paragraphs found, try getting all text
        if not content:
            content = ' '.join(soup.stripped_strings)
            
        return content[:5000]  # Limit content length to avoid overwhelmingly large texts
        
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return ""
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return ""

def fact_check(statement):
    queries = [
        f'"{statement}" scientific evidence',
        f'"{statement}" debunked'
    ]

    results = []  # will hold (url, content) pairs

    for query in queries:
        for url in google_search(query):
            content = fetch_page_content(url)
            if content.strip():
                results.append((url, content))

    return results

def ask_ai(statement, page_content):
    user_message = f"Statement: {statement}\n\nWebsite content:\n{page_content}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a highly accurate and reliable source-checking AI. "
                "You will receive a statement and a website content. "
                "Analyze the content thoroughly and decide if it CLEARLY SUPPORTS the statement, "
                "CLEARLY OPPOSES it, or if the content is UNCLEAR about the statement. "
                "Reply with exactly one word: Supports, Opposes, or Unclear. "
                "Ensure your decision is based solely on the provided content and is as precise as possible."
            )
        ),
        contents=[user_message]
    )
    return response.candidates[0].content.parts[0].text.strip()

def main(STATEMENT):
    new_statement = sentence_reword(STATEMENT)
    url_contents = fact_check(new_statement)

    whitelisted_results = []
    non_whitelisted_results = []

    for url, content in url_contents:
        reliable, domain = rsc.is_url_reliable(url)
        verdict = ask_ai(new_statement, content)
        
        result = {
            "url": url,
            "domain": domain,
            "verdict": verdict,
            "whitelisted": reliable
        }
        
        if reliable:
            whitelisted_results.append(result)
        else:
            non_whitelisted_results.append(result)

    # If no whitelisted sources found, calculate percentage based on non-whitelisted sources
    using_non_whitelisted = len(whitelisted_results) == 0 and len(non_whitelisted_results) > 0
    
    # Combine results, putting whitelisted first
    all_results = whitelisted_results + non_whitelisted_results
    
    # Calculate percentage based on appropriate source list
    results_to_use = whitelisted_results if len(whitelisted_results) > 0 else non_whitelisted_results
    total = len(results_to_use)
    supports = sum(1 for r in results_to_use if r["verdict"].lower() == "supports")
    support_percentage = (supports / total) * 100 if total > 0 else 0
        
    return all_results, support_percentage, using_non_whitelisted



if __name__ == "__main__":
    main()

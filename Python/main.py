from googlesearch import search
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
import reliable_site_scraper as rsc
from dotenv import load_dotenv
import os

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
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        content = ' '.join([p.text for p in soup.find_all("p")])
        #print(f"\n--- Content from {url} ---\n")
        #print(content[:0])
        #print("\n--- End of Content Preview ---\n")
        return content
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
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
                "You are a source-checking AI. You will receive a statement and a website content. "
                "Decide if the content SUPPORTS the statement, OPPOSES it, or is UNCLEAR. "
                "Reply with exactly one word: Supports, Opposes, or Unclear."
            )
        ),
        contents=[user_message]
    )
    return response.candidates[0].content.parts[0].text.strip()

def main(STATEMENT):
    new_statement = sentence_reword(STATEMENT)
    url_contents = fact_check(new_statement)

    results = []

    for url, content in url_contents:
        reliable, domain = rsc.is_url_reliable(url)
        if not reliable:
            continue  # skip non-whitelisted domains

        verdict = ask_ai(new_statement, content)

        results.append({
            "url": url,
            "domain": domain,
            "verdict": verdict
        })
        
    return results



if __name__ == "__main__":
    main()

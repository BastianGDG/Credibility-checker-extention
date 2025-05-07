from googlesearch import search
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
import reliable_site_scraper as rsc
from dotenv import load_dotenv
import os
import urllib3
import concurrent.futures
import time

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
    start_time = time.time()
    page_content = ""  # Default content
    duration = 0.0
    try:
        if not url or '//' not in url:
            return "", time.time() - start_time

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=1.5, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        for script in soup(["script", "style"]):
            script.decompose()
            
        content = ' '.join([p.text.strip() for p in soup.find_all("p") if p.text.strip()])
        
        if not content:
            content = ' '.join(soup.stripped_strings)
            
        page_content = content[:5000]
        
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
    except Exception as e:
        print(f"Error processing {url}: {e}")
    finally:
        duration = time.time() - start_time
    return page_content, duration

def fact_check(statement):
    queries = [
        f'"{statement}" scientific evidence',
        f'"{statement}" debunked'
    ]

    results = []  # Stores (url, content)
    fetch_durations = []  # Stores (url, duration)
    urls_to_fetch = set() # Use a set to avoid duplicate URLs from different queries

    # Concurrently perform Google searches
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(queries)) as executor:
        # Submit all google_search calls
        future_to_query = {executor.submit(google_search, query): query for query in queries}
        for future in concurrent.futures.as_completed(future_to_query):
            try:
                search_results = future.result()
                for url in search_results:
                    urls_to_fetch.add(url)
            except Exception as exc:
                print(f'Google search for query generated an exception: {exc}')

    # Convert set of URLs to a list for the next step
    urls_list_to_fetch = list(urls_to_fetch)

    # Concurrently fetch page content for all unique URLs found
    if urls_list_to_fetch:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(fetch_page_content, url): url for url in urls_list_to_fetch}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    content, duration = future.result()
                    fetch_durations.append((url, duration))
                    if content and content.strip():
                        results.append((url, content))
                except Exception as exc:
                    print(f'{url} generated an exception during fetch processing: {exc}')
    return results, fetch_durations

def ask_ai(statement, page_content):
    start_time = time.time()
    verdict = "Unclear"  # Default verdict
    duration = 0.0
    try:
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
        verdict = response.candidates[0].content.parts[0].text.strip()
    except Exception as e:
        print(f"AI call failed for statement '{statement[:30]}...': {e}")
    finally:
        duration = time.time() - start_time
    return verdict, duration

def main(STATEMENT):
    total_start_time = time.time()

    new_statement = sentence_reword(STATEMENT)
    url_contents, fetch_durations = fact_check(new_statement)

    whitelisted_results = []
    non_whitelisted_results = []
    ai_durations = []  # To store (url, duration) for AI calls

    ai_call_args = []
    for url, content in url_contents:
        ai_call_args.append((new_statement, content, url))

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_original_url = {
            executor.submit(ask_ai, stmt, cont): url_val 
            for stmt, cont, url_val in ai_call_args
        }

        for future in concurrent.futures.as_completed(future_to_original_url):
            original_url = future_to_original_url[future]
            try:
                verdict, ai_duration = future.result()
                ai_durations.append((original_url, ai_duration))
                
                reliable, domain = rsc.is_url_reliable(original_url)
                
                result = {
                    "url": original_url,
                    "domain": domain,
                    "verdict": verdict,
                    "whitelisted": reliable
                }
                
                if reliable:
                    whitelisted_results.append(result)
                else:
                    non_whitelisted_results.append(result)
            except Exception as exc:
                print(f'Processing AI result for {original_url} generated an exception: {exc}')

    using_non_whitelisted = len(whitelisted_results) == 0 and len(non_whitelisted_results) > 0
    all_results = whitelisted_results + non_whitelisted_results
    
    results_to_use = whitelisted_results if len(whitelisted_results) > 0 else non_whitelisted_results
    total_sources_for_calc = len(results_to_use)
    supports = sum(1 for r in results_to_use if r["verdict"].lower() == "supports")
    support_percentage = (supports / total_sources_for_calc) * 100 if total_sources_for_calc > 0 else 0
    
    # --- Summary of API Call Times ---
    print("\n--- API Call Time Summary ---")
    total_fetch_time = 0
    if fetch_durations:
        print("Fetch Times:")
        for url, duration in fetch_durations:
            print(f"  - Fetch {url}: {duration:.2f}s")
            total_fetch_time += duration
        print(f"Total Fetch Time: {total_fetch_time:.2f}s")
    else:
        print("No successful page fetches with duration recorded.")

    total_ai_time = 0
    if ai_durations:
        print("AI Call Times:")
        for url, duration in ai_durations:
            print(f"  - AI for {url}: {duration:.2f}s")
            total_ai_time += duration
        print(f"Total AI Time: {total_ai_time:.2f}s")
    else:
        print("No successful AI calls with duration recorded.")
    
    grand_total_api_time = total_fetch_time + total_ai_time
    print(f"Grand Total API Time (Fetch + AI): {grand_total_api_time:.2f}s")
    
    main_execution_time = time.time() - total_start_time
    print(f"Total 'main' function execution time: {main_execution_time:.2f}s")
    print("---------------------------\n")
        
    return all_results, support_percentage, using_non_whitelisted

if __name__ == "__main__":
    sample_statement = "Python is a versatile programming language."
    print(f"Running main for statement: '{sample_statement}'")
    results, percentage, using_non_whitelisted_sources = main(sample_statement)
    print("\n--- Main Function Output ---")
    print(f"Results: {results}")
    print(f"Support Percentage: {percentage:.2f}%")
    print(f"Using Non-Whitelisted Sources: {using_non_whitelisted_sources}")
    print("---------------------------\n")

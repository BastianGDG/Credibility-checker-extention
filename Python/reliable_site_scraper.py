from scraper_modules import webScraping
from scraper_modules import domain_trimmer




def get_links_cleaned(url):
    links = webScraping.get_html_links(url)
    links = set(links)

    domains_full = []
    domains_only = []


    for link in links:
        if link is not None:
            a = domain_trimmer.link_cleanup(link)
            if a is not None:
                domains_full.append((a, link))
                domains_only.append(a)
    
    domains_only = set(domains_only)

    return domains_full, domains_only




def get_all_subdomains(url):
    links, domains = get_links_cleaned(url)
    
    domains = set(domains)
    domains.add(domain_trimmer.link_cleanup(url))
        
    #for i in domains:
     #   print(i)
    
    return domains



def is_url_reliable(url):
    with open(r'Python\whitelist.txt', 'r') as file:
        whitelist = [line.strip() for line in file.readlines()]
    
    found_domains = get_all_subdomains(url)
    
    is_reliable = False
    reliable_domain = None
    
    for domain in found_domains:
        if domain in whitelist:
            is_reliable = True
            reliable_domain = domain
            break
    
    return is_reliable, reliable_domain
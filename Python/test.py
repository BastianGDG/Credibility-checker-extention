import reliable_site_scraper as m


url = "https://www.information.dk/debat/2021/10/tidligere-konspirationsteoretiker-derfor-droppede-kampen-sandheden"
temp, domain = m.is_url_reliable(url)

print(f"Is the URL reliable? {temp}, {domain} was found in the whitelist.")
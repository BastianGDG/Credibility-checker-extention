from urllib.parse import urlparse

def link_cleanup(link, only_root_name = False):
    parsed_uri = urlparse(link)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    result = result.replace("https://", "")
    result = result.replace("http://", "")
    result = result.replace("/", "")
    result = result.replace("www.", "")
    result = result.replace(":", "")
    
    result = result.split(".")

    if len(result) == 1:
        return None

    if result[-2] in ["com", "co"] and len(result) >= 3:
        result = ".".join(result[-3:])
    else:
        result = ".".join(result[-2:])

    if result != "":
        if only_root_name:
            return(result.split(".")[0])
        else:
            return(result)
    else:
        return None
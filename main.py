from bs4 import BeautifulSoup
import requests
import csv
import string
from unidecode import unidecode

def Reachable_URL(respones):
    #=> https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    status_code = respones.status_code
    
    # ALL ACCEPTED
    # 200 OK
    if status_code == 200: return True

    # 3xx Redirects
    # 301 Moved Permanently
    if status_code == 301: return True
    # 302 Found
    if status_code == 302: return True
    # 307 Temporary Redirect
    if status_code == 307: return True
    # 308 Permanent Redirect
    if status_code == 308: return True


    # ALL DENIED (LOG ERROR!)
    # 4xx Client Response Errors
    # 401 Unauthorized 
    if status_code == 401: return False
    # 403 Forbidden
    if status_code == 403: return False
    # 404 Not Found
    if status_code == 404: return False
    # 408 Request Timeout
    if status_code == 408: return False
    # 429 Too Many Requests
    if status_code == 429: return False

    # 5xx Server Response Errors
    # 500 Internal Server Error
    if status_code == 500: return False
    # 501 Not Implemented
    if status_code == 501: return False
    # 502 Bad Gateway
    if status_code == 502: return False
    # 503 Service Unavailable
    if status_code == 503: return False
    # 504 Gateway Timeout
    if status_code == 504: return False
    # 508 Loop Detected
    if status_code == 508: return False
    # 511 Network Authentication Required
    if status_code == 511: return False

def Load_URL(url):
    try:
        response = requests.get(url)
        if Reachable_URL(response):
            return response
        else: return None
    except: return None

def Clean_Link(link,DOMAIN):
    #Fix relative URL
    if 'http' not in link:
        if str(link).startswith('/'):
            link = DOMAIN + link
        else:
            link = DOMAIN + '/' + link
    #Removes the parameters
    if "?" in link:
        link = link.split('?', 1)[0]
    #Removes the jumpmark
    if "#" in link:
        link = link.split('#', 1)[0]      
    return link

def Check_Link_Validity(link):
    # Not valid if: Empty, a Telephone Link or a Mail Link
    if link == '': return False
    if 'tel:' in link: return False
    if 'mailto:' in link: return False
    return True

def Find_Links(soup,DOMAIN):
    found_links = []
    try:
        # Get all <a> Elements with a Href (Link)
        linkElements = soup.find_all('a', href=True)
        # Loop through every Element, extract the Link URL, check if it is valid and clean it
        for linkElement in linkElements: 
            link = linkElement['href']
            if Check_Link_Validity(link):
                cleaned_link = Clean_Link(link,DOMAIN)
                found_links.append(cleaned_link)
        return found_links
    except: return found_links

def store_Link(links,visited_urls,queued_urls,found_links, current_url,INTERNAL):
    for link_url in found_links:
        # Store Link (if Currrent_URL already exists, add to the List, else create a List with Link_URL)
        if current_url in links:
            links[current_url].append(link_url)
        else:
            links[current_url] = [link_url]

        # If Link has not yet been visited or queued up
        if link_url not in visited_urls and link_url not in queued_urls:
            # If Link is Internal
            if INTERNAL in link_url:
                # Add Link to Queue
                queued_urls.append(link_url) 

# CRAWLER INFORMATION

DOMAIN = "https://www.otodom.pl"
headers_ = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
responses = requests.get("https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/lodzkie/lodz/lodz/lodz",headers=headers_)
soup = BeautifulSoup(responses.text, 'lxml')
soup_divs = soup.find_all('a', href=True, class_ = "css-16vl3c1 e1x0p3r10" )
queued_urls = []
visited_urls = [] 
print("Loading")
for listing in soup_divs:
    link=Clean_Link(listing['href'],DOMAIN)
    print('*', end='')
    if not (Reachable_URL(requests.get(link,headers=headers_))):
        pass
    elif link not in visited_urls:
        queued_urls.append(link)
print("\n") 
for url in queued_urls:
    url_response = requests.get(url,headers=headers_)
    url_soup = BeautifulSoup(url_response.text,'lxml')
    url_tags = url_soup.find_all('header', class_ = "css-vutdsw efcnut33" )
    url_tags.append(url_soup.find('header', class_ = "css-1qz5jgi efcnut36" ))
    tag = url_tags[0]
    print(unidecode(tag.h1.contents[0]))
    print(url)
    price=unidecode(str(tag.strong.contents[0])).replace('zl','')
    print(int(price.replace(" ","")))
    print("-----------------------")


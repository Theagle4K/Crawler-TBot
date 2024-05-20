from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import json, codecs
from tables import create_table_from_json
from graphs import plot_price_per_area
from graphs import plot_price_per_rooms
import subprocess
from datetime import date
import os

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

def scrap_links(respondlink,DOMAIN,headers_,queued_urls):
    #Scrap links that belong to each post
    responses = requests.get(respondlink,headers=headers_)
    soup = BeautifulSoup(responses.text, 'lxml')
    soup_divs = soup.find_all('a', href=True, class_ = "css-16vl3c1 e1x0p3r10" )

    #Fix every link and add it to the list
    for listing in soup_divs:
        link=Clean_Link(listing['href'],DOMAIN)
        print('*', end='')
        #Add link to the list if only it is reachable 
        if not (Reachable_URL(requests.get(link,headers=headers_))):
            pass
        #And it is not visited
        elif link not in visited_urls:
            queued_urls.append(link)
    return queued_urls

def scrap_url(url):
    #Scrap all the contents of the url in the list
    response = requests.get(url,headers=headers_)
    soup = BeautifulSoup(response.text,'lxml')
    return soup

def scrap_postinfo(soup):
    #Scrap Tags which contain name of the post and pricing
    url_tags = soup.find_all('header', class_ = "css-vutdsw efcnut33" )
    url_tags.append(soup.find('header', class_ = "css-1qz5jgi efcnut36" ))
    return url_tags[0]

def scrap_roominfo(soup):
    #Scrap number of rooms
    #Find the issue when room number doesn't exist
    room_n = soup.find('div', attrs={'aria-label':'Liczba pokoi'})
    return int(room_n.contents[2].contents[0].text)

def scrap_expense_info(soup):
    #Scrap the expenses such as water and heating
    expenses = soup.find('div', attrs={'aria-label':'Czynsz'})
    expenses = unidecode(expenses.contents[2].text)
    #If expenses are not given
    if expenses != "Czynsz":
        expenses = str(expenses.replace(' zl/miesiac', '').split(',')[0])
        expenses = int(expenses.replace(' ', ''))
    #The value is set to 0 for easy data compression
    else: expenses = 0
    return expenses

def scrap_area_info(soup):
    #Scrap the area of the house
    area = soup.find('div', attrs={'aria-label':'Powierzchnia'})
    area=str(area.contents[4].text.split(" ")[0])
    return float(area.replace(',','.'))

def scrap_name(tag):
    #This scraps the name of the post
    return unidecode(tag.h1.contents[0])

def scrap_price(tag):
    #This scraps the price of the post
    price = unidecode(str(tag.strong.contents[0])).replace('zl','')
    return int(price.replace(' ', ""))

def ouput_data(element_list):
    #Data Output
    with open('data.json', 'wb') as f:
        json.dump(element_list, codecs.getwriter('utf-8')(f),indent=4)

def main(element_list, url):
    #Main Algorithm
    for url in queued_urls:
        url_soup = scrap_url(url)
        tag = scrap_postinfo(url_soup)
        room_n = scrap_roominfo(url_soup)
        area = scrap_area_info(url_soup)
        expenses = scrap_expense_info(url_soup)
        name = scrap_name(tag)
        price= scrap_price(tag)
        dict1 = {
            'Place-Info':{
            'Post Name' : name,
            'Number of Rooms' : room_n,
            'Area of Place' : area,
            'Monthly Spending' : expenses,
            'Price' : price, 
            'Scraped Date' : date.today().strftime('%d/%m/%Y')
            
        }}
        element_list.append(dict1)  

# CRAWLER INFORMATION
DOMAIN = "https://www.otodom.pl"
headers_ = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
respondlink = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/lodzkie/lodz/lodz/lodz"
queued_urls = []
visited_urls = [] 
element_list = []

print("Loading")
if os.path.isfile('data.json'):
    with open('data.json', 'r') as f:
            data=json.load(f)
            if data[0]["Place-Info"]['Scraped Date'] == date.today().strftime('%d/%m/%Y'):
                pass
            else: 
                url = scrap_links(respondlink,DOMAIN,headers_,queued_urls)
                main(element_list,url)
                ouput_data(element_list)
else: 
    url = scrap_links(respondlink,DOMAIN,headers_,queued_urls)
    main(element_list,url)
    ouput_data(element_list)


# Create table from data.json
create_table_from_json('data.json')

# Load the JSON data to pass to the graph functions
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Visualize and save the graphs
plot_price_per_area(data)
plot_price_per_rooms(data)

# Display the DataFrame
subprocess.call('wkhtmltoimage -f png --width 0 data.html data.png', shell=True)

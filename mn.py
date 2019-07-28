import requests
from bs4 import BeautifulSoup as bs
import csv
from concurrent.futures import ThreadPoolExecutor


count = 0
start_url = 'https://krisha.kz/prodazha/kvartiry/nur-sultan/'
paging = 'https://krisha.kz/prodazha/kvartiry/nur-sultan/?page='
main_url = 'https://krisha.kz'

ex1 = ThreadPoolExecutor(max_workers=20)
ex2 = ThreadPoolExecutor(max_workers=20)


with open('krisha.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(['rooms', 'area', 'year', 'price', 'url'])





html = requests.get(start_url).text
soup = bs(html, 'html.parser')
nav = soup.find('nav', class_='paginator')
alar = nav.findAll('a')
san = int(alar[-2].getText().strip())




def get_infos(url):
    try:
        global count
        digits = '0123456789'
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        h1 = soup.find('h1').getText().strip()
        room_count = h1[: h1.index('-')]
        area = h1.split()[2]
        price = ''
        k = soup.find('div', class_='offer__price').getText().strip().split()
        for x in k:
            uz = len(x)
            c = 0
            for xx in x:
                if (xx in digits):
                    c += 1
            if (uz == c):
                price += x

        div = soup.find('div', class_='offer__short-description')
        divs = div.findAll('div', class_='offer__info-item')
        div_year = divs[1]
        t = div_year.findAll('div')[-1].getText().strip().split()
        if (len(t) == 3):
            year = t[1]
        elif (len(t) == 2):
            year = t[0]




        with open('krisha.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow([room_count, area, year, price, url])
        count += 1
        print('yeah', count)
    except:
        count += 1
        print('no', count)






def get_page_infos(url):
    try:
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        section = soup.find('section', class_='a-list a-search-list a-list-with-favs')
        divs = section.findAll('div', class_='a-card a-storage-live ddl_product ddl_product_link not-colored is-visible')
        for div in divs:
            a = div.find('a')
            kv_url = main_url + a['href']
            # get_infos(kv_url)
            ex2.submit(get_infos, kv_url)
    except:
        pass



for i in range(1, san + 1):
    # get_page_infos(paging + str(i))
    ex1.submit(get_page_infos, paging + str(i))











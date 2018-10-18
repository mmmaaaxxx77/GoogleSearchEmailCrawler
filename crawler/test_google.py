import datetime
from time import sleep
from bs4 import BeautifulSoup
import traceback

import re
from GoogleScraper import scrape_with_config

# https://github.com/NikolaiT/GoogleScraper/blob/master/GoogleScraper/scrape_config.py
# https://github.com/NikolaiT/GoogleScraper/blob/master/GoogleScraper/search_engine_parameters.py
# https://github.com/NikolaiT/GoogleScraper

import requests
from urllib.parse import urlparse, parse_qs
from pandas import DataFrame


def run_job(tilte, url):
    query = tilte

    config = {
        'use_own_ip': True,
        'keyword': query,
        'search_engines': ['Google'],
        # 'num_results_per_page': 10,  # this is ignored by bing, 10 results per page
        'num_pages_for_keyword': 100,
        'scrape_method': 'selenium',
        # 'scrape_method': 'http',
        'sel_browser': 'chrome',
        # 'do_sleep': False,
        # 'browser_mode': 'normal',
        'browser_mode': 'headless',
        # 'chromedriver_path': '/Users/johnny/Downloads/chromedriver',
        'chromedriver_path': '/app/chromeDriver/chromedriver',
        'do_caching': False,
        # 'print_results': 'summarize',
        'google_search_url': url,
    }

    search = scrape_with_config(config)

    result = []

    print(search.serps)
    for serp in search.serps:
        for link in serp.links:
            if link.snippet and link.visible_link:
                title = link.snippet.replace("\n", "")
                link = link.visible_link

                if len(title) > 50:
                    title = f"{title[:30]}..."

                if 'https' not in link[:5]:
                    link = f'http://{link}'

                    result.append({
                        'title': title,
                        'link': link
                    })

                print(title)
                print(link)
                print("-------")
    return result


skip = [
    '.jpg', '.JPG',
    '.PNG', '.png'
]


def crawler_email(curl):
    resp = requests.get(url=curl, timeout=30)
    content = resp.text
    match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', content)
    # match = re.findall(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', content)
    match = list(set(match))

    soup = BeautifulSoup(content, 'html.parser')
    title = soup.find('title')

    for m in match:
        for sk in skip:
            if sk in m:
                del m

    if len(match) > 0:
        print(match)

    return match, title


url = 'http://gcrawler-api:8000/api/inscheduledjob'
# url = 'http://localhost:8000/api/inscheduledjob'


def save_data(id, skip_count, total_count, filename):
    data = {
        'id': id,
        'skip_count': skip_count,
        'total_count': total_count,
        'filename': filename
    }
    try:
        requests.post(url, data=data, json=True)
    except Exception as e:
        print(traceback.format_exc())
        print(f"Save Exception {e}")


def expand_url(url):
    result = []

    url_obj = urlparse(url)
    hot = url_obj.netloc
    host_url = f"{url_obj.scheme}://{url_obj.netloc}"

    resp = requests.get(url=host_url, timeout=30)
    content = resp.text

    soup = BeautifulSoup(content, 'html.parser')

    a_tags = soup.find_all('a')

    done = []
    for tag in a_tags:
        href = tag.get('href')

        r_url_obj = urlparse(href)

        if r_url_obj.path in done:
            continue
        else:
            done.append(r_url_obj.path)

        if not href:
            continue

        cont = False
        for sk in skip:
            if sk in href:
                cont = True
        if cont:
            continue

        if "mailto" in href or "javascript" in href:
            continue

        if hot in href or "http" not in href[:6]:
            r_url = href
            if "http" not in href[:6]:
                r_url = f"{host_url}{r_url}"

            result.append(r_url)

    result = list(set(result))
    print("expand_url result")
    print(result)

    return result


resp = requests.get(url=url)
data = resp.json()
print(data)
# url_obj = urlparse(data[0]['query_url'])
# query_obj = parse_qs(url_obj.query)
# print(query_obj['as_q'][0])

for da in data:
    total_result = []
    url_obj = urlparse(da['query_url'])
    print(url_obj)
    try:
        query_obj = parse_qs(url_obj.query)
        title = query_obj['as_q'][0]
        id = da['id']
        create_time = da['created_at']
        create_time = datetime.datetime.strptime(create_time, "%Y-%m-%dT%H:%M:%S.%fZ").date().strftime("%Y-%m-%d")

        skip_url = []
        if len(da['skip_url']) > 2:
            skip_url = da['skip_url']
            skip_url = skip_url.split(",")

        # get google search result
        r = run_job(title, da['query_url'])
        total_result.extend(r)
        print(total_result)

        # get host and + 1 level page
        done = []
        for res in total_result:
            stitle = res.get('title', None)
            slink = res['link']

            if slink[:10] in done:
                continue
            else:
                done.append(slink[:10])

            try:
                expand_urls = expand_url(slink)
            except Exception as e:
                print(e)
                continue
            expand_urls = list(set(expand_urls))
            total_result.extend([{
                'title': None,
                'link': ul
            } for ul in expand_urls])

        print("DONE expand_url")

        skip_count = 0

        crawler_result = []
        for res in total_result:
            stitle = res.get('title', None)
            link = res['link']

            counti = True

            for sku in skip_url:
                if sku in link:
                    counti = False
                    break
            if not counti:
                skip_count += 1
                continue

            try:
                emails, title = crawler_email(link)
                crawler_result.append({
                    'title': title if title else stitle,
                    'link': link,
                    'emails': emails
                })
                sleep(1)
            except Exception as e:
                # print(traceback.format_exc())
                print(f"Exception {link}")
                print(e)

        l1 = []
        l2 = []
        l3 = []

        for res in crawler_result:
            stitle = res['title']
            link = res['link']
            emails = res['emails']
            for email in emails:

                if email not in l3:
                    l1.append(stitle)
                    l2.append(link)
                    l3.append(email)

        df = DataFrame({'URL': l2, '網頁名稱': l1, 'EMAIL': l3})
        if not title:
            title = "無法取得網站名稱"
        else:
            title = title.replace(" ", "")

        path = "/data/"
        # path = ""
        filename = f'{create_time}_{title}.xlsx'
        df.to_excel(path + filename, sheet_name='sheet1', index=False, encoding='utf-8')

        # save
        if len(crawler_result) > 0:
            save_data(id, skip_count, len(crawler_result), filename)
    except Exception as e:
        print(traceback.format_exc())
        print(f"Exception {e}")

sleep(30)

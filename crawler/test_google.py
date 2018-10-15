import datetime
from time import sleep

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
        'num_results_per_page': 10,  # this is ignored by bing, 10 results per page
        'num_pages_for_keyword': 50,
        'scrape_method': 'selenium',
        'sel_browser': 'chrome',
        # 'do_sleep': False,
        # 'browser_mode': 'normal',
        #'chromedriver_path': '/Users/johnny/Downloads/chromedriver',
        'chromedriver_path': '/usr/local/bin/chromedriver',
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

    for m in match:
        for sk in skip:
            if sk in m:
                del m

    if len(match) > 0:
        print(match)

    return match


url = 'http://gcrawler-api:8000/api/inscheduledjob'


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
        print(f"Save Exception {e}")


resp = requests.get(url=url)
data = resp.json()
# print(data[0])
# url_obj = urlparse(data[0]['query_url'])
# query_obj = parse_qs(url_obj.query)
# print(query_obj['as_q'][0])

for da in data:
    total_result = []
    url_obj = urlparse(da['query_url'])
    query_obj = parse_qs(url_obj.query)
    title = query_obj['as_q'][0]
    id = da['id']
    create_time = da['created_at']
    create_time = datetime.datetime.strptime(create_time, "%Y-%m-%dT%H:%M:%S.%fZ").date().strftime("%Y-%m-%d")

    skip_url = []
    if len(da['skip_url']) > 2:
        skip_url = da['skip_url']
        skip_url = skip_url.split(",")

    r = run_job(title, da['query_url'])
    total_result.extend(r)

    skip_count = 0

    crawler_result = []
    for res in total_result:
        stitle = res['title']
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
            emails = crawler_email(link)
            crawler_result.append({
                'title': stitle,
                'link': link,
                'emails': emails
            })
        except Exception as e:
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
            l1.append(stitle)
            l2.append(link)
            l3.append(email)

    df = DataFrame({'URL': l2, '網頁名稱': l1, 'EMAIL': l3})
    title = title.replace(" ", "")

    path = ""
    filename = f'{create_time}_{title}.xlsx'
    df.to_excel(path + filename, sheet_name='sheet1', index=False)

    # save
    save_data(id, skip_count, len(crawler_result), filename)

sleep(30)
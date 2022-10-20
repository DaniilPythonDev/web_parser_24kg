import json
import random
import time

import requests
from bs4 import BeautifulSoup as Bs4
from fake_useragent import UserAgent


def get_page_data(url, attempt=5):
    try:
        useragent = UserAgent().chrome
        headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": f"{useragent}",
        }
        if attempt == 5:
            print(f'[INFO] start parsing -> {url} ... ', end='')
            time.sleep(random.randrange(1, 3))

        elif attempt != 5:
            print(f'[INFO] Attempt {attempt}: start parsing  -> {url} ... ', end='')
            time.sleep(random.randrange(10, 12))

        set_response = requests.get(url, headers=headers)
        # st = set_response.json()
        if set_response:
            print('done!')
            return set_response

        else:
            print('Not done!')
            raise

    except Exception as _ex:
        if attempt != 1:
            return get_page_data(url=url, attempt=attempt - 1)
        else:
            return


def news_lents(html):
    date_g = ''
    soup = Bs4(html, 'lxml')
    find_list_data = soup.find('div', {"id": "newslist"}).find_all(class_="col-xs-12")[1].find_all('div')
    dic = {'date': {}}
    for ix, block in enumerate(find_list_data):
        class_div = str(block.get('class'))
        if "one" in class_div:
            try:
                time_post = block.find(class_='time').text
                title = block.find(class_='title')
                link = f"https://24.kg{title.find('a').get('href')}"
                dic['date'][f'{date_g.strip()}'][f'time_{ix}'] = f'{time_post.strip()}'
                dic['date'][f'{date_g.strip()}'][f'title_{ix}'] = f'{title.text.strip()}'.replace('\xa0', ' ')
                dic['date'][f'{date_g.strip()}'][f'link_{ix}'] = f'{link.strip()}'

            except AttributeError as _ex:
                continue
        elif "lineDate" in class_div:
            date_g = block.text
            dic['date'][f'{date_g.strip()}'] = {}
    return dic


def write_read_json(dic_: dict = None, file_name: str = 'data.json', mod: str = 'r', ensure_ascii=False):
    with open(f'{file_name}', f'{mod}', encoding="utf-8") as file:
        if mod == 'r':
            data = file.read()
        elif mod == 'w':
            json.dump(dic_, file, indent=4, ensure_ascii=ensure_ascii)
            data = 'Done!'
        return data


def get_more_info(html):
    soup = Bs4(html, 'lxml')
    title = soup.find(class_='newsTitle').text
    text_content = soup.find('div', {"class": "cont", "itemprop": "articleBody"})
    return {'title': f"{title}", "content_text": f"{text_content}"}


def main():
    url = "https://24.kg/vlast/248515_davlenie_nasmi_hidjabyi_jenyi_oligarhov_chto_esche_volnuet_deputatov/"
    data = get_page_data(url=url)
    # dic = news_lents(data.text)
    # rez = write_read_json(dic,mod='w')
    # print(rez)
    r = get_more_info(data.text)
    print(r)


if __name__ == '__main__':
    main()

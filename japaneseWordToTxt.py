import errno
import os
import re

import requests
from bs4 import BeautifulSoup  # BeautifulSoup import

# 네이버 단어장에 있는 n?급 단어들의 예제들을 추출해서 txt 로 만들어줌

# 밑 이 두변수만 수정하면됨, 해당 변수는 n3급 35페이지까지 추출한다 라고 되어있음 (바로 밑의 주석처리 변수는 예이며 실제 변수는 main 함수에 있다)
# level = 3
# max_page = 35



url_array = []


def get_urls(n_level, number):
    url_array.clear()

    naver_url = 'https://ja.dict.naver.com'
    url = 'https://ja.dict.naver.com/jlpt/level-' + n_level + '/parts-0/p' + number + '.nhn'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    words = soup.find_all("span", class_="jp")
    for word in words:
        urls = word.find_all("a")
        for url in urls:
            url_array.append(naver_url + url['href'])


def get_words(n_level, number, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    cookie = {'JAKODICT_MODE': '1', 'JPDIC2_HURION': 'off', 'JPDIC2_EX': 'opened'}
    response = requests.get(url, headers=headers, cookies=cookie)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    word = ""
    try:
        hiragana = soup.find("span", class_="maintitle").text
        try:
            kanji = soup.find("em", class_="ps").text
            word = hiragana + " " + kanji
        except:
            word = hiragana
    except:
        pass
    print(word)
    print()

    texts = soup.find_all("li", class_="inner_lst")
    for tex in texts:
        tex = tex.find_all("p")
        try:
            for te in tex:
                try:
                    t = te.find_all("span")
                    result = re.sub(r'\([^)]*\)', '', t[1].text)
                    if len(result) > 1:
                        print(result)
                        print(number)
                        with open('n' + n_level + '/' + number + '.txt', 'a') as f:
                            f.write(result + "\n")
                except:
                    print("오류")

        except:
            pass

    print()
    print()


def create_folder(n_level):
    try:
        path1 = "n" + n_level

        if not os.path.exists(path1):
            os.makedirs(path1)

    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    return


if __name__ == "__main__":

    # n몇급짜리를?
    level = 3
    # ?페이지까지 추출할것인가
    max_page = 35

    # 폴더 생성
    create_folder(str(level))

    # 단어 추출 후 저장
    for i in range(max_page+1):
        get_urls(str(level), str(i))
        for ur in url_array:
            get_words(str(level), str(i), ur)

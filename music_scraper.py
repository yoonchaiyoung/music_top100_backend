import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient("mongodb://yoonchaiyoung:9452@18.222.215.81", 27017)
db = client.music_top100
print(db)
# db 잘 작동하는 지 확인

def scrap_vibe_top100():
    URL = "https://music.bugs.co.kr/chart"
    headers = {
        'User-Agent': "Mozilla/5.0"
    }

    data = requests.get(URL, headers=headers)
    # print("data는~~~", data)
    # print("data.text는~~~", data.text)
    # 데이터 잘 들어오는 지 확인완료

    soup = BeautifulSoup(data.text, 'html.parser')
    music_lst = soup.select("#CHARTrealtime > table > tbody > tr")
    # print(music_lst)

    # 이제 밑의 데이터들을 하나씩 뽑아서 {} 딕서너리 형태 파일에 넣기
    # 데이터 : 순위, 제목, 앨범아트, 아티스트 목록, 앨범명

    for tr in music_lst:
        rank = tr.select_one("td > div > strong").text
        # print(rank)
        title = tr.select_one("th > p > a").text
        # print(title)
        album_art = tr.select_one("td > a > img").get('src')
        # print(album_art)
        artist = tr.select_one("td > .artist > a").text
        # print(artist)
        album_name = tr.select_one("td > .album").text
        # print(album_name)

        doc = {
            "rank": rank,
            "title": title,
            "album_art": album_art,
            "artist": artist,
            "album_name": album_name
        }
        # print(doc)

        db.music.insert_one(doc)

if __name__ == "__main__":
    scrap_vibe_top100()
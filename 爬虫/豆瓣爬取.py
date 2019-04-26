#coding=UTF-8
import requests
from bs4 import BeautifulSoup
import MySQLdb


def get_movies():
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Host': 'movie.douban.com'
    }
    movie_list = []
    for i in range(0, 10):
        link = 'https://movie.douban.com/top250?start=' + str(i * 25)
        r = requests.get(link, headers=headers, timeout=10)
        print(str(i + 1), "页响应状态码:", r.status_code)

        soup = BeautifulSoup(r.text, "lxml")
        div_list = soup.find_all('div', class_='hd')
        for each in div_list:
            movie = each.a.span.text.strip()
            movie_list.append(movie)
    return movie_list


movies = get_movies()
conn = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='123456',
    db='mydjango',
    charset='utf8')
cur = conn.cursor()
sqlClear = "TRUNCATE TABLE movie_dbtop250"
cur.execute(sqlClear)
for movie in movies:
    cur.execute("INSERT INTO movie_dbtop250 (m_name) VALUES('" + movie + "')")
cur.close()
conn.commit()
conn.close()

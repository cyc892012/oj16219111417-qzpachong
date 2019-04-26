from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import re
import MySQLdb


def get_phones():
    headers = {
        "User-Agent":"Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 5.1;360SE)"
    }
    phone_list = []
    for i in range(0, 1):
        link = 'https://list.jd.com/list.html?cat=9987,653,655&page='+str(i)+'&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=10#J_main'
        r = requests.get(link, headers=headers, timeout=10)
        print(str(i + 1), "页响应状态码:", r.status_code)
        soup = BeautifulSoup(r.text, "lxml")
        div_list = soup.find_all('div', class_='p-name')
        for each in div_list:
            url = "http:"+each.a.get('href')
            phone_list.append(get_page(url))
    return phone_list

def get_page(url):
    headers = {
        "User-Agent":"Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 5.1;360SE)"
    }
    reponse = requests.get(url,headers=headers)
    if reponse.status_code == 200:
        html = reponse.text
    else:
        return None
    result_list = []
    result_dict = {}
    soup = BeautifulSoup(html,'html.parser')
    title = soup.select('.sku-name')[0].text.strip()

    caps = webdriver.DesiredCapabilities().FIREFOX
    caps["marionette"] = False
    binary = FirefoxBinary(r'F:\Program Files\Mozilla Firefox\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary, capabilities=caps)
    driver.get(url)
    price_span = driver.find_element_by_class_name("price J-p-5204048")
    price=price_span.text
    phone=[title,price]
    return phone

'''
phone_list = get_phones()
conn = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='123456',
    db='mydjango',
    charset='utf8')
cur = conn.cursor()
cur.execute("TRUNCATE TABLE movie_dbtop250")
for phone in phone_list:
    cur.execute("INSERT INTO jd_phone (p_name,p_price) VALUES('" + phone[0] + "','"+ phone[1] +"')")
cur.close()
conn.commit()
conn.close()
'''
phone = get_page("https://item.jd.com/5204048.html")
print(phone)

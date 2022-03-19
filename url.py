import requests
from bs4 import BeautifulSoup

def html(url):
    """
    urlから特定のサイトの情報をBeautifulSoup型にして返す
    """
    dummy_user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'  # 偽装エージェントの作成
    res = requests.get(url,headers={"User-Agent": dummy_user_agent})
    content = res.text  # webサイトのhtmlを取得
    soup = BeautifulSoup(content,'lxml')  # str型をBeautifulSoup型に変更
    return soup

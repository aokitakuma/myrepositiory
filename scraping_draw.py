from tkinter import *

from prefecture_dict import *
from get_data import *
from get_draw_display import *
from url import *

def choice_prefecture(cv_main,combo):
    """
    引数として、キャンバスとプルダウンリストを取得し、
    それを元にdraw_itemを呼び出す
    """
    global img_tks  # 変数をグローバル変数にしている
    img_tks = []  # スキー場の画像のurlを入れていく
    img_tks.clear()  # 配列の要素を全て消去する
    global prefecture
    prefecture = combo.get()  # プルダウンリストに表示されている都道府県が入る
    url = "https://surfsnow.jp/search/list/spl_area01.php?kencd={0}&sort=snow".format(prefecture_dict[f"{prefecture}"])  # kencd=の後に都道府県別の値を入れている
    soup = html(url)  #urlのあるサイトの情報をbs4.BeautifulSoup型にして変数に入れている

    snow_values,snow_types, weathers, place_names, img_urls = get_data(soup)  # get_data関数を呼び出し、スキー場の情報を取り出している
    for k in range(5):  # 1回目のループが第1位、2回目のループが第2位、第3位、第4位、第5位と順に表示していく
        j = k % 2  # 偶数ならキャンバスの左側に奇数ならキャンバスの右側に表示するための変数
        i = int(k / 2)  # スキー場のframeをどの行に配置する。0,0,1,1,2の順に出力したいのでi = k / 2にしてint型にすることで小数点以下を切り捨てることができる。
        if len(snow_values) > k:#スキー場のデータがあるかどうか判断する
            draw_item(cv_main,img_tks,i,j,k,snow_values,place_names,snow_types,weathers,img_urls)  # スキー場の情報をframeの中に入れて配置する
        else:
            draw_item(cv_main,img_tks,i,j,k,snow_values,place_names,snow_types,weathers,img_urls,False)  # 「存在しません」と書かれたframeを配置する

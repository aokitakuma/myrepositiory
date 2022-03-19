def get_data(soup):
    """
    引数として検索したwebサイトの情報をBeautifulsoup型で取得し、
    その情報を元にスキー場の情報(積雪深、雪質、天気、場所、画像)を返す
    """
    main_result = soup.select("body > #main_result")[0]  # スキー場の数を調べるために全てのスキー場の情報が存在しているタグを取得
    count = len(main_result.find_all(class_="list_result"))  # 検索したサイトにあるスキー場の数を取得
    
    if len(main_result.find_all(class_="section_article")) == 1:  # 関連記事を表示するタグがない都道府県があるので#section_article(関連記事を表示するタグ)を用いて場合分けをしている
        j = 3  # div:nth-of-typeの何番目から始まるか
    elif len(main_result.find_all("ul")) > 1: # そもそもスキー場がない都道府県が存在するのでulタグ(次のページに行くために使われている)を用いて場合分けをする
        j = 2
    else:
        return [],[],[],[],[]
    snow_values ,snow_types, weathers = get_condition_part(soup, count, j)  # 積雪深と雪質(ゆきしつ)と天気を取得する関数を起動
    place_names = get_place_names_part(soup, count, j)  # スキー場の名前を取得する関数を起動
    img_urls = get_image_urls_part(soup, count, j)  # スキー場の画像のＵＲＬを取得する関数を起動
    return snow_values,snow_types, weathers, place_names, img_urls

def get_condition_part(soup,count, j):
    """
    get_data関数の中で使われる。
    引数としてBeautifulsoup型の情報と検索したサイトに存在しているスキー場の情報、そしてタグが何番目から始まるかを取得して、
    スキー場の情報(積雪深、雪質、天気)を返す
    """
    snow_values = []  # 積雪深を入れていく配列
    snow_types = []  # 雪質を入れていく配列
    weathers = []  # 天気を入れていく配列

    for k in range (3):  # 1回目のループが積雪深を取得、2回目のループが雪質を取得、3回目のループが天気を取得
        x = str(k + 1)  # 積雪深や雪質や天気の情報があるタグを示す
        for i in range(count):
            condition_table = soup.select(f"body>#main_result > div:nth-of-type({i+j}) > div > table.condition")  # 積雪深や雪質などが記載されているtableタグの内容を取得
            condition_table_0 = condition_table[0]  # 取得した値は配列に入っているので、配列から取り出す
            condition = condition_table_0.select('tr:nth-of-type(1) > td:nth-of-type(' + x + ')')  # 1回目のループで積雪深が記載されているタグを取得、2回目のループで雪質が記載されているタグを取得、3回目のループで天気が記載されているタグを取得
            str_condition = str(condition)  # 文字列の部分比較を行うためにlist型の状態で文字列に変換
            if k == 0:  # 積雪深の場合
                if "cm" in str_condition:  # 部分比較よりcmが入っていない場合、値がないということ
                    snow_value = str_condition.split("<td>")[1].split("cm")[0]  # 積雪深を取得
                    snow_values.append(snow_value)
                else:snow_values.append(0)
                    
            elif k  == 1:  # 雪質の場合
                if "</td>]" in str_condition:  # 部分比較より</td>]が入っていない場合、雪質がないということ
                    snow_type = str_condition.split("<td>")[1].split("</td>]")[0]  # 雪質の取得
                    snow_types.append(snow_type)
                else:snow_types.append("-")

            elif k == 2:  # 天気の場合
                if"</td>" in str_condition:  # 部分比較より</td>が入っていない場合、天気がないということ
                    weather = str_condition.split("<td>")[1].split("</td>")[0]  # 天気の取得
                    weathers.append(weather)
                else:weathers.append("-")
    return snow_values,snow_types, weathers

def get_place_names_part(soup,count,j):
    """
    get_data関数の中で使われる。
    引数としてBeautifulsoup型の情報と検索したサイトに存在しているスキー場の情報、そしてタグが何番目から始まるかを取得して、
    スキー場の名前を返す
    """
    place_names = []  # スキー場の名前を入れていく配列
    for i in range(count):
        soup_name = soup.select(f"#main_result > div:nth-of-type({i + j}) > h2 > a")  # スキー場の名前が記載されているタグを取得
        place_name = soup_name[0].contents[0]  # aタグの記載内容(list型)を取り出す
        place_name = str(place_name)  # bs4.element.NavigableString型をstring型に変換
        place_names.append(place_name)
        
    return place_names

def get_image_urls_part(soup,count,j):
    """
    get_data関数の中で使われる。
    引数としてBeautifulsoup型の情報と検索したサイトに存在しているスキー場の情報、そしてタグが何番目から始まるかを取得して、
    スキー場の画像を返す
    """
    img_urls = []  # スキー場の画像のurlを入れていく配列
    for i in range(count):
        soup_img = soup.select(f"#main_result > div:nth-of-type({i + j}) > h3 > a > img")  # スキー場の画像のurlが記載されているタグを取得
        soup_img = soup_img[0]
        soup_img = str(soup_img)  # bs4.element.Tag型を文字列型に変換
        img_url = soup_img.split("src=\"")[1].split("\"/>")[0]  # スキー場の画像のurlを取得
        if img_url == "/contents/img/search/pc/no_image.jpg":  # 画像がNo Imageとなっている場合
            img_url = "https://surfsnow.jp/contents/img/search/pc/no_image.jpg"  # No Imageのurlを入れる
        elif ".gif" in img_url:  # スキー場の画像が.gifの場合
            img_url = "https://surfsnow.jp/contents/img/search/pc/no_image.jpg"  # No Imageのurlを入れる
        img_urls.append(img_url)                  
    return img_urls        

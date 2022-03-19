from tkinter import *
from PIL import Image,ImageTk
from urllib.request import urlopen

def draw_item(cv_main,img_tks,row,column,k,snow_values,place_names,snow_types,weathers,img_urls,exist=True):
    """
    スキー場の情報をframe_mainの中に入れてキャンバスに配置する
    """
    if exist == True:  # スキー場の情報が存在するかどうか
        frame_main = Frame(cv_main,relief="groove",bd=5,width=645,height=130)  # スキー場の情報を載せるframe_mainを作成
        frame_main.grid(row=row,column=column)  # frameを配置
        frame_main.grid_propagate(0)  # frameのサイズを固定
        frame_left = Frame(frame_main)  # スキー場の図を載せるためにframe_mainの中の左側にframe_leftを作成
        frame_left.grid(row=0,column=0)  # frame_leftを配置
        frame_right = Frame(frame_main)  # 積雪深や雪質を表示するためにframe_mainの中の右側にframe_rightを作成
        frame_right.grid(row=0,column=1)  # frame_rightを配置
        #左側のキャンバス
        cv_left = Canvas(frame_left,width=310,height=115)  # frame_leftの中にキャンバス(cv_left)を作成する
        cv_left.grid(row=0,column=0)  # cv_leftを配置
        cv_left.grid_propagate(0)  # cv_leftのサイズを固定
        img = Image.open(urlopen(img_urls[k]))
        w = img.width #imgの幅を取得
        h = img.height #imgの高さを取得
        img = img.resize(( int(115 * (w/h)),115 )) #imgの大きさをリサイズ
        img_tk=ImageTk.PhotoImage(img)  # スキー場の画像を変数に入れる
        img_tks.append(img_tk) # スキーの画像を配列の中に入れる
        cv_left.create_image(155,57,image=img_tks[k])  # キャンバス(cv_left)の真ん中に画像を表示
        #右側のキャンバス
        cv_right = Canvas(frame_right,width=310,height=115)  # frame_rightの中にキャンバス(cv_right)を作成
        cv_right.grid(row=0,column=0)  # frame_rightを配置
        cv_right.grid_propagate(0)  # frame_rightのサイズを固定
        rank=Label(cv_right,text=f"第{k+1}位")  # 第何位かを表示するラベル(rank)を作成
        rank.grid(row=0,column=0,sticky=E+W)   # rankをcv_rightの1番上に配置
        label_place_name = Label(cv_right,text=f"場所:{place_names[k]}")  # 場所を表示するラベル(label_place_name)を作成
        label_place_name.grid(row=1,column=0,sticky=E+W)  # label_place_nameを上から2番目に配置
        label_snow_value = Label(cv_right,text=f"積雪深:{snow_values[k]}")  # 積雪深を表示するラベル(label_snow_value)を作成
        label_snow_value.grid(row=2,column=0,sticky=E+W)  # label_place_nameを上から3番目に配置
        label_snow_type = Label(cv_right,text=f"雪質:{snow_types[k]}")  # 雪質を表示するラベル(label_snow_type)を作成
        label_snow_type.grid(row=3,column=0,sticky=E+W)  # label_snow_typeを上から4番目に配置
        label_weather = Label(cv_right,text=f"天気:{weathers[k]}")  # 天気を表示するラベル(label_weather)を作成
        label_weather.grid(row=4,column=0,stick=E+W)  # label_weatherを上から5番目に配置
        cv_right.rowconfigure(0,weight=1)  # 0行目に配置されているLabelを指定した方向へと引き延ばす
        cv_right.rowconfigure(1,weight=1)  # 1行目に配置されているLabelを指定した方向へと引き延ばす
        cv_right.columnconfigure(0,weight=1)  # 0列目に配置されいるLabelを指定した方向へと引き延ばす
    else:
        frame_main = Frame(cv_main,relief="groove",bd=5,width=645,height=130)  # 「存在しません」というLabelを入れるためのフレーム(frame_main)を用意
        frame_main.grid(row=row,column=column)  # frame_mainを配置
        frame_main.grid_propagate(0)  # frame_mainのサイズを固定
        label_no_exist = Label(frame_main,text="存在しません")  # 「存在しません」と表示したラベル(label_no_exist)を作成
        label_no_exist.grid(row=0,column=0,sticky="wens")  # label_no_existを配置
        frame_main.rowconfigure(0,weight=1)  # 0行目に配置されているLabelを指定した方向へと引き延ばす
        frame_main.columnconfigure(0,weight=1)  # 0列目に配置されいるLabelを指定した方向へと引き延ばす

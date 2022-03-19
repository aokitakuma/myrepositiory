from tkinter import *
from tkinter import ttk
from scraping_draw import *

if __name__ == "__main__":
    win = Tk()  # ウィンドウの作成
    win.state("zoomed")  # ウィンドウを全画面にする
    win.title("ski_best_choice")  # ウィンドウのタイトル
    cv_main = Canvas(win)  # キャンバスの作成
    cv_main.place(x=0, y=110, width=1300, height=550)  # キャンバスの配置
    combo = ttk.Combobox(win, values=pull_down_list, state="readonly")  # プルダウンリストを作成  記入不可にすることでユーザーにミスを起こさせない．ユーザーのストレスを減らすことに繋がる
    combo.set("北海道")  # プルダウンリスト
    combo.place(x=100,y=20)  # プルダウンリストを配置
    button = ttk.Button(win,text="表示",width=50,command=lambda :choice_prefecture(cv_main,combo))  #ボタンの作成 ボタンを押すとchoice_prefecture関数が呼び出される
    button.place(x=400,y=20)  # ボタンの配置
    win.mainloop()

from numpy.lib.function_base import append
from openpyxl.worksheet import worksheet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core import groupby
import seaborn as sns
import math
from sklearn.preprocessing import LabelEncoder

import_file_path="C:/Users/aokik/OneDrive/ドキュメント/GitHub/excel"#データを取り出すためのパス
export_file_path="C:/Users/aokik/OneDrive/ドキュメント/GitHub/excel/output"#出力するためのパス

def labelencode(x):
    le=LabelEncoder()
    return le.fit_transform(x)

data=pd.read_excel(import_file_path+"/"+"人間の馬力実験.xlsx")
df_data=data.copy()#dataをコピーしておき、これからはdf_dataを使う

index_count=df_data.shape[0]#取得したデータの行数
columns_count=df_data.shape[1]#取得したデータの列数
null_count=df_data.isnull().any().sum()#データの中にある欠損値の数
columns_name=df_data.columns#列を名前を入れる

if null_count>0:
    df_data=df_data.dropna(how="any",axis=0)
    index_count=df_data.shape[0]#新しい行数を代入


#objectかどうかの判別
obj_columns=[]#object型のlist
obj_columns_len=0
for column in columns_name:
    if df_data[column].dtype=="object":
        obj_columns.append(column)#objectだった列を入れておく
obj_columns_len=len(obj_columns)

#objectごとにgroupby()を使う
obj_group=pd.DataFrame()
for i in range(obj_columns_len):
    obj_group=df_data.groupby(obj_columns[i]).mean()
    obj_group.to_excel(export_file_path+"/"+f"group_{obj_columns[i]}.xlsx")


#objectの列をlabel化するしてdf_dataにくっつける
label_data=df_data[obj_columns].apply(labelencode)
df_data=pd.concat([df_data.drop(obj_columns,axis=1),label_data],axis=1)#df_dataからobject型の列を除去したものとobject型の列をlabelにしたものをくっつけた


#列同士の回帰直線を作った際の傾きと切片をDataFrameにしている
coef_df=pd.DataFrame(index=columns_name,columns=columns_name)
for x_name in columns_name:
    for y_name in columns_name:
        coef=np.polyfit(x=df_data[x_name],y=df_data[y_name],deg=1)
        coef_str=f"傾き:{round(coef[0], 2 - math.ceil(math.log10(abs(coef[0]))))} 切片:{round(coef[1], 2 - math.ceil(math.log10(abs(coef[1]))))}"
        coef_df.loc[x_name,y_name]=coef_str
coef_df.reset_index(inplace=True)
coef_df.to_excel(export_file_path+"/"+"coef_df.xlsx")


#object型の列を除いた列だけでグラフを書いている
obj_except_data=df_data.drop(obj_columns,axis=1)
sns.pairplot(obj_except_data,kind="reg")
plt.savefig("pairplot.png")


#coef_dfにグラフを貼り付けている
import openpyxl
from openpyxl.drawing.image import Image

wb=openpyxl.load_workbook(export_file_path+"/"+"coef_df.xlsx")
img=Image("pairplot.png")
ws=wb.worksheets[0]
ws.add_image(img,"K2")
wb.save(export_file_path+"/"+"coef_df.xlsx")

#今ある技術でどれだけ様々なデータ(列が違ったり、行が違ったり)のグラフを表示できるかを試した
#頑張ったところグラフの丁寧さ

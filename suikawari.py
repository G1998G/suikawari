import random as random
import PySimpleGUI as sg
import math as math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox 
from matplotlib import animation
import sqlite3 as sqlite3
from PIL import Image as pl_img
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys as sys

#-----------------------------------------------------------------------------
#ゲーム値設定

n = 5 #移動可能回数
m_list= list(range(0,2)) #1回の移動可能メートル
randint_range =(0,5) #初期座標範囲

#-----------------------------------------------------------------------------
class Zahyou_input: #スイカとユーザーの初期座標を作成
    def zahyou(self):
        x = random.randint(randint_range[0],randint_range[1])
        y = random.randint(randint_range[0],randint_range[1])
        zahyou = [x,y]
        return zahyou



class Zahyou_check: #各種判定用
    def zahyou_distance(self,watermelon,user): #三平方の定理で２座標間の距離取得
        self.watermelon = watermelon
        self.user = user
        x_distance=2**(watermelon[0]-user[0])
        y_distance=2**(watermelon[1]-user[1])
        distance= round(math.sqrt(x_distance + y_distance),2)
        return distance

    def result (self): #結果判定メソッド
        if distance == 0:
            return 'おめでとうございます！スイカを割ることができました。'
        else :
            return 'スイカ割り失敗です。'



class Zahyou_Select: #選択座標を計算
    def make_input_amount(self,values):#
        self.values =input_dict 
        get_y = input_dict.get('sn_select') #keyを取り出す
        get_x = input_dict.get('ew_select') #keyを取り出す
        if get_y == southnorth[0]: #keyが北と一致する場合y座標にプラス
            y_input = input_dict.get('x_m')
        elif get_y == southnorth[1]: #keyが南と一致する場合y座標にマイナス
            y_input = (0 - input_dict.get('x_m'))
        if get_x == eastwest[0]:
            x_input = input_dict.get('y_m')
        elif get_x ==eastwest[1]:
             x_input = (0-input_dict.get('y_m'))           
        input_amount = [int(x_input),int(y_input)] 
        return input_amount #入力された移動数

    def zahyou_move(self,user,input_amount): #入力された移動数をuser座標に反映
        self.user = user
        self.input_amount = input_amount
        user[0] = input_amount[0] + user[0]
        user[1] = input_amount[1] + user[1]
        return user




class SQL: 
    def __init__(self):
        global conn
        global cur
        conn = sqlite3.connect(":memory:") #メモリに一時保存
        cur = conn.cursor()
        cur.execute('CREATE TABLE zahyou_memory (x INTEGER ,y INTEGER)') #tableの作成

    def sql_save (self,zahyou): #座標を記録する
        self.zahyou = zahyou
        # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
        # executeメソッドの第2引数に?に当てはめる値をタプルで渡す
        sql = 'insert into zahyou_memory (x,y) values (?,?)'
        zahyou_memory = (zahyou[0], zahyou[1])
        cur.execute(sql, zahyou_memory)
    
        #記録をリストとして取り出し
        global saved_list
        saved_list = []
        for make_list in cur.execute("SELECT * From zahyou_memory "): 
            saved_list.append(make_list)
        return saved_list #saved_listは二次元配列となる。
    
    def close_sql(self): #メモリからデータ削除
        conn.close()
#***************************************************************************
class Matplt:

    def plot_images(self,x, y, image, ax=None): #マーカー画像表示用
        self.x = x
        self.y = y
        self.image = image
        self.ax = ax
        ax = ax or plt.gca()
        im = OffsetImage(image, zoom=5/ax.figure.dpi)
        im.image.axes = ax
        ab = AnnotationBbox(im, (x,y), frameon=False, pad=0.0)
        ax.add_artist(ab)

    def plotdata(self): #グラフプロット

        fig = plt.figure(figsize= (4, 3))
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1) #余分な余白を無くす
        ax = fig.add_subplot(1, 1, 1)
        ax.axis("off") #座標表示など消す
        x,y = zip(*saved_list) #二次元配列を解体
        footprint = ax.scatter(x,y) 
        ax.plot (x,y)       
        ax.scatter(watermelon[0],watermelon[1])

        #https://stackoverflow.com/questions/2318288/how-to-use-custom-png-image-marker-with-plot 参考
        path = ['watermelon.png','user.png']
        watermelon_image = plt.imread(path[0])
        user_image = plt.imread(path[1])
        self.plot_images(watermelon[0], watermelon[1], watermelon_image, ax=ax) #スイカのscatter画像で表示
        for x , y in zip(x,y): #userのscatterを画像で表示 #イテラブルな値を受け付けないのでint化
            self.plot_images(x, y, user_image, ax=ax) 

        #ims = []
        #ims.append(footprint)
        #ani = animation.ArtistAnimation(fig, ims, interval=50, repeat=True) pysimpleguiにemmbedすると動かない

        xlim = ax.get_xlim() #x軸の範囲を取得
        ylim = ax.get_ylim() #y軸の範囲を取得
        im = pl_img.open("beach-sand-pattern-5.jpg")
        ax.imshow(im, extent=[*xlim, *ylim], aspect='auto') #背景画像表示。x,ylimを使いplotグラフと同じサイズにする。
        return fig
    
    def draw_figure(self,canvas, figure):
        #https://qiita.com/bear_montblanc/items/cce4e8c58dfa236200f6 よりコピペ↓　pysimpleguiに埋め込む
        self.canvas = canvas
        self.figure = figure
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
#-----------------------------------------------------------------------------
#インスタンス作成
watermelon_initial=Zahyou_input()
user_initial=Zahyou_input()
hantei=Zahyou_check()
zahyou_select = Zahyou_Select()
sql =SQL()
matplt = Matplt()
#-----------------------------------------------------------------------------
watermelon=watermelon_initial.zahyou() #初期座標取得
user=user_initial.zahyou() #初期座標取得
sql.sql_save(user) #初期座標の保存
distance=hantei.zahyou_distance(watermelon,user) #初回距離判定
#-----------------------------------------------------------------------------
#GUI 
southnorth=['南に','北に'] 
eastwest=['東に','西に']
#最初のウィンドウのレイアウト
layout = [[sg.Image(pl_img.open("beach-sand-pattern-5.jpg"))],
[sg.Text('スイカから'+str(distance)+'M距離があります。', key='tx1')],
[sg.Text('あと'+str(n)+'回移動できます',key='tx2') ],
[sg.Combo(southnorth, default_value=southnorth[0],key='sn_select',size=(5, 1)),sg.Combo(m_list,default_value=m_list[0],key='x_m'),sg.Text('M、')],
[sg.Combo(eastwest, default_value=eastwest[0],key='ew_select',size=(5, 1)),sg.Combo(m_list,default_value=m_list[0],key='y_m'),sg.Text('M移動する。')],[sg.Button('移動する',key='execute_button'),sg.Button('ゲームをリセット',key='reset_button'),sg.Button('ゲームを終了する',key='finish_button')]] 
window1 = sg.Window('スイカ割りゲーム',layout ,size=(300,300)) #最初のウィンドウを表示させる

while True: #最初のウィンドウの処理
    event, values = window1.read() # イベントの読み取り
    print(str(5-n)+'回目の移動'+'イベント:',event,',値:',values)
    if event == None:
        sys.exit()
    elif n <1: #残り移動可能数が0の場合
        break
    elif event =='finish_button':
        sys.exit()
    elif event =='reset_button':
        break
    elif event =='execute_button': #ボタンが押された場合
        input_dict =values #valuesをinput_dictという辞書にする
        input_amount =zahyou_select.make_input_amount( input_dict )
        user=zahyou_select.zahyou_move(user,input_amount)
        print(user)
        distance=hantei.zahyou_distance(watermelon,user) 
        sql.sql_save(user) #座標を記録する
        print('距離'+str(distance))
        n -=1 #ボタンを押すごとに残り移動回数を減らす
        window1['tx1'].Update('スイカから'+str(distance)+'M距離があります。')
        window1['tx2'].Update('あと'+str(n)+'回移動できます.')
        if distance == 0: #スイカとの距離が０になった場合
            break
        else: #スイカと距離がある場合
            continue

window1.close()
result = hantei.result() #結果を判定
#-----------------------------------------------------------------------------
#結果ウィンドウのレイアウト
result_layout =[[sg.Text('スイカの位置は以下の通りでした。')],[sg.Text(watermelon)],  
[sg.Text('あなたの位置は以下の通りに推移しました。')],[sg.Text(saved_list)],[sg.Text(result)],[sg.Canvas(key='-CANVAS-')],
[sg.Button('リトライ',key='retry_button'),sg.Button('ゲームを終了する',key='finish_button')] ]
result_window = sg.Window ('スイカ割りゲーム結果',result_layout,finalize=True) #結果表示ウィンドウを表示させる

fig = matplt.plotdata()
fig_agg = matplt.draw_figure(result_window['-CANVAS-'].TKCanvas,fig) #canvasの中身

while True: #結果ウィンドウの処理
    event, values = result_window.read()
    if event == None:
        sys.exit()
    elif event =='retry_button':
        window1 = sg.Window('スイカ割りゲーム',layout) 
        break
    elif event =='finish_button':
        sys.exit()
        
result_window.close()
print(saved_list)
matplt.plotdata()
sql.close_sql()
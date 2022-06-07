from turtle import pos
import pygame as pg
import random
import sys
import time

hxy_list = [(150, 175),(400, 175),(650, 175),(150, 450),(400, 450),(650, 450)]  #ゲーム内で使うxy座標のリスト
K_list = [ "Q", "W", "E", "I", "O", "P"]    #穴に対応するキーの文字を表示するためのリスト
KF_list = [ pg.K_q, pg.K_w, pg.K_e, pg.K_i, pg.K_o, pg.K_p] #キーのリスト
score = 0       #モグラをたたいた回数のカウント
score_kf = 0    #スコアを一秒間に一回のみカウントするためのフラグ
n = 30      #モグラをたたく回数

class Screen:              #ウィンドウの作成
    def __init__(self, xy, title):
        pg.display.set_caption(title)   #ウィンドウの名前の設定
        self.scr = pg.display.set_mode(xy)       #画面用のsurface
        self.scr.fill((169, 206, 236)) #画面を水色で作成


class hole(pg.sprite.Sprite):
    def __init__(self, r, xy):
        super().__init__()
        self.r = r  #穴の半径
        self.image = pg.Surface((self.r, self.r)) # モグラの穴のSurface
        self.image.set_colorkey((0,0,0))     # 円の外側部分を透過する
        self.rect = self.image.get_rect()      # 穴用Rect
        self.rect.centerx, self.rect.centery = xy   #穴用rectの座標

    def update(self, hole, scr):
        pg.draw.circle(scr.scr, (101,80,88),(self.rect.centerx, self.rect.centery), self.r) # モグラの穴Surfaceに円を描く
        hole.draw(scr.scr)  #描画


class key_place(pg.sprite.Sprite):    #穴に対応するキーを表示する
    
    def __init__(self, font, i):
        super().__init__()
        self.text = font.render( K_list[i], True, (153,153,153)) #フォントのサーフェイス
        self.x, self.y = hxy_list[i]    #文字を表示するxy座標を定める

    def update(self, scr):
        scr.scr.blit(self.text, (self.x-50, self.y-50)) #文字を描画



def i_scr(scr, font):   #スタート画面の作成
    while True: 
        ft_i = (250,250)     #文字の描画位置
        text = font.render("Press R to start game", False, (255,255,255))
        scr.scr.blit(text, ft_i) #文字を描画
        pg.display.update()   
        for event in pg.event.get():    #eventの種類を受け取る
            if event.type == pg.QUIT:   #Xボタンを押したとき
                return pg.quit()        #ウィンドウを閉じる
            if event.type == pg.KEYDOWN: #キーを押したとき
                if event.key == pg.K_r: #rキーを押したとき
                    return

def f_scr(scr, font):   #スタート画面の作成
    while True: 
        scr.scr.fill((169, 206, 236))   #背景を水色で埋める
        ft_i = (300,150)     #文字の描画位置
        text = font.render("Game Clear", False, (255,255,255))  #textのサーフェイス
        scr.scr.blit(text, ft_i)
        pg.font.init()
        text1 = font.render("Press ESC to exit the game", False, (255, 255, 255))
        scr.scr.blit(text1, (200, 200))
        pg.font.init()
        text2 = font.render("made by C0B21012", False, (255, 255, 255))
        scr.scr.blit(text2, (250, 350))
        pg.display.update()   
        for event in pg.event.get():    #eventの種類を受け取る
            if event.type == pg.QUIT:   #Xボタンを押したとき
                return pg.quit()        #ウィンドウを閉じる
            if event.type == pg.KEYDOWN: #キーを押したとき
                if event.key == pg.K_ESCAPE: #escapeキーを押したとき
                    return


def mole(scr, figure):
    x,y = hxy_list[figure]  #画像のxy座標
    pos = pg.mouse.get_pos()
    if score_kf == 0:
        mole_img = pg.image.load("kadai06/mogura.png")  #モグラの画像
        mole_img = pg.transform.rotozoom(mole_img, 0 , 0.2) #モグラの画像の大きさの調整
        scr.scr.blit(mole_img, (x-50, y))
    if score_kf == 1:
        mole_img = pg.image.load("kadai06/mogura2.png") #たたかれたモグラの画像
        mole_img = pg.transform.rotozoom(mole_img, 0 , 0.075) #たたかれたモグラの画像の大きさ調整
        font2 = pg.font.SysFont(None, 70)
        point = font2.render("+1", True, (0, 0, 0))
        scr.scr.blit(mole_img, (x-75, y-25))
        scr.scr.blit(point, (x-50, y))




def key_flag(figure):
    global score, score_kf
    pressed = pg.key.get_pressed()
    if pressed[KF_list[figure]]:    #リストに対応するキーが押されたときに
        if score_kf == 0:
            score_kf = 1            #スコアカウントのフラグ
            score += 1              #モグラを叩いた回数のカウント


def score_disp(scr, font):
    obj = n        #モグラをたたく回数
    pg.font.init()
    text = font.render( "SCORE:"+str(score) + " (remain" + str(obj-score) + ")", False, (255,255,250)) #フォントのサーフェイス
    scr.scr.blit(text, (0, 0))
    

def game_h(scr, font):
    global score_kf
    scr.img = pg.image.load("kadai06/kusa.jpg")  # 背景画像用のSurface
    scr.img = pg.transform.rotozoom(scr.img, 0, 2.0)
    scr.rect= scr.img.get_rect()    # 背景画像用のRect
    figure = random.randint(0, 5)   #ランダムな数字を得る
    start_time = time.time()    #計測初めの時間

    holes = pg.sprite.Group()       #穴のスプライトグループを作成
    for i in hxy_list:
        holes.add(hole(100.0, i))
    
    k_bind = pg.sprite.Group()      #穴に対応するキーの文字のスプライトグループ
    for i in range(len(K_list)):    
        k_bind.add(key_place(font, i)) 

    while True:
        scr.scr.blit(scr.img, scr.rect)
        holes.update(holes, scr)    #updateメソッドを呼び出す
        k_bind.update(scr)
        count = time.time()         #現在時刻の計測
        if (count - start_time) >= 1:   #一秒経過したときに呼び出し
            score_kf = 0                #1秒間の一度だけscoreを数えるためのフラグ
            start_time = count          #start_timeにcountを代入する
            figure = random.randint(0, 5)
        mole(scr, figure)       #モグラの画像の呼び出し 
        score_disp(scr, font)   #スコアの表示
        pg.display.update()       
        for event in pg.event.get():    #eventの種類を受け取る
            if event.type == pg.QUIT:   #Xボタンを押したとき
                return pg.quit()
        key_flag(figure)    #モグラをたたいた回数の処理
        if score == n:     #モグラをn回たたいたら終了
            return
       



def main():
    scr_xy = (800, 600)     #画面の大きさ
    scr = Screen(scr_xy, "モグラたたき") #画面のインスタンス
    font = pg.font.Font(None, 50)   #文字のフォントを作成
    
    i_scr(scr, font)    #スタート画面の表示
    game_h(scr, font)   #ゲーム本体
    f_scr(scr, font)    #エンディング画面の表示



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
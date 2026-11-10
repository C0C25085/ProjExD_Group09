import math
import os
import random
import sys
import time
import pygame as pg


WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：食材のRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


class Aiming:
    """
    照準クラス
    """
    def __init__(self):
        self.img = pg.image.load("fig/syoujyun.png")
        self.img = pg.transform.rotozoom(self.img, 0, 0.07)
        self.rct = self.img.get_rect()
        self.rct.center = 550,325


class Food:
    def __init__(self,name,img,x,y):
        self.name = name
        self.img = pg.image.load(img)
        self.img = pg.transform.rotozoom(self.img, 0, 0.2)
        self.rct = self.img.get_rect()
        self.rct.center = (x, y)


#書き足したスコアクラス
class Score:
    """
    スコアクラス
    引数:なし
    戻り値:なし
    """
    def __init__(self):
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50) #スコア用のフォント・初期値・描画位置の設定
        self.color = (255, 0, 0)
        self.value = 0 #スコアの初期値
        self.img = self.fonto.render(f"スコア:{self.value}", 0, self.color)
        self.rct = self.img.get_rect()
        self.rct.center = (100, HEIGHT - 50) #画面左下に配置

    def update(self, screen: pg.Surface): #スコアの数値を毎フレーム更新して画面に描画
        self.img = self.fonto.render(f"スコア:{self.value}", 0, self.color)
        screen.blit(self.img, self.rct)


#書き足したゲームオーバークラス
def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバークラス
    引数:screen
    戻り値:なし
    """
    jimg = pg.image.load("fig/jikan_gire.png")#画像を読み込む
    jimg = pg.transform.scale(jimg, (WIDTH, HEIGHT))#画面のサイズに合わせて拡大・縮小
    screen.blit(jimg, [0, 0])#画面の左上に貼り付ける


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/mori.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    aiming = Aiming()
    #スコアとタイマー設定↓
    score = Score()
    time_limit = 30  #制限時間
    start= pg.time.get_ticks()  # 開始時の時間
    font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
    #スコアとタイマー設定↑

    while True:
        #残り時間の計算とタイムアップ↓
        nokori = (pg.time.get_ticks() - start) / 1000
        timeup = max(0.0, time_limit - nokori)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pass  #シュートするやつに書き換える

        #ゲームオーバー画面↓
        if timeup <= 0:
            gameover(screen)
            pg.display.update()
            time.sleep(5) #5秒待機
            return
            
        screen.blit(bg_img, [0, 0])
        screen.blit(aiming.img,aiming.rct)
        score.update(screen)  #スコアを画面に表示
        time_mo = font.render(f"残り時間: {timeup:.1f}", True, (255, 255, 0))  #残り時間の文字
        time_rct = time_mo.get_rect()
        time_rct.center = (WIDTH - 190, HEIGHT - 50)
        screen.blit(time_mo, time_rct) # 残り時間を画面に表示


        pg.display.update()
        
        clock.tick(60)       
        
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
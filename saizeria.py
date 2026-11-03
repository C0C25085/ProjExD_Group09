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

def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/mori.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    aiming = Aiming()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pass  #シュートするやつに書き換える
            
        screen.blit(bg_img, [0, 0])
        screen.blit(aiming.img,aiming.rct)
        pg.display.update()
        
        clock.tick(60)       
        
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
import math
import os
import random
import sys
import time
import pygame as pg


WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SOUND_FILE = "sound/ピコッ.mp3"  # 効果音のファイル
SE_MAXTIME = 500 #効果音の長さ

MISS_SOUND_FILE = "sound/パフ.mp3"  #外れた時の効果音
MISS_SE_MAXTIME = 300


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
        self.normal_img = pg.image.load("fig/syoujyun.png")
        self.normal_img = pg.transform.rotozoom(self.normal_img, 0, 0.07)

        self.exp_img = pg.image.load("fig/explosion.gif")
        self.exp_img = pg.transform.rotozoom(self.exp_img, 0, 0.5)

        self.img = self.normal_img
        self.rct = self.normal_img.get_rect()
        self.rct.center = 550,325
        self.speed = 10
        self.exp_timer = 0 #爆発画像の残り時間
        self.mask = pg.mask.from_surface(self.img) #透過の余白部分を除外

    def update(self, key_lst: list[bool]):
        #矢印キーで移動
        if key_lst[pg.K_UP]:
            self.rct.centery -= self.speed
        if key_lst[pg.K_DOWN]:
            self.rct.centery += self.speed
        if key_lst[pg.K_LEFT]:
            self.rct.centerx -= self.speed
        if key_lst[pg.K_RIGHT]:
            self.rct.centerx += self.speed

        self.rct.clamp_ip(pg.Rect(0, 0, WIDTH, HEIGHT))#標準が画面外へ出ないようにする

        if self.exp_timer > 0:
            self.exp_timer -= 1
            self.img = self.exp_img
        else:
            self.img = self.normal_img #照準のまま

    def shoot(self):
        self.exp_timer = 15#0.25秒だけ爆発の画像を表示

class Food:

    foodlist = {
        "Wsosu": "fig/Wsosu.png"
    }
    
    def __init__(self,name,img,x,y):
        self.name = name
        self.img = pg.image.load(img)
        self.img = pg.transform.rotozoom(self.img, 0, 0.9)
        self.rct = self.img.get_rect()
        self.rct.center = (x, y)
        self.mask = pg.mask.from_surface(self.img)

        

def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/mori.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    aiming = Aiming()

    shot_sound = pg.mixer.Sound(SOUND_FILE) #効果音読み込み
    miss_shot_sound = pg.mixer.Sound(MISS_SOUND_FILE)

    foodlist = []
    
    for i, (name, path) in enumerate(Food.foodlist.items()):
        x = 400 + i * 150
        y = 300
        foodlist.append(Food(name, path, x, y))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                   hit_foods = []
                   for food in foodlist:
                        if aiming.rct.colliderect(food.rct): #照準と食材が重なっているか（大まか）
                            offset_x = food.rct.x - aiming.rct.x
                            offset_y = food.rct.y - aiming.rct.y #標準と食材はどれだけ離れているか
                            if aiming.mask.overlap(food.mask, (offset_x, offset_y)): #画像の色のついた部分同士が重なっているか
                                hit_foods.append(food)      
                        if  hit_foods:
                            aiming.shoot()  
                            if SE_MAXTIME is not None:
                                shot_sound.play(maxtime=SE_MAXTIME)
                            else:
                                shot_sound.play()
                        
                            for food in hit_foods:
                                foodlist.remove(food)  
                        else:
                            if MISS_SE_MAXTIME is not None:
                                miss_shot_sound.play(maxtime=MISS_SE_MAXTIME)
                            else:
                                miss_shot_sound.play()

        key_lst = pg.key.get_pressed()
        aiming.update(key_lst)
            
        screen.blit(bg_img, [0, 0])

        for food in foodlist:
            judge.check_syokuzai(food.name)
            screen.blit(food.img, food.rct)
        
        screen.blit(aiming.img,aiming.rct)
        pg.display.update()
        
        clock.tick(60)       
        
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
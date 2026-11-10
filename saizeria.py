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
    """
    食材に関するクラス
    """
    cheese = pg.image.load("fig/cheese.png")
    corn = pg.image.load("fig/corn.png")
    dore = pg.image.load("fig/dore.png")
    ebi = pg.image.load("fig/ebi.png")
    hikiniku = pg.image.load("fig/hikiniku.png")
    imo = pg.image.load("fig/imo.png")
    kiji = pg.image.load("fig/kiji.png")
    kome = pg.image.load("fig/kome.png")
    koukaton = pg.image.load("fig/koukaton.png")
    Wsosu = pg.image.load("fig/Wsosu.png")
    nori = pg.image.load("fig/nori.png")
    tamanegi = pg.image.load("fig/tamanegi.png")
    pasuta = pg.image.load("fig/pasuta.png")
    retasu = pg.image.load("fig/retasu.png")
    sosu = pg.image.load("fig/sosu.png")
    tarako = pg.image.load("fig/tarako.png")
    tomato = pg.image.load("fig/tomato.png")

    foods = {"cheese": cheese, "corn": corn, "dore": dore, "ebi": ebi, "hikiniku": hikiniku, "imo": imo, "kiji": kiji, "kome": kome, "koukaton": koukaton, "Wsosu": Wsosu, "nori": nori, "tamanegi": tamanegi, "pasuta": pasuta, "retasu": retasu, "sosu": sosu, "tarako": tarako, "tomato": tomato}
    recipes = {"辛味チキン":["koukaton"], "たらこソースパスタ":["tarako", "pasuta", "nori"], "マルゲリータ":["kiji","cheese","tomato"], "小エビのサラダ":["ebi", "retasu", "tomato", "dore"], "ハンバーグ":["hikiniku", "corn", "imo", "sosu"], "ミラノ風ドリア":["kome", "Wsosu", "tomato", "tamanegi"], "若鳥のディアボラ":["koukaton", "corn", "sosu", "imo"]}

    def __init__(self, name: str):  
        self.name = name
        self.img = Food.foods[name]
        if name == "koukaton":  #画像サイズのランダム決定（こうかとんとホワイトソースのみ画像サイズを調整）
            self.img = pg.transform.rotozoom(self.img, 0, random.uniform(0.5, 1.5))
        elif name == "Wsosu":
            self.img = pg.transform.rotozoom(self.img, 0, random.uniform(0.1, 0.2))
        else:
            self.img = pg.transform.rotozoom(self.img, 0, random.uniform(0.1, 0.35))

        self.rct = self.img.get_rect()
        self.rct.center = (random.randint(50, 1050), random.randint(50, 600))  #食材の初期位置をランダム決定
        kakudo = random.uniform(0, 2*math.pi)  #食材の動く角度をランダム決定
        self.vx = math.cos(kakudo)
        self.vy = math.sin(kakudo)
        self.speed  = random.randint(4,10)  #食材の動くスピードをランダム決定

    def update(self) -> None:
        """
        食材の移動をする
        """
        self.rct.move_ip(self.speed*self.vx, self.speed*self.vy)
        yoko, tate = check_bound(self.rct)
        if not yoko:  #壁で跳ね返る処理
            self.vx *= -1
        if not tate:
            self.vy *= -1


def recipefoodlist(foodlist_of_recipe: list) -> list:
        """
        画面に表示する食材を決定
        引数：レシピに必要な食材のリスト
        戻り値：画面に表示する食材のリスト
        """
        foodlist = []  #画面に表示される食材リスト
        allfood = list(Food.foods.keys())  #すべての食材リスト生成
        for i in foodlist_of_recipe:  #レシピに必須な食材をfoodlistに加える
            foodlist.append(Food(i))
        for n in range(20):  #ダミー食材をランダムにfoodlistに加える
            foodlist.append(Food(random.choice(allfood)))
        return foodlist


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/mori.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    aiming = Aiming()
    pg.mixer.music.load("sound/kamatamago_C00003_heaven-and-hell.mp3")  #BGM:Kamatamago (https://kamatamago.com)
    pg.mixer.music.play(-1)

    # foodlist_of_recipe = Food.recipes[recipe_hyouji.name]  #マージ後に有効化
    # foodlist = recipefoodlist(foodlist_of_recipe)

    #テスト用（マージ後削除）↓↓↓
    foodlist = []
    recipe = random.choice(list(Food.recipes.keys()))  
    allfood = list(Food.foods.keys())
    need = Food.recipes[recipe]
    for i in need:
        foodlist.append(Food(i))
    for n in range(10):
        foodlist.append(Food(random.choice(allfood)))
    #テスト用（マージ後削除）↑↑↑

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pass  #シュートするやつに書き換える

        # if judge.get_status() == "CLEAR":  #マージ後有効化
        #     foodlist = recipefoodlist(foodlist_of_recipe)
        #     recipe_hyouji.next_recipe()  #完成したら次の食材に更新
            
        screen.blit(bg_img, [0, 0])
        for food in foodlist:  #食材のblit
            food.update()
            screen.blit(food.img, food.rct)
        screen.blit(aiming.img,aiming.rct)
        # if recipe_hyouji.timeover():  #マージ後有効化
        #     foodlist = recipefoodlist(foodlist_of_recipe)  #時間が切れたら新しいレシピを表示
        pg.display.update()
        clock.tick(60)       
        
        
if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    main()
    pg.quit()
    sys.exit()
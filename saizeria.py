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
    照準クラス(仮追加後)
    """
    def __init__(self):
        self.normal_img = pg.image.load("fig/syoujyun.png")  # normal_imgに変更
        self.normal_img = pg.transform.rotozoom(self.normal_img, 0, 0.07)   # normal_imgに変更
        self.exp_img = pg.image.load("fig/explosion.gif")
        self.exp_img = pg.transform.rotozoom(self.exp_img, 0, 0.5)

        self.img = self.normal_img
        self.rct = self.normal_img.get_rect()
        self.rct.center = 550,325
        self.speed = 10
        self.exp_timer = 0

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

        self.rct.clamp_ip(pg.Rect(0, 0, WIDTH, HEIGHT))#画面外へ出ないようにする

        if self.exp_timer > 0:
            self.exp_timer -= 1
            self.img = self.exp_img
        else:
            self.img = self.normal_img#  タイマーが残っていれば爆発画像、終わっていれば通常画像を表示

    def shoot(self):
        self.exp_timer = 15#0.25秒だけ爆発の画像を表示

        # self.rct = self.img.get_rect()
        # self.rct.center = 550,325


class Food:
    """
    フードクラス(仮)
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


    def __init__(self, name, x, y):  
        self.name = name
        self.img = Food.foods[name]
        self.img = pg.transform.rotozoom(self.img, 0, 0.22)
        self.rct = self.img.get_rect()
        self.rct.center = (random.randint(50, 1050), random.randint(50, 600))

class Score:
    """
    スコアクラス(仮)
    """
    def __init__(self):
        self.fonto = pg.font.Font(None, 50)
        self.color = (255, 0, 0)
        self.value = 0
        self.img = self.fonto.render(f"Score:{self.value}", 0, self.color)
        self.rct = self.img.get_rect()
        self.rct.center = (100, HEIGHT - 50)

    def update(self, screen: pg.Surface):
        self.img = self.fonto.render(f"Score:{self.value}", 0, self.color)
        screen.blit(self.img, self.rct)

class Recipe:
    """
    レシピ管理クラス(仮)
    """
    #各レシピの難易度
    STARS = {
        "辛味チキン": 1,
        "たらこソースパスタ": 2,
        "マルゲリータ": 2,
        "小エビのサラダ": 3,
        "ハンバーグ": 3,
        "ミラノ風ドリア": 4,
        "若鳥のディアボラ": 4,
    }

    def __init__(self):
        """レシピ、タイマーの初期設定"""
        self.name = ""
        self.syokuzailist = []
        self.stars = 1
        self.time = 600  # タイマー初期値10秒
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 24)
        self.select_newrecipe()

    def select_newrecipe(self):
        """ランダムで新しいレシピを選択、タイマーをリセット"""
        self.name = random.choice(list(Food.recipes.keys()))
        self.syokuzailist = list(Food.recipes[self.name])
        self.stars = Recipe.STARS.get(self.name, 1)
        self.time = 600  # タイマーリセット

    def update(self):
        """毎フレーム、タイマーが減る"""
        self.time -= 1

    def draw(self, screen):
        """レシピと残り時間を画面に表示する"""
        bg_rect = pg.Rect(10, 5, 370, 130)
        #レシピ表示の背景の四角
        pg.draw.rect(screen, (61, 38, 18), bg_rect, border_radius=15)
        pg.draw.rect(screen, (212, 163, 89), bg_rect, width=4, border_radius=15)

        # 星の数レシピ名
        text = self.font.render(f"【{'★' * self.stars}】 {self.name}", True, (255, 255, 255))
        screen.blit(text, (20, 15))

        # 必要な食材の画像
        x, y = 22, 45
        for syokuzai in self.syokuzailist:
            img = pg.transform.rotozoom(Food.foods[syokuzai], 0, 0.12)
            screen.blit(img, (x, y))
            x += img.get_width() + 10

        # 残り時間
        timer_text = self.font.render(
            f"残り時間: {self.get_timelimit():.1f}秒", True, (255, 230, 100)
        )
        screen.blit(timer_text, (24, 95))

    def get_name(self) -> str:
        """現在のレシピ名を返す"""
        return self.name

    def get_syokuzailist(self) -> list[str]:
        """必要な食材のリストを返す"""
        return list(self.syokuzailist)

    def get_stars(self) -> int:
        """レシピの星の数を返す"""
        return self.stars

    def get_time(self) -> int:
        """現在の残りフレーム数(self.time)を返す"""
        return self.time
    
    def get_timelimit(self) -> float:
        """残り時間を秒数で返す"""
        return max(0.0, self.time / 60)

    def timeover(self) -> bool:
        """制限時間が終了したか判定"""
        return self.time <= 0

    def next_recipe(self):
        """次のレシピに切り替える処理"""
        self.select_newrecipe()

class Judgment:
    """
    正誤判定を行うクラス(川辺)
    """
    def __init__(self, recipe):
        self.motteru_syokuzai = []  # 取得した食材のリスト
        self.status = "PLAYING"  # "PLAYING", "CLEAR", "BURNT"
        self.recipe = recipe

    def get_motteru_syokuzai(self):
        """
        取得した食材のリストの取得
        """
        return self.motteru_syokuzai

    def get_status(self):
        """
        現在のゲームのステータスを取得
        """
        return self.status

    def get_recipe(self):
        """
        現在のレシピ取得
        """
        return self.recipe

    def set_recipe(self, recipe):
        """
        次のレシピへ更新
        """
        self.recipe = recipe
        self.motteru_syokuzai.clear()
        self.status = "PLAYING"

    def check_syokuzai(self, syokuzai_name):
        """
        撃ち落とした食材の正誤を判定
        """
        if self.status != "PLAYING":
            return

        nerau_syokuzai = self.recipe.get_syokuzailist()  # 狙う食材を定義(川辺)

        # 黒焦げを残すならコメントアウトしない
        # if syokuzai_name not in nerau_syokuzai:
        #     self.status = "BURNT"
        #     return

        self.motteru_syokuzai.append(syokuzai_name)  # ゲットした食材を追加

        if self.is_recipe_completed(nerau_syokuzai):
            self.status = "CLEAR"

    def is_recipe_completed(self, nerau_syokuzai):
        """
        レシピの必要食材がすべて集まったか判定
        """
        for item in set(nerau_syokuzai):
            if self.motteru_syokuzai.count(item) < nerau_syokuzai.count(item):
                return False
        return True   


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/mori.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    aiming = Aiming()
    recipe_hyouji = Recipe()
    score = Score()
    judge = Judgment(recipe_hyouji) #(川辺)
    time_limit = 30  
    start= pg.time.get_ticks()  
    font = pg.font.Font(None, 50)

    foodlist = []
    recipe = random.choice(list(Food.recipes.keys()))
    allfood = list(Food.foods.keys())
    need = Food.recipes[recipe]
    for i in need:
        foodlist.append(Food(i, random.randint(50, 1050), random.randint(50, 600)))
    for n in range(15):
         foodlist.append(Food(random.choice(allfood), random.randint(50, 1050), random.randint(50, 600)))

    while True:
        nokori = (pg.time.get_ticks() - start) / 1000
        timeup = max(0.0, time_limit - nokori)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    hit_foods = [food for food in foodlist if aiming.rct.colliderect(food.rct)]
                    if  hit_foods:
                        aiming.shoot()  
                        for food in hit_foods:
                            judge.check_syokuzai(food.name)
                            foodlist.remove(food)  
                    pass  #　シュートするやつに書き換える

        # レシピの判定（CLEARならスコア加算） (川辺↓)
        if judge.get_status() == "CLEAR":
            # 難易度(星の数) × 100点 を加算
            score.value += recipe_hyouji.get_stars() * 100 
            recipe_hyouji.next_recipe()      # 次のレシピへ
            judge.set_recipe(recipe_hyouji)  # 判定も次のレシピへ更新


        key_lst = pg.key.get_pressed()
        aiming.update(key_lst)
            
        
        screen.blit(bg_img, [0, 0])
        for food in foodlist: 
                        screen.blit(food.img, food.rct)
        screen.blit(aiming.img,aiming.rct)
        score.update(screen)  # スコアを画面に表示
        time_mo = font.render(f"Time: {timeup:.1f}", True, (255, 255, 0))  # 残り時間の文字
        time_rct = time_mo.get_rect()
        time_rct.center = (WIDTH - 150, HEIGHT - 50)
        screen.blit(time_mo, time_rct)  # 残り時間を画面に表示
        recipe_hyouji.update()
        if recipe_hyouji.timeover():
            recipe_hyouji.next_recipe()
        recipe_hyouji.draw(screen)

        pg.display.update()
        
        clock.tick(60)       

       
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
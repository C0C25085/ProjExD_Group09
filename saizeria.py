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
        self.mask = pg.mask.from_surface(self.img)

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

        


class Recipe:
    """
    レシピ管理クラス(廣嶋)
    """
    # 各レシピの難易度
    STARS = {
        "辛味チキン": 1,
        "たらこソースパスタ": 2,
        "マルゲリータ": 2,
        "小エビのサラダ": 3,
        "ハンバーグ": 3,
        "ミラノ風ドリア": 4,
        "若鳥のディアボラ": 4,
    }

    def __init__(self)-> None:
        """
        レシピとタイマーの初期設定を行う関数
        引数 なし
        戻り値：なし
        """
        self.name = ""
        self.syokuzailist = []
        self.stars = 1
        self.time = 600  # タイマー初期値10秒 (600フレーム)
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 24)
        self.select_newrecipe()

    def select_newrecipe(self)-> None:
        """
        レシピを選択し、タイマーをリセットする関数
        引数：なし
        戻り値：なし
        """
        self.name = random.choice(list(Food.recipes.keys()))    
        self.syokuzailist = list(Food.recipes[self.name])
        self.stars = Recipe.STARS.get(self.name, 1)
        self.time = 600  # タイマーリセット

    def update(self)-> None:
        """
        毎フレームタイマーを1減算する関数
        引数：なし
        戻り値：なし
        """
        self.time -= 1

    def draw(self, screen: pg.Surface)-> None:
        """
        レシピ名、必要な食材画像、残り時間を画面上に描画する関数
        引数 screen
        戻り値：なし
        """
        bg_rect = pg.Rect(10, 5, 370, 130)
        # レシピ表示背景の四角枠描画
        pg.draw.rect(screen, (61, 38, 18), bg_rect, border_radius=15)
        pg.draw.rect(screen, (212, 163, 89), bg_rect, width=4, border_radius=15)

        # 星の数とレシピ名
        text = self.font.render(f"【{'★' * self.stars}】 {self.name}", True, (255, 255, 255))
        screen.blit(text, (20, 15))

        # 必要な食材のミニ画像
        x, y = 22, 45
        for syokuzai in self.syokuzailist:
            img = pg.transform.rotozoom(Food.foods[syokuzai], 0, 0.12)
            screen.blit(img, (x, y))
            x += img.get_width() + 10

        # 残り秒数表示
        timer_text = self.font.render(
            f"残り時間: {self.get_timelimit():.1f}秒", True, (255, 230, 100)
        )
        screen.blit(timer_text, (24, 95))

    def get_name(self) -> str:
        """
        現在のレシピ名を返すゲッター関数
        引数：なし
        戻り値：現在のレシピ名
        """
        return self.name

    def get_syokuzailist(self) -> list[str]:
        """
        必要な食材リストを返すゲッター関数
        引数：なし
        戻り値：必要な食材名のリスト
        """
        return list(self.syokuzailist)

    def get_stars(self) -> int:
        """
        レシピの星の数を返すゲッター関数
        引数：なし
        戻り値：難易度の星の数
        """
        return self.stars

    def get_time(self) -> int:
        """
        現在の残りフレーム数を返すゲッター関数
        引数：なし
        戻り値：残りフレーム数
        """
        return self.time

    def get_timelimit(self) -> float:
        """
        残り時間を秒数に換算して返すゲッター関数
        引数：なし
        戻り値：残り秒数
        """
        return max(0.0, self.time / 60)

    def timeover(self) -> bool:
        """
        制限時間（タイマー）が終了したか判定する関数
        引数：なし
        戻り値：制限時間終了判定結果（終了：True／継続：False）
        """
        return self.time <= 0

    def next_recipe(self)-> None:
        """
        次の新しいレシピに切り替える関数
        引数：なし
        戻り値：なし
        """
        self.select_newrecipe()



class Recipe:
    """
    レシピ管理クラス(廣嶋)
    """
    # 各レシピの難易度
    STARS = {
        "辛味チキン": 1,
        "たらこソースパスタ": 2,
        "マルゲリータ": 2,
        "小エビのサラダ": 3,
        "ハンバーグ": 3,
        "ミラノ風ドリア": 4,
        "若鳥のディアボラ": 4,
    }

    def __init__(self)-> None:
        """
        レシピとタイマーの初期設定を行う関数
        引数 なし
        戻り値：なし
        """
        self.name = ""
        self.syokuzailist = []
        self.stars = 1
        self.time = 600  # タイマー初期値10秒 (600フレーム)
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 24)
        self.select_newrecipe()

    def select_newrecipe(self)-> None:
        """
        レシピを選択し、タイマーをリセットする関数
        引数：なし
        戻り値：なし
        """
        self.name = random.choice(list(Food.recipes.keys()))    
        self.syokuzailist = list(Food.recipes[self.name])
        self.stars = Recipe.STARS.get(self.name, 1)
        self.time = 600  # タイマーリセット

    def update(self)-> None:
        """
        毎フレームタイマーを1減算する関数
        引数：なし
        戻り値：なし
        """
        self.time -= 1

    def draw(self, screen: pg.Surface)-> None:
        """
        レシピ名、必要な食材画像、残り時間を画面上に描画する関数
        引数 screen
        戻り値：なし
        """
        bg_rect = pg.Rect(10, 5, 370, 130)
        # レシピ表示背景の四角枠描画
        pg.draw.rect(screen, (61, 38, 18), bg_rect, border_radius=15)
        pg.draw.rect(screen, (212, 163, 89), bg_rect, width=4, border_radius=15)

        # 星の数とレシピ名
        text = self.font.render(f"【{'★' * self.stars}】 {self.name}", True, (255, 255, 255))
        screen.blit(text, (20, 15))

        # 必要な食材のミニ画像
        x, y = 22, 45
        for syokuzai in self.syokuzailist:
            img = pg.transform.rotozoom(Food.foods[syokuzai], 0, 0.12)
            screen.blit(img, (x, y))
            x += img.get_width() + 10

        # 残り秒数表示
        timer_text = self.font.render(
            f"残り時間: {self.get_timelimit():.1f}秒", True, (255, 230, 100)
        )
        screen.blit(timer_text, (24, 95))

    def get_name(self) -> str:
        """
        現在のレシピ名を返すゲッター関数
        引数：なし
        戻り値：現在のレシピ名
        """
        return self.name

    def get_syokuzailist(self) -> list[str]:
        """
        必要な食材リストを返すゲッター関数
        引数：なし
        戻り値：必要な食材名のリスト
        """
        return list(self.syokuzailist)

    def get_stars(self) -> int:
        """
        レシピの星の数を返すゲッター関数
        引数：なし
        戻り値：難易度の星の数
        """
        return self.stars

    def get_time(self) -> int:
        """
        現在の残りフレーム数を返すゲッター関数
        引数：なし
        戻り値：残りフレーム数
        """
        return self.time

    def get_timelimit(self) -> float:
        """
        残り時間を秒数に換算して返すゲッター関数
        引数：なし
        戻り値：残り秒数
        """
        return max(0.0, self.time / 60)

    def timeover(self) -> bool:
        """
        制限時間（タイマー）が終了したか判定する関数
        引数：なし
        戻り値：制限時間終了判定結果（終了：True／継続：False）
        """
        return self.time <= 0

    def next_recipe(self)-> None:
        """
        次の新しいレシピに切り替える関数
        引数：なし
        戻り値：なし
        """
        self.select_newrecipe()


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/mori.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    clock = pg.time.Clock()
    aiming = Aiming()

    shot_sound = pg.mixer.Sound(SOUND_FILE) #効果音読み込み
    miss_shot_sound = pg.mixer.Sound(MISS_SOUND_FILE)

    foodlist_of_recipe = recipe_hyouji.syokuzailist
    Food.foodlist_of_recipe(foodlist_of_recipe)
    
    recipe_hyouji = Recipe()

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

        # if judge.get_status() == "CLEAR":  #マージ後有効化
        #     foodlist = recipefoodlist(foodlist_of_recipe)
        #     recipe_hyouji.next_recipe()  #完成したら次の食材に更新
            
        screen.blit(bg_img, [0, 0])

        for food in foodlist:
            food.update()
            # judge.check_syokuzai(food.name)
            screen.blit(food.img, food.rct)
        
        screen.blit(aiming.img,aiming.rct)
        # if recipe_hyouji.timeover():  #マージ後有効化
        #     foodlist = recipefoodlist(foodlist_of_recipe)  #時間が切れたら新しいレシピを表示

        # タイマー更新
        recipe_hyouji.update()

        #タイムオーバーのとき
        if recipe_hyouji.timeover():
            foodlist = recipefoodlist(foodlist_of_recipe)  #時間が切れたら新しいレシピを表示
            recipe_hyouji.next_recipe()

        # レシピ表示の描画
        recipe_hyouji.draw(screen)
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    main()
    pg.quit()
    sys.exit()
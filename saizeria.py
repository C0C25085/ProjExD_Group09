import math
import os
import random
import sys
import time
import pygame as pg

WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ

# 画面の状態
START = "START"
PLAYING = "PLAYING"
CLEAR = "CLEAR"
GAMEOVER = "GAMEOVER"
SCORE = "SCORE"

# 画面の色
DARK_GREEN = (48, 91, 57)
GREEN = (105, 153, 103)
LIGHT_GREEN = (220, 241, 213)
CREAM = (255, 225, 157)
WHITE = (255, 255, 240)
BROWN = (115, 91, 61)

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
    照準クラス(仮追加後)
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

    def get_name(self) -> str:
        return self.name
        
    def get_img(self) -> pg.Surface:
        return self.img
        
    def get_rct(self) -> pg.Rect:
        return self.rct

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

    
def draw_text(screen: pg.Surface, text: str, size: int, x: int, y: int) -> None:
    """
    文字を画面の中央に表示する。
    """
    font = pg.font.SysFont(["meiryo", "yu gothic", "hiraginosans"], size)
    img = font.render(text, True, GREEN)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)


def draw_button(screen: pg.Surface, text: str, x: int, y: int, w: int, h: int) -> pg.Rect:
    """
    黄色のボタンを表示する。
    """
    rect = pg.Rect(x, y, w, h)

    pg.draw.rect(screen, CREAM, rect)
    pg.draw.rect(screen, DARK_GREEN, rect, 3)

    draw_text(screen, text, 35, x + w // 2, y + h // 2)

    return rect


def draw_start(screen: pg.Surface, bg_img: pg.Surface) -> pg.Rect:
    """スタート画面を表示する。"""
    screen.blit(bg_img, (0, 0))

    draw_text(screen, "サイゼリア", 60, 550, 220)

    return draw_button(screen, "スタート", 400, 370, 300, 85)


def draw_game(screen: pg.Surface, bg_img: pg.Surface, aiming: Aiming) -> None:
    """ゲーム画面を表示する。"""
    screen.blit(bg_img, (0, 0))
    screen.blit(aiming.get_img(), aiming.get_rct())
    


def draw_clear(screen: pg.Surface, bg_img: pg.Surface) -> pg.Rect:
    """クリア画面を表示する。"""
    screen.blit(bg_img, (0, 0))

    draw_text(screen, "クリア！", 60, 550, 200)
    draw_text(screen, "料理が完成しました！", 32, 550, 280)

    return draw_button(screen, "次へ", 425, 370, 250, 80)


def draw_gameover(screen: pg.Surface, bg_img: pg.Surface) -> pg.Rect:
    """ゲームオーバー画面を表示する。"""
    screen.blit(bg_img, (0, 0))
    draw_text(screen, "ゲームオーバー", 60, 550, 220)
    draw_text(screen, "また挑戦してみよう！", 32, 550, 300)

    return draw_button(screen, "リトライ", 400, 380, 300, 80)


def draw_score(screen: pg.Surface, bg_img: pg.Surface, score: int, food_count: int) -> pg.Rect:
    """最終スコア画面を表示する（完成料理の表示を削除）。"""
    screen.blit(bg_img, (0, 0))

    draw_text(screen, "最終スコア", 60, 550, 160)

    # 2項目（スコア・集めた食材）に合わせて白枠とY座標を整列
    pg.draw.rect(screen, WHITE, (300, 230, 500, 180))
    pg.draw.rect(screen, GREEN, (300, 230, 500, 180), 3)

    draw_text(screen, f"スコア：{score}", 35, 550, 285)
    draw_text(screen, f"集めた食材：{food_count}個", 35, 550, 355)

    return draw_button(screen, "タイトルに戻る", 375, 470, 350, 80)
    
    
def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("サイゼリア - 食材シューティング")
    bg_img = pg.image.load("fig/mori.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    aiming = Aiming()

    pg.mixer.music.load("sound/kamatamago_C00003_heaven-and-hell.mp3")
    pg.mixer.music.play(-1)
    recipe_hyouji = Recipe()
    shot_sound = pg.mixer.Sound(SOUND_FILE) #効果音読み込み
    miss_shot_sound = pg.mixer.Sound(MISS_SOUND_FILE)

    foodlist_of_recipe = Food.recipes[recipe_hyouji.name]
    foodlist = recipefoodlist(foodlist_of_recipe)

    # 最初はスタート画面
    game_state = START

    # 最終スコア
    score = 0
    food_count = 0

    button = None
    recipe_hyouji = Recipe()
    #score = Score()
    judge = Judgment(recipe_hyouji) #(川辺)
    time_limit = 30  
    start= pg.time.get_ticks()  
    font = pg.font.Font(None, 50)

    while True:
        # イベント処理
        nokori = (pg.time.get_ticks() - start) / 1000
        timeup = max(0.0, time_limit - nokori)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            # ボタンをクリックしたとき
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
                            judge.check_syokuzai(food.name)
                            foodlist.remove(food)  
                            
                    else:
                        if MISS_SE_MAXTIME is not None:
                            miss_shot_sound.play(maxtime=MISS_SE_MAXTIME)
                        else:
                            miss_shot_sound.play()
                # レシピの判定（CLEARならスコア加算） (川辺↓)
            if judge.get_status() == "CLEAR":
                # 難易度(星の数) × 100点 を加算
                score.value += recipe_hyouji.get_stars() * 100 
                recipe_hyouji.next_recipe()      # 次のレシピへ
                judge.set_recipe(recipe_hyouji)  # 判定も次のレシピへ更新

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if button is not None and button.collidepoint(event.pos):
                    if game_state == START:
                        game_state = PLAYING
                        score = 0
                        food_count = 0

                    elif game_state == CLEAR:
                        game_state = SCORE

                    elif game_state == GAMEOVER:
                        game_state = PLAYING
                        score = 0
                        food_count = 0

                    elif game_state == SCORE:
                        game_state = START

        button = None
        if game_state == START:
            button = draw_start(screen, bg_img)

        elif game_state == PLAYING:
            draw_game(screen, bg_img, aiming)
            for food in foodlist:
                food.update()
                # judge.check_syokuzai(food.name)
                screen.blit(food.img, food.rct)
            
            screen.blit(aiming.img,aiming.rct)
        
            # タイマー更新
            recipe_hyouji.update()
    
            #タイムオーバーのとき
            if recipe_hyouji.timeover():
                foodlist = recipefoodlist(foodlist_of_recipe)  #時間が切れたら新しいレシピを表示
                recipe_hyouji.next_recipe()
    
            # レシピ表示の描画
            recipe_hyouji.draw(screen)

            # if judge.get_status() == "CLEAR":  #マージ後有効化
            #     foodlist = recipefoodlist(foodlist_of_recipe)
            #     recipe_hyouji.next_recipe()  #完成したら次の食材に更新

        elif game_state == CLEAR:
            button = draw_clear(screen, bg_img)

        elif game_state == GAMEOVER:
            button = draw_gameover(screen, bg_img)

        elif game_state == SCORE:
            button = draw_score(screen, bg_img, score, food_count)


        key_lst = pg.key.get_pressed()
        aiming.update(key_lst)

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    main()
    pg.quit()
    sys.exit()
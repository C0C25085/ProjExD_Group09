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
        self.rct.center = 550, 325


class Food:
    """
    食材クラス
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

    foods = {
        "cheese": cheese, "corn": corn, "dore": dore, "ebi": ebi, 
        "hikiniku": hikiniku, "imo": imo, "kiji": kiji, "kome": kome, 
        "koukaton": koukaton, "Wsosu": Wsosu, "nori": nori, "tamanegi": tamanegi, 
        "pasuta": pasuta, "retasu": retasu, "sosu": sosu, "tarako": tarako, "tomato": tomato
    }
    recipes = {
        "辛味チキン": ["koukaton"], 
        "たらこソースパスタ": ["tarako", "pasuta", "nori"], 
        "マルゲリータ": ["kiji", "cheese", "tomato"], 
        "小エビのサラダ": ["ebi", "retasu", "tomato", "dore"], 
        "ハンバーグ": ["hikiniku", "corn", "imo", "sosu"], 
        "ミラノ風ドリア": ["kome", "Wsosu", "tomato", "tamanegi"], 
        "若鳥のディアボラ": ["koukaton", "corn", "sosu", "imo"]
    }

    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.img = Food.foods[name]
        self.img = pg.transform.rotozoom(self.img, 0, 0.22)
        self.rct = self.img.get_rect()
        self.rct.center = (x, y)


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
    recipe_hyouji = Recipe()


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pass #シュートするやつに書き換える
                
        screen.blit(bg_img, [0, 0])
        screen.blit(aiming.img,aiming.rct)

        # タイマー更新
        recipe_hyouji.update()

        #タイムオーバーのとき
        if recipe_hyouji.timeover():
            recipe_hyouji.next_recipe()

        # レシピ表示の描画
        recipe_hyouji.draw(screen)
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
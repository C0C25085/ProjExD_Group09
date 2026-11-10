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
    """照準クラス"""

    def __init__(self) -> None:
        self.img = pg.image.load("fig/syoujyun.png")
        self.img = pg.transform.rotozoom(self.img, 0, 0.07)
        self.rct = self.img.get_rect()
        self.rct.center = 550, 325

    def get_img(self) -> pg.Surface:
        return self.img

    def get_rct(self) -> pg.Rect:
        return self.rct


class Food:
    """食材クラス"""

    def __init__(self, name: str, img: str, x: int, y: int) -> None:
        self.name = name
        self.img = pg.image.load(img)
        self.img = pg.transform.rotozoom(self.img, 0, 0.2)
        self.rct = self.img.get_rect()
        self.rct.center = (x, y)

    def get_name(self) -> str:
        return self.name

    def get_img(self) -> pg.Surface:
        return self.img

    def get_rct(self) -> pg.Rect:
        return self.rct


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

    # 最初はスタート画面
    game_state = START

    # 最終スコア
    score = 0
    food_count = 0

    button = None

    while True:
        # イベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            # ボタンをクリックしたとき
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

            if event.type == pg.KEYDOWN:
                if game_state == PLAYING:
                    if event.key == pg.K_SPACE:
                        pass
                    elif event.key == pg.K_c:
                        score += 1200
                        food_count += 4
                        game_state = CLEAR
                    elif event.key == pg.K_g:
                        game_state = GAMEOVER

        button = None
        if game_state == START:
            button = draw_start(screen, bg_img)

        elif game_state == PLAYING:
            draw_game(screen, bg_img, aiming)

        elif game_state == CLEAR:
            button = draw_clear(screen, bg_img)

        elif game_state == GAMEOVER:
            button = draw_gameover(screen, bg_img)

        elif game_state == SCORE:
            button = draw_score(screen, bg_img, score, food_count)

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
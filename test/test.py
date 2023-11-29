#色々テストするところ
"""
import sys
from pathlib import Path

# 現在のスクリプトのパスを取得し、ひとつ上のフォルダのパスをsys.pathに追加
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# ひとつ上のフォルダにあるモジュールをインポート
import generate_maze
"""

import pygame
import sys

# Pygameの初期化
pygame.init()

# ウィンドウの設定
size = width, height =1024,1024
screen = pygame.display.set_mode(size)
pygame.display.set_caption("画像とメッセージウィンドウの例")

# 色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# フォントの設定
font = pygame.font.SysFont('meiryo', 36)

# メッセージウィンドウの設定
message_window_rect = pygame.Rect(100, 150, 440, 150)
message_window_visible = False

# 画像の読み込み
image_path = 'D:\\Download\\DALL·E 2023-11-22 21.32.09 - A seamless, repeatable tile pattern featuring an ancient, forgotten stone wall of a ruin, covered in overgrown vines and moss. The wall is detailed wi.PNG'  # 画像のパスを指定
image = pygame.image.load(image_path)
image_rect = image.get_rect(center=(width // 2, height // 2))

def draw_message_window(screen,message,command):
    """メッセージウィンドウを描画する"""
    message_lines = message.split('\n')
    font = pygame.font.SysFont('meiryo', 24)
    # テキストサイズの計算
    max_width = 0
    total_height = 0
    for line in message_lines:
        line_width, line_height = font.size(line)
        max_width = max(max_width, line_width)
        total_height += line_height

    # メッセージウィンドウのサイズと位置を決定
    padding = 20
    window_width = max_width + padding * 2
    window_height = total_height + padding * 2
    window_x = (screen.get_width() - window_width) // 2
    window_y = (screen.get_height() - window_height) // 2
    message_window_rect = pygame.Rect(window_x, window_y, window_width, window_height)
    window_height = 0  # 初期幅は0
    animation_speed = 20  # アニメーションの回数
    # 元の画面をバッファに保存
    buffer = screen.copy()
    # メッセージウィンドウを表示するアニメーション
    while window_height < total_height + padding * 2:
        window_height += ((total_height + padding * 2)//animation_speed)
        window_y = (height - window_height) // 2
        message_window_rect = pygame.Rect(window_x, window_y, window_width, window_height)

        # メッセージウィンドウの背景を描画
        pygame.draw.rect(screen, BLACK, message_window_rect)
        pygame.draw.rect(screen, WHITE, message_window_rect,width = 3)

        pygame.display.flip()
        pygame.time.wait(12)
    #message_window_rect = pygame.Rect(window_x, window_y, window_width, total_height + padding * 2)
    # メッセージウィンドウの背景を描画
    pygame.draw.rect(screen, BLACK, message_window_rect)
    pygame.draw.rect(screen, WHITE, message_window_rect,width = 5)
    # メッセージを描画
    y_offset = window_y + padding
    for line in message_lines:
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (window_x + padding, y_offset))
        y_offset += font.size(line)[1]
    pygame.display.flip()
    # コマンドの選択（ここではキーボード入力で模擬）
    command_selected = False
    while not command_selected:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                command_selected = True
    # メッセージウィンドウを閉じるアニメーション
    animation_speed = 10  # アニメーションの回数
    while window_height > 0:
        window_height -= ((total_height + padding * 2)//animation_speed)
        window_y = (height - window_height) // 2
        message_window_rect = pygame.Rect(window_x, window_y, window_width, window_height)

        screen.blit(buffer, (0, 0))  # バッファから画面を復元
        pygame.draw.rect(screen, BLACK, message_window_rect)
        pygame.draw.rect(screen, WHITE, message_window_rect,width = 5)

        pygame.display.flip()
        pygame.time.wait(12)

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                message_window_visible = not message_window_visible

    #screen.fill(BLACK)
    screen.blit(image, image_rect)

    if message_window_visible:
        mes = """
かつて、この世界は魔法と剣が支配する時代であった。
広大な大陸には、数々の王国と帝国が栄え、英雄たちの伝説が語り継がれていた。
しかし、平和は長くは続かなかった。暗黒の時代が訪れ、世界は混沌に包まれた。
<改頁>
その原因は、遥か古の地下深くに眠るとされる「影の迷宮」にあった。
伝説によると、この迷宮は古代の魔法使いによって作られ、彼の死後、封印されたという。
しかし、何者かによって封印が解かれ、迷宮から逃れた邪悪な力が世界を覆い始めたのだ。
<改頁>
あなたは、この危機を救うために選ばれた勇者の一人である。
王国の最後の希望として、あなたには「影の迷宮」を探索し、
世界を脅かす邪悪な力の源を断つ使命が与えられた。
<改頁>
冒険の始まりは、王国の古い城の地下にある秘密の入り口からだ。
あなたは、選ばれし仲間たちと共に、暗く、謎に満ちた迷宮の入り口に立っている。
迷宮は無限に広がり、数え切れない罠とモンスター、
そして失われた宝物があなたを待ち受けている。
<改頁>
「影の迷宮」は、ただの迷宮ではない。それは生きており、侵入者を試すかのように
常に変化し続ける。壁が動き、通路が変わり、部屋が消える。
迷宮の中では、時間も空間も意味をなさない。
<改頁>
しかし、あなたには勇気がある。剣と魔法、そして仲間との絆がある。
この冒険が、あなたを真の英雄へと導く道となるだろう。
<改頁>
「さあ、行こう。運命は我々の手の中にある。」
あなたは仲間たちに呼びかけ、一歩を踏み出す。
影の迷宮の深淵へと、その旅は始まった。
<一時停止>
"""
        command = ["ok","no","cancel"]
        draw_message_window(screen,mes,command)
        message_window_visible = False

    pygame.display.flip()
    pygame.time.wait(10)
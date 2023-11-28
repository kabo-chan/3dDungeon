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
image_path = 'D:\\Download\\DALL·E 2023-11-28 00.58.42 - An animated skeleton wearing tattered leather armor and wielding a rusty sword, depicted in a pixel art style. The image should feature a black backgr.PNG'  # 画像のパスを指定
image = pygame.image.load(image_path)
image_rect = image.get_rect(center=(width // 2, height // 2))

def draw_message_window():
    """メッセージウィンドウを描画する"""
    pygame.draw.rect(screen, GRAY, message_window_rect)
    text = font.render("メッセージウィンドウです", True, WHITE)
    screen.blit(text, (message_window_rect.x + 20, message_window_rect.y + 20))

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                message_window_visible = not message_window_visible

    screen.fill(BLACK)
    screen.blit(image, image_rect)

    if message_window_visible:
        draw_message_window()

    pygame.display.flip()
    pygame.time.wait(10)
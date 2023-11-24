import pygame
import random
### 自作モジュール
import generate_maze    #generate_maze, remove_wall, add_random_rooms
import draw_3d

def draw_text(game_settings ):
    screen = game_settings['screen']
    player_x = game_settings['player_x']
    player_y = game_settings['player_y']
    player_dir = game_settings['player_dir']
    num_walls = game_settings['num_walls']
    # 方向を文字列に変換
    directions = ["North", "East", "South", "West"]
    direction_text = directions[player_dir]

    # テキストをレンダリング
    font = pygame.font.SysFont('meiryo', 24)  # 日本語フォントと大きさ
    position_text = f"Position: ({player_x}, {player_y}), Direction: {direction_text}, LightLength: {num_walls}"
    text_surface = font.render(position_text, True, (255, 255, 255))

    # テキストを画面に描画
    screen.blit(text_surface, (10, screen.get_height()-50))
def draw_maze_around_player(game_settings ):
    screen = game_settings['screen']
    maze = game_settings['maze']
    player_x = game_settings['player_x']
    player_y = game_settings['player_y']
    cell_size = game_settings['cell_size']
    num_walls = game_settings['num_walls']
    N = game_settings['N']
    # 画面の中央座標を計算
    screen_center_x = screen.get_width() // 2 - cell_size // 2
    screen_center_y = screen.get_height() // 2 - cell_size // 2

    # プレイヤーを中心に周囲の迷路を描画する
    view = int(num_walls/2)
    for i in range(-view, view+1):
        for j in range(-view, view+1):
            x = player_x + j
            y = player_y + i

            # 描画座標を計算
            draw_x = screen_center_x + j * cell_size
            draw_y = screen_center_y + i * cell_size

            if 0 <= x < N and 0 <= y < N:
                cell = maze[y][x]
                # プレイヤー以外のセルの壁を描画
                if cell & 1:
                    pygame.draw.line(screen, (0, 160, 0), (draw_x, draw_y), (draw_x + cell_size, draw_y), 1)
                if cell & 2:
                    pygame.draw.line(screen, (0, 160, 0), (draw_x + cell_size, draw_y), (draw_x + cell_size, draw_y + cell_size), 1)
                if cell & 4:
                    pygame.draw.line(screen, (0, 160, 0), (draw_x, draw_y + cell_size), (draw_x + cell_size, draw_y + cell_size), 1)
                if cell & 8:
                    pygame.draw.line(screen, (0, 160, 0), (draw_x, draw_y), (draw_x, draw_y + cell_size), 1)
def draw_player_direction(game_settings ):
    screen = game_settings['screen']
    player_dir = game_settings['player_dir']
    # プレイヤーの向きを表示
    arrow_text = ""
    if player_dir == 0:
        arrow_text = "▲"
    elif player_dir == 1:
        arrow_text = "▶"
    elif player_dir == 2:
        arrow_text = "▼"
    elif player_dir == 3:
        arrow_text = "◀"
    fontsize = 12
    font = pygame.font.SysFont('meiryo', fontsize)  # 日本語フォントと大きさ
    text_surface = font.render(arrow_text, True, (255, 0, 0))  # 赤色の矢印
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2 + 1, screen.get_height() // 2+1))
    screen.blit(text_surface, text_rect)
def handle_keys(game_settings):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        game_settings['wire'] = not game_settings['wire']
        game_settings['moved'] = True
    if keys[pygame.K_q]:
        game_settings['num_walls'] = (game_settings['num_walls'] % 8) + 1
        game_settings['moved'] = True
    direction_mapping = {
        pygame.K_a: -1,  # 左に90度回転
        pygame.K_d: 1,   # 右に90度回転
        pygame.K_w: {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)},  # 前に進む
        pygame.K_s: 2,   # 180度回転
    }

    for key, action in direction_mapping.items():
        if keys[key]:
            if isinstance(action, int):
                game_settings['player_dir'] = (game_settings['player_dir'] + action) % 4
            elif isinstance(action, dict):
                dx, dy = action[game_settings['player_dir']]
                front_wall, _, _ = draw_3d.is_wall_present( game_settings['player_x'], game_settings['player_y'], game_settings)
                if True:  # not front_wall: # デバッグとして壁を通り抜けられる
                    game_settings['player_x'] = (game_settings['player_x'] + dx) % game_settings['N']
                    game_settings['player_y'] = (game_settings['player_y'] + dy) % game_settings['N']
            game_settings['moved'] = True

##### 変数などの初期設定
game_settings = {
    'N': 20,
    'maze': [[15 for _ in range(20)] for _ in range(20)],
    'cell_size': 20,
    'wire': True,
    'player_x': 0,
    'player_y': 0,
    'player_dir': 0,
    'wall_size': (800, 0.618),
    'screen': pygame.display.set_mode((640, 480)),
    'wall_color': (160, 160, 160),
    'bg_color': (0, 0, 0),
    'num_walls': 5,
    'moved':True
}

##### 初期設定
# フォントの初期化
pygame.font.init()
#font = pygame.font.SysFont('meiryo', 24)  # 日本語フォントと大きさ
# 迷路の生成
random.seed()  # 乱数のシード値を設定
generate_maze.generate_maze(0, 0,game_settings)  # 迷路生成を開始
# ランダムな部屋の追加
generate_maze.add_random_rooms(2, 5, 5,game_settings)  # 2x2から5x5のサイズの部屋を2から5個追加

# Pygameの初期化
pygame.init()

##### ゲームのメインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    handle_keys(game_settings)  # キー操作の処理
    if game_settings['moved']:
        draw_3d.draw_player_view(game_settings)  # プレイヤーの視点からの壁の描画
        draw_text(game_settings)  # テキストの描画
        draw_maze_around_player(game_settings)  # プレイヤーの周囲の迷路を描画
        draw_player_direction(game_settings)  # プレイヤーの向きを表示
        
        pygame.display.flip()  # 画面の更新
        pygame.time.delay(200)  # スリープを挿入

    game_settings['moved'] = False  # 移動フラグをリセット
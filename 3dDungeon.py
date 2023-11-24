import pygame
import random
### 自作モジュール
import generate_maze    #generate_maze, remove_wall, add_random_rooms
import draw_3d
import utl

def handle_keys(game_settings): #キー操作
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        game_settings['wire'] = not game_settings['wire']
        game_settings['moved'] = True
    if keys[pygame.K_q]:
        game_settings['num_walls'] = (game_settings['num_walls'] % 8) + 1
        game_settings['moved'] = True
    if keys[pygame.K_e]:
        game_settings['draw_minimap'] = not game_settings['draw_minimap'] 
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
    'wall_size': (800, 500),
    'screen': pygame.display.set_mode((640, 480)),
    'wall_color': (160, 160, 160),
    'bg_color': (0, 0, 0),
    'door_color':(152,81,75),
    'num_walls': 5,
    'moved':True,
    'draw_minimap':True
}

##### 初期設定
# 迷路の生成
random.seed()  # 乱数のシード値を設定
generate_maze.generate_maze(0, 0,game_settings)  # 迷路生成を開始
# ランダムな部屋の追加
generate_maze.add_random_rooms(2, 5, 5,game_settings)  # 2x2から5x5のサイズの部屋を2から5個追加
generate_maze.add_doors(30, game_settings)  # 10個前後のドアを迷路に追加

# Pygameの初期化
pygame.init()
# フォントの初期化
pygame.font.init()

##### ゲームのメインループ
while True:
    for event in pygame.event.get():    #ウィンドウを閉じたら終了
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    handle_keys(game_settings)  # キー操作の処理

    if game_settings['moved']:  #画面描画フラグ
        draw_3d.draw_player_view(game_settings)  # プレイヤーの視点からの壁の描画
        utl.draw_text(game_settings)  # 情報の表示
        if game_settings['draw_minimap']:
            utl.draw_maze_around_player(game_settings)  # プレイヤーの周囲の迷路を描画
            utl.draw_player_direction(game_settings)  # プレイヤーの向きを表示
        
        pygame.display.flip()  # 画面の更新
        pygame.time.delay(200)  # スリープを挿入

    game_settings['moved'] = False  # 移動フラグをリセット
    pygame.time.delay(10)  # スリープを挿入
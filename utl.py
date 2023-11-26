import pygame

def draw_text(game_settings ):  #画面したに情報表示
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
def draw_maze_around_player(game_settings, full=False):
    screen = game_settings['screen']
    maze = game_settings['maze']
    cell_size = game_settings['cell_size']
    num_walls = game_settings['num_walls']
    N = game_settings['N']
    player_x = game_settings['player_x']
    player_y = game_settings['player_y']

    if full:
        # 画面の中央にプレイヤーを表示する場合、プレイヤーの座標を計算する
        cx = N // 2
        cy = N // 2
        view = 20
    else:
        cx = player_x
        cy = player_y
        view = num_walls

    # 画面の中央座標を計算
    screen_center_x = screen.get_width() // 2 - cell_size // 2
    screen_center_y = screen.get_height() // 2 - cell_size // 2

    # プレイヤーを中心に周囲の迷路を描画する
    view = int(view / 2)
    for i in range(-view, view + 1):
        for j in range(-view, view + 1):
            x = cx + j
            y = cy + i

            # 描画座標を計算
            draw_x = screen_center_x + j * cell_size
            draw_y = screen_center_y + i * cell_size

            if 0 <= x < N and 0 <= y < N:
                floor_obj = ''
                floor_obj_color = 0,0,0
                cell = maze[y][x]
                # プレイヤー以外のセルの壁を描画
                if cell & 1:
                    pygame.draw.line(screen, (0, 160, 0), (draw_x, draw_y+2), (draw_x + cell_size, draw_y+2), 1)
                if cell & 2:
                    pygame.draw.line(screen, (0, 160, 0), (draw_x + cell_size-2, draw_y), (draw_x + cell_size-2, draw_y + cell_size), 1)
                if cell & 4:
                    pygame.draw.line(screen, (0, 160, 0), (draw_x, draw_y + cell_size-2), (draw_x + cell_size, draw_y + cell_size-2), 1)
                if cell & 8:
                    pygame.draw.line(screen, (0, 160, 0), (draw_x+2, draw_y), (draw_x+2, draw_y + cell_size), 1)
                # プレイヤー以外のセルのドアを描画
                if cell & 16:
                    pygame.draw.line(screen, (160, 160, 0), (draw_x + 4, draw_y + 4), (draw_x + cell_size - 4, draw_y + 4), 1)
                if cell & 32:
                    pygame.draw.line(screen, (160, 160, 0), (draw_x + cell_size - 4, draw_y + 4), (draw_x + cell_size - 4, draw_y + cell_size - 4), 1)
                if cell & 64:
                    pygame.draw.line(screen, (160, 160, 0), (draw_x + 4, draw_y + cell_size - 4), (draw_x + cell_size - 4, draw_y + cell_size - 4), 1)
                if cell & 128:
                    pygame.draw.line(screen, (160, 160, 0), (draw_x + 4, draw_y + 4), (draw_x + 4, draw_y + cell_size - 4), 1)
                floor = game_settings['maze_floor'][y][x]
                if floor & 2:   #room
                    floor_obj = '・'
                    floor_obj_color = 120,120,0
                if floor & 4:   #下り階段
                    floor_obj = '⇓'
                    floor_obj_color = 200,0,0
                if floor & 8:   #上り階段
                    floor_obj = '⇑'
                    floor_obj_color = 200,0,0
                   
                if floor_obj != '' : 
                    font = pygame.font.SysFont('meiryo', cell_size // 4 * 3)  # 日本語フォントと大きさ
                    text_width, text_height = font.size(floor_obj)
                    text_surface = font.render(floor_obj, True, floor_obj_color)
                    screen.blit(text_surface, (draw_x + (cell_size - text_width) / 2, draw_y + (cell_size - text_height) / 2))
                    pygame.display.flip() 



def draw_player_direction(game_settings ):  #画面中心にプレイヤーの向きの▲を表示
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
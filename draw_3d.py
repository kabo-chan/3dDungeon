import pygame

def calculate_wall_dimensions(x, z, game_settings):
    wall_size = game_settings['wall_size']
    screen = game_settings['screen']
    # 壁の高さと幅を計算
    wsize = wall_size[0]
    if z >= 0 : wsize = wsize / (2 * (1 + z))
    hsize = wsize*wall_size[1]
    # 壁の左上の基準位置を計算（ｘ＝０場合の正面の位置）
    xpos = (screen.get_width() - wsize) / 2 + x * wsize
    ypos = (screen.get_height() - hsize) / 2

    return wsize, hsize, xpos, ypos
def draw_wall_sub(points, z,game_settings):
    wall_color = game_settings['wall_color']
    bg_color = game_settings['bg_color']
    screen = game_settings['screen']
    wire = game_settings['wire']
    num_walls = game_settings['num_walls']
    # 奥行きに応じて壁の色を計算
    blend_factor = min(z / num_walls, 1)  # 壁の色をbg_colorに近づけるための係数
    color = [int(wall_color[i] * (1 - blend_factor) + bg_color[i] * blend_factor) for i in range(3)]

    if wire :
        pygame.draw.polygon(screen, bg_color, points, width = 0)
        pygame.draw.polygon(screen, color, points, width=1)
    else:
        pygame.draw.polygon(screen, bg_color, points, width = 0)
        pygame.draw.polygon(screen, color, points, width=0)
def draw_wall(x, z, game_settings): #ｘは左右　ｚは奥行き
    #正面の壁を描く
    points = []
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x, z, game_settings)
    points.append((xpos, ypos))
    points.append((xpos, ypos+hsize))
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z, game_settings)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))

    draw_wall_sub(points,z, game_settings)
def draw_sidewall(x,z, game_settings):
    points = []
    if x < 0:
        # 左の壁を描画
        draw_leftsidewall(x,z, game_settings)
    elif x == 0:
        # 左右両方の壁を描画
        draw_leftsidewall(x,z, game_settings)
        draw_rightsidewall(x,z, game_settings)
    else:
        # 右の壁を描画
        draw_rightsidewall(x,z, game_settings)
def draw_leftsidewall(x,z, game_settings):
    points = []
    #左の横壁を描く
    _, hsize, xpos, ypos = calculate_wall_dimensions(x, z, game_settings)
    points.append((xpos, ypos))
    points.append((xpos, ypos+ hsize))
    _, hsize, xpos, ypos = calculate_wall_dimensions(x, z-1, game_settings)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))
    draw_wall_sub(points,z, game_settings)
def draw_rightsidewall(x,z, game_settings):
    points = []
    #右の横壁を描く
    _, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z, game_settings)
    points.append((xpos, ypos))
    points.append((xpos, ypos+ hsize))
    _, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z-1, game_settings)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))
    draw_wall_sub(points,z, game_settings)

def get_maze_coordinates(i, j,game_settings):
    player_x = game_settings['player_x']
    player_y = game_settings['player_y']
    player_dir = game_settings['player_dir']

    if player_dir == 0:  # 北を向いている
        return player_x + j, player_y - i
    elif player_dir == 1:  # 東を向いている
        return player_x + i, player_y + j
    elif player_dir == 2:  # 南を向いている
        return player_x - j, player_y + i
    elif player_dir == 3:  # 西を向いている
        return player_x - i, player_y - j
def is_wall_present(x, y, game_settings):
    maze = game_settings['maze']
    player_dir = game_settings['player_dir']
    N = game_settings['N']

    # 迷路の範囲外を処理する関数
    def wrap_around(value):
        return (value + N) % N

    # 現在のセルの壁の状態をチェック
    def check_wall(x, y, direction):
        x, y = wrap_around(x), wrap_around(y)
        return (maze[y][x] & (1 << direction)) != 0

    # プレイヤーの方向に応じて前方、左側、右側の壁をチェック
    front_wall = check_wall(x, y, player_dir)
    left_wall = check_wall(x, y, (player_dir - 1) % 4)
    right_wall = check_wall(x, y, (player_dir + 1) % 4)

    return front_wall, left_wall, right_wall
def draw_player_view(game_settings):
    # 主人公の視点から見える壁を描画する
    # この関数は、player_x, player_y, player_dirに基づいて、
    # 適切な壁の描画処理を行う必要があります。
    screen = game_settings['screen']
    num_walls = game_settings['num_walls']
    maze = game_settings['maze']
    player_x = game_settings['player_x']
    player_y = game_settings['player_y']
    player_dir = game_settings['player_dir']
    # 画面クリア
    screen.fill((0, 0, 0))
    
    # 壁の描画
    for i in range(num_walls, -1, -1):
        for j in range(-i-2,i + 2):
            #先に正面壁
            x,y = get_maze_coordinates(i, j,game_settings)
            front_wall, left_wall, right_wall = is_wall_present(x, y, game_settings)
            if front_wall : draw_wall(j,i,game_settings)
        for j in range(-i-2,i + 2):
            #あとから左右の壁
            x,y = get_maze_coordinates(i, j,game_settings)
            front_wall, left_wall, right_wall = is_wall_present(x, y, game_settings)
            if j>=0 :
                if right_wall : draw_rightsidewall(j,i, game_settings)
            if j<=0 :
                if left_wall : draw_leftsidewall(j,i, game_settings)
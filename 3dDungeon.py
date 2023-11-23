import pygame
import random

N = 20  # 迷路のサイズ
maze = [[15 for _ in range(N)] for _ in range(N)]  # 全ての壁がある状態で初期化
cell_size = 20
wire = True
# 主人公の初期状態
player_x, player_y = 0, 0  # 主人公の位置（迷路のスタート地点）
player_dir = 0  # 主人公の向き（0: 北, 1: 東, 2: 南, 3: 西）

wall_size = 800,0.618   #横の幅、縦の比率
screen = pygame.display.set_mode((640, 480))

# 壁の色と線の色
wall_color = (160, 160, 160)
bg_color = (0, 0, 0)

# 奥行きの上限
num_walls = 5
def remove_wall(x, y, direction):
    """ 指定された壁を取り除く関数 """
    maze[y][x] &= ~direction
    if direction == 1 and y > 0:  # 北側の壁
        maze[y-1][x] &= ~4
    elif direction == 2 and x < N-1:  # 東側の壁
        maze[y][x+1] &= ~8
    elif direction == 4 and y < N-1:  # 南側の壁
        maze[y+1][x] &= ~1
    elif direction == 8 and x > 0:  # 西側の壁
        maze[y][x-1] &= ~2

def generate_maze(x, y):
    """ 迷路を生成する関数 """
    directions = [1, 2, 4, 8]
    random.shuffle(directions)
    for direction in directions:
        nx, ny = x, y
        if direction == 1: ny -= 1  # 北
        elif direction == 2: nx += 1  # 東
        elif direction == 4: ny += 1  # 南
        elif direction == 8: nx -= 1  # 西

        if 0 <= nx < N and 0 <= ny < N and maze[ny][nx] == 15:
            remove_wall(x, y, direction)
            generate_maze(nx, ny)
def add_random_rooms(maze, min_size, max_size, num_rooms):
    for _ in range(random.randint(2, num_rooms)):
        room_width = random.randint(min_size, max_size)
        room_height = random.randint(min_size, max_size)
        x = random.randint(0, N - room_width)
        y = random.randint(0, N - room_height)

        # 部屋内のセルを空にする（壁を取り除く）
        for i in range(x, x + room_width):
            for j in range(y, y + room_height):
                maze[j][i] = 0
# 迷路の生成
random.seed()  # 乱数のシード値を設定
generate_maze(0, 0)  # 迷路生成を開始
# ランダムな部屋の追加
add_random_rooms(maze, 2, 5, 5)  # 2x2から5x5のサイズの部屋を2から5個追加

# Pygameの初期化
pygame.init()

def calculate_wall_dimensions(x, z):
    # 壁の高さと幅を計算
    wsize = wall_size[0]
    if z >= 0 : wsize = wsize / (2 * (1 + z))
    hsize = wsize*wall_size[1]
    # 壁の左上の基準位置を計算（ｘ＝０場合の正面の位置）
    xpos = (screen.get_width() - wsize) / 2 + x * wsize
    ypos = (screen.get_height() - hsize) / 2

    return wsize, hsize, xpos, ypos

def draw_wall_sub(points, z):
    # 奥行きに応じて壁の色を計算
    blend_factor = min(z / num_walls, 1)  # 壁の色をbg_colorに近づけるための係数
    color = [int(wall_color[i] * (1 - blend_factor) + bg_color[i] * blend_factor) for i in range(3)]

    if wire :
        pygame.draw.polygon(screen, bg_color, points, width = 0)
        pygame.draw.polygon(screen, color, points, width=1)
    else:
        pygame.draw.polygon(screen, bg_color, points, width = 0)
        pygame.draw.polygon(screen, color, points, width=0)

def draw_wall(x, z): #ｘは左右　ｚは奥行き
    #正面の壁を描く
    points = []
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x, z)
    points.append((xpos, ypos))
    points.append((xpos, ypos+hsize))
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))

    draw_wall_sub(points,z)

def draw_sidewall(x,z):
    points = []
    if x < 0:
        # 左の壁を描画
        draw_leftsidewall(x,z)
    elif x == 0:
        # 左右両方の壁を描画
        draw_leftsidewall(x,z)
        draw_rightsidewall(x,z)
    else:
        # 右の壁を描画
        draw_rightsidewall(x,z)
        
def draw_leftsidewall(x,z):
    points = []
    #左の横壁を描く
    _, hsize, xpos, ypos = calculate_wall_dimensions(x, z)
    points.append((xpos, ypos))
    points.append((xpos, ypos+ hsize))
    _, hsize, xpos, ypos = calculate_wall_dimensions(x, z-1)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))
    draw_wall_sub(points,z)
    
def draw_rightsidewall(x,z):
    points = []
    #右の横壁を描く
    _, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z)
    points.append((xpos, ypos))
    points.append((xpos, ypos+ hsize))
    _, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z-1)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))
    draw_wall_sub(points,z)
    
    


def handle_keys():
    global player_x, player_y, player_dir, moved, wire,num_walls
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        wire = not wire  # スペースキーで線と塗りつぶしを切り替え
        moved = True
    if keys[pygame.K_q]:
        num_walls = (num_walls % 8) + 1
        moved = True
    direction_mapping = {
        pygame.K_a: -1,  # 左に90度回転
        pygame.K_d: 1,   # 右に90度回転
        pygame.K_w: {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)},  # 前に進む
        pygame.K_s: 2,   # 180度回転
    }

    for key, action in direction_mapping.items():
        if keys[key]:
            if isinstance(action, int):
                player_dir = (player_dir + action) % 4
            elif isinstance(action, dict):
                dx, dy = action[player_dir]
                front_wall, _, _ = is_wall_present(maze, player_x, player_y, player_dir)
                if True : #not front_wall: #デバッグとして壁を通り抜けられる
                    player_x = (player_x + dx) % N
                    player_y = (player_y + dy) % N
            moved = True
        
def get_maze_coordinates(player_x, player_y, player_dir, i, j):
    if player_dir == 0:  # 北を向いている
        return player_x + j, player_y - i
    elif player_dir == 1:  # 東を向いている
        return player_x + i, player_y + j
    elif player_dir == 2:  # 南を向いている
        return player_x - j, player_y + i
    elif player_dir == 3:  # 西を向いている
        return player_x - i, player_y - j
def is_wall_present(maze, x, y, player_dir):
    N = len(maze)  # 迷路のサイズ

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
def draw_player_view():
    # 主人公の視点から見える壁を描画する
    # この関数は、player_x, player_y, player_dirに基づいて、
    # 適切な壁の描画処理を行う必要があります。

    # 画面クリア
    screen.fill((0, 0, 0))
    
    # 壁の描画
    for i in range(num_walls, -1, -1):
        for j in range(-i-2,i + 2):
            #先に正面壁
            x,y = get_maze_coordinates(player_x, player_y, player_dir, i, j)
            front_wall, left_wall, right_wall = is_wall_present(maze, x, y, player_dir)
            if front_wall : draw_wall(j,i)
        for j in range(-i-2,i + 2):
            #あとから左右の壁
            x,y = get_maze_coordinates(player_x, player_y, player_dir, i, j)
            front_wall, left_wall, right_wall = is_wall_present(maze, x, y, player_dir)
            if j>=0 :
                if right_wall : draw_rightsidewall(j,i)
            if j<=0 :
                if left_wall : draw_leftsidewall(j,i)
            
            
# フォントの初期化
pygame.font.init()
font = pygame.font.Font(None, 36)  # デフォルトのフォントと大きさ

def draw_text():
    # 方向を文字列に変換
    directions = ["North", "East", "South", "West"]
    direction_text = directions[player_dir]

    # テキストをレンダリング
    position_text = f"Position: ({player_x}, {player_y}), Direction: {direction_text}"
    text_surface = font.render(position_text, True, (255, 255, 255))

    # テキストを画面に描画
    screen.blit(text_surface, (10, screen.get_height()-50))
def draw_player():
    # プレイヤーのセル内での中心点を計算
    player_center = (player_x * cell_size + cell_size // 2, player_y * cell_size + cell_size // 2)

    # プレイヤーの向きに応じて表示する矢印を決定
    if player_dir == 0:  # 北
        arrow = "A"
    elif player_dir == 1:  # 東
        arrow = ">"
    elif player_dir == 2:  # 南
        arrow = "V"
    elif player_dir == 3:  # 西
        arrow = "<"

    # フォントを設定（サイズはセルサイズに合わせて調整）
    font = pygame.font.Font(None, cell_size)

    # テキストをレンダリングしてプレイヤーの位置に描画
    text_surface = font.render(arrow, True, (255, 0, 0))  # 赤色の矢印
    text_rect = text_surface.get_rect(center=player_center)
    screen.blit(text_surface, text_rect)
def draw_maze():
    for y in range(N):
        for x in range(N):
            cell = maze[y][x]
            # 北側の壁
            if cell & 1:
                pygame.draw.line(screen, (0, 160, 0), (x * cell_size, y * cell_size), ((x + 1) * cell_size, y * cell_size), 1)
            # 東側の壁
            if cell & 2:
                pygame.draw.line(screen, (0, 160, 0), ((x + 1) * cell_size, y * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size), 1)
            # 南側の壁
            if cell & 4:
                pygame.draw.line(screen, (0, 160, 0), (x * cell_size, (y + 1) * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size), 1)
            # 西側の壁
            if cell & 8:
                pygame.draw.line(screen, (0, 160, 0), (x * cell_size, y * cell_size), (x * cell_size, (y + 1) * cell_size), 1)

def draw_maze_around_player(player_x, player_y, maze):
    # 画面の中央座標を計算
    screen_center_x = screen.get_width() // 2 - cell_size // 2
    screen_center_y = screen.get_height() // 2 - cell_size // 2

    # プレイヤーを中心に周囲の 5x5 の範囲の迷路を描画する
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

def draw_player_direction():
    # プレイヤーの向きを表示
    arrow_text = ""
    if player_dir == 0:
        arrow_text = "A"
    elif player_dir == 1:
        arrow_text = ">"
    elif player_dir == 2:
        arrow_text = "V"
    elif player_dir == 3:
        arrow_text = "<"

    font = pygame.font.Font(None, cell_size)
    text_surface = font.render(arrow_text, True, (255, 0, 0))  # 赤色の矢印
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)

# ゲームのメインループ
moved = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    handle_keys()  # キー操作の処理
    if moved:
        draw_player_view()  # プレイヤーの視点からの壁の描画
        draw_text()  # テキストの描画
        #draw_maze()
        #draw_player()
        draw_maze_around_player(player_x, player_y, maze)  # プレイヤーの周囲の迷路を描画
        draw_player_direction()  # プレイヤーの向きを表示
        
        pygame.display.flip()  # 画面の更新
        pygame.time.delay(200)  # スリープを挿入

    moved = False  # 移動フラグをリセット        

#   迷宮作成ルーチン

import random
import pygame
import utl
from copy import deepcopy

def generate_maze(x, y, game_settings, maze_status):  # 迷路を生成する関数
    #print(f'generate_maze({x},{y})')
    maze_status[y][x] = 1
    #maze = game_settings['maze']
    N = game_settings['N']
    directions = [0,1,2,3]
    random.shuffle(directions)
    for direction in directions:
        nx, ny = x, y
        if direction == 0: ny -= 1  # 北
        elif direction == 1: nx += 1  # 東
        elif direction == 2: ny += 1  # 南
        elif direction == 3: nx -= 1  # 西

        if 0 <= nx < N and 0 <= ny < N and maze_status[ny][nx] == 0:
            remove_wall(y, x, direction, game_settings)
            maze_status[ny][nx] = 1
            generate_maze(nx, ny, game_settings,maze_status)
def remove_wall(y, x, direction,game_settings):  #指定された壁を取り除く関数
    #print(f'remove_wall({x},{y} d={direction})')
    maze = game_settings['maze']
    N = game_settings['N']

    #maze[y][x] &= ~(1 << direction)  # 該当するビットをクリアして壁を取り除く

    if direction == 0 :  # 北側の壁
        maze[y][x] &= ~1
        if y>0 : maze[y-1][x] &= ~4
    if direction == 1 :  # 東側の壁
        maze[y][x] &= ~2
        if x+1<N : maze[y][x+1] &= ~8
    if direction == 2 :  # 南側の壁
        maze[y][x] &= ~4
        if y+1<N : maze[y+1][x] &= ~1
    if direction == 3 :  # 西側の壁
        maze[y][x] &= ~8
        if x>0 : maze[y][x-1] &= ~2
def find_uncreated_cell(N, maze_status):    # 未作成のセルを探す関数
    #print('find_uncreated_cell')
    for y in range(N):
        for x in range(N):
            if maze_status[y][x] == 0:
                return x, y
    return None  # 未作成のセルが見つからない場合は None を返す
def build_wall(y,x,direction,game_settings):    #壁を作る
    maze = game_settings['maze']
    N = game_settings['N']
    if direction == 0:  #上
        maze[y][x] |= 1
        if y>0 : maze[y - 1][x] |= 4
    if direction == 1:  #右
        maze[y][x] |= 2
        if x+1<N : maze[y][x + 1] |= 8
    if direction == 2:   #下
        maze[y][x] |= 4
        if y+1<N : maze[y + 1][x] |= 1
    if direction == 3:  #左
        maze[y][x] |= 8
        if x>0 : maze[y][x - 1] |= 2
def build_door(y,x,direction,game_settings):    #ドアを作る
    #print(f'build_door y={y} x={x}')
    maze = game_settings['maze']
    N = game_settings['N']
    #ドアがマップ端に作られる場合、マップの逆にもドアをつける
    if direction == 0:  #上16 
        maze[y][x] |= 16
        if y>0 : maze[y - 1][x] |= 64
        else: maze[N][x] |= 64
    if direction == 1:  #右32
        maze[y][x] |= 32
        if x+1<N : maze[y][x + 1] |= 128
        else: maze[y][0] |= 128
    if direction == 2:   #下64
        maze[y][x] |= 64
        if y+1<N : maze[y + 1][x] |= 16
        else: maze[0][x] |= 16
    if direction == 3:  #左128
        maze[y][x] |= 128
        if x>0 : maze[y][x - 1] |= 32
        else: maze[y][N] |= 32
def add_random_rooms(min_size, max_size, num_rooms, game_settings, maze_status):    #指定されたサイズ、数の閉じた部屋を作る
    #print('add_random_rooms')
    maze = game_settings['maze']
    N = game_settings['N']
    for _ in range(num_rooms):
        room_width = random.randint(min_size, max_size)
        room_height = random.randint(min_size, max_size)
        x, y = find_valid_room_position(room_width, room_height, N, maze_status)

        if x is not None and y is not None:
            # 部屋内のセルを空にする（壁を取り除く）
            for i in range(x, x + room_width):
                for j in range(y, y + room_height):
                    maze[j][i] = maze[j][i] & ~0b1111  #四方の壁がない
                    maze_status[j][i] = 2   #部屋
                    #部屋の4辺に壁
                    if i == x                       :build_wall(j,i,3,game_settings)    #左
                    if i == (x + room_width - 1)    :build_wall(j,i,1,game_settings)    #右
                    if j == y                       :build_wall(j,i,0,game_settings)   #上 
                    if j == (y + room_height - 1)   :build_wall(j,i,2,game_settings) #下
def add_random_spaces(min_size, max_size, num_rooms, game_settings, maze_status):   #指定されたサイズ、数の空間を作る
    #print('add_random_space')
    maze = game_settings['maze']
    N = game_settings['N']
    for _ in range(num_rooms):
        room_width = random.randint(min_size, max_size)
        room_height = random.randint(min_size, max_size)
        x, y = find_valid_room_position(room_width, room_height, N, maze_status)
        if x is not None and y is not None:
            # Create a room without surrounding walls
            for i in range(x, x + room_width):
                for j in range(y, y + room_height):
                    maze[j][i] = maze[j][i] & ~0b1111  #四方の壁がない
                    maze_status[j][i] = 1  # 壁のない部屋は通路扱い
                    if i == x                   : remove_wall(j,i,3,game_settings)   #左のマスの右側の壁も取り除く
                    if i == (x + room_width-1)  : remove_wall(j,i,1,game_settings)   #右のマスの左側の壁も取り除く
                    if j == y                   : remove_wall(j,i,0,game_settings)
                    if j == (y + room_height-1) : remove_wall(j,i,2,game_settings)
def find_valid_room_position(room_width, room_height, N, maze_status):  # 部屋の位置を決定する関数
    #print('find_valid_room_position')
    for _ in range(100):  # 最大100回試行
        x = random.randint(0, N - room_width)
        y = random.randint(0, N - room_height)

        # 部屋が既存の部屋と重ならないかチェック
        overlapping = False
        for i in range(x, x + room_width):
            for j in range(y, y + room_height):
                if maze_status[j][i] == 2:  # 既存の部屋と重なる
                    overlapping = True
                    break
            if overlapping:
                break

        if not overlapping:
            # 部屋が重ならない位置が見つかった
            return x, y

    return None, None  # 適切な位置が見つからない場合は None を返す


def check_all_wall_door_consistency(maze):  #　迷路の壁とドアの整合性の確認
    N = len(maze)
    for y in range(N):
        for x in range(N):
            if x+1<N :
                if (maze[y][x] >> 0 & 1) != (maze[y][x+1] >> 3 & 1 ) : 
                    print(f'x:{x},y:{y} の東がへん {maze[y][x] >> 1 & 1}:{maze[y][x+1] >> 3 & 1}')
            if y+1<N :
                if (maze[y][x] >> 2 & 1) != (maze[y+1][x] >> 0 & 1 ) : 
                    print(f'x:{x},y:{y} の南がへん {maze[y][x] >> 2 & 1}:{maze[y+1][x] >> 4 & 1}')
def check_passability(maze, maze_check, x, y):  #通れない部屋がないか確認
    N = len(maze)

    if x < 0 or x >= N or y < 0 or y >= N or maze_check[y][x] == 1:
        return
    
    maze_check[y][x] = 1  # 通行可能なセルとマーク

    # 上下左右のセルを再帰的にチェック
    if (maze[y][x] & 0b0001 == 0) or (maze[y][x] & 0b00010000 == 0b00010000):
        check_passability(maze, maze_check, x, y - 1)  # 上
    if (maze[y][x] & 0b0010 == 0) or (maze[y][x] & 0b00100000 == 0b00100000):
        check_passability(maze, maze_check, x + 1, y)  # 右
    if (maze[y][x] & 0b0100 == 0) or (maze[y][x] & 0b01000000 == 0b01000000):
        check_passability(maze, maze_check, x, y + 1)  # 下
    if (maze[y][x] & 0b1000 == 0) or (maze[y][x] & 0b10000000 == 0b10000000):
        check_passability(maze, maze_check, x - 1, y)  # 左
def decode_maze_cell(cell_value):
    """
    Decodes the cell value of the maze to determine the presence of walls and doors.
    
    Args:
    cell_value (int): The value of the maze cell.

    Returns:
    tuple: A tuple containing two lists, the first list represents the walls (1 for wall, 0 for no wall)
           in the order [north, east, south, west], and the second list represents the doors in the same order.
    """
    walls = [(cell_value >> i) & 1 for i in range(4)]
    doors = [(cell_value >> (i + 4)) & 1 for i in range(4)]
    return walls, doors
def find_staircase_locations_optimal(maze):
    """
    Finds the optimal locations for staircase placement in the maze based on the presence of walls and doors.

    Args:
    maze (list): The maze data.

    Returns:
    list: A list of tuples, each tuple representing the (x, y) coordinates and category of an optimal staircase location.
    """
    maze_width = len(maze[0])
    maze_height = len(maze)
    staircase_locations = []

    for y in range(maze_height):
        for x in range(maze_width):
            walls, doors = decode_maze_cell(maze[y][x])

            # Criteria 1: Not next to a door
            if not any(doors):
                if walls.count(0) == 4:
                    staircase_locations.append((x, y, "No walls"))
                elif walls.count(1) == 3:
                    staircase_locations.append((x, y, "3 walls"))
                elif walls.count(1) ==2:
                    staircase_locations.append((x, y, "2 walls"))
                else:
                    staircase_locations.append((x, y, "Other"))
            else:
                # If next to a door, classify as 'Other'
                staircase_locations.append((x, y, "Other"))
    #print(staircase_locations)
    return staircase_locations

def generate_new_maze(game_settings):   # 新しい迷路を生成
    N = game_settings['N']
    game_settings['maze'] = [[15 for _ in range(N)] for _ in range(N)]
    maze_status = [[0 for _ in range(N)] for _ in range(N)]  # 迷路のセルのステータス
    
    seed=random.randint(0,65536)
    print(f'seed-{seed}')
    random.seed(seed)
    add_random_spaces(2, 2, 15, game_settings, maze_status)
    add_random_rooms(2, 3, 20, game_settings, maze_status)
    
    start_cell = find_uncreated_cell(N, maze_status)
    while start_cell:
        x, y = start_cell
        generate_maze(x, y, game_settings, maze_status)
        start_cell = find_uncreated_cell(N, maze_status)
    #　迷宮の外枠を作る
    for x in range(N):
        game_settings['maze'][0][x] |= 1
        game_settings['maze'][N-1][x] |= 4
    for y in range(N):
        game_settings['maze'][y][0] |= 8
        game_settings['maze'][y][N-1] |= 2

    # 通れない部屋がないか確認
    maze_check = [[0 for _ in range(N)] for _ in range(N)]
    check_passability(game_settings['maze'], maze_check, 0, 0)
    # 通れない部屋があるか確認
    while any(cell == 0 for row in maze_check for cell in row):
        #print("通れない部屋があります。")
                
        # 通れない部屋の隣接するセルが１ならリストに追加
        adjacent_cells = []
        for y in range(N):
            for x in range(N):
                if maze_check[y][x] == 0:
                    if y > 0 and maze_check[y - 1][x] == 1: # 上
                        adjacent_cells.append((y, x,0))
                    if x < N - 1 and maze_check[y][x + 1] == 1:    # 右
                        adjacent_cells.append((y, x,1))
                    if y < N - 1 and maze_check[y + 1][x] == 1:    # 下
                        adjacent_cells.append((y, x,2))
                    if x > 0 and maze_check[y][x - 1] == 1:    # 左
                        adjacent_cells.append((y, x,3))

        if adjacent_cells:
            # ランダムに1つのセルを選択
            random_cell = random.choice(adjacent_cells)
            y, x, direction = random_cell

            # 選んだ方向に扉を設置
            build_door(y,x,direction,game_settings)
             
        maze_check = [[0 for _ in range(N)] for _ in range(N)]
        check_passability(game_settings['maze'], maze_check, 0, 0)
    #check_all_wall_door_consistency(game_settings['maze'])
    #print(game_settings['maze'])
    staircase_locations=find_staircase_locations_optimal(game_settings['maze'])
    locations_only = [(x, y) for x, y, category in staircase_locations if category in ['3 walls', 'No walls']] 
    if not locations_only : 
        locations_only = [(x, y) for x, y, category in staircase_locations if category == '2 walls']

    (dx,dy),(ux,uy)= random.sample(locations_only,2)
    #print(staircase_locations)
    game_settings['maze_floor'] = deepcopy(maze_status)
    game_settings['maze_floor'][dy][dx] += 4
    game_settings['maze_floor'][uy][ux] += 8
    print(dx,dy,ux,uy)
    


if __name__ == "__main__":  # モジュールテスト
    pygame.init()  # pygame を初期化する

    # フォントの初期化
    pygame.font.init()
    N=20
    game_settings = {
        'N': N,
        'maze': [[0b1111 for _ in range(N)] for _ in range(N)],
        'maze_floor':[[0 for _ in range(20)] for _ in range(20)],
        'cell_size': 40,
        'wire': True,
        'player_x': 0,
        'player_y': 0,
        'player_dir': 0,
        'wall_size': (800, 500),
        'screen': pygame.display.set_mode((850, 850)),
        'wall_color': (160, 160, 160),
        'bg_color': (0, 0, 0),
        'door_color': (152, 81, 75),
        'num_walls': 5,
        'moved': True,
        'draw_minimap': True
    }
    # 迷路の生成
    random.seed()  # 乱数のシード値を設定
    generate_new_maze(game_settings)  # 新しい迷路生成を開始
    draw_flag= True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # スペースキーが押された場合
                    # game_settings を初期化して新しい迷路を生成
                    generate_new_maze(game_settings)
                    draw_flag= True
        if draw_flag:
            # 迷路を描画（full=True でプレイヤーの座標を中央に設定）
            game_settings['screen'].fill((0, 0, 0))
            utl.draw_maze_around_player(game_settings, full=True)
            # 画面を更新
            pygame.display.flip()
            draw_flag = False
        pygame.time.delay(100)  # スリープを挿入
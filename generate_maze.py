
import random
import pygame
import utl

def generate_maze(x, y, game_settings, maze_status):  # 迷路を生成する関数
    maze = game_settings['maze']
    N = game_settings['N']
    directions = [1, 2, 4, 8]
    random.shuffle(directions)
    for direction in directions:
        nx, ny = x, y
        if direction == 1: ny -= 1  # 北
        elif direction == 2: nx += 1  # 東
        elif direction == 4: ny += 1  # 南
        elif direction == 8: nx -= 1  # 西

        if 0 <= nx < N and 0 <= ny < N and maze_status[ny][nx] == 0:
            remove_wall(x, y, direction, game_settings)
            maze_status[ny][nx] = 1
            generate_maze(nx, ny, game_settings,maze_status)

def remove_wall(x, y, direction,game_settings):  #指定された壁を取り除く関数
    maze = game_settings['maze']
    N = game_settings['N']

    maze[y][x] &= ~direction
    if direction == 1 and y > 0:  # 北側の壁
        maze[y-1][x] &= ~4
    elif direction == 2 and x < N-1:  # 東側の壁
        maze[y][x+1] &= ~8
    elif direction == 4 and y < N-1:  # 南側の壁
        maze[y+1][x] &= ~1
    elif direction == 8 and x > 0:  # 西側の壁
        maze[y][x-1] &= ~2

# 未作成のセルを探す関数
def find_uncreated_cell(N, maze_status):
    for y in range(N):
        for x in range(N):
            if maze_status[y][x] == 0:
                return x, y
    return None  # 未作成のセルが見つからない場合は None を返す
def modified_add_random_rooms(min_size, max_size, num_rooms, game_settings, maze_status):
    maze = game_settings['maze']
    N = game_settings['N']
    for _ in range(num_rooms):
        room_width = random.randint(min_size, max_size)
        room_height = random.randint(min_size, max_size)
        x, y = find_valid_room_position(room_width, room_height, N, maze_status)

        if x is not None and y is not None:
            if random.choice([True, False]):  # 50% chance
                # 部屋内のセルを空にする（壁を取り除く）
                for i in range(x, x + room_width):
                    for j in range(y, y + room_height):
                        maze[j][i] = 0  #四方の壁がない
                        maze_status[j][i] = 2   #部屋
                        #部屋の4辺に壁
                        if i == x:
                            maze[j][i - 1] |= 2
                            maze[j][i] |= 8
                        if i == (x + room_width - 1):
                            maze[j][i + 1] |= 8
                            maze[j][i] |= 2
                        if j == y:
                            maze[j - 1][i] |= 4
                            maze[j][i] |= 1
                        if j == (y + room_height - 1):
                            maze[j + 1][i] |= 1
                            maze[j][i] |= 4

                # 部屋の壁を選択
                walls = ['left', 'right', 'top', 'bottom']
                selected_wall = random.choice(walls)

                # 扉の位置を決定
                if selected_wall == 'left':
                    door_position = random.randint(y, y + room_height - 1)
                    maze[door_position][x - 1] |= 32  # 左の壁の扉
                    maze[door_position][x] |= 128  # 左の壁の扉
                elif selected_wall == 'right':
                    door_position = random.randint(y, y + room_height - 1)
                    maze[door_position][x + room_width - 1] |= 32  # 右の壁の扉
                    maze[door_position][x + room_width] |= 128  # 右の壁の扉
                elif selected_wall == 'top':
                    door_position = random.randint(x, x + room_width - 1)
                    maze[y - 1][door_position] |= 64  # 上の壁の扉
                    maze[y][door_position] |= 16  # 上の壁の扉
                elif selected_wall == 'bottom':
                    door_position = random.randint(x, x + room_width - 1)
                    maze[y + room_height - 1][door_position] |= 64  # 下の壁の扉
                    maze[y + room_height][door_position] |= 16  # 下の壁の扉
            else:
                # Create a room without surrounding walls
                for i in range(x, x + room_width):
                    for j in range(y, y + room_height):
                        maze[j][i] = 0  # Clear the cell
                        maze_status[j][i] = 2  # 部屋
                        if i == x : maze[j][i-1] &= ~2   #左のマスの右側の壁も取り除く
                        if i == (x + room_width-1) : maze[j][i+1] &= ~8   #右のマスの左側の壁も取り除く
                        if j == y : maze[j-1][i] &= ~4
                        if j == (y + room_height-1) : maze[j+1][i] &= ~1

# 部屋の位置を決定する関数
def find_valid_room_position(room_width, room_height, N, maze_status):
    for _ in range(100):  # 最大100回試行
        x = random.randint(1, N - room_width - 1)
        y = random.randint(1, N - room_height - 1)

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

def add_doors(num_doors, game_settings):
    maze = game_settings['maze']
    N = game_settings['N']
    directions = [0b10000, 0b100000, 0b1000000, 0b10000000]  # 北、東、南、西のドアを示すビット

    for _ in range(num_doors):
        while True:
            x = random.randint(0, N - 1)
            y = random.randint(0, N - 1)
            wall_directions = [1, 2, 4, 8]  # 北、東、南、西の壁を示すビット
            possible_doors = []

            for dir_bit, door_bit in zip(wall_directions, directions):
                if maze[y][x] & dir_bit:
                    possible_doors.append(door_bit)

            if possible_doors:
                maze[y][x] |= random.choice(possible_doors)
                break
# 新しい迷路を生成
def generate_new_maze(game_settings):
    N = game_settings['N']
    game_settings['maze'] = [[15 for _ in range(N)] for _ in range(N)]
    maze_status = [[0 for _ in range(N)] for _ in range(N)]  # 迷路のセルのステータス
    
    modified_add_random_rooms(2, 3, 8, game_settings, maze_status)

    start_cell = find_uncreated_cell(N, maze_status)
    while start_cell:
        x, y = start_cell
        generate_maze(x, y, game_settings, maze_status)
        start_cell = find_uncreated_cell(N, maze_status)

# モジュールテスト
if __name__ == "__main__":
    pygame.init()  # pygame を初期化する

    # フォントの初期化
    pygame.font.init()
    N=20
    game_settings = {
        'N': N,
        'maze': [[15 for _ in range(N)] for _ in range(N)],
        'cell_size': 20,
        'wire': True,
        'player_x': 0,
        'player_y': 0,
        'player_dir': 0,
        'wall_size': (800, 500),
        'screen': pygame.display.set_mode((640, 480)),
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # スペースキーが押された場合
                    # game_settings を初期化して新しい迷路を生成
                    generate_new_maze(game_settings)

        # 迷路を描画（full=True でプレイヤーの座標を中央に設定）
        game_settings['screen'].fill((0, 0, 0))
        utl.draw_maze_around_player(game_settings, full=True)

        # 画面を更新
        pygame.display.flip()

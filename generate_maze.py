import random

def generate_maze(x, y, game_settings):  # 迷路を生成する関数
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

        if 0 <= nx < N and 0 <= ny < N and maze[ny][nx] == 15:
            remove_wall(x, y, direction, game_settings)
            generate_maze(nx, ny, game_settings)


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

def add_random_rooms(min_size, max_size, num_rooms,game_settings):  #迷路内に大きな空間を作る
    maze = game_settings['maze']
    N = game_settings['N']
    for _ in range(random.randint(2, num_rooms)):
        room_width = random.randint(min_size, max_size)
        room_height = random.randint(min_size, max_size)
        x = random.randint(0, N - room_width)
        y = random.randint(0, N - room_height)

        # 部屋内のセルを空にする（壁を取り除く）
        for i in range(x, x + room_width):
            for j in range(y, y + room_height):
                maze[j][i] = 0
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
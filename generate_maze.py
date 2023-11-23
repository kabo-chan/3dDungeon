import random

def generate_maze(x, y,maze,N):    #迷路を生成する関数
    directions = [1, 2, 4, 8]
    random.shuffle(directions)
    for direction in directions:
        nx, ny = x, y
        if direction == 1: ny -= 1  # 北
        elif direction == 2: nx += 1  # 東
        elif direction == 4: ny += 1  # 南
        elif direction == 8: nx -= 1  # 西

        if 0 <= nx < N and 0 <= ny < N and maze[ny][nx] == 15:
            remove_wall(x, y, direction,maze,N)
            generate_maze(nx, ny,maze,N)

def remove_wall(x, y, direction,maze,N):  #指定された壁を取り除く関数
    maze[y][x] &= ~direction
    if direction == 1 and y > 0:  # 北側の壁
        maze[y-1][x] &= ~4
    elif direction == 2 and x < N-1:  # 東側の壁
        maze[y][x+1] &= ~8
    elif direction == 4 and y < N-1:  # 南側の壁
        maze[y+1][x] &= ~1
    elif direction == 8 and x > 0:  # 西側の壁
        maze[y][x-1] &= ~2

def add_random_rooms(maze, min_size, max_size, num_rooms,N):  #迷路内に大きな空間を作る
    for _ in range(random.randint(2, num_rooms)):
        room_width = random.randint(min_size, max_size)
        room_height = random.randint(min_size, max_size)
        x = random.randint(0, N - room_width)
        y = random.randint(0, N - room_height)

        # 部屋内のセルを空にする（壁を取り除く）
        for i in range(x, x + room_width):
            for j in range(y, y + room_height):
                maze[j][i] = 0
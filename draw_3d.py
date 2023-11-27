import pygame
import numpy as np

def transform_points_with_points_list(points_to_transform, quad_points):
    rect = np.array([[0, 0], [0, 500], [800, 500], [800, 0]])
    matrix = compute_transformation_matrix(rect, np.array(quad_points))
    transformed_points = [apply_transformation(matrix, point) for point in points_to_transform]
    return transformed_points

def compute_transformation_matrix(from_coords, to_coords):
    A = []
    B = []
    for i in range(4):
        x, y = from_coords[i, 0], from_coords[i, 1]
        u, v = to_coords[i, 0], to_coords[i, 1]
        A.append([x, y, 1, 0, 0, 0, -u*x, -u*y])
        A.append([0, 0, 0, x, y, 1, -v*x, -v*y])
        B.append(u)
        B.append(v)
    A = np.array(A)
    B = np.array(B)
    transform_matrix = np.linalg.solve(A, B)
    transform_matrix = np.append(transform_matrix, 1).reshape(3, 3)
    return transform_matrix

def apply_transformation(matrix, point):
    point = np.array([point[0], point[1], 1])
    transformed_point = np.dot(matrix, point)
    transformed_point = transformed_point / transformed_point[2]
    return transformed_point[:2]

def calculate_wall_dimensions(x, z, game_settings):
    wall_size = game_settings['wall_size']
    screen = game_settings['screen']
    wsize = wall_size[0]
    if z >= 0:
        wsize = wsize / (2 * (1 + z))
    hsize = wsize * wall_size[1] / wall_size[0]
    xpos = (screen.get_width() - wsize) / 2 + x * wsize
    ypos = (screen.get_height() - hsize) / 2
    return wsize, hsize, xpos, ypos

def draw_wall_sub(points, z, base_color, game_settings):
    bg_color = game_settings['bg_color']
    screen = game_settings['screen']
    wire = game_settings['wire']
    num_walls = game_settings['num_walls']
    blend_factor = min(z / num_walls, 1)
    color = [int(base_color[i] * (1 - blend_factor) + bg_color[i] * blend_factor) for i in range(3)]
    if wire:
        pygame.draw.polygon(screen, bg_color, points, width=0)
        pygame.draw.polygon(screen, color, points, width=1)
    else:
        pygame.draw.polygon(screen, color, points, width=0)
def draw_stairs(x,z,game_settings,is_down=False,is_up=False):
    points = []
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x, z, game_settings)
    points.append((xpos, ypos+hsize))
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x, z-1, game_settings)
    points.append((xpos, ypos+hsize))
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z-1, game_settings)
    points.append((xpos, ypos+hsize))
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z, game_settings)
    points.append((xpos, ypos+hsize))
    if is_down:
        stair_points = [(200, 200), (200, 400), (600, 400), (600, 200)]
        points = transform_points_with_points_list(stair_points, points)

    draw_wall_sub(points, z, game_settings['stair_color'] if is_down or is_up else game_settings['floor_color'] , game_settings)

def draw_wall(x, z, game_settings, is_door=False, is_left=False, is_right=False):
    points = []
    if is_left:
        _, hsize, xpos, ypos = calculate_wall_dimensions(x, z, game_settings)
        points.append((xpos, ypos))
        points.append((xpos, ypos + hsize))
        _, hsize, xpos, ypos = calculate_wall_dimensions(x, z - 1, game_settings)
        points.append((xpos, ypos + hsize))
        points.append((xpos, ypos))
    elif is_right:
        _, hsize, xpos, ypos = calculate_wall_dimensions(x + 1, z, game_settings)
        points.append((xpos, ypos))
        points.append((xpos, ypos + hsize))
        _, hsize, xpos, ypos = calculate_wall_dimensions(x + 1, z - 1, game_settings)
        points.append((xpos, ypos + hsize))
        points.append((xpos, ypos))
    else:
        _, hsize, xpos, ypos = calculate_wall_dimensions(x, z, game_settings)
        points.append((xpos, ypos))
        points.append((xpos, ypos + hsize))
        _, hsize, xpos, ypos = calculate_wall_dimensions(x + 1, z, game_settings)
        points.append((xpos, ypos + hsize))
        points.append((xpos, ypos))

    if is_door:
        door_points = [(250, 100), (250, 500), (550, 500), (550, 100)]
        points = transform_points_with_points_list(door_points, points)

    draw_wall_sub(points, z, game_settings['door_color'] if is_door else game_settings['wall_color'], game_settings)

# その他の関数 (get_maze_coordinates, is_wall_present, is_door_present, draw_player_view) は以前と変わらず


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
def is_door_present(x, y, game_settings):
    maze = game_settings['maze']
    player_dir = game_settings['player_dir']
    N = game_settings['N']

    # 迷路の範囲外を処理する関数
    def wrap_around(value):
        return (value + N) % N

    # 現在のセルの壁の状態をチェック
    def check_door(x, y, direction):
        x, y = wrap_around(x), wrap_around(y)
        return (maze[y][x] & (1 << (direction+4))) != 0

    # プレイヤーの方向に応じて前方、左側、右側の壁をチェック
    front_door = check_door(x, y, player_dir)
    left_door = check_door(x, y, (player_dir - 1) % 4)
    right_door = check_door(x, y, (player_dir + 1) % 4)

    return front_door, left_door, right_door
def is_floor_present(x, y, game_settings):
    maze_floor = game_settings['maze_floor']
    player_dir = game_settings['player_dir']
    N = game_settings['N']

    # 迷路の範囲外を処理する関数
    def wrap_around(value):
        return (value + N) % N

    # プレイヤーの方向に応じて前方、左側、右側の壁をチェック
    is_down = game_settings['maze_floor'][ wrap_around(y)][ wrap_around(x)] & 4 == 4
    is_up = game_settings['maze_floor'][ wrap_around(y)][ wrap_around(x)] & 8 == 8

    return is_down,is_up
def draw_player_view(game_settings):
    screen = game_settings['screen']
    num_walls = game_settings['num_walls']

    # 画面クリア
    screen.fill((0, 0, 0))
    
    # 壁の描画
    for i in range(num_walls, -1, -1):  #奥から描く
        for j in range(-i - 2, i + 2):#正面壁
            x, y = get_maze_coordinates(i, j, game_settings)
            front_wall, left_wall, right_wall = is_wall_present(x, y, game_settings)
            front_door, left_door, right_door = is_door_present(x, y, game_settings)

            # 正面の壁またはドアの描画
            if front_wall: draw_wall(j, i, game_settings)
            if front_door: draw_wall(j, i, game_settings, is_door=True)
        for j in range(-i - 2, i + 2):#床
            draw_stairs(j,i,game_settings)
            x, y = get_maze_coordinates(i, j, game_settings)
            is_down,is_up =is_floor_present(x, y, game_settings)
            if is_down: draw_stairs(j,i,game_settings,is_down=True)
        for j in range(-i - 2, i + 2):#左右の壁
            x, y = get_maze_coordinates(i, j, game_settings)
            front_wall, left_wall, right_wall = is_wall_present(x, y, game_settings)
            front_door, left_door, right_door = is_door_present(x, y, game_settings)
            # 右の壁またはドアの描画
            if j >= 0:
                if right_wall: draw_wall(j, i, game_settings, is_right=True)
                if right_door: draw_wall(j, i, game_settings, is_door=True, is_right=True)
            # 左の壁またはドアの描画
            if j <= 0:
                if left_wall: draw_wall(j, i, game_settings, is_left=True)
                if left_door: draw_wall(j, i, game_settings, is_door=True, is_left=True)



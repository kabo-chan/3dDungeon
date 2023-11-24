import pygame
import numpy as np

def transform_points_with_points_list(points_to_transform, quad_points):
    """
    Transforms a list of points from an initial rectangle (800x500) to a new quadrilateral defined by
    the quad_points list [(x1, y1), (x2, y2), (x3, y3), (x4, y4)].
    
    :param points_to_transform: List of points to be transformed.
    :param quad_points: List of four points defining the new quadrilateral.
    :return: List of transformed points.
    """

    # Initial rectangle coordinates
    rect = np.array([[0, 0], [0, 500], [800, 500], [800, 0]])

    # Compute the transformation matrix from the rectangle to the quadrilateral
    matrix = compute_transformation_matrix(rect, np.array(quad_points))

    # Transform each point in the list
    transformed_points = [apply_transformation(matrix, point) for point in points_to_transform]

    return transformed_points

def compute_transformation_matrix(from_coords, to_coords):
    """
    Computes the transformation matrix to map a set of coordinates to a new set of coordinates.
    """

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

    # Solve the system of linear equations to find the transformation matrix
    transform_matrix = np.linalg.solve(A, B)
    transform_matrix = np.append(transform_matrix, 1).reshape(3, 3)

    return transform_matrix

def apply_transformation(matrix, point):
    """
    Applies the transformation defined by the matrix to a point.
    """
    point = np.array([point[0], point[1], 1])
    transformed_point = np.dot(matrix, point)
    transformed_point = transformed_point / transformed_point[2]
    return transformed_point[:2]


def calculate_wall_dimensions(x, z, game_settings):
    wall_size = game_settings['wall_size']
    screen = game_settings['screen']
    # 壁の高さと幅を計算
    wsize = wall_size[0]
    if z >= 0 : wsize = wsize / (2 * (1 + z))
    hsize = wsize*wall_size[1]/wall_size[0]
    # 壁の左上の基準位置を計算（ｘ＝０場合の正面の位置）
    xpos = (screen.get_width() - wsize) / 2 + x * wsize
    ypos = (screen.get_height() - hsize) / 2

    return wsize, hsize, xpos, ypos
def draw_wall_sub(points, z,base_color,game_settings):
    bg_color = game_settings['bg_color']
    screen = game_settings['screen']
    wire = game_settings['wire']
    num_walls = game_settings['num_walls']
    # 奥行きに応じて壁の色を計算
    blend_factor = min(z / num_walls, 1)  # 壁の色をbg_colorに近づけるための係数
    color = [int(base_color[i] * (1 - blend_factor) + bg_color[i] * blend_factor) for i in range(3)]

    if wire :
        pygame.draw.polygon(screen, bg_color, points, width = 0)
        pygame.draw.polygon(screen, color, points, width=1)
    else:
        pygame.draw.polygon(screen, bg_color, points, width = 0)
        pygame.draw.polygon(screen, color, points, width=0)
def draw_door(x, z, game_settings): #ｘは左右　ｚは奥行き
    #正面のドアを描く
    points = []
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x, z, game_settings)
    points.append((xpos, ypos))
    points.append((xpos, ypos+hsize))
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z, game_settings)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))
    door_points = [(250,100),(250,500),(550,500),(550,100)]

    draw_wall_sub(transform_points_with_points_list(door_points, points),z,game_settings['door_color'], game_settings)
def draw_wall(x, z, game_settings): #ｘは左右　ｚは奥行き
    #正面の壁を描く
    points = []
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x, z, game_settings)
    points.append((xpos, ypos))
    points.append((xpos, ypos+hsize))
    wsize, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z, game_settings)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))

    draw_wall_sub(points,z, game_settings['wall_color'],game_settings)
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
    draw_wall_sub(points,z, game_settings['wall_color'],game_settings)
def draw_leftsidedoor(x,z, game_settings):
    points = []
    #左の横壁を描く
    _, hsize, xpos, ypos = calculate_wall_dimensions(x, z, game_settings)
    points.append((xpos, ypos))
    points.append((xpos, ypos+ hsize))
    _, hsize, xpos, ypos = calculate_wall_dimensions(x, z-1, game_settings)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))
    door_points = [(250,100),(250,500),(550,500),(550,100)]
    draw_wall_sub(transform_points_with_points_list(door_points, points),z,game_settings['door_color'], game_settings)
def draw_rightsidewall(x,z, game_settings):
    points = []
    #右の横壁を描く
    _, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z, game_settings)
    points.append((xpos, ypos))
    points.append((xpos, ypos+ hsize))
    _, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z-1, game_settings)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))
    draw_wall_sub(points,z, game_settings['wall_color'],game_settings)
def draw_rightsidedoor(x,z, game_settings):
    points = []
    #右の横壁を描く
    _, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z, game_settings)
    points.append((xpos, ypos))
    points.append((xpos, ypos+ hsize))
    _, hsize, xpos, ypos = calculate_wall_dimensions(x+1, z-1, game_settings)
    points.append((xpos, ypos+hsize))
    points.append((xpos, ypos))
    door_points = [(250,100),(250,500),(550,500),(550,100)]
    draw_wall_sub(transform_points_with_points_list(door_points, points),z,game_settings['door_color'], game_settings)

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
            front_door, left_door, right_door = is_door_present(x, y, game_settings)
            if front_door : draw_door(j,i,game_settings)
        for j in range(-i-2,i + 2):
            #あとから左右の壁
            x,y = get_maze_coordinates(i, j,game_settings)
            front_wall, left_wall, right_wall = is_wall_present(x, y, game_settings)
            front_door, left_door, right_door = is_door_present(x, y, game_settings)
            if j>=0 :
                if right_wall : draw_rightsidewall(j,i, game_settings)
                if right_door : draw_rightsidedoor(j,i, game_settings)
            if j<=0 :
                if left_wall : draw_leftsidewall(j,i, game_settings)
                if left_door : draw_leftsidedoor(j,i, game_settings)
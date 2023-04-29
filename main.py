"""
DEFINITELY NOT TETRIS
100 % NOT A TETRIS COPY BUT A FULLY ORIGINAL GAME
INVOLVING FALLING TETROMINOS
"""


import pygame
import sys
import random
import math


def generate_tetromino_list():
    """
    Function generating new list of next 1000 elements,
    different elements are in form of t number from 0 to 6.
    We are also making sure that we do not have 2 same tetrominos in t row
    and that in each 10 tetrominos, we have at least one of each.
    """
    last = [0] * 7
    tet_list = [0] * 1000
    for t in range(1000):
        tet_list[t] = random.randint(0, 6)
        if tet_list[t - 1] == tet_list[t]:
            tet_list[t] = random.randint(0, 6)
        last[tet_list[t]] = t
        if t > 10:
            for b in range(7):
                if t - last[b] > 10:
                    tet_list[t] = b
                    last[tet_list[t]] = t
    return tet_list


def movement_holding(k, dx_left, dx_right, tet_fs):
    """
    Function taking care of movement related to holding a button.
    k - is an array of boolean values of every button state
    dx_left and dx_right are vector values in left and right directions'
    tet_fs - is tetrominos falling speed
    """
    if k[pygame.K_RIGHT]:
        dx_right = 1
    elif not k[pygame.K_RIGHT]:
        dx_right = 0
    if k[pygame.K_LEFT]:
        dx_left = 1
    elif not k[pygame.K_LEFT]:
        dx_left = 0
    if k[pygame.K_DOWN]:
        tet_fs = 2
    elif not k[pygame.K_DOWN]:
        tet_fs = tetromino_fall_speed_gm[gm_nr]
    return dx_right, dx_left, tet_fs


def getting_x(tet):
    """
    a function returning x value of each block of the tetromino
    and putting them in an array
    tet - tetromino which is an array of 2 element arrays
          each holding x and y value of each block in tetromino
    array - previously mentioned array with x values of blocks
    """
    array = [int((tet[0][0] - margin_horizontal) / tile_size),
             int((tet[1][0] - margin_horizontal) / tile_size),
             int((tet[2][0] - margin_horizontal) / tile_size),
             int((tet[3][0] - margin_horizontal) / tile_size)]
    return array


def getting_y(tet):
    """
        a function returning y value of each block of the tetromino
        and putting them in an array
        tet - tetromino which is an array of 2 element arrays
              each holding x and y value of each block in tetromino
        array - previously mentioned array with y values of blocks
        """
    array = (int((tet[0][1] - margin_vertical) / tile_size),
             int((tet[1][1] - margin_vertical) / tile_size),
             int((tet[2][1] - margin_vertical) / tile_size),
             int((tet[3][1] - margin_vertical) / tile_size))
    return array


def tetromino_update(tet_x, tet_y, tet_nr, tet_r):
    """
    function that updates tetrominos x and y based on its rotation (tet_r)
    and its type (tet_nr)
    tet_x and tet_y are values of x and y coordinate of the rotation block
    it returns an array holding coordinates of all tetromino blocks
    """
    global grid_coordinates, ROTATIONS
    tet = (grid_coordinates[tet_x % 10][tet_y],
           grid_coordinates[(tet_x + ROTATIONS[tet_nr][tet_r][0][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][0][1]],
           grid_coordinates[(tet_x + ROTATIONS[tet_nr][tet_r][1][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][1][1]],
           grid_coordinates[(tet_x + ROTATIONS[tet_nr][tet_r][2][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][2][1]])
    return tet


def tetromino_update_next(tet_x, tet_y, tet_nr, tet_r):
    """
    function that updates next tetrominos x and y based on its rotation (tet_r)
    and its type (tet_nr)
    tet_x and tet_y are values of x and y coordinate of the rotation block
    it returns an array holding coordinates of all tetromino blocks
    """
    global grid_coordinates_next, ROTATIONS
    tet = (grid_coordinates_next[tet_x % 10][tet_y],
           grid_coordinates_next[(tet_x + ROTATIONS[tet_nr][tet_r][0][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][0][1]],
           grid_coordinates_next[(tet_x + ROTATIONS[tet_nr][tet_r][1][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][1][1]],
           grid_coordinates_next[(tet_x + ROTATIONS[tet_nr][tet_r][2][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][2][1]])
    return tet


def point_calculator(point_system, b2b_points,
                     is_last_tetris, no_lines_cleared, lvl):
    """
    function that returns the number of points
    gained by clearing the lines based on the number of lines
    cleared, level and on the last clear being tetris or not.
    """
    return (lvl + 1) * (point_system[no_lines_cleared - 1] +
                        b2b_points * is_last_tetris)


def tetromino_update_hold(tet_x, tet_y, tet_nr, tet_r):
    """
    function that updates held tetrominos x and y based on its rotation (tet_r)
    and its type (tet_nr)
    tet_x and tet_y are values of x and y coordinate of the rotation block
    it returns an array holding coordinates of all tetromino blocks
    """
    global grid_coordinates_hold, ROTATIONS
    tet = (grid_coordinates_hold[tet_x % 10][tet_y],
           grid_coordinates_hold[(tet_x + ROTATIONS[tet_nr][tet_r][0][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][0][1]],
           grid_coordinates_hold[(tet_x + ROTATIONS[tet_nr][tet_r][1][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][1][1]],
           grid_coordinates_hold[(tet_x + ROTATIONS[tet_nr][tet_r][2][0]) % 10]
           [tet_y + ROTATIONS[tet_nr][tet_r][2][1]])
    return tet


def new_tetromino(tet_list, tet_nr):
    """
    function returning starting position and nr and rotation
    of a new tetromino
    tet_x and tet_y - coordinates of tetrominos rotation block
    tet_nr - number of tetrominos type
    tet_r - current state of tetrominos rotation
    """
    global TETROMINO_STARTING_POS
    tet_nr += 1
    tet_x = TETROMINO_STARTING_POS[tet_list[tet_nr]][0]
    tet_y = TETROMINO_STARTING_POS[tet_list[tet_nr]][1]
    tet_r = 0
    return tet_x, tet_y, tet_nr, tet_r


def horizontal_check_left_border(arr_x):
    """
    function that checks if tetromino is
    hugging left wall
    arr_x - array holding tetrominos coordinates
    """
    for t in range(4):
        if arr_x[t] == 0:
            return False
    return True


def horizontal_check_right_border(arr_x):
    """
    function that checks if tetromino is
    hugging right wall
    arr_x - array holding tetrominos coordinates
    """
    for t in range(4):
        if arr_x[t] == 9:
            return False
    return True


def horizontal_check_left_grid(arr_x, arr_y, arr_g):
    """
    function that checks if the block on the left of
    tetromino is full
    arr_x - array holding tetrominos x coordinates
    arr_y - array holding tetrominos y coordinates
    arr_g - array holding the state of each grid
    """
    for t in range(4):
        if arr_x[t] > 0:
            if arr_g[arr_x[t] - 1][arr_y[t]] > 0:
                return False
    return True


def horizontal_check_right_grid(arr_x, arr_y, arr_g):
    """
    function that checks if the block on the right of
    tetromino is full
    arr_x - array holding tetrominos x coordinates
    arr_y - array holding tetrominos y coordinates
    arr_g - array holding the state of each grid
    """
    for t in range(4):
        if arr_x[t] < 9:
            if arr_g[arr_x[t] + 1][arr_y[t]] > 0:
                return False
    return True


def checking_rotate_viability(tet_arr, tet_x, tet_y, tet_nr, tet_r, tet_list):
    """
    function that checks if the actual grid state makes it possible
    for the tetromino to rotate
    tet_x - array holding tetrominos x coordinates
    tet_y - array holding tetrominos y coordinates
    tet_arr - array holding the state of each grid
    tet_nr - the nr of tetromino
    tet_list - list of all tetrominos
    tet_r - starting rotation state
    """
    tet_new = tetromino_update(tet_x, tet_y, tet_list[tet_nr], tet_r)
    tet_new_x = getting_x(tet_new)
    tet_new_y = getting_y(tet_new)
    for t in range(4):
        if tet_arr[tet_new_x[t]][tet_new_y[t]] > 0:
            return False
    return True


def rotation_check_border(tet, tet_x, tet_y, tet_nr, rot_nr):
    """
    function that checks if by rotation the tetromino wouldn't
    go out of grid
    tet - array holding coordinates of current tetromino
    tet_x - array holding tetrominos x coordinates
    tet_y - array holding tetrominos y coordinates
    tet_arr - array holding the state of each grid
    tet_nr - the nr of tetromino
    tet_r - starting rotation state
    """
    if tet_x < 5:
        for t in range(4):
            if getting_x(tet)[t] == 8:
                tet_x += 2
                tet = tetromino_update(tet_x, tet_y, tet_nr, rot_nr)
            elif getting_x(tet)[t] == 9:
                tet_x += 1
                tet = tetromino_update(tet_x, tet_y, tet_nr, rot_nr)
    if tet_x > 5:
        for t in range(4):
            if getting_x(tet)[t] == 1:
                tet_x -= 2
                tet = tetromino_update(tet_x, tet_y, tet_nr, rot_nr)
            elif getting_x(tet)[t] == 0:
                tet_x -= 1
                tet = tetromino_update(tet_x, tet_y, tet_nr, rot_nr)
    return tet, tet_x


def rotation_check_width(tet_arr, tet_x, tet_y, tet_nr, tet_r, tet_list):
    """
    function that checks if the actual grid state makes it possible
    for the tetromino to rotate based on width of tetromino after rotation
    and the width of the free space
    tet_x - array holding tetrominos x coordinates
    tet_y - array holding tetrominos y coordinates
    tet_arr - array holding the state of each grid
    tet_nr - the nr of tetromino
    tet_list - list of all tetrominos
    tet_r - starting rotation state
    """
    tet_new = tetromino_update(tet_x, tet_y, tet_list[tet_nr], tet_r)
    tet_new_x = getting_x(tet_new)
    if tet_x < 5:
        for t in range(4):
            if tet_new_x[t] > 7:
                tet_new_x[t] = tet_new_x[t] - 10
    if tet_x > 5:
        for t in range(4):
            if tet_new_x[t] < 3:
                tet_new_x[t] = tet_new_x[t] + 10
    width_tet = max(tet_new_x) - min(tet_new_x) + 1
    tet_arr_left = -5
    tet_arr_right = -5
    for t in range(10):
        if tet_arr[t][tet_y] > 0:
            tet_arr_left = t
            break
    for t in range(9, -1, -1):
        if tet_arr[t][tet_y] > 0:
            tet_arr_right = t
            break
    if tet_arr_left > 0 or tet_arr_right > 0:
        if tet_x < 5:
            if width_tet > tet_arr_left:
                return False
        if tet_x > 5:
            if width_tet > 10 - tet_arr_right - 1:
                return False
    return True


def freeze(tet_arr, tet_nr, arr_game):
    """
    function that freezes the tetromino in place after it reaching the bottom
    by changing the values of arr_game
    arr_game - array holding the state of each grid
    tet_nr - the nr of tetromino
    tet_arr - array holding coordinates of current tetromino
    """
    tet_y = getting_y(tet_arr)
    tet_x = getting_x(tet_arr)
    for t in range(4):
        arr_game[tet_x[t]][tet_y[t]] = tet_nr + 1
    return arr_game


def game_freeze_control(tet_arr, tet_nr, arr_game, islast_hold):
    """
    function that checks if tetromino is at the bottom, and if it is it
    freezes it in place using the freeze function
    arr_game - array holding the state of each grid
    tet_nr - the nr of tetromino
    tet_arr - array holding coordinates of current tetromino
    islast_hold - boolean value saying if the last tetromino was held
    """
    tet_y = getting_y(tet_arr)
    tet_x = getting_x(tet_arr)
    for t in range(4):
        if tet_y[t] == 23:
            arr_game = freeze(tet_arr, tet_nr, arr_game)
            islast_hold = False
            return arr_game, True, islast_hold
        elif arr_game[int(tet_x[t])][int(tet_y[t]) + 1] > 0:
            arr_game = freeze(tet_arr, tet_nr, arr_game)
            islast_hold = False
            return arr_game, True, islast_hold
    return arr_game, False, islast_hold


def drawing_grid(arr_game):
    """
    Function drawing all the frozen tetrominos in the grid.
    arr_game - array holding the state of each grid(tetromino block)
    """
    global width, height, grid_coordinates
    for c in range(width):
        for b in range(height):
            if arr_game[c][b] > 0:
                pygame.draw.rect(scr, TETROMINO_COLOR[arr_game[c][b] - 1],
                                 pygame.Rect(grid_coordinates[c][b][0],
                                             grid_coordinates[c][b][1],
                                             tile_size, tile_size))


def space_used(grid_tet, is_fr, tet, tet_nr_type, tet_x, tet_y,
               rot_nr, tet_nr, tet_list, islast_hold):
    """
    Function that moves the tetromino down to the board after
    the space bar being pressed after which it freezes tetromino in place.
    """
    while not is_fr:
        grid_tet, is_fr, islast_hold = game_freeze_control(tet, tet_nr_type,
                                                           grid_tet,
                                                           islast_hold)
        if is_fr:
            tet_x, tet_y, tet_nr, rot_nr = new_tetromino(tet_list, tet_nr)
            break
        tet_y += 1
        tet = tetromino_update(tet_x, tet_y, tet_nr_type, rot_nr)
    return grid_tet, is_fr, tet, tet_nr_type, tet_x, tet_y, rot_nr, tet_nr, \
        islast_hold


def game_end_check(arr_game):
    """
    Function that checks if the player lost
    arr_game - array holding the state of the board
    """
    for c in range(width):
        for b in range(4):
            if arr_game[c][b] > 0:
                return True
    return False


def is_line_full(tet_arr, line):
    """
    Function checking if a line is full.
    tet_arr - array holding the state of the board
    line - the number of the line being checked
    """
    for c in range(10):
        if tet_arr[c][line] == 0:
            return False
    return True


def line_clear(tet_arr, line):
    """
    Function clearing a line.
    tet_arr - array holding the state of the board
    line - the number of the line being checked
    """
    for c in range(10):
        tet_arr[c][line] = 0
    for c in range(10):
        for b in range(line, 0, -1):
            tet_arr[c][b] = tet_arr[c][b - 1]
    return tet_arr


def line_handler(tet_arr, no_lines_cleared, point, point_system, b2b_points,
                 is_last_tetris, lvl, tet_falling_speed, tet_falling_speed_gm):
    """
    Function handling lines, clearing them if they are full,
    and returning the number of lines cleared, and points.
    tet_arr - array holding the state of the board
    no_lines_cleared - number of lines cleared to this points
    point - number of points
    point_system - array holding number of points for each number of lines
    b2b_points - how many points for back to back tetris
    is_last_tetris - boolean variable saying if the last clear was tetris
    lvl - level
    tet_falling_speed - falling speed of the tetromino
    """
    lines_cleared_rn = 0
    for c in range(23, -1, -1):
        if is_line_full(tet_arr, c):
            tet_arr = line_clear(tet_arr, c)
            lines_cleared_rn += 1
    if lines_cleared_rn > 0:
        for c in range(23, -1, -1):
            if is_line_full(tet_arr, c):
                tet_arr = line_clear(tet_arr, c)
                lines_cleared_rn += 1
        for c in range(23, -1, -1):
            if is_line_full(tet_arr, c):
                tet_arr = line_clear(tet_arr, c)
                lines_cleared_rn += 1
        point += point_calculator(point_system, b2b_points, is_last_tetris,
                                  lines_cleared_rn, lvl)
        if lines_cleared_rn == 4:
            is_last_tetris = True
        else:
            is_last_tetris = False
        tet_falling_speed = tet_falling_speed_gm[lvl]
    no_lines_cleared += lines_cleared_rn
    return tet_arr, no_lines_cleared, point, is_last_tetris, tet_falling_speed


def event_handler():
    """
    function taking care of user key inputs in game state
    """
    global rotate_nr, tetromino, tetromino_x, tetromino_y, tetromino_list
    global tetromino_nr, grid_tetris, is_freeze, tetromino_nr
    global speed_control, speed_control_player, is_last_hold, held_tetromino
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_z:
                if rotation_check_width(grid_tetris, tetromino_x,
                                        tetromino_y, tetromino_nr,
                                        ((rotate_nr + 1) % 4),
                                        tetromino_list):
                    if checking_rotate_viability(grid_tetris, tetromino_x,
                                                 tetromino_y, tetromino_nr,
                                                 (rotate_nr + 1) % 4,
                                                 tetromino_list):
                        rotate_nr = (rotate_nr + 1) % 4
                        tetromino = tetromino_update(tetromino_x, tetromino_y,
                                                     tetromino_list[
                                                         tetromino_nr],
                                                     rotate_nr)
                        tetromino, tetromino_x = \
                            rotation_check_border(tetromino, tetromino_x,
                                                  tetromino_y,
                                                  tetromino_list[tetromino_nr],
                                                  rotate_nr)
            if ev.key == pygame.K_UP:
                if rotation_check_width(grid_tetris, tetromino_x,
                                        tetromino_y, tetromino_nr,
                                        ((rotate_nr - 1) % 4), tetromino_list):
                    if checking_rotate_viability(grid_tetris, tetromino_x,
                                                 tetromino_y, tetromino_nr,
                                                 (rotate_nr - 1) % 4,
                                                 tetromino_list):
                        rotate_nr = (rotate_nr - 1) % 4
                        tetromino = tetromino_update(tetromino_x, tetromino_y,
                                                     tetromino_list[
                                                         tetromino_nr],
                                                     rotate_nr)
                        tetromino, tetromino_x = \
                            rotation_check_border(tetromino, tetromino_x,
                                                  tetromino_y,
                                                  tetromino_list[tetromino_nr],
                                                  rotate_nr)
            if ev.key == pygame.K_SPACE:
                grid_tetris, is_freeze, tetromino, tetromino_list[
                    tetromino_nr], tetromino_x, tetromino_y, rotate_nr, \
                    tetromino_nr, is_last_hold = space_used(grid_tetris,
                                                            is_freeze,
                                                            tetromino,
                                                            tetromino_list[
                                                                tetromino_nr],
                                                            tetromino_x,
                                                            tetromino_y,
                                                            rotate_nr,
                                                            tetromino_nr,
                                                            tetromino_list,
                                                            is_last_hold)
            if ev.key == pygame.K_RIGHT:
                if horizontal_check_right_border(getting_x(
                        tetromino)) and \
                        horizontal_check_right_grid(getting_x(tetromino),
                                                    getting_y(tetromino),
                                                    grid_tetris):
                    tetromino_x += 1
                    speed_control_player = 0
            if ev.key == pygame.K_LEFT:
                if horizontal_check_left_border(getting_x(
                        tetromino)) and \
                        horizontal_check_left_grid(getting_x(tetromino),
                                                   getting_y(tetromino),
                                                   grid_tetris):
                    tetromino_x -= 1
                    speed_control_player = 0
            if ev.key == pygame.K_c:
                if not is_last_hold:
                    if held_tetromino >= 0:
                        temporary = tetromino_list[tetromino_nr]
                        tetromino_list[tetromino_nr] = tetromino_list[
                            held_tetromino]
                        tetromino_list[held_tetromino] = temporary
                        tetromino_x = \
                            TETROMINO_STARTING_POS[
                                tetromino_list[tetromino_nr]][0]
                        tetromino_y = \
                            TETROMINO_STARTING_POS[
                                tetromino_list[tetromino_nr]][1]
                        rotate_nr = 0
                        tetromino = tetromino_update(tetromino_x, tetromino_y,
                                                     tetromino_list[
                                                         tetromino_nr],
                                                     rotate_nr)
                        is_last_hold = True
                    else:
                        held_tetromino = tetromino_nr
                        tetromino_x, tetromino_y, tetromino_nr, rotate_nr = \
                            new_tetromino(tetromino_list, tetromino_nr)
                        tetromino = tetromino_update(tetromino_x, tetromino_y,
                                                     tetromino_list[
                                                         tetromino_nr],
                                                     rotate_nr)
                        is_last_hold = True


def draw_next():
    """
    function drawing the tetromino that will be next
    """
    global margin_horizontal, tile_size, width, margin_vertical, height
    global tetromino_nr, tetromino_list
    ad_x = 0
    pygame.draw.rect(scr, (255, 255, 255), ((
                                                margin_horizontal + tile_size *
                                                width + margin_horizontal / 5,
                                                margin_vertical + tile_size *
                                                height / 10),
                                            (margin_horizontal * 3 / 5,
                                             margin_horizontal * 3 / 5 * 4)),
                     2)

    for j in range(4):
        if tetromino_list[tetromino_nr + 1 + j] in [2, 6]:
            ad_x = 1
        tempo_tetromino = tetromino_update_next(2 + ad_x, 3 + j * 6,
                                                tetromino_list[
                                                   tetromino_nr + 1 + j], 0)
        ad_x = 0
        for c in range(4):
            pygame.draw.rect(scr,
                             TETROMINO_COLOR[
                                 tetromino_list[tetromino_nr + 1 + j]],
                             pygame.Rect(tempo_tetromino[c][0],
                                         tempo_tetromino[c][1],
                                         margin_horizontal * 3 / 5 / 6,
                                         margin_horizontal * 3 / 5 / 6))


def values_reset():
    """
    function resetting all the values to starting values
    """
    global tetromino_x, tetromino_y, tetromino_nr, tetromino_list, grid_tetris
    global speed_control, dx_r, dx_l, tetromino_falling_speed, gm_nr, is_freeze
    global is_last_hold, held_tetromino, speed_control_player, lines_cleared, \
        level, points
    tetromino_x = -10
    tetromino_y = -10
    tetromino_nr = 0
    tetromino_list = generate_tetromino_list()
    grid_tetris = [[0] * height for _ in range(width)]
    speed_control = 1
    dx_r = 0
    dx_l = 0
    tetromino_falling_speed = 50
    gm_nr = 0
    is_freeze = False
    is_last_hold = False
    held_tetromino = -5
    speed_control_player = 0
    lines_cleared = 0
    level = 1
    points = 0


def changing_button_color(button, mouse_pos, color):
    """
    function that changes the number of a button if you hover
    the mouse over it
    """
    if button.collidepoint(mouse_pos):
        color = (51, 51, 255)
    return color


def menu_buttons(screen, buttons, texts, msg_boxs, colors):
    """
    function drawing buttons in the menu
    """
    screen.fill((204, 229, 255))
    pygame.draw.rect(screen, colors[0], buttons[0])
    pygame.draw.rect(screen, colors[1], buttons[1])
    pygame.draw.rect(screen, colors[2], buttons[2])
    pygame.draw.rect(screen, (0, 0, 102), buttons[0], 4)
    pygame.draw.rect(screen, (0, 0, 102), buttons[1], 4)
    pygame.draw.rect(screen, (0, 0, 102), buttons[2], 4)
    screen.blit(texts[0], msg_boxs[0])
    screen.blit(texts[1], msg_boxs[1])
    screen.blit(texts[2], msg_boxs[2])


def drawing_logo(log, log_rect, log_rect_y_start, sin_v, screen):
    """
    funtion drawing logo in the menu also responsible
    for the up and down movement
    """
    screen.blit(log, log_rect)
    log_rect.centery = log_rect_y_start + math.sin(sin_v) * 12
    sin_v = pygame.time.get_ticks() / 185
    return sin_v


def resolution_change():
    """
    function changing sizes of buttons and texts when the resolution changes
    """
    global scr, logo, logo_rect, logo_rect_y_start, start_button, start_text
    global msg_box_start_text, settings_button, instructions_exit_button
    global instructions_button, msg_box_points_text, points_nr_text
    global instructions_exit_text, msg_box_instructions_exit_text, ins_text_1
    global msg_box_ins_text_1, ins_text_2, msg_box_ins_text_2
    global ins_text_3, msg_box_ins_text_3, ins_text_4
    global msg_box_ins_text_4, ins_text_5, msg_box_ins_text_5
    global ins_text_6, msg_box_ins_text_6, points_box, points_text
    global msg_box_points_text, points_nr_text, settings_text
    global msg_box_settings_text, instructions_text
    global msg_box_instructions_text, msg_box_points_nr_text
    global level_text, gm_nr, msg_box_level_text, buttons_list
    global text_list, msg_box_text_list, lost_text, msg_button_lost_text
    global lost_points_text, msg_button_lost_points_text, lost_back_to_menu_text
    global msg_lost_back_to_menu_text, button_1_text, msg_box_button_1_text
    global button_2_text, msg_box_button_2_text, screen_size, win, grid
    global height, width, grid_coordinates_next, grid_coordinates_hold
    global grid_coordinates

    screen_size = (width * tile_size + margin_horizontal * 2,
                   height * tile_size + margin_vertical * 2)
    scr = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    pygame.display.set_caption("DEFINITELY NOT TETRIS")
    win = scr.get_rect()

    grid_coordinates = [[0] * height for _ in range(width)]
    for c in range(width):
        for y in range(height):
            grid_coordinates[c][y] = (margin_horizontal + tile_size * c,
                                      margin_vertical + tile_size * y)

    grid_coordinates_next = [[0] * 24 for _ in range(6)]
    for c in range(6):
        for y in range(24):
            grid_coordinates_next[c][y] = (
                margin_horizontal + tile_size * width + margin_horizontal /
                5 + margin_horizontal * 3 / 5 / 6 * c,
                margin_vertical + tile_size * height / 10 +
                margin_horizontal * 3 / 5 / 6 * y)

    grid_coordinates_hold = [[0] * 6 for _ in range(6)]
    for c in range(6):
        for y in range(6):
            grid_coordinates_hold[c][y] = (
                margin_horizontal / 5 + margin_horizontal * 3 / 5 / 6 * c,
                margin_vertical + tile_size * height / 10 +
                margin_horizontal * 3 / 5 / 6 * y)

    grid = [[0] * (height - 4) for _ in range(width)]
    for c in range(width):
        for y in range(height - 4):
            grid[c][y] = pygame.Rect(grid_coordinates[c][y][0],
                                     grid_coordinates[c][y][1] + 4 * tile_size,
                                     tile_size, tile_size)

    logo = pygame.image.load("tetris_logo.png")
    logo = pygame.transform.scale(logo, (600, 200))
    logo_rect = logo.get_rect()
    logo_rect.center = (
        pygame.Surface.get_width(scr) / 2, pygame.Surface.get_height(scr) / 6)
    logo_rect_y_start = logo_rect.centery

    start_button = pygame.Rect(0, 0, 300, 80)
    start_button.center = (
        pygame.Surface.get_width(scr) / 2,
        pygame.Surface.get_height(scr) / 8 * 3)
    start_text = button_font.render("START", True, (0, 0, 102))
    msg_box_start_text = start_text.get_rect()
    msg_box_start_text.center = start_button.center

    settings_button = pygame.Rect(0, 0, 300, 80)
    settings_button.center = (pygame.Surface.get_width(scr) / 2,
                              pygame.Surface.get_height(scr) / 8 * 4.5)
    settings_text = button_font.render("SETTINGS", True, (0, 0, 102))
    msg_box_settings_text = settings_text.get_rect()
    msg_box_settings_text.center = settings_button.center

    instructions_button = pygame.Rect(0, 0, 300, 80)
    instructions_button.center = (pygame.Surface.get_width(scr) / 2,
                                  pygame.Surface.get_height(scr) / 8 * 6)
    instructions_text = button_font.render("INSTRUCTIONS", True, (0, 0, 102))
    msg_box_instructions_text = instructions_text.get_rect()
    msg_box_instructions_text.center = instructions_button.center

    instructions_exit_button = pygame.Rect(0, 0, 300, 80)
    instructions_exit_button.center = (pygame.Surface.get_width(scr) / 2,
                                       pygame.Surface.get_height(scr) / 8 * 6)
    instructions_exit_text = button_font.render("EXIT", True, (0, 0, 102))
    msg_box_instructions_exit_text = instructions_exit_text.get_rect()
    msg_box_instructions_exit_text.center = instructions_exit_button.center

    ins_text_1 = instruction_font.render(
        "YOUR GOAL IS TO CLEAR AS MANY LINES AS POSSIBLE", True, (0, 0, 102))
    msg_box_ins_text_1 = ins_text_1.get_rect()
    msg_box_ins_text_1.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 1)
    ins_text_2 = instruction_font.render(
        "Z / KEY UP BUTTON - ROTATE", True, (0, 0, 102))
    msg_box_ins_text_2 = ins_text_2.get_rect()
    msg_box_ins_text_2.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 2.5)
    ins_text_3 = instruction_font.render(
        "LEFT / RIGHT KEY BUTTON - MOVE THE TETROMINO", True, (0, 0, 102))
    msg_box_ins_text_3 = ins_text_3.get_rect()
    msg_box_ins_text_3.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 3)
    ins_text_4 = instruction_font.render(
        "KEY DOWN BUTTON - SOFT DROP", True, (0, 0, 102))
    msg_box_ins_text_4 = ins_text_4.get_rect()
    msg_box_ins_text_4.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 3.5)
    ins_text_5 = instruction_font.render(
        "SPACE BAR - HARD DROP", True, (0, 0, 102))
    msg_box_ins_text_5 = ins_text_5.get_rect()
    msg_box_ins_text_5.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 4)
    ins_text_6 = instruction_font.render(
        "C BUTTON - HOLD", True, (0, 0, 102))
    msg_box_ins_text_6 = ins_text_6.get_rect()
    msg_box_ins_text_6.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 4.5)

    points_box = pygame.Rect(int(margin_horizontal / 5),
                             int(margin_vertical + tile_size *
                                 height / 10 * 4),
                             int(margin_horizontal * 3 / 5),
                             int(margin_horizontal * 3 / 5))

    points_text = instruction_font.render(
        "POINTS:", True, (255, 255, 255))
    msg_box_points_text = points_text.get_rect()
    msg_box_points_text.center = (margin_horizontal / 2, win.centery)

    points_nr_text = instruction_font.render(
        str(points), True,
        (255, 255, 255))
    msg_box_points_nr_text = points_nr_text.get_rect()
    msg_box_points_nr_text.center = (
        margin_horizontal / 2, win.centery * 11 / 10)

    level_text = instruction_font.render("LEVEL: " + str(gm_nr + 1), True,
                                         (255, 255, 255))
    msg_box_level_text = level_text.get_rect()
    msg_box_level_text.center = (margin_horizontal / 2, win.centery * 3 / 2)

    buttons_list = [start_button, settings_button, instructions_button]
    text_list = [start_text, settings_text, instructions_text]
    msg_box_text_list = [msg_box_start_text, msg_box_settings_text,
                         msg_box_instructions_text]

    lost_text = lost_font.render("YOU LOST!", True, (255, 255, 255))
    msg_button_lost_text = lost_text.get_rect()
    msg_button_lost_text.center = (win.centerx, win.centery * 4 / 5)

    lost_points_text = lost_font.render("POINTS: " + str(points), True,
                                        (255, 255, 255))
    msg_button_lost_points_text = lost_points_text.get_rect()
    msg_button_lost_points_text.center = (win.centerx, win.centery * 6 / 5)

    lost_back_to_menu_text = back_to_menu_font.render(
        "PRESS SPACE TO GO BACK TO MENU", True,
        (255, 255, 255))
    msg_lost_back_to_menu_text = lost_back_to_menu_text.get_rect()
    msg_lost_back_to_menu_text.center = (win.centerx, win.centery * 6.7 / 5)

    button_1_text = button_font.render("BIG WINDOW", True, (0, 0, 102))
    msg_box_button_1_text = button_1_text.get_rect()
    msg_box_button_1_text.center = settings_button.center

    button_2_text = button_font.render("SMALL WINDOW", True, (0, 0, 102))
    msg_box_button_2_text = button_2_text.get_rect()
    msg_box_button_2_text.center = start_button.center


def menu(gam_state, set_state, ins_state, buttons, texts, msg_boxs, screen, log,
         log_rect, log_rect_y_start, sin_v):
    """
    function taking care of the menu
    """
    while True:
        mouse_position = pygame.mouse.get_pos()
        color_start = (255, 255, 255)
        color_instruction = (255, 255, 255)
        color_settings = (255, 255, 255)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONUP:
                if buttons[0].collidepoint(mouse_position):
                    men_state = False
                    gam_state = True
                    return men_state, gam_state, set_state, ins_state
                if buttons[1].collidepoint(mouse_position):
                    men_state = False
                    set_state = True
                    return men_state, gam_state, set_state, ins_state
                if buttons[2].collidepoint(mouse_position):
                    men_state = False
                    ins_state = True
                    return men_state, gam_state, set_state, ins_state
        color_start = changing_button_color(buttons[0], mouse_position,
                                            color_start)
        color_settings = changing_button_color(buttons[1], mouse_position,
                                               color_settings)
        color_instruction = changing_button_color(buttons[2], mouse_position,
                                                  color_instruction)
        colors_list = [color_start, color_settings, color_instruction]
        menu_buttons(screen, buttons, texts, msg_boxs, colors_list)
        sin_v = drawing_logo(log, log_rect, log_rect_y_start, sin_v, screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    # starting variable of the main block of each tetromino
    TETROMINO_STARTING_POS = ((4, 2), (4, 2), (5, 2), (4, 2),
                              (5, 2), (4, 2), (5, 2))

    TETROMINO_COLOR = ((255, 255, 0), (254, 0, 0), (3, 185, 23),
                       (2, 214, 255), (171, 36, 205), (0, 0, 186),
                       (237, 158, 4))

    # variables saying how many tiles horizontally and vertically the playing
    # grid has
    width, height = 10, 24

    # the margin from the left/right and from up/down
    margin_horizontal, margin_vertical = 250, 11

    # the size of each tile (every tile is a square,
    # so we need only one variable)
    tile_size = 30

    # screen size based on width, height, tile size and margins
    screen_size = (width * tile_size + margin_horizontal * 2,
                   height * tile_size + margin_vertical * 2)

    # variable holding the color of the grid
    GRID_COLOR = (150, 150, 150)

    # creating an array of coordinates of every square on the grid
    grid_coordinates = [[0] * height for y in range(width)]
    for x in range(width):
        for y in range(height):
            grid_coordinates[x][y] = (margin_horizontal + tile_size * x,
                                      margin_vertical + tile_size * y)

    grid_coordinates_next = [[0] * 24 for y in range(6)]
    for x in range(6):
        for y in range(24):
            grid_coordinates_next[x][y] = (
                margin_horizontal + tile_size * width + margin_horizontal /
                5 + margin_horizontal * 3 / 5 / 6 * x,
                margin_vertical + tile_size * height / 10 +
                margin_horizontal * 3 / 5 / 6 * y)

    grid_coordinates_hold = [[0] * 6 for y in range(6)]
    for x in range(6):
        for y in range(6):
            grid_coordinates_hold[x][y] = (
                margin_horizontal / 5 + margin_horizontal * 3 / 5 / 6 * x,
                margin_vertical + tile_size * height / 10 +
                margin_horizontal * 3 / 5 / 6 * y)

    # arrays holding vectors from the main block of each tetromino of the rest 3
    # tetrominos

    O_ROTATION = (
        ((1, 0), (0, -1), (1, -1)),
        ((1, 0), (0, -1), (1, -1)),
        ((1, 0), (0, -1), (1, -1)),
        ((1, 0), (0, -1), (1, -1)))
    S_ROTATION = (
        ((0, 1), (1, 0), (1, -1)),
        ((-1, 0), (0, 1), (1, 1)),
        ((-1, 0), (-1, 1), (0, -1)),
        ((1, 0), (0, -1), (-1, -1)))
    Z_ROTATION = (
        ((0, 1), (-1, 0), (-1, -1)),
        ((-1, 0), (0, -1), (1, -1)),
        ((1, 0), (0, -1), (1, 1)),
        ((0, 1), (-1, 1), (1, 0)))
    I_ROTATION = (
        ((1, 0), (2, 0), (-1, 0)),
        ((0, 1), (0, 2), (0, -1)),
        ((-1, 0), (-2, 0), (1, 0)),
        ((0, 1), (0, -1), (0, -2)))
    T_ROTATION = (
        ((1, 0), (0, 1), (-1, 0)),
        ((0, 1), (-1, 0), (0, -1)),
        ((-1, 0), (0, -1), (1, 0)),
        ((0, 1), (0, -1), (1, 0)))
    J_ROTATION = (
        ((0, 1), (1, 0), (2, 0)),
        ((0, 2), (0, 1), (-1, 0)),
        ((-2, 0), (-1, 0), (0, -1)),
        ((1, 0), (0, -1), (0, -2)))
    L_ROTATION = (
        ((0, 1), (-2, 0), (-1, 0)),
        ((-1, 0), (0, -1), (0, -2)),
        ((1, 0), (2, 0), (0, -1)),
        ((0, 2), (0, 1), (1, 0)))

    # array holding all the arrays of rotation
    ROTATIONS = (O_ROTATION, S_ROTATION, Z_ROTATION, I_ROTATION,
                 T_ROTATION, J_ROTATION, L_ROTATION)

    FPS = 60

    # array holding the number of points for breaking each number of lines
    POINT_SYSTEM = (100, 300, 500, 800)

    # the number of points you get for back to back tetris
    BACK_TO_BACK_POINTS = 400

    # level the players is on
    level = 1

    # number of lines cleared by player
    lines_cleared = 0

    # number of points of player
    points = 0

    # Declaration of screen
    scr = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    pygame.display.set_caption("DEFINITELY NOT TETRIS")
    win = scr.get_rect()

    """
    creating an array that has all the placed rectangles
    having a block at position x, y
    gris_tetris[x][y] =
    0 - a square is free
    1 - o-block
    2 - s-block
    3 - z-block
    4 - i-block
    5 - t-block
    6 - j-block
    7 - l-block
    """
    grid_tetris = [[0] * height for y in range(width)]

    # creating a two-dimensional array made of rectangles which is later used
    # to draw the grid
    grid = [[0] * (height - 4) for y in range(width)]
    for x in range(width):
        for y in range(height - 4):
            grid[x][y] = pygame.Rect(grid_coordinates[x][y][0],
                                     grid_coordinates[x][y][1] + 4 * tile_size,
                                     tile_size, tile_size)

    tetromino_x = -10
    tetromino_y = -10
    tetromino_nr = 0
    tetromino_list = generate_tetromino_list()

    # variable holding the number of the iteration, all time based events
    # base on it
    speed_control = 1

    # 2 variables holding the left and right vector of the falling tetromino
    dx_r = 0
    dx_l = 0

    # starting position of rotation
    rotate_nr = 0

    # variable holding the players speed
    player_speed = 3

    # variable holding the tetromino falling speed - it depends on level.
    tetromino_falling_speed = 50

    # array holding tetrominos falling speed based on gm
    tetromino_fall_speed_gm = (50, 40, 30, 20, 10, 5, 2, 1)

    # variable holding the game number - level
    gm_nr = 0

    # delay between pressing a button by player and the tetromino starting a
    # smooth movement it enables the player to easily use the tap method,
    # so it is easy to have greater accuracy
    delay_player = 11

    # boolean variable saying if the tetromino is frozen at a specific frame
    is_freeze = False

    # variable saying if the last tetromino was held
    is_last_hold = False

    # variable saying if the last time the lines were broken,
    # whether it was tetris
    last_tetris = False

    # variable holding the number of the held tetromino
    held_tetromino = -5

    # variable used to determine player speed
    speed_control_player = 0

    # all the font declarations
    button_font = pygame.font.SysFont("arial black", 30)
    instruction_font = pygame.font.SysFont("arial black", 25)
    lost_font = pygame.font.SysFont("arial black", 40)
    back_to_menu_font = pygame.font.SysFont("arial black", 15)

    # all the buttons and texts declarations
    logo = pygame.image.load("tetris_logo.png")
    logo = pygame.transform.scale(logo, (600, 200))
    logo_rect = logo.get_rect()
    logo_rect.center = (
        pygame.Surface.get_width(scr) / 2, pygame.Surface.get_height(scr) / 6)
    logo_rect_y_start = logo_rect.centery

    start_button = pygame.Rect(0, 0, 300, 80)
    start_button.center = (
        pygame.Surface.get_width(scr) / 2,
        pygame.Surface.get_height(scr) / 8 * 3)
    start_text = button_font.render("START", True, (0, 0, 102))
    msg_box_start_text = start_text.get_rect()
    msg_box_start_text.center = start_button.center

    settings_button = pygame.Rect(0, 0, 300, 80)
    settings_button.center = (pygame.Surface.get_width(scr) / 2,
                              pygame.Surface.get_height(scr) / 8 * 4.5)
    settings_text = button_font.render("SETTINGS", True, (0, 0, 102))
    msg_box_settings_text = settings_text.get_rect()
    msg_box_settings_text.center = settings_button.center

    instructions_button = pygame.Rect(0, 0, 300, 80)
    instructions_button.center = (pygame.Surface.get_width(scr) / 2,
                                  pygame.Surface.get_height(scr) / 8 * 6)
    instructions_text = button_font.render("INSTRUCTIONS", True, (0, 0, 102))
    msg_box_instructions_text = instructions_text.get_rect()
    msg_box_instructions_text.center = instructions_button.center

    instructions_exit_button = pygame.Rect(0, 0, 300, 80)
    instructions_exit_button.center = (pygame.Surface.get_width(scr) / 2,
                                       pygame.Surface.get_height(scr) / 8 * 6)
    instructions_exit_text = button_font.render("EXIT", True, (0, 0, 102))
    msg_box_instructions_exit_text = instructions_exit_text.get_rect()
    msg_box_instructions_exit_text.center = instructions_exit_button.center

    ins_text_1 = \
        instruction_font.render(
                                "YOUR GOAL IS TO CLEAR AS MANY LINES AS "
                                "POSSIBLE", True, (0, 0, 102))
    msg_box_ins_text_1 = ins_text_1.get_rect()
    msg_box_ins_text_1.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 1)
    ins_text_2 = instruction_font.render(
        "Z / KEY UP BUTTON - ROTATE", True, (0, 0, 102))
    msg_box_ins_text_2 = ins_text_2.get_rect()
    msg_box_ins_text_2.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 2.5)
    ins_text_3 = instruction_font.render(
        "LEFT / RIGHT KEY BUTTON - MOVE THE TETROMINO", True, (0, 0, 102))
    msg_box_ins_text_3 = ins_text_3.get_rect()
    msg_box_ins_text_3.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 3)
    ins_text_4 = instruction_font.render(
        "KEY DOWN BUTTON - SOFT DROP", True, (0, 0, 102))
    msg_box_ins_text_4 = ins_text_4.get_rect()
    msg_box_ins_text_4.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 3.5)
    ins_text_5 = instruction_font.render(
        "SPACE BAR - HARD DROP", True, (0, 0, 102))
    msg_box_ins_text_5 = ins_text_5.get_rect()
    msg_box_ins_text_5.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 4)
    ins_text_6 = instruction_font.render(
        "C BUTTON - HOLD", True, (0, 0, 102))
    msg_box_ins_text_6 = ins_text_6.get_rect()
    msg_box_ins_text_6.center = (pygame.Surface.get_width(scr) / 2,
                                 pygame.Surface.get_height(scr) / 8 * 4.5)

    points_box = pygame.Rect(int(margin_horizontal / 5), int(margin_vertical +
                                                             tile_size *
                                                             height / 10 * 4),
                             int(margin_horizontal * 3 / 5),
                             int(margin_horizontal * 3 / 5))

    points_text = instruction_font.render(
        "POINTS:", True, (255, 255, 255))
    msg_box_points_text = points_text.get_rect()
    msg_box_points_text.center = (margin_horizontal/2, win.centery)

    points_nr_text = instruction_font.render(
        str(points), True,
        (255, 255, 255))
    msg_box_points_nr_text = points_nr_text.get_rect()
    msg_box_points_nr_text.center = (
                                     margin_horizontal / 2,
                                     win.centery * 11/10)

    level_text = instruction_font.render("LEVEL: " + str(gm_nr+1), True,
                                         (255, 255, 255))
    msg_box_level_text = level_text.get_rect()
    msg_box_level_text.center = (margin_horizontal/2, win.centery*3/2)

    buttons_list = [start_button, settings_button, instructions_button]
    text_list = [start_text, settings_text, instructions_text]
    msg_box_text_list = [msg_box_start_text, msg_box_settings_text,
                         msg_box_instructions_text]

    lost_text = lost_font.render("YOU LOST!", True, (255, 255, 255))
    msg_button_lost_text = lost_text.get_rect()
    msg_button_lost_text.center = (win.centerx, win.centery*4/5)

    lost_points_text = lost_font.render("POINTS: " + str(points), True, (255,
                                                                         255,
                                                                         255))
    msg_button_lost_points_text = lost_points_text.get_rect()
    msg_button_lost_points_text.center = (win.centerx, win.centery * 6 / 5)

    lost_back_to_menu_text = back_to_menu_font.render("PRESS SPACE "
                                                      "TO GO BACK TO MENU",
                                                      True,
                                                      (255, 255, 255))
    msg_lost_back_to_menu_text = lost_back_to_menu_text.get_rect()
    msg_lost_back_to_menu_text.center = (win.centerx, win.centery * 6.7 / 5)

    button_1_text = button_font.render("BIG WINDOW", True, (0, 0, 102))
    msg_box_button_1_text = button_1_text.get_rect()
    msg_box_button_1_text.center = settings_button.center

    button_2_text = button_font.render("SMALL WINDOW", True, (0, 0, 102))
    msg_box_button_2_text = button_2_text.get_rect()
    msg_box_button_2_text.center = start_button.center

    menu_state = True
    game_state = False
    instructions_state = False
    settings_menu_state = False

    value_sin = 0

    fps = pygame.time.Clock()
    keys = pygame.key.get_pressed()
    while True:
        while menu_state:
            menu_state, game_state, settings_menu_state, instructions_state = \
                menu(game_state, settings_menu_state, instructions_state,
                     buttons_list, text_list, msg_box_text_list, scr, logo,
                     logo_rect, logo_rect_y_start, value_sin)
        while instructions_state:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if instructions_exit_button.collidepoint(pos):
                        instructions_state = False
                        menu_state = True
            instructions_exit_color = (255, 255, 255)
            instructions_exit_color = \
                changing_button_color(instructions_button,
                                      pos,
                                      instructions_exit_color)
            scr.fill((204, 229, 255))
            pygame.draw.rect(scr, instructions_exit_color,
                             instructions_exit_button)
            pygame.draw.rect(scr, (0, 0, 102), instructions_exit_button, 4)
            scr.blit(instructions_exit_text, msg_box_instructions_exit_text)
            scr.blit(ins_text_1, msg_box_ins_text_1)
            scr.blit(ins_text_2, msg_box_ins_text_2)
            scr.blit(ins_text_3, msg_box_ins_text_3)
            scr.blit(ins_text_4, msg_box_ins_text_4)
            scr.blit(ins_text_5, msg_box_ins_text_5)
            scr.blit(ins_text_6, msg_box_ins_text_6)
            pygame.display.flip()
        while settings_menu_state:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if start_button.collidepoint(pos):
                        margin_horizontal, margin_vertical = 250, 11
                        tile_size = 30
                        resolution_change()
                    if settings_button.collidepoint(pos):
                        margin_horizontal, margin_vertical = 350, 11
                        tile_size = 40
                        resolution_change()
                    if instructions_exit_button.collidepoint(pos):
                        settings_menu_state = False
                        menu_state = True
            instructions_exit_color = (255, 255, 255)
            button_1_color = (255, 255, 255)
            button_1_color = changing_button_color(settings_button, pos,
                                                   button_1_color)
            instructions_exit_color = \
                changing_button_color(instructions_button,
                                      pos,
                                      instructions_exit_color)
            button_2_color = (255, 255, 255)
            button_2_color = changing_button_color(start_button, pos,
                                                   button_2_color)
            instructions_exit_color = \
                changing_button_color(instructions_button,
                                      pos,
                                      instructions_exit_color)
            scr.fill((204, 229, 255))
            pygame.draw.rect(scr, instructions_exit_color,
                             instructions_exit_button)
            pygame.draw.rect(scr, (0, 0, 102), instructions_exit_button, 4)
            pygame.draw.rect(scr, button_1_color, settings_button)
            pygame.draw.rect(scr, (0, 0, 102), settings_button, 4)
            pygame.draw.rect(scr, button_2_color, start_button)
            pygame.draw.rect(scr, (0, 0, 102), start_button, 4)
            scr.blit(instructions_exit_text, msg_box_instructions_exit_text)
            scr.blit(button_1_text, msg_box_button_1_text)
            scr.blit(button_2_text, msg_box_button_2_text)
            pygame.display.flip()
        while game_state:
            if game_end_check(grid_tetris):
                while game_state:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                menu_state = True
                                game_state = False
                                values_reset()
                    end_button = pygame.Rect(0, 0,
                                             pygame.Surface.get_width(scr) / 2,
                                             pygame.Surface.get_height(scr) / 2)
                    end_button.center = (pygame.Surface.get_width(scr) / 2,
                                         pygame.Surface.get_height(scr) / 2)
                    pygame.draw.rect(scr, (204, 0, 0), end_button)
                    pygame.draw.rect(scr, (102, 0, 0), end_button, 10)
                    lost_points_text = lost_font.render(
                        "POINTS: " + str(points), True, (255, 255, 255))
                    msg_button_lost_points_text = lost_points_text.get_rect()
                    msg_button_lost_points_text.center = (
                                                          win.centerx,
                                                          win.centery * 6 / 5)
                    scr.blit(lost_points_text, msg_button_lost_points_text)
                    scr.blit(lost_text, msg_button_lost_text)
                    scr.blit(lost_back_to_menu_text, msg_lost_back_to_menu_text)
                    pygame.display.flip()
                    fps.tick(FPS)

            if tetromino_x == -10 and tetromino_y == -10:
                tetromino_x, tetromino_y, tetromino_nr, rotate_nr = \
                    new_tetromino(tetromino_list, tetromino_nr)
            tetromino = tetromino_update(tetromino_x, tetromino_y,
                                         tetromino_list[tetromino_nr],
                                         rotate_nr)
            keys = pygame.key.get_pressed()
            scr.fill(pygame.Color("black"))
            speed_control += 1
            if speed_control % tetromino_falling_speed == 0:
                grid_tetris, is_freeze, is_last_hold = game_freeze_control(
                    tetromino,
                    tetromino_list[
                        tetromino_nr],
                    grid_tetris, is_last_hold)
                tetromino_y += 1
                speed_control = 0
                if is_freeze:
                    tetromino_x, tetromino_y, tetromino_nr, rotate_nr = \
                        new_tetromino(tetromino_list, tetromino_nr)
                    if_freeze = False
            event_handler()

            tetromino = tetromino_update(tetromino_x, tetromino_y,
                                         tetromino_list[tetromino_nr],
                                         rotate_nr)

            if speed_control_player > delay_player:
                if speed_control_player % player_speed == 0:
                    if dx_r != dx_l:
                        if horizontal_check_left_border(getting_x(
                                tetromino)) and horizontal_check_left_grid(
                            getting_x(tetromino), getting_y(tetromino),
                                grid_tetris):
                            tetromino_x -= dx_l
                        if horizontal_check_right_border(getting_x(
                                tetromino)) and horizontal_check_right_grid(
                            getting_x(tetromino), getting_y(tetromino),
                                grid_tetris):
                            tetromino_x += dx_r

            tetromino = tetromino_update(tetromino_x, tetromino_y,
                                         tetromino_list[tetromino_nr],
                                         rotate_nr)

            dx_r, dx_l, tetromino_falling_speed = \
                movement_holding(keys, dx_r, dx_l, tetromino_falling_speed)

            tetromino = tetromino_update(tetromino_x, tetromino_y,
                                         tetromino_list[tetromino_nr],
                                         rotate_nr)

            grid_tetris, lines_cleared, points, last_tetris, \
                tetromino_falling_speed = line_handler(grid_tetris,
                                                       lines_cleared,
                                                       points,
                                                       POINT_SYSTEM,
                                                       BACK_TO_BACK_POINTS,
                                                       last_tetris, gm_nr,
                                                       tetromino_falling_speed,
                                                       tetromino_fall_speed_gm)
            gm_nr = lines_cleared // 8

            if not game_end_check(grid_tetris):
                for i in range(4):
                    pygame.draw.rect(scr, TETROMINO_COLOR[
                        tetromino_list[tetromino_nr]],
                                     pygame.Rect(tetromino[i][0],
                                                 tetromino[i][1],
                                                 tile_size, tile_size))

            drawing_grid(grid_tetris)

            # Drawing Grid
            for x in range(width):
                for y in range(height - 4):
                    pygame.draw.rect(scr, GRID_COLOR, grid[x][y], 1)

            draw_next()

            pygame.draw.rect(scr, (255, 255, 255), (
                int(margin_horizontal / 5), int(margin_vertical + tile_size *
                                                height / 10),
                int(margin_horizontal * 3 / 5),
                int(margin_horizontal * 3 / 5)), 2)

            if held_tetromino > 0:
                add_x = 0
                if tetromino_list[held_tetromino] in [2, 6]:
                    add_x = 1
                temp_tetromino = tetromino_update_hold(2 + add_x, 2,
                                                       tetromino_list[
                                                           held_tetromino], 0)
                for a in range(4):
                    pygame.draw.rect(scr, TETROMINO_COLOR[
                        tetromino_list[held_tetromino]],
                                     pygame.Rect(temp_tetromino[a][0],
                                                 temp_tetromino[a][1],
                                                 margin_horizontal * 3 / 5 / 6,
                                                 margin_horizontal * 3 / 5 / 6))
            points_nr_text = instruction_font.render(
                                                     str(points), True,
                                                     (255, 255, 255))
            msg_box_points_nr_text = points_nr_text.get_rect()
            msg_box_points_nr_text.center = (
                margin_horizontal / 2, win.centery * 11 / 10)
            level_text = instruction_font.render("LEVEL: " + str(gm_nr + 1),
                                                 True, (255, 255, 255))
            msg_box_level_text = level_text.get_rect()
            msg_box_level_text.center = (
                                         margin_horizontal / 2,
                                         win.centery * 3 / 2)
            scr.blit(level_text, msg_box_level_text)
            scr.blit(points_text, msg_box_points_text)
            scr.blit(points_nr_text, msg_box_points_nr_text)
            speed_control_player += 1
            pygame.display.flip()
            fps.tick(FPS)

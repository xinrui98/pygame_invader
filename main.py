import sys
import pygame
import random
import images


pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (0, 0, 0)
player_size = 50
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

score = 0

SPEED = 0

number_of_enemies = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)


def set_level_speed_enemynum(score, SPEED, number_of_enemies):
    SPEED = score/3 + 10
    if score <10:
        number_of_enemies =5
    elif score<20:
        number_of_enemies = 15
    else:
        number_of_enemies = 30

    speed_and_enemy_number = [SPEED, number_of_enemies]

    return speed_and_enemy_number


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < (set_level_speed_enemynum(score, SPEED, number_of_enemies))[1] and delay < 0.3:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        # pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

        enemy = pygame.image.load("images/shark_png.png")
        enemy = pygame.transform.scale(enemy, (enemy_size, enemy_size))
        screen.blit(enemy, (enemy_pos[0], enemy_pos[1]))


def update_enemy_position(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score+=1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    # check for overlap
    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False


game_over = False

while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                if player_pos[0] <= 0:
                    pass
                else:
                    x -= player_size

            elif event.key == pygame.K_RIGHT:
                if player_pos[0] >= (WIDTH - player_size):
                    pass
                else:
                    x += player_size

            player_pos = [x, y]

    screen.fill(BACKGROUND_COLOR)

    if detect_collision(player_pos, enemy_pos):
        game_over = True
        break

    drop_enemies(enemy_list)
    score = update_enemy_position(enemy_list, score)
    SPEED = (set_level_speed_enemynum(score, SPEED, number_of_enemies))[0]


    text = "Score : " + str(score)
    label = myFont.render(text,1,YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))

    if collision_check(enemy_list, player_pos):
        game_over = True

    draw_enemies(enemy_list)
    turtle = pygame.image.load("images/cute_turtle.png")
    turtle = pygame.transform.scale(turtle, (player_size,player_size))
    screen.blit(turtle,(player_pos[0], player_pos[1]))

    # pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    pygame.display.update()

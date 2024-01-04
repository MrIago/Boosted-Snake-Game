import pygame
import time
import random

pygame.init()

# Cores e configurações iniciais
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 102)
black = (0, 0, 0)
dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

snake_block = 10
initial_speed = 15
boost_duration = 10  # Duração do boost em segundos

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_text(message, color, x, y):
    mesg = font_style.render(message, True, color)
    dis.blit(mesg, [x, y])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0       
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    speed = initial_speed
    apples_eaten = 0
    boost_available = False
    boost_active = False
    boost_end_time = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            display_text("You Lost! Press Q-Quit or C-Play Again", red, dis_width / 6, dis_height / 3)
            display_text("Your Score: " + str(length_of_snake - 1), yellow, 0, 0)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_SPACE and boost_available and not boost_active:
                    boost_active = True
                    boost_available = False
                    boost_end_time = time.time() + boost_duration
                    speed /= 2  # Reduzir a velocidade em 50%

        if boost_active and time.time() > boost_end_time:
            boost_active = False
            speed = initial_speed + 0.01 * initial_speed * apples_eaten  # Restaurar a velocidade anterior

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

        display_text("Speed: " + str(round(speed, 2)), yellow, 0, 20)
        display_text("Boost: " + ("Available" if boost_available else "Not Available"), red if boost_available else white, 0, 40)
        if boost_active:
            remaining_time = round(boost_end_time - time.time(), 1)
            display_text("Boost Active! Time remaining: " + str(remaining_time), green, 0, 60)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            apples_eaten += 1
            if not boost_active:
                speed += 0.25 * initial_speed
            if apples_eaten % 3 == 0 and not boost_active:
                boost_available = True

        clock.tick(speed)

    pygame.quit()
    quit()

gameLoop()

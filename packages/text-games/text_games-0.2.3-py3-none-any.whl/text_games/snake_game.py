import pygame
import random

def run_snake_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    SNAKE_BLOCK = 10
    SNAKE_SPEED = 15

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)

    def show_score(score):
        value = score_font.render(f"Your Score: {score}", True, (0, 255, 0))
        screen.blit(value, [10, 10])

    def draw_snake(snake_list):
        for x in snake_list:
            pygame.draw.rect(screen, (0, 0, 255), [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])

    def game_loop():
        game_over = False
        game_close = False

        x1, y1 = WIDTH / 2, HEIGHT / 2
        x1_change, y1_change = 0, 0

        snake_list = []
        length_of_snake = 1

        foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

        while not game_over:
            while game_close:
                screen.fill((0, 0, 0))
                msg = font.render("You Lost! Press Q to Quit or C to Play Again", True, (255, 0, 0))
                screen.blit(msg, [WIDTH / 6, HEIGHT / 3])
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            game_loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change, y1_change = -SNAKE_BLOCK, 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change, y1_change = SNAKE_BLOCK, 0
                    elif event.key == pygame.K_UP:
                        x1_change, y1_change = 0, -SNAKE_BLOCK
                    elif event.key == pygame.K_DOWN:
                        x1_change, y1_change = 0, SNAKE_BLOCK

            if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (0, 255, 0), [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for block in snake_list[:-1]:
                if block == snake_head:
                    game_close = True

            draw_snake(snake_list)
            show_score(length_of_snake - 1)
            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                length_of_snake += 1

            clock.tick(SNAKE_SPEED)

    game_loop()
    pygame.quit()

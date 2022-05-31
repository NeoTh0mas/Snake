import pygame
import random

# game initialization
pygame.init()

# variables
game_end = False
width = 640
height = 480
snake_speed = 10
snake_size = (10, 10)
fps = 20
random_n = 0
apple_size = (10, 10)
score = 0
check = random.randint(1, 5)
raibow_head = False
snake_tail = []

# creating display and run update
display = pygame.display.set_mode((width, height))

pygame.display.update()
pygame.display.set_caption("Snake")


def label(score):
    if not game_end:
        font = pygame.font.Font(None, 30)
        scoretext = font.render(str(score), 1, (255, 255, 255))
        display.blit(scoretext, (0, 0))
    elif game_end is True:
        font = pygame.font.Font(None, 60)
        gameovertext = font.render("Game Over!", 1, (255, 0, 0))
        font = pygame.font.Font(None, 30)
        scoretext = font.render(str(score), 1, (255, 255, 255))
        display.blit(gameovertext, (width / 2 - 126, height / 2 - 45))
        display.blit(scoretext, (0, 0))


colors = {
    "snake_head": (0, 255, 0),
    "snake_tail": (0, 150, 0),
    "apple": (255, 0, 0)
}

snake_pos = {
    "x": width / 2 - 10,
    "y": height / 2 - 10,
    "x_change": 0,
    "y_change": 0
}

# apple
apple_pos = {
    'x': round(random.randint(0, width - snake_size[0]) / 10) * 10,
    'y': round(random.randint(0, height - snake_size[1]) / 10) * 10
}

clock = pygame.time.Clock()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT and snake_pos["x_change"] == 0:
                snake_pos["x_change"] = -snake_speed
                snake_pos["y_change"] = 0

            elif event.key == pygame.K_RIGHT and snake_pos["x_change"] == 0:
                snake_pos["x_change"] = snake_speed
                snake_pos["y_change"] = 0

            elif event.key == pygame.K_DOWN and snake_pos["y_change"] == 0:
                snake_pos["x_change"] = 0
                snake_pos["y_change"] = snake_speed

            elif event.key == pygame.K_UP and snake_pos["y_change"] == 0:
                snake_pos["x_change"] = 0
                snake_pos["y_change"] = -snake_speed

    display.fill((0, 0, 0))

    # tail moving
    ltx = snake_pos["x"]
    lty = snake_pos["y"]

    for i, v in enumerate(snake_tail):
        _ltx = snake_tail[i][0]
        _lty = snake_tail[i][1]

        snake_tail[i][0] = ltx
        snake_tail[i][1] = lty

        ltx = _ltx
        lty = _lty

    # drawing tail
    for j in snake_tail:
        pygame.draw.rect(display, colors["snake_tail"], [
            j[0],
            j[1],
            snake_size[0],
            snake_size[1]])

    # changing possition of the snake
    if game_end:
        snake_pos["x"] = snake_pos["x"]
        snake_pos["y"] = snake_pos["y"]
    else:
        snake_pos["x"] += snake_pos["x_change"]
        snake_pos["y"] += snake_pos["y_change"]

    # teleport
    if snake_pos["x"] < -snake_size[0]:
        snake_pos["x"] = width

    if snake_pos["x"] > width:
        snake_pos['x'] = 0

    elif snake_pos['y'] < -snake_size[1]:
        snake_pos['y'] = height

    elif snake_pos['y'] > height:
        snake_pos['y'] = 0

    # drawing the head 
    pygame.draw.rect(display, colors["snake_head"], [
        snake_pos["x"],
        snake_pos["y"],
        snake_size[0],
        snake_size[1]])

    # drawing the apple
    pygame.draw.rect(display, colors["apple"], [
        apple_pos["x"],
        apple_pos["y"],
        apple_size[0],
        apple_size[1]])

    # collision with the apple
    if snake_pos["x"] == apple_pos["x"] and snake_pos["y"] == apple_pos["y"]:
        snake_tail.append([apple_pos["x"], apple_pos["y"]])
        apple_pos["x"] = round(random.randint(0, width - snake_size[0]) / 10) * 10
        apple_pos["y"] = round(random.randint(0, height - snake_size[1]) / 10) * 10
        ufps = fps

        if random_n == check:
            score += 5
            raibow_head = True
            if fps < 30:
                ufps = fps - 10
            elif 30 < fps < 60:
                ufps = fps - 20
            elif 60 < fps < 100:
                ufps = fps - 30
            else:
                ufps = fps - 40
        else:
            score += 1
            raibow_head = False

        random_n = random.randint(1, 5)

        fps += 1

    # random color of apple
    if random_n == check:
        colors["apple"] = (random.choice([0, 255]), random.choice([0, 255]), random.choice([0, 255]))
    else:
        colors["apple"] = (255, 0, 0)

    # random color of head
    if raibow_head:
        colors["snake_head"] = (random.choice([0, 255]), random.choice([0, 255]), random.choice([0, 255]))
    else:
        colors["snake_head"] = (0, 255, 0)

    # detect collision with tail
    for i, v in enumerate(snake_tail):
        if snake_pos["x"] + snake_pos["x_change"] == snake_tail[i][0] and snake_pos["y"] + snake_pos["y_change"] == \
                snake_tail[i][1]:
            game_end = True
            snake_speed = 0

    # displaying score
    label(score)

    pygame.display.update()

    # FPS
    if raibow_head:
        clock.tick(ufps)
    else:
        clock.tick(fps)

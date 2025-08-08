import pygame as pg
from random import randrange

window= 600
tile_size= 25
RANGE= (tile_size // 2, window - tile_size // 2, tile_size)
get_random_pos= lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0,0,tile_size-2,tile_size-2])
snake.center = get_random_pos()
length =1
segments = [snake.copy()]
snake_dir = (0,0)
time= 0
time_step=200
food = snake.copy()
food.center = get_random_pos()
screen= pg.display.set_mode([window]*2)
clock=pg.time.Clock()

pg.font.init()
font = pg.font.SysFont(None, 36)
score = 0
with open("hiscore.txt") as f :
        hiScore = f.read()
        if (hiScore != ""):
            hiScore = int(hiScore)
        else:
            hiScore = 0
        

dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key ==pg.K_w:
                snake_dir = (0, -tile_size)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key ==pg.K_s:
                snake_dir = (0, tile_size)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key ==pg.K_a:
                snake_dir = (-tile_size, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key ==pg.K_d:
                snake_dir = (tile_size, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    screen.fill('black')
    # Check borders and Self Eating
    self_eating =pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left<0 or snake.right>window or snake.top<0 or snake.bottom>window or self_eating:
        snake.center=get_random_pos()
        food.center= get_random_pos()
        length=1
        if (score>hiScore):
            with open("hiscore.txt","w") as f:
                f.write(str((score)))
            with open("hiscore.txt") as f :
                hiScore = f.read()
                if (hiScore != ""):
                    hiScore = int(hiScore)
                else:
                    hiScore = 0
        score = 0
        snake_dir =(0,0)
        segments=[snake.copy()]
    # Check Food
    if snake.center == food.center:
        food.center=get_random_pos()
        length += 1
        score += 1
    # Draw Food 
    pg.draw.rect(screen, 'red', food)
    # Draw Snake
    [pg.draw.rect(screen, 'green', segment) for segment in segments]

     # Draw Score (always every frame)
    score_text = font.render(f"Score: {score}", True, pg.Color('white'))
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {hiScore}", True, pg.Color('white'))
    screen.blit(high_score_text, (window - high_score_text.get_width() - 10, 10))
    # Move Snake
    time_now =pg.time.get_ticks()
    if time_now - time > time_step:
        time=time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments=segments [-length:]
    pg.display.flip()
    clock.tick(60)
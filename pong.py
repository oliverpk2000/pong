import pygame, sys, random, json

def ball_movement():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, base_speed, speed_increase
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1
        base_speed += speed_increase

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1
        base_speed += speed_increase

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - player.right):
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1

def player_movement():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_movement():
    opponent.y += opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_reset():
    global ball_speed_x, ball_speed_y, score_time, base_speed

    ball.center = (screen_width/2, screen_height/2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, score_color)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))

    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, score_color)
        screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))

    if 1400 < current_time - score_time < 2100:
            number_one = game_font.render("1", False, score_color)
            screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0

    else:
        ball_speed_y = base_speed * random.choice((1, -1))
        ball_speed_x = base_speed * random.choice((1, -1))
        score_time = None

#getting config for setup
with open("config.json", "r") as json_file:
    config = json.load(json_file)
json_file.close()

#setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(config.get("setup").get("caption"))
icon = pygame.image.load(config.get("setup").get("icon"))
pygame.display.set_icon(icon)

#objects
ball = pygame.Rect(screen_width/2 -15, screen_height/2 -15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 -70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 -70, 10, 140)

#colors
bg_color = pygame.Color(tuple(config.get("colors").get("bg_color")))
score_color = (tuple(config.get("colors").get("score_color")))
obj_color = (tuple(config.get("colors").get("obj_color")))  

#variables
base_speed = config.get("ball").get("base_speed")
speed_increase = config.get("ball").get("speed_increase")
ball_speed_x = base_speed * random.choice((1, -1))
ball_speed_y = base_speed * random.choice((1, -1))
player_speed = 0
opponent_speed = 0
player_max_speed = config.get("player").get("speed")
opponent_max_speed = config.get("opponent").get("speed")

#text
player_score = config.get("player").get("starting_score")
opponent_score = config.get("opponent").get("starting_score")
game_font = pygame.font.Font("freesansbold.ttf", 32)

#timer
score_time = True

#sound
pong_sound = pygame.mixer.Sound(config.get("sounds").get("pong_sound"))
score_sound = pygame.mixer.Sound(config.get("sounds").get("score_sound"))

#main loop
while True:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += player_max_speed
            if event.key == pygame.K_UP:
                player_speed -= player_max_speed
            if event.key == pygame.K_s:
                opponent_speed += opponent_max_speed
            if event.key == pygame.K_w:
                opponent_speed -= opponent_max_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= player_max_speed
            if event.key == pygame.K_UP:
                player_speed += player_max_speed
            if event.key == pygame.K_s:
                opponent_speed -= opponent_max_speed
            if event.key == pygame.K_w:
                opponent_speed += opponent_max_speed

    ball_movement()
    player_movement()
    opponent_movement()

    #visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, obj_color, player)
    pygame.draw.rect(screen, obj_color, opponent)
    pygame.draw.ellipse(screen, obj_color, ball)
    pygame.draw.aaline(screen, obj_color, (screen_width/2, 0), (screen_width/2, screen_height))

    if score_time:
        ball_reset()

    player_text = game_font.render(f"{player_score}", False, score_color)
    screen.blit(player_text, (660, 470))
    opponent_text = game_font.render(f"{opponent_score}", False, score_color)
    screen.blit(opponent_text, (600, 470))

    #update window
    pygame.display.flip()
    clock.tick(60)
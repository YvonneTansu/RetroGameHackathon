import pygame, sys, random
from pygame.locals import *
from PIL import Image

image = Image.open('assets/food.png')
new_image = image.resize((20, 20))
new_image.save('assets/food_20.png')

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,450))
    screen.blit(floor_surface, (floor_x_pos+288,450))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos-150))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def create_bonus(pipes):
    random_bonus_pos = random.choice(bonus_height)
    bonus = bonus_surface.get_rect(midtop = (350,random_bonus_pos))
    for pipe in pipes:
        while bonus.colliderect(pipe):
            random_bonus_pos = random.choice(bonus_height)
            bonus = bonus_surface.get_rect(midtop = (350,random_bonus_pos))
        return bonus
    
    return bonus

def move_bonuses(bonuses):
    for bonus in bonuses:
        bonus.centerx -= 2.5
    return bonuses

def draw_bonuses(bonuses):
    for bonus in bonuses:
        screen.blit(bonus_surface, bonus)

def check_food(bonuses):
    global score
    for bonus in bonuses:
        if bonus.top <= bird_rect.y <= bonus.bottom and bonus.x == 50:
            score_sound.play()
            score += 1
            return True
    return False

def check_collison(pipes):
    global score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
        if pipe.x == bird_rect.x:
            score_sound.play()
            score += 1
            break
            return True
            
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        death_sound.play()
        return False
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 6,1)
    return new_bird
    
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird,new_bird_rect
    
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255)) # antialias text looks sharper
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255)) # antialias text looks sharper
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
        
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255)) # antialias text looks sharper
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 40000, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((288,512),pygame.RESIZABLE) # width and height of screen
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 20)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
scored = False

bg_surface = pygame.image.load("assets/background-day.png").convert()
#bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("assets/base.png").convert()
#floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

#bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center = (50,256))
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
#pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

bonus_surface = pygame.image.load("assets/food_20.png").convert_alpha()
bonus_list = []

# Using timer to spawn pipe
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200) # length of trigger (1200ms): How time time we want to pass since it is going to be triggered
pipe_height = [200,300,400]

SPAWNBONUS = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNBONUS,1000) # length of trigger (1000ms): How time time we want to pass since it is going to be triggered
bonus_height = [150,200,250,300,350,400]

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

bet = True
bet_score = 0
bet_amount = 0
bet_amount_y = False
bet_score_y = False
betting = False
# win = False
    
while True:
    # Look for all the events happening like moving mouse, closing window or time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Check if any of the keys on the keyboard is pressed down
        if event.type == pygame.KEYDOWN: 
            # Check for specific key
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bonus_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0
            if event.key == pygame.K_DOWN and game_active == False:
                bet = False
            if event.key == pygame.K_UP and game_active == False:
                if bet_amount_y:
                    if bet_amount > bet_score/5:
                        bet_amount = 0
                    else:
                        bet_amount_y = False
                        betting = True
                if bet_score_y:
                    bet_score_y = False
                    bet_amount_y = True
                if bet:
                    bet_score_y = True
                    bet = False
            if event.key == pygame.K_LEFT and game_active == False:
                if bet_score_y:
                    bet_score -= 1
                if bet_amount_y:
                    bet_amount -= 1
            if event.key == pygame.K_RIGHT and game_active == False:
                if bet_score_y:
                    bet_score += 1
                if bet_amount_y:
                    bet_amount += 1
            # if event.key == pygame.K_ENTER and game_active == False:
                
                
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
        if event.type == SPAWNBONUS:
            bonus_list.append(create_bonus(pipe_list))
            
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()
            
        # if event.type == pygame.VIDEORESIZE:
        #     # There's some code to add back window content here.
        #     surface = pygame.display.set_mode((event.w, event.h),
        #                                       pygame.RESIZABLE)
    
    screen.blit(bg_surface, (0,0))
    
    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collison(pipe_list)
        
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        # Bonus
        bonus_list = move_bonuses(bonus_list)
        draw_bonuses(bonus_list)
        
        bonus_score = check_food(bonus_list)
        # if bonus_score:
        #     score_sound.play()
        #     score += 1
            
        score_display('main game')
        
    else:
        if bet:
            bet_srf = game_font.render(str("[UP] - yes, [DOWN] - no"), True, (255,255,255)) # antialias text looks sharper
            bet_srf_rect = bet_srf.get_rect(center = (144,150))
            screen.blit(bet_srf,bet_srf_rect)
            
            bet_surface = game_font.render(str("Bet?"), True, (255,255,255)) # antialias text looks sharper
            bet_rect = bet_surface.get_rect(center = (144,200))
            screen.blit(bet_surface,bet_rect)
            
            bet_exp2_surface = game_font.render(str("Bet Score <= Bet Amount/5"), True, (255,255,255)) # antialias text looks sharper
            bet_exp2_rect = bet_exp2_surface.get_rect(center = (144,250))
            screen.blit(bet_exp2_surface,bet_exp2_rect)
            
        if bet_score_y:
            bet_scr_surface = game_font.render(str("[LEFT] (+1), [RIGHT] (-1)"), True, (255,255,255)) # antialias text looks sharper
            bet_scr_rect = bet_scr_surface.get_rect(center = (144,150))
            screen.blit(bet_scr_surface,bet_scr_rect)
            
            bet_scr_next = game_font.render(str("[UP]-next"), True, (255,255,255)) # antialias text looks sharper
            bet_scr_next_rect = bet_scr_next.get_rect(center = (144,250))
            screen.blit(bet_scr_next,bet_scr_next_rect)
            
            bet_score_surface = game_font.render(f'Bet Score: {int(bet_score)}', True, (255,255,255)) # antialias text looks sharper
            bet_score_rect = bet_score_surface.get_rect(center = (144,200))
            screen.blit(bet_score_surface,bet_score_rect)
            
            bet_exp3_surface = game_font.render(str("<Score you want to achieve>"), True, (255,255,255)) # antialias text looks sharper
            bet_exp3_rect = bet_exp3_surface.get_rect(center = (144,300))
            screen.blit(bet_exp3_surface,bet_exp3_rect)
            
        if bet_amount_y:
            bet_amt_surface = game_font.render(str("[LEFT] (+1), [RIGHT] (-1)"), True, (255,255,255)) # antialias text looks sharper
            bet_amt_rect = bet_amt_surface.get_rect(center = (144,150))
            screen.blit(bet_amt_surface,bet_amt_rect)
            
            bet_amt_next = game_font.render(str("[UP]-next"), True, (255,255,255)) # antialias text looks sharper
            bet_amt_next_rect = bet_amt_next.get_rect(center = (144,250))
            screen.blit(bet_amt_next,bet_amt_next_rect)
            
            bet_amount_surface = game_font.render(f'Bet Amount: {int(bet_amount)}', True, (255,255,255)) # antialias text looks sharper
            bet_amount_rect = bet_amount_surface.get_rect(center = (144,200))
            screen.blit(bet_amount_surface,bet_amount_rect)
            
            bet_exp4_surface = game_font.render(str("<Will added into final score>"), True, (255,255,255)) # antialias text looks sharper
            bet_exp4_rect = bet_exp4_surface.get_rect(center = (144,300))
            screen.blit(bet_exp4_surface,bet_exp4_rect)
            
            bet_exp5_surface = game_font.render(str("<If Bet Score is achieved>"), True, (255,255,255)) # antialias text looks sharper
            bet_exp5_rect = bet_exp5_surface.get_rect(center = (144,350))
            screen.blit(bet_exp5_surface,bet_exp5_rect)
                
        if bet_amount_y == False and bet == False and bet_score_y == False:
            if betting and score >= bet_score:
                score += bet_amount
                betting = False
                # # win = True
                # screen.blit(game_over_surface,game_over_rect)
                # high_score = update_score(score,high_score)
                # score_display('game over')
            else:
                screen.blit(game_over_surface,game_over_rect)
                high_score = update_score(score,high_score)
                score_display('game over')
        
    # Floor
    floor_x_pos -= 1
    draw_floor()
    # generate_bonus()
    if floor_x_pos <= -288:
        floor_x_pos=0
    
    pygame.display.update() #take anything before the update and draws on the screen
    
    # Frames per second (how fast our game updates)
    # Limit framerate
    clock.tick(120) # <= 120 frames per second
    
    # Display surface vs Regular surface
    # There can only be one vs As many as you need
    # Will always be shown
    
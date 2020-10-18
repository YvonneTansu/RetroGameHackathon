import pygame, sys, random
from pygame.locals import *

# score doesnt work yet
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
        # if pipe.x == bird_rect.x:
        #     score_sound.play()
        #     score += 1
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
    
def check_collison(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
        if pipe.x == bird_rect.x:
            score_sound.play()
            score += 1
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

def generate_bonus():
    location_y = random.choice([150,200,250,300,350,400])
    location_x = random.choice([100, 200, 300])
    location_x -= 2.5
    rect = Rect(location_x, location_y, 10,10)
    pygame.draw.rect(screen, (255,255,255), rect)
    # screen.blit(rect, (location_x, location_y))

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
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

# Using timer to spawn pipe
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200) # length of trigger (1200ms): How time time we want to pass since it is going to be triggered
pipe_height = [200,300,400]

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

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
                pipe_list .clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0
                
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
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
        
        # score += 0.01
        score_display('main game')
        # score_sound_countdown -= 1
        # if score_sound_countdown <= 0:
        #     score_sound.play()
        #     score_sound_countdown = 1000/6
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game over')
        
    # Floor
    floor_x_pos -= 1
    draw_floor()
    generate_bonus()
    if floor_x_pos <= -288:
        floor_x_pos=0
    
    pygame.display.update() #take anything before the update and draws on the screen
    
    # Frames per second (how fast our game updates)
    # Limit framerate
    clock.tick(120) # <= 120 frames per second
    
    # Display surface vs Regular surface
    # There can only be one vs As many as you need
    # Will always be shown
    
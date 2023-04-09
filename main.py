##  Music Credit
##  dklon - jump_01, 02 & 03
##  Pixabay - damage, death
##

import pygame
from pygame import mixer
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/monkey_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/monkey_2.png').convert_alpha()
        player_walk_3 = pygame.image.load('graphics/player/monkey_3.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/monkey_1.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.gravity = 0
        self.lives = 3

        self.jump_sound = pygame.mixer.Sound('audio/jump_01.wav')
        self.jump_sound1 = pygame.mixer.Sound('audio/jump_02.wav')
        self.jump_sound2 = pygame.mixer.Sound('audio/jump_03.wav')

        self.player_sounds = [self.jump_sound, self.jump_sound1, self.jump_sound2]
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.player_sounds[randint(0, len(self.player_sounds)-1)].play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += .1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def getlives(self):
        return lives
class Enemy (pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        y_pos = 0
        if type == 'parrot':
            fly_1 = pygame.image.load('graphics/Parrot/parrot_1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Parrot/parrot_2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 200
        else:
            spider_1 = pygame.image.load('graphics/Spider/spider1.png').convert_alpha()
            spider_2 = pygame.image.load('graphics/Spider/spider2.png').convert_alpha()
            self.frames = [spider_1, spider_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))


    def animation(self):
        if type == 'fly':
            self.animation_index += .1
        else:
            self.animation_index += .3

        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()
        self.rect.x -= 5

    def delete(self):
        if self.rect.x <= -50:
            self.kill()

class Fruit (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        banana_1 = pygame.image.load('graphics/Banana/banana_1.png').convert_alpha()
        banana_2 = pygame.image.load('graphics/Banana/banana_2.png').convert_alpha()
        self.frames = [banana_1, banana_2]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), 200))

    def animation(self):
        self.animation_index += .1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()
        self.rect.x -= 3

    def delete(self):
        if self.rect.x <= -50:
            self.kill()

def update_time(extra_score):
    time = extra_score + int((pygame.time.get_ticks() - start_time)/10)
    time_surf = test_font.render(f'{time}', False, (2, 9, 56))
    time_rect = time_surf.get_rect(midright = (775,30))
    screen.blit(time_surf,time_rect)

def collision_enemy():
    # Returns true if the player is colliding with an enemey
    if pygame.sprite.spritecollide(player.sprite, enemies, True):
        return True
    else: return False

def collision_fruit():
    # Returns true if the player is colliding with a fruit
    if pygame.sprite.spritecollide(player.sprite, fruit, True):
        return True
    else: return False


pygame.init()

# OST
mixer.init()
mixer.music.load('audio/background.mp3')
mixer.music.set_volume(.2)
mixer.music.play(-1)

# Game details
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/ARCADECLASSIC.TTF', 50)
game_active = True
highscore = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
enemies = pygame.sprite.Group()
fruit = pygame.sprite.GroupSingle()
fruit.add(Fruit())

# Background, scores and game over screen surfaces and rectangles
sky_surf = pygame.image.load('graphics/Background/background.png').convert()
ground_surf = pygame.image.load('graphics/Background/floor.png').convert()

score_surf = test_font.render('Score', False, 'Black')
score_rect = score_surf.get_rect(midright = (600,30))

best_surf = test_font.render('Best', False, 'Black')
best_rect = best_surf.get_rect(midright = (600,70))

highscore_surf = test_font.render(f'{highscore}', False, 'Black')
highscore_rect = highscore_surf.get_rect(midright = (775,70))

gameover_surf = test_font.render('YOU       DIED', False, 'Black')
gameover_rect = gameover_surf.get_rect(center = (400,25))

retry_surf = test_font.render('Press    SPACE    to    try    again', False, 'Black')
retry_rect = retry_surf.get_rect(center = (400,350))

emoji_surf = pygame.image.load('graphics/cryemoji.png').convert_alpha()
emoji_surf = pygame.transform.rotozoom(emoji_surf,0,.5)
emoji_rect = emoji_surf.get_rect(midleft = (60,200))

# Stats
lives = 3  # Game closes on 0
invincible = False  # Invincibility state, triggered upon taking damage
invTime = 0  # Each collision's time is stored and checked until 2.5 seconds have passed, disabling invincibility
start_time = 0
score = 0
extra_score = 0

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

fruit_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fruit_timer, (randint(10,20)*1000))

# Running loop for the game
while True:
    # Event loop to check for player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quits if the user chooses the 'X' window button
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                # Spawns enemies with a 1/4 chance for fly and 3/4 for snail
                enemies.add(Enemy(choice(['parrot', 'spider', 'spider', 'spider'])))
            if event.type == fruit_timer:
                # Spawns fruit
                fruit.add(Fruit())
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active:
                    # Checks if the user wants to restart, if so lives and score are reset, with the high score being updated
                    lives = 3
                    start_time = pygame.time.get_ticks()
                    highscore_surf = test_font.render(f'{highscore}', False, 'Black')
                    highscore_rect = highscore_surf.get_rect(midright=(775, 70))
                    score = 0
                    extra_score = 0
                    game_active = True


    if game_active:

        # Background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0,300))
        pygame.draw.rect(screen, (54, 42, 133), pygame.Rect(20,15,315,22))
        pygame.draw.line(screen, (240, 10, 105), (25,25), (25 + (100*lives),25),15)
        screen.blit(score_surf, score_rect)
        screen.blit(highscore_surf, highscore_rect)
        screen.blit(best_surf,best_rect)
        update_time(extra_score)

        # Enemies
        enemies.draw(screen)
        enemies.update()

        # Fruit
        fruit.draw(screen)
        fruit.update()

        # Player
        player.draw(screen)
        player.update()

        # Collision
        # Checks time since last hit, resetting invincibility once 2.5 secs has elapsed.
        if pygame.time.get_ticks() - invTime > 2500: invincible = False
        # Checks to see if an enemy collided with the monkey when he is vulnerable
        if collision_enemy() and not invincible:
            # If so, activates invibility and removes a life, ending the game if lives hits 0 and saving the score
            invincible = True
            invTime = pygame.time.get_ticks()
            lives -= 1
            damage_sound = pygame.mixer.Sound('audio/damage.mp3')
            damage_sound.play()
            if lives == 0:
                death_sound = pygame.mixer.Sound('audio/death.mp3')
                death_sound.play()
                game_active = False
                enemies.empty()
                score = int((pygame.time.get_ticks() - start_time)/10)
                if score > highscore:
                    highscore = int((pygame.time.get_ticks() - start_time)/10)

        # Checks to see if the monkey collides with the banana
        if collision_fruit():
            # If the mmonkey is not at full health (3 lives), he regains 1 life, otherwise 1000 score is added.
            banana_sound = pygame.mixer.Sound('audio/banana_pickup.mp3')
            banana_sound.play()
            if lives < 3: lives += 1
            else: extra_score += 1000


    else:

        # Game Over
        screen.fill((70, 5, 117))
        screen.blit(emoji_surf, emoji_rect)
        screen.blit(gameover_surf, gameover_rect)
        screen.blit(retry_surf, retry_rect)
        highscore_surf = test_font.render(f'High Score     {highscore}', False, 'Black')
        highscore_rect = highscore_surf.get_rect(midright=(725, 215))
        result_surf = test_font.render(f'Your Score     {score}', False, 'Black')
        result_rect = result_surf.get_rect(midright=(725, 165))
        screen.blit(highscore_surf, highscore_rect)
        screen.blit(result_surf, result_rect)

    # Refreshes the game to 60 FPS
    pygame.display.update()
    clock.tick(60)

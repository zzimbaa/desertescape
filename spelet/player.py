import os
import pygame
from .settings import Settings

class Action(object):
#Character actions

    IDLE = 0
    RUN = 1
    JUMP = 2
    DEATH = 3

class Frames(object):

    def __init__(self, action: int, image_folder: str, scale, restart=True):
        self.action = action
        self.frames = []
        self.flipped_frames = []
        self.num_of_frames = len(os.listdir(image_folder))
        for i in range(0, self.num_of_frames):
            img = pygame.image.load(f'{image_folder}/{i+1}.png')
            img = pygame.transform.scale(img, (int(Settings.CHARACTER_WIDTH*scale), int(Settings.CHARACTER_HEIGHT*scale)))
            self.frames.append(img)
            self.flipped_frames.append(pygame.transform.flip(img, True, False))
        self.curr_frame = 0
        self.restart = restart

    def get_frame(self, flipped=False):
        return self.flipped_frames[self.curr_frame] if flipped else self.frames[self.curr_frame]

    def reset_frame(self):
        self.curr_frame = 0

    def next_frame(self):
        self.curr_frame += 1
        if self.curr_frame >= self.num_of_frames:
            if self.restart:
                self.curr_frame = 0
            else:
                self.curr_frame = self.num_of_frames - 1

class Player(pygame.sprite.Sprite):

    def __init__(self, screen, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.actionframes = {
            Action.IDLE: Frames(Action.IDLE, "bilder/cowboyplayer/Idle", scale),
            Action.RUN: Frames(Action.RUN, "bilder/cowboyplayer/Run", scale),
            Action.JUMP: Frames(Action.JUMP, "bilder/cowboyplayer/Jump", scale),
            Action.DEATH: Frames(Action.DEATH, "bilder/cowboyplayer/Death", scale, restart=False)
        }
        self.reset(screen, char_type, x, y, scale, speed)
        self.rightSensor = 0
        self.scroll = 0 #Detta är till för att räkna ut spelarens position

    @property
    def health(self):
        return self._health

    @property
    def alive(self):
        return self._health > 0

    @health.setter
    def health(self, value):
        self._health = value
        if self.health <= 0:
            self._health = 0
            self.speed = 0
            self.update_action()

    def getPos (self, scroll): #Eventuellt kan du ha scrollen här
        return (self.rect.x + scroll, self.rect.y)

    def getScore (self):
        return self.score
        
    def move(self, tile_list):
        dx = 0
        dy = 0 
        
        if self.moving_left:
            dx = -self.speed
            self.direction = -1
        if self.moving_right:
            dx = self.speed
            self.direction = 1
            
        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        

        # gravitation
        self.vel_y += Settings.GRAVITY
        dy += self.vel_y

        # kollision med tiles
        for tile in tile_list:
            #Sensor
            if (tile.rect.y - 50 < self.rect.y) and (self.rect.y < tile.rect.y + 50):
                if tile.rect.x > self.rect.x: #ifall den är till höger om spelaren
                    distance = tile.rect.x - self.rect.x
                    if distance < self.rightSensor or self.rightSensor == 0:
                        self.rightSensor = distance
            # kollision i x-led
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width-Settings.CHARACTER_MARGIN_SIDE, self.height-Settings.CHARACTER_MARGIN_BOTTOM):
                dx = 0
            #kollision i y-led
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width-Settings.CHARACTER_MARGIN_SIDE, self.height-Settings.CHARACTER_MARGIN_BOTTOM):
                # check if below the ground, i.e jumping
                if self.vel_y < 0:
                    dy = tile.rect.bottom - self.rect.top + Settings.CHARACTER_MARGIN_BOTTOM
                    self.vel_y = 0
                # check if above the ground, i.e falling
                elif self.vel_y >= 0:
                    dy = tile.rect.top - self.rect.bottom + Settings.CHARACTER_MARGIN_BOTTOM
                    self.vel_y = 0
                    self.in_air = False
        #if sensortest != 100000:
        #    print(sensortest) 
        # rectangle pos
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == "player":
            # if self.moving_right and (self.rect.right > Settings.SCREEN_WIDTH - Settings.SCROLL_THRESH):
            #     self.screen_scroll = -dx
            # elif self.moving_left and (self.rect.left < Settings.SCROLL_THRESH):
            #     self.screen_scroll = -dx
            #else:
            self.rect.x += dx + self.screen_scroll
            self.screen_scroll = -1

            return self.screen_scroll
        
    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # updating image depend on current frame
        self.image = self.actionframes[self.action].get_frame(self.direction == -1)
        # kolla tiden
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.actionframes[self.action].next_frame()
       
    def update_action(self):
        new_action = Action.IDLE
        if self.in_air:
            new_action = Action.JUMP
        elif self.moving_left or self.moving_right:
            new_action = Action.RUN
        if not self.alive:
            new_action = Action.DEATH
        
        # kolla om ny action är samma eller olik från förra
        if new_action != self.action:
            self.action = new_action
            # uppdatering av animation
            self.actionframes[self.action].reset_frame()
            self.update_time = pygame.time.get_ticks()

    def reset(self, screen, char_type, x, y, scale, speed):
        self.screen = screen
        self.char_type = char_type
        self.speed = speed
        self._health = Settings.MAX_HEALTH
        self.score = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.action = Action.IDLE
        self.update_time = pygame.time.get_ticks()
        self.screen_scroll = 0
        self.image = self.actionframes[self.action].get_frame()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.floor_y = Settings.FLOOR_Y + Settings.CHARACTER_MARGIN_BOTTOM
        self.victory = False
        self.moving_left = False
        self.moving_right = False

    
    def draw(self):
        self.screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f"bilder/enemy/Idle/Idle (1).png")
        self.image = self.image = pygame.transform.scale(img, (Settings.TILE_SIZE , Settings.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 80:
            self.move_direction *= -1
            self.move_counter *= -1


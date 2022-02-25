import os
import pygame
from .settings import Settings
import math
from .world_data import world1_data
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
        self.scroll = 0 #Detta är till för att räkna ut spelarens position KANSKE KAN TAS BORT
        self.pos = 0
        self.dx = 0
        self.sensors = []
        self.completeTime = 0

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
    
    def getPos (self, scroll): #Eventuellt kan du ha scrollen här Det ska vara background scroll
        return (self.rect.x + scroll, self.rect.y)

    def getScore (self):
        return self.score
    

    def sensor(self,scroll):
        waterholes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1] #Alla ställen där det är ett hål som leder till vatten 
        ytile = math.floor(self.rect.centery/60) #Ger vilken Y nivå spelaren är på enligt world_data (Ändra 60 till tile_size)
        xtile = math.floor((self.rect.centerx + scroll)/60)
        data = world1_data
        ylevel = data[ytile]
        #Right sensorn
        #Gå igenom hur många tiles det är till nästa väg
        count = 1 #1 betyder alltså att det är ett block precis framför
        start = xtile + 1 #Börja på tilen framför gubben
        for i in range(start, len(ylevel)): 
            tile = ylevel[i]
            #print(tile)
            if not (tile in [1,7,9,10,11,12,13,14,15,16,17]): #1 betyder väg
                count += 1
            else:
                break
        rightsensor = 1/count #Tekniskt sätt kan du göra en optimering så om gubben är på samma y-nivå nästa frame så behövs inte for loopen köras
        

        #Sensor som säger vart närmaste "step-ner" är (10 ex
        #                                              01)
        #GÖR BARA DETTA NÄR GRABBEN INTE ÄR I LUFTEN eller om count inte är 1
        count1 = 0
        ylevel = data[ytile + 1]
        if count != 1 and not self.in_air and (ytile + 1) != 11:
            count1 = 1 #1 betyder alltså att det är ett block precis framför
            for i in range(start, start + count): #Kolla på y-nivån under spelaren 
                tile = ylevel[i]
                if not (tile == 0): 
                    count1 += 1
                else:
                    break
        if count1 - 1 == count or count1 == 0:
            holesensor = 0
        else:
            holesensor = 1/count1
        #Ifall count1 == count så finns det ingen hål emellan
        
        
        #Vattenhålsensor
        count2 = 1 #1 betyder alltså att det är ett block precis framför 
        broke = False
        for i in range(start, len(ylevel)): 
            tile = waterholes[i]
            #print(tile)
            if not (tile == 1): #1 betyder vattenhål
                count2 += 1
            else:
                broke = True #Används för att veta om den faktiskt hittade ett hål överhuvudtaget
                break
        if not broke:
            watersensor = 0
        else:
            watersensor = 1/count2
        if count1 == count2: #Holesensor kommer fortfarande se vattenhål vilket gör att om det är ett vattenhål den detekterar så gör vi så den inte detekterar något alls
            holesensor = 0

        return (rightsensor,holesensor,watersensor)
    def move(self, tile_list,scroll):
        self.dx = 0
        dy = 0 
        if self.moving_left:
            self.dx = -self.speed
            self.direction = -1
        if self.moving_right:
            self.dx = self.speed
            self.direction = 1
            
        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        

        # gravitation
        self.vel_y += Settings.GRAVITY
        dy += self.vel_y

        #Sensors
        if self.alive:
            self.sensors = self.sensor(scroll)
        else:
            self.sensors = (0,0,0)
        # kollision med tiles
        #self.rightSensor = 10000
        for tile in tile_list:
            # #Sensor
            # if (tile.rect.bottom > self.rect.centery + 20) and (self.rect.centery + 20 > tile.rect.top):
            #     if tile.rect.centerx > self.rect.centerx: #ifall den är till höger om spelaren
            #         #print(tile.rect.bottom, tile.rect.top, self.rect.centery)
            #         distance = tile.rect.centerx - self.rect.centerx
            #         if distance < self.rightSensor:
            #             self.rightSensor = distance
            # kollision i x-led
            if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width-Settings.CHARACTER_MARGIN_SIDE, self.height-Settings.CHARACTER_MARGIN_BOTTOM):
                self.dx = 0
                self.wall = True
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
        self.rect.y += dy
        #self.pos = self.getPos(scroll) #Uppdaterar spelaren postion DEtta kanske ska göras efter rect.x ändras?
        #update scroll based on player position
        
        
        #if self.char_type == "player":
            # if self.moving_right and (self.rect.right > Settings.SCREEN_WIDTH - Settings.SCROLL_THRESH):
            #     self.screen_scroll = -dx
            # elif self.moving_left and (self.rect.left < Settings.SCROLL_THRESH):
            #     self.screen_scroll = -dx
            #else:
            
            #self.screen_scroll = -dx

            #return self.screen_scroll

            #if scroll == 0: #Betyder att vi inte behöver ta hänsyn till skrollen
            
            #self.rect.x += self.dx + scroll 
            
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


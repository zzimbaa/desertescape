import pygame
import os

class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        self.char_type = char_type
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        # images for the character
        animation_types = ["Idle", "Run", "Jump"]
        for animation in animation_types:
            temp_list = []
            # räkna nummer av filer. 
            num_of_frames = len(os.listdir(f'bilder/{self.char_type}/{animation}'))
            for i in range(1, num_of_frames):
                img = pygame.image.load(f'bilder/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

            # temp_list = []
            # for i in range(1, 9):
            #     img = pygame.image.load(f'E:/dev/platformerspelTest/bilder/Run/{i}.png')
            #     img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height()) * scale))
            #     temp_list.append(img)
            # self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

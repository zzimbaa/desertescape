import time
from typing import Set
import pygame
from pygame.constants import DROPTEXT
from .settings import Settings
from .player import Player, Action, Enemy
from .tiles import Tile, Coin, Healthpotion, Water, Finish
from .world_data import world1_data

class World():
    def __init__(self, screen, data):
        self.screen = screen
        self.screen_scroll = 0
        self.bg_scroll = 0
        self.font = pygame.font.SysFont("Bauhaus 93", 30)
        self.world_data = data
        self.playerList = []
        playerA = 2 #Amount of players to create
        for i in range(playerA):
            l = Player(screen, char_type='player', x=300, y=300, scale=0.3, speed=5)
            self.playerList.append(l)
        self._init_world()

    def _init_world(self):
        self.game_over_time = time.time() + Settings.PLAY_TIME
        self.game_over = False
        self.victory = False
        self.coin_group = pygame.sprite.Group()
        self.healpot_group = pygame.sprite.Group()
        self.movingenemy_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.finish_group = pygame.sprite.Group()
        self.tile_list = []
        row_count = 0
        for row in self.world_data:
            col_count = 0
            for cell in row:
                if cell == 1:
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/2.png")
                    self.tile_list.append(tile)
                elif cell == 2:
                    coin = Coin(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/items/coingold.png")
                    self.coin_group.add(coin)
                elif cell == 3:
                    healpot = Healthpotion(col_count * Settings.TILE_SIZE,
                                           row_count * Settings.TILE_SIZE,
                                           f"bilder/items/healpotionblue.png")
                    self.healpot_group.add(healpot)
                elif cell == 4:
                    movingenemy = Enemy(col_count * Settings.TILE_SIZE + 6,
                                  row_count * Settings.TILE_SIZE + 6)
                    self.movingenemy_group.add(movingenemy)
                elif cell == 5:
                    water = Water(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/tiles/water.png")
                    self.water_group.add(water)
                elif cell == 6:
                    finish = Finish(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE - (Settings.TILE_SIZE // 2),
                                f"bilder/items/door.png")
                    self.finish_group.add(finish)

                col_count += 1
            row_count += 1
    
    def draw_text(self, text, font, text_col, x, y):
        self.image = font.render(text, True, text_col)
        self.screen.blit(self.image, (x, y))

    def reset_world(self): #Finns ingen poäng med den här för AI eftersom vi bara kommer att starta om hela spelet istället för att reseta världen?
        for player in self.playerList:
            player.reset(self.screen, char_type='player', x=300, y=300, scale=1, speed=5)
        self.screen_scroll = 0
        self.bg_scroll = 0
        self._init_world()

    def draw(self):
        self.screen.fill(Settings.BG_COLOR)
        cloudbg_img = pygame.image.load(f"bilder/cloud.jpg")
        WIDTH = cloudbg_img.get_width()

        for i in range(5):
            self.screen.blit(cloudbg_img, ((i * WIDTH) - self.bg_scroll, 0))

        for tile in self.tile_list:
            tile.rect[0] += self.screen_scroll
            self.screen.blit(tile.img, tile.rect)
        
        for coin in self.coin_group:
            coin.rect[0] += self.screen_scroll
            self.screen.blit(coin.image, coin.rect)
        
        for healpot in self.healpot_group:
            healpot.rect[0] += self.screen_scroll
            self.screen.blit(healpot.image, healpot.rect)
        
        for movingenemy in self.movingenemy_group:
            movingenemy.rect[0] += self.screen_scroll
            self.screen.blit(movingenemy.image, movingenemy.rect)

        for water in self.water_group:
            water.rect[0] += self.screen_scroll
            self.screen.blit(water.image, water.rect)
        
        for finish in self.finish_group:
            finish.rect[0] += self.screen_scroll
            self.screen.blit(finish.image, finish.rect)
        
        #self.game_over = self.game_over or not self.player.alive #När en spelare dör är det inte game over
        #self.victory = self.player.victory #Kommer inte direkt finnas någon victory för spelaren
        self.game_over = True
        for player in self.playerList:
                if not player.alive or not player.victory: #Ifall någon av spelaren inte har dött eller klarat banan så resetar vi inte
                    self.game_over = False
        # if not self.victory: Ingenting händer om en spelare vinner
        #     if not self.game_over:
        #         self.movingenemy_group.update()
        #         self.coin_group.draw(self.screen)
        #         self.healpot_group.draw(self.screen)
        #         self.movingenemy_group.draw(self.screen)
        #         self.water_group.draw(self.screen)
        #     self.finish_group.draw(self.screen)

        if not self.game_over:
            time_left = int(self.game_over_time - time.time())
            if time_left <= 0:
                self.game_over = True
                #self.player.health = 0 # GÖR FOR LOOP HÄR
                #Tror inte det här behövs eftersom vi bara startar om spelet
                for player in self.playerList:
                    player.health = 0
            #text = f'X{self.player.score}' if self.game_over else f'X{self.player.score} {time_left}'
            #Detta behövs nog inte heller?
            # self.draw_text (text,
            #                 self.font,
            #                 Settings.BG_COLOR,
            #                 Settings.TILE_SIZE,
            #                 20)

    def update_player(self):
        furthest_player = None
        for player in self.playerList:
            player.update_animation() # FÖR LOOP HÄR
            player.draw()

            #kollision med items
            if pygame.sprite.spritecollide(player, self.coin_group, True):
                player.score += 1

            #kollision med enemies
            if pygame.sprite.spritecollide(player, self.movingenemy_group, False):
                player.health = 0
                player.speed = 0#Lade till
            if pygame.sprite.spritecollide(player, self.water_group, False):
                player.health = 0
                player.speed = 0 #Lade till
            if pygame.sprite.spritecollide(player, self.finish_group, False):
                player.victory = True
                player.speed = 0

            if player.alive:
                player.update_action()
                player.move(self.tile_list)
                
        
        self.screen_scroll = -1 #self.playerList[0].move(self.tile_list)
        self.bg_scroll -= self.screen_scroll

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
        self.player = Player(screen, char_type='player', x=300, y=300, scale=0.5, speed=5)
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
                    #vanlig jord tile med gräs
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/2.png")
                    self.tile_list.append(tile)
                elif cell == 7:
                    #vanlig jord tile
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/5.png")
                    self.tile_list.append(tile)
                elif cell == 8:
                    #jordplattform längt åt vänster
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/14.png")
                    self.tile_list.append(tile)
                elif cell == 9:
                    #jordplattform mitten
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/15.png")
                    self.tile_list.append(tile)
                elif cell == 10:
                    #jordplattform längst åt höger
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/16.png")
                    self.tile_list.append(tile)
                elif cell == 11:
                    #jord tile för brantsluttning åt höger
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/13.png")
                    self.tile_list.append(tile)
                elif cell == 12:
                    #vanlig jord tile med gräs och komma upp/ner från vänster
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/1.png")
                    self.tile_list.append(tile)
                elif cell == 13:
                    #vanlig jord tile med gräs och komma upp/ner från höger
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/3.png")
                    self.tile_list.append(tile)
                elif cell == 14:
                    #vanlig jord tile för att binda
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/8.png")
                    self.tile_list.append(tile)
                elif cell == 15:
                    #vanlig jord tile för att binda
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/10.png")
                    self.tile_list.append(tile)
                elif cell == 16:
                    #jordplattform slutning åt vänster
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/4.png")
                    self.tile_list.append(tile)
                elif cell == 17:
                    #jordplattform slutning åt höger
                    tile = Tile(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/cowboytiles/6.png")
                    self.tile_list.append(tile)
                elif cell == 2:
                    #coins
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
                    #fiende
                    movingenemy = Enemy(col_count * Settings.TILE_SIZE + 6,
                                  row_count * Settings.TILE_SIZE + 6)
                    self.movingenemy_group.add(movingenemy)
                elif cell == 5:
                    #vatten
                    water = Water(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE,
                                f"bilder/tiles/water.png")
                    self.water_group.add(water)
                elif cell == 6:
                    #mål
                    finish = Finish(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE - (Settings.TILE_SIZE // 2),
                                f"bilder/items/door.png")
                    self.finish_group.add(finish)

                col_count += 1
            row_count += 1
    
    def draw_text(self, text, font, text_col, x, y):
        self.image = font.render(text, True, text_col)
        self.screen.blit(self.image, (x, y))

    def reset_world(self):
        self.player.reset(self.screen, char_type='player', x=300, y=300, scale=1, speed=5)
        self.screen_scroll = 0
        self.bg_scroll = 0
        self._init_world()

    def draw(self):
        self.screen.fill(Settings.BG_COLOR)
        cloudbg_img = pygame.image.load(f"bilder/cowboytiles/western.jpg")
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
        
        self.game_over = self.game_over or not self.player.alive
        self.victory = self.player.victory

        if not self.victory:
            if not self.game_over:
                self.movingenemy_group.update()
                self.coin_group.draw(self.screen)
                self.healpot_group.draw(self.screen)
                self.movingenemy_group.draw(self.screen)
                self.water_group.draw(self.screen)
            self.finish_group.draw(self.screen)

        if not self.game_over and not self.victory:
            time_left = int(self.game_over_time - time.time())
            if time_left <= 0:
                self.game_over = True
                self.player.health = 0
                self.screen_scroll = 0
            text = f'X{self.player.score}' if self.game_over else f'X{self.player.score} {time_left}'
            self.draw_text (text,
                            self.font,
                            Settings.BG_COLOR,
                            Settings.TILE_SIZE,
                            20)

    def update_player(self):
        self.player.update_animation()
        self.player.draw()

        #kollision med items
        if pygame.sprite.spritecollide(self.player, self.coin_group, True):
            self.player.score += 1

        #kollision med enemies
        if pygame.sprite.spritecollide(self.player, self.movingenemy_group, False):
            self.player.health = 0
            self.screen_scroll = 0

        if pygame.sprite.spritecollide(self.player, self.water_group, False):
            self.player.health = 0
            self.screen_scroll = 0

        if pygame.sprite.spritecollide(self.player, self.finish_group, False):
            self.player.victory = True
            self.player.speed = 0

        if self.player.alive:
            self.player.update_action()
            self.screen_scroll = self.player.move(self.tile_list)
            self.bg_scroll -= self.screen_scroll

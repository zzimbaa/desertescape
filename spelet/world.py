import time
import random
from typing import Set
import pygame
from pygame.constants import DROPTEXT
from .settings import Settings
from .player import Player, Action, Enemy
from .tiles import Tile, Coin, Healthpotion, Water, Finish, Tree, Bush
from .world_data import world1_data
from .drawNetworkFuncs import * 
class World():
    def __init__(self, screen, data,time1, genomes):
        self.screen = screen
        self.screen_scroll = 0
        self.bg_scroll = -200
        self.font = pygame.font.SysFont("Bauhaus 93", 30)
        self.world_data = data
        self.playerList = []
        self.old_player = None
        playerA = 50 #Amount of players to create
        for i in range(playerA):
            l = Player(screen, char_type='player', x=500, y=500, scale=0.3, speed=5)
            l.network = genomes[i]
            self.playerList.append(l)
        self.furthest_player = self.playerList[0]
        self._init_world(time1)

    def _init_world(self,time1):
        self.game_over_time = time.time() + time1
        self.start_time = time.time()
        self.game_over = False
        self.victory = False
        self.coin_group = pygame.sprite.Group()
        self.healpot_group = pygame.sprite.Group()
        self.movingenemy_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.finish_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.bush_group = pygame.sprite.Group()
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
                                f"bilder/items/Gold_1.png")
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
                                row_count * Settings.TILE_SIZE - (Settings.TILE_SIZE // 3),
                                f"bilder/items/Skeleton.png")
                    self.finish_group.add(finish)
                elif cell == 20:
                    #föremål utan kollision
                    tree = Tree(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE- (Settings.TILE_SIZE),
                                f"bilder/items/Tree.png")
                    self.tree_group.add(tree)
                elif cell == 21:
                    #föremål utan kollision
                    bush = Bush(col_count * Settings.TILE_SIZE,
                                row_count * Settings.TILE_SIZE - (Settings.TILE_SIZE // 2),
                                f"bilder/items/Bush (1).png")
                    self.bush_group.add(bush)
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

    def draw_network(self):
        #Funktionerna ligger i drawNetworkFuncs.py
        #if 
        network = self.furthest_player.network.brain
        height = (0, Settings.SCREEN_HEIGHT/2)
        width = (5/8 * Settings.SCREEN_WIDTH, Settings.SCREEN_WIDTH)
        #print(height, width)
        circles = getRects(network,width,height) #Få värdena på skärmen
        circles = assign_circle_to_node(circles, network.nodes)

        drawCircles(circles, self.screen)
        drawLines(network,circles,self.screen)
        #pygame.draw.circle(self.screen, pygame.Color(255,255,255), (750,330), 100)

    def draw(self):
        self.screen.fill(Settings.BG_COLOR)
        cloudbg_img = pygame.image.load(f"bilder/cowboytiles/western.jpg")
        WIDTH = cloudbg_img.get_width()
        
        for i in range(5):
            self.screen.blit(cloudbg_img, ((i * WIDTH) - self.bg_scroll, 0))

        for tile in self.tile_list:
            tile.rect[0] = tile.og - self.bg_scroll
            self.screen.blit(tile.img, tile.rect)
        
        for coin in self.coin_group:
            coin.rect[0] = coin.og - self.bg_scroll
            self.screen.blit(coin.image, coin.rect)
        
        for healpot in self.healpot_group:
            healpot.rect[0] = healpot.og - self.bg_scroll
            self.screen.blit(healpot.image, healpot.rect)
        
        for movingenemy in self.movingenemy_group:
            movingenemy.rect[0] = movingenemy.og - self.bg_scroll
            self.screen.blit(movingenemy.image, movingenemy.rect)

        for water in self.water_group:
            water.rect[0] = water.og - self.bg_scroll
            self.screen.blit(water.image, water.rect)
        
        for finish in self.finish_group:
            finish.rect[0] = finish.og - self.bg_scroll
            self.screen.blit(finish.image, finish.rect)
        
        for tree in self.tree_group:
            tree.rect[0] += finish.og - self.bg_scroll
            self.screen.blit(tree.image, tree.rect)

        for bush in self.bush_group:
            bush.rect[0] += finish.og - self.bg_scroll
            self.screen.blit(bush.image, bush.rect)

        self.game_over = True
        for player in self.playerList:
                #Ifall någon av spelaren inte har dött eller klarat banan så resetar vi inte
                if not player.alive or not player.victory: 
                    self.game_over = False

        if not self.game_over and not self.victory:
            time_left = int(self.game_over_time - time.time())
            if time_left <= 0:
                self.game_over = True
                for player in self.playerList:
                    player.health = 0
        self.draw_network()
    def update_player(self):
        furthest_player = None
        for player in self.playerList:
            player.update_animation() 
            player.draw()

            #kollision med items
            if pygame.sprite.spritecollide(player, self.coin_group, True):
                player.score += 1

            #kollision med enemies
            if pygame.sprite.spritecollide(player, self.movingenemy_group, False):
                player.health = 0
                player.speed = 0
                player.dx = 0
            if pygame.sprite.spritecollide(player, self.water_group, False):
                player.health = 0
                player.speed = 0 
                player.dx = 0
            if pygame.sprite.spritecollide(player, self.finish_group, False):
                player.victory = True
                player.speed = 0
                player.dx = 0
                player.health = 0 #Så att spelaren inte fortsätter efteråt
                player.completeTime = time.time() - self.start_time
            player.update_action()
            player.move(self.tile_list, self.bg_scroll) 
       
        #SKROLLUPPDATERAR
        #Ta fram spelarna som lever
        alive_players = [x for x in self.playerList if x.alive]
        #Hitta spelaren som är längst fram
        #Om någon någon spelare lever
        if len(alive_players) != 0:
            furthest_player = max(alive_players, key=lambda x: x.rect.centerx)
            #Kolla om detta är samma spelare som tidigare 
            if furthest_player is self.old_player:
                self.screen_scroll = -furthest_player.dx
                self.bg_scroll -= self.screen_scroll
                #När vi väl vet hur alla spelare vill flytta sig och vet den spelaren som är längst fram uppdaterar 
                #vi allas x position i samband med hur den spelaren längst fram vill ändra skrollen
                for player in self.playerList: 
                    player.rect.x += player.dx + self.screen_scroll
            else:
                if not self.old_player == None:
                    #Teoretiskt borde detta alltid vara positivt men det kanske finns scenarion där det inte är så
                    distance = furthest_player.rect.centerx - self.old_player.rect.centerx 
                    #Vi vill nu flytta scrollen som den nya spelaren vill men samtidigt vill vi flytta så den nya spelaren är i center
                    new_scroll = distance + furthest_player.dx
                    self.screen_scroll = -new_scroll
                    self.bg_scroll -= self.screen_scroll
                    for player in self.playerList: 
                        player.rect.x += player.dx + self.screen_scroll
            self.old_player = furthest_player
            self.furthest_player = furthest_player

import pygame
from .world import World
from .settings import Settings
from .world_data import world1_data
from .player import Player
from .restartgame import Button, ScreenFade


class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Bauhaus 93", 30)
        self.start_button = Button(screen, Settings.SCREEN_WIDTH // 2 - 350, Settings.SCREEN_HEIGHT // 2, f"bilder/items/start.png")
        self.exit_button = Button(screen, Settings.SCREEN_WIDTH // 2 + 150, Settings.SCREEN_HEIGHT // 2, f"bilder/items/exit.png")
        self.restart_button = Button(screen, Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT // 2, f"bilder/items/restart.png")
        self.reset()

    def reset(self):
        self.restart = False
        self.fade = ScreenFade(self.screen, 1, Settings.BLACK, 4)

    def draw_text(self, text, x, y):
        self.screen.blit(self.font.render(text, True, Settings.BG_COLOR),
                         (x, y))

    def draw_main(self):
        self.screen.fill(Settings.BG_COLOR)
        self.exit = self.exit_button.draw()
        self.start = self.start_button.draw()
    
    def draw_victory(self, score):
        self.fade.fade()
        text = 'YOU WIN, TRY TO BEAT YOUR RECORD!'
        x = (Settings.SCREEN_WIDTH // 2) - 200
        y = Settings.SCREEN_HEIGHT - 500
        self.draw_text(text, x, y)
        text = 'SCORE: ' + str(score)
        x = (Settings.SCREEN_WIDTH // 2) - 200
        y = Settings.SCREEN_HEIGHT - 400
        self.draw_text(text, x, y)
        if self.restart_button.draw():
            self.fade = ScreenFade(self.screen, 1, Settings.BLACK, 4)
            self.restart = True

    def draw_game_over(self):
        self.fade.fade()
        text = 'YOU LOSE, TRY AGAIN?'
        x = (Settings.SCREEN_WIDTH // 2) - 120
        y = Settings.SCREEN_HEIGHT - 500
        self.draw_text(text, x, y)
        if self.restart_button.draw():
            self.fade = ScreenFade(self.screen, 1, Settings.BLACK, 4)
            self.restart = True


class Game():

    def __init__(self, menu=False):
        pygame.init()
        self._screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self._world = None
        #self.moving_left = None
        #self.moving_right = None
        #self.jumping = None
        self.world_data = world1_data
        self.menu_enabled = menu
        self.menu = Menu(self._screen) if menu else None
        self.draw_main_menu = menu

    def game_over(self):
        return self._world.game_over

    def victory(self):
        return self._world.victory
    
    # Den ska vara såhär eftersom scrollen inte kommer förflytta sig direkt.
    def player_pos(self): #Vet inte om detta funkar med flera spelare så du får testa det? Kanske gör om till en player funktion
        return (self._world.player.rect.x + self._world.bg_scroll, self._world.player.rect.y)

    def score(self): #Player funktion?
        return self._world.player.score

    def run(self, action_fn=None):
        clock = pygame.time.Clock()
        self._world = World(self._screen, self.world_data)
        keep_going = True
        while keep_going:

            clock.tick(Settings.FPS)

            if self.draw_main_menu:
                self.menu.draw_main()
                keep_going = not self.menu.exit
                self.draw_main_menu = not self.menu.start
            else:
                self._world.draw()

                if self._world.game_over:
                    if self.menu_enabled:
                        self.menu.draw_game_over()
                        if self.menu.restart:
                            self._world.reset_world()
                            self.menu.reset()
                    else:
                        keep_going = False
                if self._world.victory:
                    if self.menu_enabled:
                        self.menu.draw_victory(self._world.player.score)
                        if self.menu.restart:
                            self._world.reset_world()
                            self.menu.reset()
                    else:
                        keep_going = False

                self._world.update_player()
            # for player in self._world.playerList:
            #     self._world.player.moving_left = self.moving_left and not self.moving_right
            #     self._world.player.moving_right = self.moving_right
            #     self._world.player.jump = self.jumping and self._world.player.alive
            # Tror inte dettta behövs för flera spelare?
            #yield self.player_pos() Tror detta gör samma sak som return fast lite anorlunda

            pygame.display.update()

import pygame
from .settings import Settings
from restartgame import Button, ScreenFade

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

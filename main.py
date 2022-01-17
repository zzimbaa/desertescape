import pygame
from spelet.game import Game, Menu
from 

def main():
    game = Game(menu=True)
    for player_pos in game.run():
        for event in pygame.event.get():
            # quitgame
            if event.type == pygame.QUIT:
                return
            # keyboard presses
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    game.moving_left = event.type == pygame.KEYDOWN
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    game.moving_right = event.type == pygame.KEYDOWN
                if event.key in [pygame.K_w, pygame.K_UP]:
                    game.jumping = event.type == pygame.KEYDOWN
                if event.key == pygame.K_ESCAPE:
                    return

    if game.game_over():
        print('Game Over!')
    elif game.victory():
        print('Victory!', f'Score: {game.score()}')

main()

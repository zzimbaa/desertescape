from spelet.game import Game


def main():
    game = Game()
    print(game.world_data)  # tiles i spelet, det spelaren ser
    for player_pos in game.run(): #kappe gör så här fast med AI ;)
        i = 1
        for player in game._world.playerList:
            print(True)
            if i == 1:
                player.moving_right = True
                i += 1
            else:
                player.moving_left = True
main()
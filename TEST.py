from spelet.game import Game


def main():
    game = Game()
    print(game.world_data)  # tiles i spelet, det spelaren ser
    i = 1
    for player_pos in game.run(): #kappe gör så här fast med AI ;)
        #print(1/(game._world.playerList[0].rightSensor/50)) 
        #print((game._world.playerList[0].rightSensor))
        game._world.playerList[0].moving_right = True
        game._world.playerList[0].jump = True
        print(game._world.playerList[0].sensor(game._world.bg_scroll))
        # if i == 1:
        #     game._world.playerList[0].moving_right = True
        # if i == 100:
        #     game._world.playerList[0].moving_right = False
        #     game._world.playerList[1].moving_right = True
        # i += 1
main()
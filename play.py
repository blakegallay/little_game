from game import Game

if __name__ == "__main__":
    game = Game()

    play_game = input("Start game? Y/N\n").upper()
    if(play_game == "Y"):
        game.play()
    else:
        quit()

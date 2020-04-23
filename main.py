#!/usr/bin/env python

# set version (kinda irrelevant but so what)
VERSION = "0.1"

# import modules
try:
    import sys
    import pygame
    from game import Game
    from scenes.splash import SplashScreen
    from scenes.inital import InitialScreen
    from scenes.gameplay import GameplayScreen
    from scenes.battle import BattleScreen
    from scenes.defeat import DefeatScreen
    from scenes.victory import VictoryScreen
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


# main game function
if __name__ == "__main__":
    pygame.init()  # initialize pygame
    screen = pygame.display.set_mode((1280, 720))  # set window size
    pygame.display.set_caption("Riskier")  # set window captions
    # create dictionary of states
    states = {"SPLASH": SplashScreen(),
              "INITIAL": InitialScreen(),
              "GAMEPLAY": GameplayScreen(),
              "BATTLE": BattleScreen(),
              "DEFEAT": DefeatScreen(),
              "VICTORY": VictoryScreen()}
    game = Game(screen, states, "SPLASH")  # Initialize Game object
    game.run()  # start game
    pygame.quit()  # after game has finished running, quit pygame
    sys.exit()  # exit the program

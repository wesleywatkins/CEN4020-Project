# import modules
try:
    import math
    import os
    import random
    import pygame
    import sys
    import time
    from classes.player import Player
    from components.actionbar import ActionBar
    from components.board import Board
    from components.menubar import MenuBar
    from gui.circlelabel import CircleLabel
    from scenes.gamestate import GameState
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class InitialScreen(GameState):
    def __init__(self):
        # scene stuff
        super(InitialScreen, self).__init__()
        self.next_state = "GAMEPLAY"
        # board
        self.board = Board()
        # region positions
        self.positions = list()
        self.read_in_regions()
        # objects
        self.player = Player("Player")
        self.ai = Player("AI")
        # gui elements
        self.action_bar = ActionBar(0, pygame.display.get_surface().get_height() - 80,
                                    pygame.display.get_surface().get_width(), 80, [])
        self.menu_bar = MenuBar(0, 0, pygame.display.get_surface().get_width(), 40, middle='Select a Starting Region')
        # flags
        self.user_choosing = True
        self.ai_choosing = False
        # timer for basic things
        self.end_time = time.time()

    def get_event(self, event):
        # close window
        if event.type == pygame.QUIT:
            self.quit = True
        # choose region
        if self.user_choosing and event.type == pygame.MOUSEBUTTONDOWN:
            # get region and set player troops
            region = self.get_clicked_region(event)
            self.player.troops.update({str(region): 3})
            self.player.set_home_region(str(region))
            # change flags
            self.ai_choosing = True
            self.user_choosing = False
            # update timer
            self.end_time = time.time() + 2

    def update(self, dt):
        # handle ai choosing a region
        if self.ai_choosing and time.time() > self.end_time:
            # randomly select ai region
            player_region = int(list(self.player.troops.keys())[0])
            region = random.randint(0, len(self.positions) - 1)
            while abs(player_region - region) < (len(self.positions)/2 - 1):
                region = random.randint(0, len(self.positions) - 1)
            self.ai.troops[str(region)] = 3
            self.ai.home_region = str(region)
            # update time and flags
            self.end_time = time.time() + 2
            self.ai_choosing = False
        # change to gameplay scene
        if not self.ai_choosing and not self.user_choosing and time.time() > self.end_time:
            self.persist_state()
            self.done = True
        self.update_menu_bar()

    def render(self, surface):
        # draw ocean
        surface.fill(pygame.Color("dodgerblue"))
        # draw board, action bar, and menu bar
        self.board.render(surface)
        self.action_bar.render(surface)
        self.menu_bar.render(surface)
        # draw regions
        self.draw_regions(surface)

    def update_menu_bar(self):
        if self.user_choosing:
            self.menu_bar.update_middle('Select a Starting Region')
        elif self.ai_choosing:
            self.menu_bar.update_middle('AI is Choosing a Starting Region')
        else:
            self.menu_bar.update_middle('AI Has Chosen a Starting Region')

    def draw_regions(self, surface):
        # draw player labels
        for key, value in self.player.troops.items():
            x, y = self.positions[int(key)]
            if key == self.player.home_region:
                cl = CircleLabel(str(value), x, y, rad=20, bc=(0, 0, 0), fc=(0, 200, 0))
            else:
                cl = CircleLabel(str(value), x, y, rad=20, bc=(0, 255, 0))
            cl.render(surface)
        # draw ai labels
        for key, value in self.ai.troops.items():
            x, y = self.positions[int(key)]
            if key == self.ai.home_region:
                cl = CircleLabel(str(value), x, y, rad=20, bc=(0, 0, 0), fc=(200, 0, 0))
            else:
                cl = CircleLabel(str(value), x, y, rad=20, bc=(200, 0, 0))
            cl.render(surface)

    def get_clicked_region(self, event):
        pos = event.pos
        distance = 1000
        region = 0
        for (i, p) in enumerate(self.positions):
            region = region
            temp = math.sqrt(math.pow((p[0] - pos[0]), 2) + math.pow((p[1] - pos[1]), 2))
            if temp < distance:
                distance = temp
                region = i
        return region

    def read_in_regions(self):
        with open(os.path.join('data', 'positions.txt')) as f:
            for line in f:
                line = line.rstrip()
                values = line.split(" ")
                self.positions.append((int(values[0]), int(values[1])))

    def startup(self, persistent):
        self.persist['difficulty'] = persistent['difficulty']

    def persist_state(self):
        self.persist['player'] = self.player
        self.persist['ai'] = self.ai

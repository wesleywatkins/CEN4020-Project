# import modules
try:
    import json
    import math
    import os
    import pygame
    import time
    import random
    import sys
    from classes.player import Player
    from components.actionbar import ActionBar
    from components.board import Board
    from components.menubar import MenuBar
    from gui.circlelabel import CircleLabel
    from scenes.gamestate import GameState
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class GameplayScreen(GameState):
    def __init__(self):
        # scene stuff
        super(GameplayScreen, self).__init__()
        self.next_state = "BATTLE"
        # board
        self.board = Board()
        # region positions
        self.positions = list()
        self.read_in_regions()
        # allowed moves
        self.read_in_allowed_moves()
        # objects
        self.player = Player()
        self.ai = Player()
        # gui elements
        self.menu_bar = MenuBar(0, 0, pygame.display.get_surface().get_width(), 40, middle='Select a Move')
        self.action_bar = ActionBar(0, pygame.display.get_surface().get_height() - 80,
                                    pygame.display.get_surface().get_width(), 80,
                                    ['Place Troops', 'Move Troops', 'End Turn'])
        # flags
        self.difficulty = 0
        self.turn = 0
        self.moves_left = 5
        self.ai_moves_left = 5
        self.new_round = True
        self.placing_troops = False
        self.moving_troops = False
        self.moving_temp = None

    def get_event(self, event):
        # Handle closing the game
        if event.type == pygame.QUIT:
            self.quit = True
        # REMOVE LATER: Go to battle screen
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            self.done = True
        # Handle clicking "PLACE TROOPS"
        elif self.turn == 0 and self.action_bar.get_event(event) == 'Place Troops':
            self.moving_troops = False
            self.moving_temp = None
            self.placing_troops = not self.placing_troops
        # Handle clicking "MOVE TROOPS"
        elif self.turn == 0 and self.action_bar.get_event(event) == 'Move Troops':
            self.placing_troops = False
            self.moving_troops = not self.moving_troops
            self.moving_temp = None
        # Handle clicking "END TURN"
        elif self.turn == 0 and self.action_bar.get_event(event) == 'End Turn':
            self.placing_troops = False
            self.moving_troops = False
            self.moving_temp = None
            self.turn = 1
            self.action_bar.disable_all()
        # Handle clicking 2nd region when moving troops
        elif self.moving_troops and event.type == pygame.MOUSEBUTTONUP:
            self.move_troops(event)
        # Handle placing troops event
        elif self.placing_troops and event.type == pygame.MOUSEBUTTONUP:
            self.place_troops_in_region(event)

    def update(self, dt):
        # update player and ai
        self.player.update()
        self.ai.update()
        # check if game is over
        if self.ai.troops[str(self.ai.home_region)] < 1:
            self.next_state = "VICTORY"
            self.done = True
            return
        if self.player.troops[str(self.player.home_region)] < 1:
            self.next_state = "DEFEAT"
            self.done = True
            return
        # distribute troops on new round
        if self.new_round:
            if self.difficulty == 0:
                self.player.reserve += 3
                self.ai.reserve += 3
            elif self.difficulty == 1:
                self.player.reserve += 1
                self.ai.reserve += 3
            elif self.difficulty == 2:
                self.player.reserve += 1
                self.ai.reserve += 6
            self.new_round = False
        self.action_bar.update()
        self.update_menu_bar()
        # do AI's turn
        if self.turn == 1:
            self.ai_turn()

    def render(self, surface):
        # draw ocean
        surface.fill(pygame.Color("dodgerblue"))
        # draw board
        self.board.render(surface)
        # draw gui elements
        pygame.draw.rect(surface, pygame.Color("white"), (0, 0, pygame.display.get_surface().get_width(), 40))
        self.action_bar.render(surface)
        self.menu_bar.render(surface)
        # draw regions
        self.draw_labels(surface)

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

    def place_troops_in_region(self, event):
        region = self.get_clicked_region(event)
        if str(region) in self.ai.troops.keys():
            return
        self.player.add_troops(str(region))
        if self.player.reserve < 1:
            self.placing_troops = False
            self.action_bar.disable_button('Place Troops')

    def move_troops(self, event):
        if self.moving_temp is None:
            region = self.get_clicked_region(event)
            if str(region) not in self.player.troops.keys():
                self.moving_troops = False
            else:
                self.moving_temp = region
        else:
            region = self.get_clicked_region(event)
            if str(region) in self.allowed_moves[str(self.moving_temp)]:
                self.moves_left -= 1
                if str(region) not in self.ai.troops.keys():
                    self.player.move_troops(self.moving_temp, region)
                else:
                    if str(self.moving_temp) != self.player.home_region:
                        self.persist_state()
                        self.next_state = "BATTLE"
                        self.persist['ai_region'] = region
                        self.persist['player_region'] = self.moving_temp
                        self.persist['flee'] = True
                        self.moving_troops = False
                        self.done = True
                    else:
                        self.moving_troops = False
            self.moving_temp = None
            if self.moves_left < 1:
                self.action_bar.disable_button('Move Troops')
                self.moving_troops = False
                self.moving_temp = None

    def update_menu_bar(self):
        self.menu_bar.update_left("Reserve Troops: " + str(self.player.reserve))
        self.menu_bar.update_right("Moves Left: " + str(self.moves_left))
        if self.turn == 0:
            self.menu_bar.update_middle('Select Move')
        else:
            self.menu_bar.update_middle("AI's Turn")
        if self.turn == 0:
            if self.placing_troops:
                self.menu_bar.update_middle('Select Region')
            elif self.moving_troops and self.moving_temp is None:
                self.menu_bar.update_middle('Select Move-From Region')
            elif self.moving_troops and self.moving_temp is not None:
                self.menu_bar.update_middle('Select Move-To Region')
        else:
            if self.ai.reserve >= 1:
                self.menu_bar.update_middle('AI Placing Troops')
            else:
                self.menu_bar.update_middle('AI Moving Troops')

    def ai_turn(self):
        if self.ai.reserve >= 1:
            value = random.uniform(0, 1)
            if value < 0.4:
                self.ai.add_troops(self.ai.home_region)
            elif value < 0.7:
                self.ai.add_troops(random.choice(list(self.ai.troops.keys())))
            else:
                choice = random.randint(0, len(self.positions))
                while choice in self.player.troops.keys():
                    choice = random.randint(0, len(self.positions))
                self.ai.add_troops(choice)
            time.sleep(1)
        else:
            if self.ai_moves_left > 1:
                self.ai_moves_left -= 1
                value = random.uniform(0, 1)
                if value < 0.5:
                    time.sleep(1)
                    from_region = random.choice(list(self.ai.troops.keys()))
                    to_region = random.choice(self.allowed_moves[str(from_region)])
                    if str(to_region) in self.player.troops.keys():
                        if str(from_region) == self.ai.home_region:
                            return
                        self.persist_state()
                        self.next_state = "BATTLE"
                        self.persist['ai_region'] = from_region
                        self.persist['player_region'] = to_region
                        self.persist['flee'] = False
                        self.done = True
                    else:
                        self.ai.move_troops(from_region, to_region)
            else:
                self.turn = 0
                self.moves_left = 5
                self.ai_moves_left = 5
                self.new_round = True
                self.action_bar.enable_all()

    def draw_labels(self, surface):
        for key, value in self.player.troops.items():
            try:
                x, y = self.positions[int(key)]
                if key == self.player.home_region:
                    cl = CircleLabel(str(value), x, y, rad=20, bc=(0, 0, 0), fc=(0, 200, 0))
                else:
                    cl = CircleLabel(str(value), x, y, rad=20, bc=(0, 255, 0))
                cl.render(surface)
            except IndexError as e:
                print(e)
        for key, value in self.ai.troops.items():
            try:
                x, y = self.positions[int(key)]
                if self.difficulty < 2:
                    if key == self.ai.home_region:
                        cl = CircleLabel(str(value), x, y, rad=20, bc=(0, 0, 0), fc=(200, 0, 0))
                    else:
                        cl = CircleLabel(str(value), x, y, rad=20, bc=(200, 0, 0))
                else:
                    if key == self.ai.home_region:
                        cl = CircleLabel(str(value), x, y, rad=20, bc=(0, 0, 0), fc=(200, 0, 0), ai=True)
                    else:
                        cl = CircleLabel(str(value), x, y, rad=20, bc=(200, 0, 0), ai=True)
                cl.render(surface)
            except IndexError as e:
                print(e)

    def read_in_regions(self):
        with open(os.path.join('data', 'positions.txt')) as f:
            for line in f:
                line = line.rstrip()
                values = line.split(" ")
                self.positions.append((int(values[0]), int(values[1])))

    def read_in_allowed_moves(self):
        with open(os.path.join('data', 'moves.json'), 'r') as f:
            self.allowed_moves = json.load(f)

    def startup(self, persistent):
        try:
            self.player = persistent['player']
            self.ai = persistent['ai']
            self.difficulty = persistent['difficulty']
        except KeyError as e:
            print(e)
            sys.exit(1)

    def persist_state(self):
        self.persist['player'] = self.player
        self.persist['ai'] = self.ai
        self.persist['turn'] = self.turn
        self.persist['moves_left'] = self.moves_left
        self.persist['ai_moves_left'] = self.ai_moves_left
        self.persist['new_round'] = self.new_round
        self.persist['difficulty'] = self.difficulty

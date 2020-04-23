# import modules
try:
    import pygame
    import random
    import sys
    import time
    from classes.troop import Troop
    from components.actionbar import ActionBar
    from components.menubar import MenuBar
    from scenes.gamestate import GameState
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


# this is for position the troops in the diamond shape we discussed
# it can be render to the screen, but its not. It's mostly for positioning purposes
class Board(object):

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.size = 500
        self.top = (int(self.x), int(self.y - self.size / 2))
        self.bottom = (int(self.x), int(self.y + self.size / 2))
        self.left = (int(self.x - self.size / 2), int(self.y))
        self.right = (int(self.x + self.size / 2), int(self.y))
        self.topleft = (int(self.x - self.size/4), int(self.y - self.size/4))
        self.topright = (int(self.x + self.size / 4), int(self.y - self.size / 4))
        self.bottomleft = (int(self.x - self.size / 4), int(self.y + self.size / 4))
        self.bottomright = (int(self.x + self.size / 4), int(self.y + self.size / 4))

    def render(self, surface):
        pygame.draw.line(surface, pygame.Color("black"), self.top, self.right)
        pygame.draw.line(surface, pygame.Color("black"), self.right, self.bottom)
        pygame.draw.line(surface, pygame.Color("black"), self.bottom, self.left)
        pygame.draw.line(surface, pygame.Color("black"), self.left, self.top)
        pygame.draw.line(surface, pygame.Color("black"), self.topleft, self.bottomright)
        pygame.draw.line(surface, pygame.Color("black"), self.topright, self.bottomleft)

    def get_left_pos(self):
        return int(self.x - self.size/4), int(self.y)

    def get_right_pos(self):
        return int(self.x + self.size/4), int(self.y)

    def get_top_pos(self):
        return int(self.x), int(self.y - self.size/4)

    def get_bottom_pos(self):
        return int(self.x), int(self.y + self.size/4)


#  Scene for handling battles
class BattleScreen(GameState):

    def __init__(self):
        super(BattleScreen, self).__init__()
        self.next_state = "GAMEPLAY"  # default next state for battle screen is gameplay scene
        # troop list
        self.player_troops = []  # default player troops
        self.ai_troops = []  # default ai troops
        # gui stuff
        self.player_board = Board(pygame.display.get_surface().get_width() * 0.25,
                                  pygame.display.get_surface().get_height() * 0.45)
        self.ai_board = Board(pygame.display.get_surface().get_width() * 0.75,
                              pygame.display.get_surface().get_height() * 0.45)
        self.action_bar = ActionBar(0, pygame.display.get_surface().get_height() - 120,
                                    pygame.display.get_surface().get_width(), 120,
                                    ['Attack', 'Defend', 'Move Troops', 'End Turn', 'Flee'], font_size=26)
        self.menu_bar = MenuBar(0, 0, pygame.display.get_surface().get_width(), 40, middle='Select Move')
        # flags
        self.turn = 0  # 0 == user, 1 == ai
        self.new_round = True  # flag for determining new rounds
        self.moves_left = 3  # user moves
        self.ai_moves_left = 3  # ai moves
        # flag for determining if user clicks buttons
        self.attacking = False
        self.attacking_temp = None
        self.defending = False
        self.moving = False
        self.moving_temp = None
        self.fleeing = False

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        # check for player troop clicks
        if self.turn == 0 and self.check_player_troop_clicks(event) is not None:
            troop = self.check_player_troop_clicks(event)
            if self.attacking and self.attacking_temp is None:
                self.attacking_temp = troop
            elif self.defending:
                self.player_troops[troop].defense_boost()
                self.defending = False
                self.moves_left -= 1
            elif self.moving and self.moving_temp is None:
                self.moving_temp = troop
            elif self.moving and self.moving_temp is not None:
                self.player_troops[self.moving_temp], self.player_troops[troop] = self.player_troops[troop], self.player_troops[self.moving_temp]
                self.moving = False
                self.moving_temp = None
                self.moves_left -= 1
        # check for player ai clicks
        elif self.turn == 0 and self.check_ai_troop_clicks(event) is not None:
            troop = self.check_ai_troop_clicks(event)
            if self.attacking and self.attacking_temp is not None:
                self.attack(self.attacking_temp, troop)
                self.attacking = False
                self.attacking_temp = None
                self.moves_left -= 1
        # ATTACK button
        elif self.turn == 0 and self.action_bar.get_event(event) == 'Attack':
            if not self.attacking:
                self.attacking = True
                self.attacking_temp = None
                self.defending = False
                self.moving = False
                self.menu_bar.update_middle('Select Troop')
            else:
                self.attacking = False
                self.attacking_temp = None
        # DEFEND button
        elif self.turn == 0 and self.action_bar.get_event(event) == 'Defend':
            if not self.defending:
                self.attacking = False
                self.defending = True
                self.moving = False
            else:
                self.defending = False
        # MOVE button
        elif self.turn == 0 and self.action_bar.get_event(event) == 'Move Troops':
            if not self.moving:
                self.attacking = False
                self.defending = False
                self.moving = True
                self.moving_temp = None
            else:
                self.moving = False
                self.moving_temp = None
        # END TURN button
        elif self.turn == 0 and self.action_bar.get_event(event) == 'End Turn':
            self.turn = 1
        # FLEE button
        elif self.turn == 0 and self.action_bar.get_event(event) == 'Flee':
            self.fleeing = True
            self.persist_state()
            self.done = True

    def update(self, dt):
        # new round
        if self.new_round:
            self.action_bar.enable_all()
            self.ai_moves_left = min(len(self.ai_troops), 3)
            self.moves_left = min(len(self.player_troops), 3)
            self.add_boosts()
            self.new_round = False
        # check to end round
        if self.turn == 0 and self.moves_left < 1:
            self.turn = 1
        elif self.turn == 1:
            self.action_bar.disable_all()
            self.ai_turn()
        # update troops
        self.update_troops()
        # check to disable buttons
        if not self.flee:
            self.action_bar.disable_button('Flee')
        if len(self.player_troops) < 2:
            self.action_bar.disable_button('Move Troops')
        # update menu and action bar
        self.action_bar.update()
        self.update_menu_bar()
        # check for battle over
        if len(self.player_troops) < 1 or len(self.ai_troops) < 1:
            self.done = True
            self.persist_state()

    def render(self, surface):
        # fill screen
        surface.fill(pygame.Color("white"))
        # draw gui elements
        self.menu_bar.render(surface)
        pygame.draw.line(surface, pygame.Color("black"), (0, 40), (pygame.display.get_surface().get_width(), 40))
        self.action_bar.render(surface)
        pygame.draw.line(surface, pygame.Color("black"), (0, pygame.display.get_surface().get_height() - 120),
                         (pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height() - 120))
        # draw troops
        self.draw_troops(surface)

    def update_troops(self):
        for troop in self.player_troops:
            troop.update()
        for troop in self.ai_troops:
            troop.update()
        self.player_troops = [troop for troop in self.player_troops if troop.health > 0]
        self.ai_troops = [troop for troop in self.ai_troops if troop.health > 0]

    def update_menu_bar(self):
        self.menu_bar.update_left("Your Troops: " + str(len(self.player_troops)))
        self.menu_bar.update_right("Enemy Troops: " + str(len(self.ai_troops)))
        self.menu_bar.update_middle('Moves Left: ' + str(self.moves_left))
        if self.turn == 1:
            self.menu_bar.update_middle("AI's Turn")
        elif self.attacking and self.attacking_temp is None:
            self.menu_bar.update_middle('Select Troop')
        elif self.attacking and self.attacking_temp is not None:
            self.menu_bar.update_middle('Select Enemy Troop')
        elif self.defending:
            self.menu_bar.update_middle('Select Troop')
        elif self.moving and self.moving_temp is None:
            self.menu_bar.update_middle('Select 1st Troop')
        elif self.moving and self.moving_temp is not None:
            self.menu_bar.update_middle('Select 2nd Troop')

    def check_player_troop_clicks(self, event):
        for (i, troop) in enumerate(reversed(self.player_troops)):
            if troop.get_event(event):
                return self.player_troops.index(troop)
            if i >= 2:
                return None
        return None

    def check_ai_troop_clicks(self, event):
        for (i, troop) in enumerate(reversed(self.ai_troops)):
            if troop.get_event(event):
                return self.ai_troops.index(troop)
            if i >= 2:
                return None
        return None

    def attack(self, troop1, troop2):
        if self.turn == 0:
            self.ai_troops[troop2].health -= self.player_troops[troop1].attack - (
                        self.player_troops[troop1].attack * (self.ai_troops[troop2].defense / 100))
        else:
            self.player_troops[troop2].health -= self.ai_troops[troop1].attack - (
                        self.ai_troops[troop1].attack * (self.player_troops[troop2].defense / 100))

    def add_boosts(self):
        lists = [self.player_troops, self.ai_troops]
        for current in lists:
            for (i, troop) in enumerate(reversed(current)):
                if i == 0:
                    troop.attack_boost()
                if i == 1 and i == 2:
                    troop.defense_boost()
                if i == 3:
                    break

    def draw_troops(self, surface):
        # draw player troops
        for (i, troop) in enumerate(reversed(self.player_troops)):
            if i == 0:
                troop.set_pos(self.player_board.get_right_pos())
            if i == 1:
                troop.set_pos(self.player_board.get_top_pos())
            if i == 2:
                troop.set_pos(self.player_board.get_bottom_pos())
            if i == 3:
                break
            troop.render(surface)
        # draw ai troops
        for (i, troop) in enumerate(reversed(self.ai_troops)):
            if i == 0:
                troop.set_pos(self.ai_board.get_left_pos())
            if i == 1:
                troop.set_pos(self.ai_board.get_top_pos())
            if i == 2:
                troop.set_pos(self.ai_board.get_bottom_pos())
            if i == 3:
                break
            troop.render(surface)

    def ai_turn(self):
        if self.ai_moves_left > 0:
            if len(self.ai_troops) < 1 or len(self.player_troops) < 1:
                return
            troop1 = random.randint(0, min(2, len(self.ai_troops) - 1))
            value = random.uniform(0, 1)
            if value <= 0.15:
                self.ai_troops[len(self.ai_troops) - 1 - troop1].defense_boost()
            else:
                troop2 = random.randint(0, min(2, len(self.player_troops) - 1))
                troop2 = len(self.player_troops) - 1 - troop2
                self.attack(troop1, troop2)
            self.ai_moves_left -= 1
            time.sleep(1)
        else:
            self.turn = 0
            self.new_round = True

    def startup(self, persistent):
        # read in persistent info
        try:
            self.player_region = persistent['player_region']
            self.ai_region = persistent['ai_region']
            self.player = persistent['player']
            self.ai = persistent['ai']
            self.turn = persistent['turn']
            self.gameplay_data = [persistent['turn'], persistent['moves_left'], persistent['ai_moves_left'],
                                  persistent['new_round']]
            self.flee = persistent['flee']
            self.persist['difficulty'] = persistent['difficulty']
        except KeyError as e:
            print(e)
            sys.exit(1)
        # reset moves
        self.new_round = True
        # read in troops
        self.player_troops = []
        self.ai_troops = []
        for troop in range(self.player.troops[str(self.player_region)]):
            self.player_troops.append(Troop())
        for troop in range(self.ai.troops[str(self.ai_region)]):
            self.ai_troops.append(Troop(ai=True))

    def distribute_troops(self):
        # PLAYER attacked AI region
        if self.fleeing:
            self.player.troops[str(self.player_region)] = len(self.player_troops)
            self.ai.troops[str(self.ai_region)] = len(self.ai_troops)
        elif self.gameplay_data[0] == 0:
            self.player.troops[str(self.player_region)] = 0
            self.player.troops[str(self.ai_region)] = len(self.player_troops)
            self.ai.troops[str(self.ai_region)] = len(self.ai_troops)
        # AI attacked player region
        else:
            self.ai.troops[str(self.ai_region)] = 0
            self.ai.troops[str(self.player_region)] = len(self.ai_troops)
            self.player.troops[str(self.player_region)] = len(self.player_troops)

    def persist_state(self):
        self.distribute_troops()
        self.persist['player'] = self.player
        self.persist['ai'] = self.ai
        self.persist['turn'] = self.gameplay_data[0]
        self.persist['moves_left'] = self.gameplay_data[1]
        self.persist['ai_moves_left'] = self.gameplay_data[2]
        self.persist['new_round'] = self.gameplay_data[3]

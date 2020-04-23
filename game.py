# import modules
try:
    import pygame
    import sys
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


# main game object
class Game(object):

    def __init__(self, screen, states, start_state):
        self.done = False  # flag for determining when to change scenes
        self.screen = screen  # store window object
        self.clock = pygame.time.Clock()  # clock object for setting the game to 60 FPS
        self.fps = 60  # store fps value
        self.states = states  # store state dictionary
        self.state_name = start_state  # set start state
        self.state = self.states[self.state_name]  # set current state to start state

    # this is where all user events are handles
    def event_loop(self):
        # for every event that took place, call the event handler of the current scene
        for event in pygame.event.get():
            self.state.get_event(event)

    # swap scenes
    def flip_state(self):
        next_state = self.state.next_state  # read in next scene from current scene
        self.state.done = False  # reset "done" flag
        self.state_name = next_state  # set current state name to next state
        persistent = self.state.persist  # store persistent variables
        self.state = self.states[self.state_name]  # set current state to new state
        self.state.startup(persistent)  # call startup method from new state

    # updating game logic
    def update(self, dt):
        # if user closed window, then quit
        if self.state.quit:
            self.done = True
        # if its time to change scene, call flip state
        elif self.state.done:
            self.flip_state()
        # otherwise call update function for current scene
        self.state.update(dt)

    # call render function for current scene
    def render(self):
        self.state.render(self.screen)

    # main game loop
    def run(self):
        # while user has not closed window
        while not self.done:
            dt = self.clock.tick(self.fps)  # calculate delta time (although this isn't used, it's good to have)
            self.event_loop()  # handle user events
            self.update(dt)  # update game logic
            self.render()  # render to the screen
            pygame.display.update()  # refresh window

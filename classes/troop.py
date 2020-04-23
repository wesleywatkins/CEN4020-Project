try:
    import os
    import pygame
    import sys
    from gui.label import Label
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class Troop:

    def __init__(self, x=0, y=0, ai=False):
        self.x, self.y = x, y  # position to draw troop
        self.health = 100  # troop's health
        self.ai = ai  # flag for specifying if troop is ai
        self.default_stats()  # default all troops state
        # read in sprite image for troop
        # if ai, flip the image
        if self.ai:
            self.image = pygame.transform.flip(pygame.image.load(os.path.join('assets', 'ai_soldier.png')), True, False)
        else:
            self.image = pygame.image.load(os.path.join('assets', 'player_soldier.png'))
        # rectangle surrounding troop (useful for detecting clicks)
        self.rect = self.image.get_rect()
        self.rect.center = int(self.x), int(self.y)
        # label for drawing troops health
        self.health_label = Label(str(int(self.health)), size=15)

    # detect if troop was clicked on
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            return True
        return False

    # update health label to display current health
    def update(self):
        self.health_label.set_text(str(int(self.health)))

    # draw troop to screen
    def render(self, surface):
        surface.blit(self.image, self.rect)
        self.health_label.render(surface)

    # add attack boost to troop
    def attack_boost(self):
        self.attack += 10

    # add defense boost to troop
    def defense_boost(self):
        self.defense += 10

    # set stats to default values
    def default_stats(self):
        self.attack = 20
        self.defense = 10

    # set pos to draw troop
    def set_pos(self, pos):
        self.x, self.y = pos
        self.rect.center = int(self.x), int(self.y)
        if not self.ai:
            self.health_label.set_pos((int(self.x - self.rect.w/4), int(self.y - self.rect.h/2 - 15)))
        else:
            self.health_label.set_pos((int(self.x + self.rect.w / 4), int(self.y - self.rect.h / 2 - 15)))

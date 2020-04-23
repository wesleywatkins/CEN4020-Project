try:
    import pygame
    import sys
    from gui.label import Label
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class MenuBar:

    def __init__(self, x, y, width, height, left='', middle='', right='', size1=23, size2=23, size3=23):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size1 = size1
        self.size2 = size2
        self.size3 = size3
        self.update_left(left)
        self.update_middle(middle)
        self.update_right(right)

    def get_event(self, event):
        pass

    def update(self):
        pass

    def render(self, surface):
        pygame.draw.rect(surface, pygame.Color("white"), (self.x, self.y, self.width, self.height))
        self.left.render(surface)
        self.middle.render(surface)
        self.right.render(surface)

    def update_left(self, label):
        self.left = Label(label, x=(self.width * 0.2), y=(self.y + self.height / 2))
        self.left.set_size(self.size1)

    def update_middle(self, label):
        self.middle = Label(label, x=(self.width * 0.5), y=(self.y + self.height / 2))
        self.middle.set_size(self.size2)

    def update_right(self, label):
        self.right = Label(label, x=(self.width * 0.8), y=(self.y + self.height / 2))
        self.right.set_size(self.size3)

    def update_labels(self, labels):
        if len(labels) == 3:
            self.left = Label(labels[0], x=(self.width * 0.2), y=(self.y + self.height / 2))
            self.middle = Label(labels[1], x=(self.width * 0.5), y=(self.y + self.height / 2))
            self.right = Label(labels[2], x=(self.width * 0.8), y=(self.y + self.height / 2))

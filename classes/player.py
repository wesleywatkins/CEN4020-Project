

class Player:

    def __init__(self, name="Player"):
        self.name = name  # this is never used anymore in game
        self.troops = {}  # key = region #, value = # of troops
        self.reserve = 0  # reserve troops (+3 each round)
        self.home_region = None  # region originally chosen by user (if this region has 0 troops, the game is over)

    # loop through all the values in the troops directory
    # if a region has 0 troops, just remove it from the dictionary
    def update(self):
        for key in list(self.troops.keys()):
            if self.troops[key] < 1 and key != self.home_region:
                del self.troops[key]

    # if the user has reserve troops, add a specific amount
    # of troops to a specified region
    def add_troops(self, region, amount=1):
        if amount > self.reserve:
            return False
        if str(region) in self.troops.keys():
            self.troops[str(region)] += amount
            self.reserve -= amount
        return True

    # function from moving troops from one region
    # to another region
    def move_troops(self, from_region, to_region, amount=1):
        if str(from_region) not in self.troops.keys():
            return False
        if self.troops[str(from_region)] < amount:
            return False
        if str(to_region) in self.troops.keys():
            self.troops[str(to_region)] += amount
        else:
            self.troops[str(to_region)] = amount
        self.troops[str(from_region)] -= amount
        if self.troops[str(from_region)] < 1 and str(from_region) != self.home_region:
            del self.troops[str(from_region)]

    # remove specified number of troops from
    # a specified region
    def remove_troops(self, region, amount=1):
        if str(region) in self.troops.keys():
            self.troops[str(region)] -= amount
            if self.troops[str(region)] < 1 and str(region) != self.home_region:
                del self.troops[str(region)]

    # update home region
    def set_home_region(self, region):
        self.home_region = str(region)

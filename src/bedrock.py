from enum import Enum

class Richting(Enum):
    boven = 'up'
    rechts = 'right'
    onder = 'down'
    links = 'left'

class Cel(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.can_be_occupied_in_next_round = False

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def is_voedsel(self):
        return False

    def is_slang(self):
        return False

    def is_vrij(self):
        return True

    def als_letter(self):
        return ' '

    def position_string(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"


class VoedselCel(Cel):
    def is_voedsel(self):
        return True

    def als_letter(self):
        return '*'


class SlangCel(Cel):
    def is_slang(self):
        return True

    def is_vrij(self):
        return False

    def als_letter(self):
        return '^'


class SlangStaartCel(SlangCel):
    def is_slang(self):
        return True

    # tail is free in next move
    def is_vrij(self):
        return True
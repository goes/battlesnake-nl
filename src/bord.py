from enum import Enum
from debug import Debug


class Bord(object):
  
    def __init__(self, data):
        self.snakes = []
        self.data = data
        self.init_bord()

    def __str__(self):
        return 'Bord'

    def init_bord(self):
        self.mijn_slang_id = self.data['you']['id']
        n = self.data['board']['height']
        m = self.data['board']['width']
        self.bord_breedte = m
        self.bord_hoogte = n
        self.board = [[Cel(i, j) for i in range(m)] for j in range(n)]
        self.zet_voedsel()
        self.zet_slangen()


    def zet_voedsel(self):
        foods = self.data['board']['food']
        for f in foods:
            x = f['x']
            y = f['y']
            food = VoedselCel(x, y)
            self.board[x][y] = food

    def zet_slangen(self):
        snake_datas = self.data['board']['snakes']

        for snake_data in snake_datas:
            snake = self.parse_slang(snake_data)
            self.snakes.append(snake)
            self.update_board_with_snake(snake)

        for snake in self.snakes:
            for c in self.potential_next_moves(snake):
                if not (snake.id == self.mijn_slang_id):
                  (self.board[c.x][c.y]).can_be_occupied_in_next_round = True

    def parse_slang(self, snake_data):
        snake = Slang(snake_data['id'])
        for b in (snake_data['body'])[:-1]:
            snake.add_snakePart(SlangCel(b['x'], b['y']))
        tail = SlangStaartCel(snake_data['body'][-1]['x'],
                         snake_data['body'][-1]['y'])
        snake.add_snakePart(tail)
        return snake

    def update_board_with_snake(self, snake):
        for p in snake.snakeParts:
            self.board[p.x][p.y] = p

    def potential_next_moves(self, snake):
        kop = snake.snakeParts[0]
        Debug.log_with_action(kop.position_string(), 'Head + potential moves')
        mogelijke_cellen = []
        c = self.buur_links(kop)
        if c is not None:
            mogelijke_cellen.append(PotentialSnakePart(c.x, c.y))
        c = self.buur_rechts(kop)
        if c is not None:
            mogelijke_cellen.append(PotentialSnakePart(c.x, c.y))
        c = self.buur_boven(kop)
        if c is not None:
            mogelijke_cellen.append(PotentialSnakePart(c.x, c.y))
        c = self.buur_onder(kop)
        if c is not None:
            mogelijke_cellen.append(PotentialSnakePart(c.x, c.y))
        for i in mogelijke_cellen:
          Debug.log(i.position_string())
        return mogelijke_cellen

    def buur_in_richting (self, cell, direction):
      if direction == Richting.boven:
        return self.buur_boven(cell)
      elif direction == Richting.rechts:
        return self.buur_rechts(cell)
      elif direction == Richting.onder:
        return self.buur_onder(cell)
      elif direction == Richting.links:
        return self.buur_links(cell)

    def buren(self, cel):
        Debug.log_with_action(cel.position_string(), 'Cel + buren')
        neighbours = []
        c = self.buur_links(cel)
        if c is not None:
          neighbours.append(c)
        c = self.buur_rechts(cel)
        if c is not None:
          neighbours.append(c)
        c = self.buur_boven(cel)
        if c is not None:
          neighbours.append(c)
        c = self.buur_onder(cel)
        if c is not None:
          neighbours.append(c)
        for i in neighbours:
          Debug.log(i.position_string())
        return neighbours


    def buur_rechts(self, cel):
        if cel.x == self.bord_breedte -1:
            return None
        else:
            return self.cel(cel.x + 1, cel.y)

    def buur_links(self, cell):
        if cell.x == 0:
            return None
        else:
            return self.cel(cell.x - 1, cell.y)

    def buur_boven(self, cell):
        if cell.y == self.bord_hoogte -1:
            return None
        else:
            return self.cel(cell.x, cell.y + 1)

    def buur_onder(self, cell):
        if cell.y == 0:
            return None
        else:
            return self.cel(cell.x, cell.y - 1)

    def cellen_in_richting(self, cell, direction):
        if direction == Richting.boven:
            return self.cellen_in_richting_boven(cell)
        elif direction == Richting.onder:
            return self.cellen_in_richting_onder(cell)
        elif direction == Richting.links:
            return self.cellen_in_richting_links(cell)
        elif direction == Richting.rechts:
            return self.cellen_in_richting_rechts(cell)

    def cellen_in_richting_links(self, cell):
        cells = []
        for i in reversed(range(0, cell.x)):
            cells.append(self.cel(i, cell.y))
        return cells

    def cellen_in_richting_rechts(self, cell):
        cells = []
        for i in range(cell.x + 1, self.bord_breedte):
            cells.append(self.cel(i, cell.y))
        return cells

    def cellen_in_richting_boven(self, cell):
        cells = []
        for i in range(cell.y + 1, self.bord_hoogte):
            cells.append(self.cel(cell.x, i))
        return cells

    def cellen_in_richting_onder(self, cell):
        cells = []
        for i in reversed(range(0, cell.y)):
            cells.append(self.cel(cell.x, i))
        return cells

    def number_of_free_cells(self, cell, direction):
        cells = self.cellen_in_richting(cell, direction)
        count = 0
        for c in cells:
            if not c.is_vrij():
                return count
            else:
                count = count + 1
        return count

    def is_food_in_direction(self, cell, direction):
        cells = self.cellen_in_richting(cell, direction)
        for c in cells:
            if c.is_food():
                return True
            elif c.is_slang():
                return False
        return False

    def distance_to_food(self, cell, direction):
        cells = self.cellen_in_richting(cell, direction)
        count = 0
        for c in cells:
            if c.is_vrij():
                if c.is_food():
                    return count + 1
                else:
                    count = count + 1
            elif c.is_slang():
                return count
        return count

    def cel(self, x, y):
        return self.board[x][y]

    def is_blocked(self, cell, direction):
        if self.number_of_free_cells(cell, direction) == 0:
          return True
          
        if direction == Richting.boven:
            return self.is_blocked_up(cell)
        elif direction == Richting.rechts:
            return self.is_blocked_right(cell)
        elif direction == Richting.onder:
            return self.is_blocked_down(cell)
        elif direction == Richting.links:
            return self.is_blocked_left(cell)

    def is_blocked_left(self, cell):
        if cell.x == 0:
            return True
        else:
            return self.cel(cell.x - 1, cell.y).is_slang()

    def is_blocked_right(self, cell):
        if cell.x == self.bord_breedte - 1:
            return True
        else:
            return self.cel(cell.x + 1, cell.y).is_slang()

    def is_blocked_up(self, cell):
        if cell.y == self.bord_hoogte - 1:
            return True
        else:
            return self.cel(cell.x, cell.y + 1).is_slang()

    def is_blocked_down(self, cell):
        if cell.y == 0:
            return True
        else:
            return self.cel(cell.x, cell.y - 1).is_slang()

    def print_board(self):
        str = ""
        for y in reversed(range(0, self.bord_hoogte)):
            for x in range(0, self.bord_breedte):
                str = str + self.cel(x, y).als_letter() + " "
            str = str + "\n"
        print(str)



class Cel(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.can_be_occupied_in_next_round = False

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def bevat_eten(self):
        return False

    def is_slang(self):
        return False

    def is_vrij(self):
        return True

    def als_letter(self):
        if self.can_be_occupied_in_next_round:
          return '?'
        return ' '

    def position_string(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"


class PotentialSnakePart(Cel):

    def is_vrij(self):
        return False

    def als_letter(self):
        return '?'


class VoedselCel(Cel):
    def bevat_eten(self):
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


class Richting(Enum):
    boven = 'up'
    rechts = 'right'
    onder = 'down'
    links = 'left'

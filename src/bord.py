from bedrock import Richting, Cel, VoedselCel
from slang import Slang
from debug import Debug

class Bord(object):
  
    def __init__(self, data):
        self.slangen = []
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
        self.zet_voedsel_op_bord()
        self.zet_slangen_op_bord()

    # voedsel parsen en op het bord zetten
    def zet_voedsel_op_bord(self):
        foods = self.data['board']['food']
        for f in foods:
            x = f['x']
            y = f['y']
            food = VoedselCel(x, y)
            self.board[x][y] = food

    # geef de cel op positie (x,y)
    # elke plaats op het bord is een Cel (of een subklasse)
    def cel(self, x, y):
        return self.board[x][y]

    # slangen parsen en op het bord zetten
    # dit zijn alle slangen, ook de eigen slang
    def zet_slangen_op_bord(self):
        snake_datas = self.data['board']['snakes']

        for snake_data in snake_datas:
            slang = Slang(snake_data)
            self.zet_slang_op_bord(slang)

    def zet_slang_op_bord(self, snake):
        self.slangen.append(snake)
        for segment in snake.segmenten:
            self.board[segment.x][segment.y] = segment

    # protocol om buur cellen voor een bepaalde cel te berekenen
    # buren(cel)
    # buur_in_richting(cel, richting)
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

    # protocol om alle cellen in een bepaalde richting tov een cel te berekenen
    def cellen_in_richting(self, cell, direction):
        if direction == Richting.boven:
            return self.cellen_in_richting_boven(cell)
        elif direction == Richting.onder:
            return self.cellen_in_richting_onder(cell)
        elif direction == Richting.links:
            return self.cellen_in_richting_links(cell)
        elif direction == Richting.rechts:
            return self.cellen_in_richting_rechts(cell)

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

    # geef het aantal vrije cellen in een bepaalde richting tov een cel
    def aantal_vrije_cellen(self, cell, direction):
        cells = self.cellen_in_richting(cell, direction)
        count = 0
        for c in cells:
            if not c.is_vrij():
                return count
            else:
                count = count + 1
        return count

    def is_er_eten_in_richting(self, cell, direction):
        cells = self.cellen_in_richting(cell, direction)
        for c in cells:
            if c.is_food():
                return True
            elif c.is_slang():
                return False
        return False

    def afstand_tot_voedsel(self, cell, direction):
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

    def is_geblokkeerd_in_richting(self, cell, richting):
        if self.aantal_vrije_cellen(cell, richting) == 0:
          return True
        return not self.buur_in_richting(cell, richting).is_vrij()

    def print_board(self):
        str = ""
        for y in reversed(range(0, self.bord_hoogte)):
            for x in range(0, self.bord_breedte):
                str = str + self.cel(x, y).als_letter() + " "
            str = str + "\n"
        print(str)

'''
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
'''



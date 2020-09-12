from bord import Bord
from bedrock import Richting

class SlangenBrein(object):

    possible_moves = ["up", "right", "down", "left"]
    alle_richtingen = [Richting.boven, Richting.onder, Richting.links, Richting.rechts]

    # initialiseer alles vanuit json
    def __init__(self, dataJson, bord):
        self.bord = bord
        self.data = dataJson
        self.slang_x = self.data['you']['head']['x']
        self.slang_y = self.data['you']['head']['y']
        self.gezondheid = self.data['you']['health']

    # berekenen volgende zet
    # het principe: per richting bepqql je een numerieke waarde, de richting met de hoogste waarde is de richting van de volgende zet

    def volgende_zet(self):
        richting = self.bereken_volgende_zet()
        return richting.value

    def bereken_volgende_zet(self):
        self.bord.print_board()
        richtingen = {}
        for richting in self.alle_richtingen:
            richtingen[richting] = self.bereken_waarde_voor_richting(richting)
        print(richtingen)
        new_dir = max(richtingen, key=richtingen.get)
        return new_dir

    def heeft_honger(self):
        return self.gezondheid < 40

    def bereken_waarde_voor_richting(self, richting):
        if self.is_blocked(richting):
            return -1000
            
        #beginnend bij de kop    
        cellen = self.bord.cellen_in_richting(self.kop(), richting)
        waarde = 0
        for c in cellen:
            if c.is_slang():
                return waarde
            waarde = waarde + self.celwaarde(cel)
        return waarde
      
    def calculate_next_move_random(self):
        self.free_Richtings()
        last_move_index = self.possible_moves.index(self.last_move())
        new_index = (last_move_index + 1) % 4
        new_move = self.possible_moves[new_index]
        return new_move

    # hoeveel waarde geef je een cel 
    def celwaarde(self, cel):
        if cel.is_slang():
            return -10
        elif cel.is_food():
            if self.heeft_honger:
                return 4
            else:
                return 1
        else:
            return 4 - len(self.bord.buren(cel))

 




    def kop(self):
        return self.bord.cel(self.slang_x, self.slang_y)

    def is_blocked(self, richting):
        return self.bord.is_blocked(self.kop(), richting)

    def bord_hoogte(self):
        return self.bord.bord_hoogte

    def bord_breedte(self):
        return self.bord.bord_breedte

'''
OLD

        if richting == Richting.boven:
            return self.waarde_boven()
        elif richting == Richting.rechts:
            return self.waarde_rechts()
        elif richting == Richting.onder:
            return self.waarde_onder()
        elif richting == Richting.links:
            return self.waarde_links()


    def waarde_boven(self):
        aantal = 0
        for y in range(self.slang_y + 1, self.bord_hoogte()):
            cel = self.bord.cel(self.slang_x, y)
            if cel.is_slang():
                return aantal
            aantal = aantal + self.celwaarde(cel)
        return aantal

    def waarde_onder(self):
        aantal = 0
        for y in reversed(range(self.slang_y)):
            cell = self.bord.cel(self.slang_x, y)
            if cell.is_slang():
                return aantal
            aantal = aantal + self.celwaarde(cell)
        return aantal

    def waarde_links(self):
        aantal = 0
        for x in reversed(range(self.slang_x)):
            cell = self.bord.cel(x, self.slang_y)
            if cell.is_slang():
                return aantal
            aantal = aantal + self.celwaarde(cell)
        return aantal

    def waarde_rechts(self):
        aantal = 0
        for x in range(self.slang_x + 1, self.bord_breedte()):
            cell = self.bord.cel(x, self.slang_y)
            if cell.is_slang():
                return aantal
            aantal = aantal + self.celwaarde(cell)
        return aantal
        
'''

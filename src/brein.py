from bord import Bord
from bedrock import Richting

class SlangenBrein(object):

    possible_moves = ["up", "right", "down", "left"]
    alle_richtingen = [Richting.boven, Richting.onder, Richting.links, Richting.rechts]

    # initialiseer alles vanuit json
    def __init__(self, dataJson, bord):
        self.bord = bord
        self.data = dataJson
        self.id = self.data['you']['id']
        self.slang_x = self.data['you']['head']['x']
        self.slang_y = self.data['you']['head']['y']
        self.gezondheid = self.data['you']['health']

    @classmethod
    def uiterlijk(cls):
      return {
            "apiversion": "1",
            "author": "goes",
            "color": "#c70039",
            "head": "tongue",
            "tail": "skinny",
        }

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

    # als ik honger heb wil ik sneller naar eten zoeken, maar ook niet te snel want hoe langer ik word hoe gemakkelijker mijzelf vast zet
    def heeft_honger(self):
        return self.gezondheid < 40

    # de berekening
    def bereken_waarde_voor_richting(self, richting):
        if self.is_geblokkeerd(richting):
            return -1000
            
        #beginnend bij de kop    
        cellen = self.bord.cellen_in_richting(self.kop(), richting)
        waarde = 0
        for c in cellen:
            if c.is_slang():
                return waarde
            waarde = waarde + self.celwaarde(c)
        return waarde

    # hoeveel waarde geef je een cel 
    def celwaarde(self, cel):
        if cel.is_slang():
            return -10
        elif cel.is_voedsel():
            if self.heeft_honger:
                return 4
            else:
                return 1
        else:
            return 4 - len(self.bord.buren(cel))

    def kop(self):
        return self.bord.cel(self.slang_x, self.slang_y)

    def is_geblokkeerd(self, richting):
        return self.bord.is_geblokkeerd_in_richting(self.kop(), richting)

    def andere_slangen(self):
        return filter(lambda slang: slang.id != self.id, self.bord.slangen)

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

from brein import SlangenBrein

# Pelle is very hungry all the time
class Pelle(SlangenBrein):
  
  # https://docs.battlesnake.com/references/personalization
  @classmethod
  def uiterlijk(cls):
    return {
      "apiversion": "1",
      "author": "goes",
      "color": "#00b300",
      "head": "fang",
      "tail": "hook",
      }

  def heeft_honger(self):
    return self.gezondheid < 40

  def andere_slangekoppen(self):
    return map(lambda slang: slang.segmenten[0], self.andere_slangen())

  def is_buur_van_andere_slangekop(self, cel):
    gevaarlijke_buur_cellen = []
    for sk in self.andere_slangekoppen():
      for buur in self.bord.buren(sk):
        gevaarlijke_buur_cellen.append(buur)
    return cel in gevaarlijke_buur_cellen

  def bereken_waarde_voor_richting(self, richting):
    waarde = super().bereken_waarde_voor_richting(richting)
    cel = self.bord.buur_in_richting(self.kop(), richting)  
    # pelle is slim, als de volgende cel in de buurt is van een andere slangekop dan vermijden we die richting
    if cel is not None:
      if self.is_buur_van_andere_slangekop(cel):
        waarde = waarde - 250
    return waarde

  # hoeveel waarde geef je een cel 
  # de som van de waarden van de cellen bepaalt de waarde van een bepaalde richting
  def celwaarde(self, cel):
    if cel.is_slang():
        return -10
    elif cel.is_voedsel():
        if self.heeft_honger():
          return 20
        else:
          return 2
    else:
        return 10 - (2 * len(self.bord.buren(cel)))
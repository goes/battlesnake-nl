from brein import SlangenBrein
import random

class Soetkin(SlangenBrein):
  
  @classmethod
  def uiterlijk(cls):
    return {
      "apiversion": "1",
      "author": "soetkin",
      "color": "#FFC0CB",
      "head": "safe",
      "tail": "round-bum",
      }

  def bereken_waarde_voor_richting(self, richting):
     if self.is_geblokkeerd(richting):
            return -1000
            
     # soetkin kiest willekeurig    
     return random.randint(0, 100)
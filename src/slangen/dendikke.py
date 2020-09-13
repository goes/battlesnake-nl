from brein import SlangenBrein

# Den Dikke heeft altijd honger
class DenDikke(SlangenBrein):
  
  # https://docs.battlesnake.com/references/personalization
  @classmethod
  def uiterlijk(cls):
    return {
      "apiversion": "1",
      "author": "goes",
      "color": "#00b300",
      "head": "pixel",
      "tail": "pixel",
      }

  def heeft_honger(self):
    return True
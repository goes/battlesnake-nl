# from src.brein import SlangenBrein

import context
import json
from pathlib import Path
from src.bord import Bord
from src.brein import SlangenBrein


path = Path(__file__).parent / "example.json"
with open(path) as json_file:
    data = json.load(json_file)

bord = Bord(data)
slang = SlangenBrein(data, bord)
move = slang.volgende_zet()
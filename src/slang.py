from bedrock import SlangCel, SlangStaartCel

class Slang():

    def __init__(self, json):
        self.segmenten = []
        self.id = json['id']
        for b in (json['body'])[:-1]:
            self.voeg_segment_toe(SlangCel(b['x'], b['y']))
        staart = SlangStaartCel(json['body'][-1]['x'], json['body'][-1]['y'])
        self.voeg_segment_toe(staart)

    def voeg_segment_toe(self, sp):
        self.segmenten.append(sp)
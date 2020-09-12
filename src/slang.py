from bord import Cell
class Slang():
    def __init__(self, json):
        self.id = json['id']
        for b in (json['body'])[:-1]:
            self.add_snakePart(SnakePart(b['x'], b['y']))
        tail = SnakeTail(snake_data['body'][-1]['x'],
                         snake_data['body'][-1]['y'])
        snake.add_snakePart(tail)
        return snake

    def add_snakePart(self, sp):
        self.snakeParts.append(sp)
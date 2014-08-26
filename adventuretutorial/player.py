from adventuretutorial import items

__author__ = 'Phillip Johnson'


class Player():
    inventory = [items.Gold(15), items.Rock()]
    hp = 100
    location_x, location_y = (2, 4)
    victory = False
    available_actions = []

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')



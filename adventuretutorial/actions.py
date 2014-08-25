"""Describes the actions a player can make in the game"""
__author__ = 'Phillip Johnson'

import random

from adventuretutorial import items
from adventuretutorial.game import World


class Action():
    """The base class for all actions"""
    def __init__(self, name, ends_turn, hotkey):
        """Creates a new action

        :param name: the name of the action
        :param ends_turn: True if the player is expected to move after this action else False
        :param hotkey: The keyboard key the player should use to initiate this action
        """
        self.ends_turn = ends_turn
        self.hotkey = hotkey
        self.name = name

    def do(self, player):
        """Process the action"""
        raise NotImplementedError()

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)


class MoveAction(Action):
    """A base class action that represents the Player moving in the world space"""
    def __init__(self, name, hotkey, dx, dy):
        """Creates a new move action

        :param dx: the change in the x-coordinate position of the Player
        :param dy: the change in the y-coordinate position of the Player
        """
        self.dx = dx
        self.dy = dy
        super().__init__(name=name, ends_turn=True, hotkey=hotkey)

    def do(self, player):
        """Changes the position of the player and displays the information from the new tile"""
        player.location_x += self.dx
        player.location_y += self.dy
        print(World.instance().tile_exists(player.location_x, player.location_y).intro_text())


class MoveNorth(MoveAction):
    def __init__(self):
        super().__init__(name='Move north', hotkey='n', dx=0, dy=-1)


class MoveSouth(MoveAction):
    def __init__(self):
        super().__init__(name='Move south', hotkey='s', dx=0, dy=1)


class MoveEast(MoveAction):
    def __init__(self):
        super().__init__(name='Move east', hotkey='e', dx=1, dy=0)


class MoveWest(MoveAction):
    def __init__(self):
        super().__init__(name='Move west', hotkey='w', dx=-1, dy=0)


class ViewInventory(Action):
    """Prints the player's inventory"""
    def __init__(self):
        super().__init__(name='View inventory', ends_turn=False, hotkey='i')

    def do(self, player):
        player.print_inventory()


class Attack(Action):
    def __init__(self, enemy):
        self.enemy = enemy
        super().__init__(name="Attack", ends_turn=False, hotkey='a')

    def do(self, player):
        best_weapon = None
        max_dmg = 0
        for i in player.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        print("You use {} against {}!".format(best_weapon.name, self.enemy.name))
        self.enemy.hp -= best_weapon.damage
        if not self.enemy.is_alive():
            print("You killed {}!".format(self.enemy.name))
        else:
            print("{} HP is {}.".format(self.enemy.name, self.enemy.hp))


class Flee(Action):
    """Moves the player randomly to an adjacent tile"""
    def __init__(self, tile):
        self.tile = tile
        super().__init__(name="Flee", ends_turn=True, hotkey='f')

    def do(self, player):
        available_moves = self.tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        available_moves[r].do(player)
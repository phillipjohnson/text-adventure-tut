"""Describes the actions a player can make in the game"""
__author__ = 'Phillip Johnson'

import random

from adventuretutorial import items
import world


class Action():
    """The base class for all actions"""
    def __init__(self, name, ends_turn, hotkey, player):
        """Creates a new action

        :param name: the name of the action
        :param ends_turn: True if the player is expected to move after this action else False
        :param hotkey: The keyboard key the player should use to initiate this action
        :param player: The player object on which this action should be executed
        """
        self.ends_turn = ends_turn
        self.hotkey = hotkey
        self.name = name
        self.player = player

    def execute(self):
        """Process the action"""
        raise NotImplementedError()

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)


class MoveAction(Action):
    """A base class action that represents the Player moving in the world space"""
    def __init__(self, name, hotkey, player, dx, dy):
        """Creates a new move action

        :param dx: the change in the x-coordinate position of the Player
        :param dy: the change in the y-coordinate position of the Player
        """
        self.dx = dx
        self.dy = dy
        super().__init__(name=name, ends_turn=True, hotkey=hotkey, player=player)

    def execute(self):
        """Changes the position of the player and displays the information from the new tile"""
        self.player.location_x += self.dx
        self.player.location_y += self.dy
        print(world.tile_exists(self.player.location_x, self.player.location_y).intro_text())


class MoveNorth(MoveAction):
    def __init__(self, player):
        super().__init__(name='Move north', hotkey='n', player=player, dx=0, dy=-1)


class MoveSouth(MoveAction):
    def __init__(self, player):
        super().__init__(name='Move south', hotkey='s', player=player, dx=0, dy=1)


class MoveEast(MoveAction):
    def __init__(self, player):
        super().__init__(name='Move east', hotkey='e', player=player, dx=1, dy=0)


class MoveWest(MoveAction):
    def __init__(self, player):
        super().__init__(name='Move west', hotkey='w', player=player, dx=-1, dy=0)


class ViewInventory(Action):
    """Prints the player's inventory"""
    def __init__(self, player):
        super().__init__(name='View inventory', ends_turn=False, hotkey='i', player=player)

    def execute(self):
        self.player.print_inventory()


class Attack(Action):
    def __init__(self, player, enemy):
        self.enemy = enemy
        super().__init__(name="Attack", ends_turn=False, hotkey='a', player=player)

    def execute(self):
        best_weapon = None
        max_dmg = 0
        for i in self.player.inventory:
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
    def __init__(self, player, tile):
        self.tile = tile
        super().__init__(name="Flee", ends_turn=True, hotkey='f', player=player)

    def execute(self):
        available_moves = self.tile.adjacent_moves(self.player)
        r = random.randint(0, len(available_moves) - 1)
        available_moves[r].execute()
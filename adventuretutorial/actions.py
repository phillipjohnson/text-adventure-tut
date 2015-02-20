"""Describes the actions a player can make in the game"""
__author__ = 'Phillip Johnson'

from player import Player


class Action():
    """The base class for all actions"""
    def __init__(self, method, name, hotkey, **kwargs):
        """Creates a new action

        :param method: the function object to execute
        :param name: the name of the action
        :param ends_turn: True if the player is expected to move after this action else False
        :param hotkey: The keyboard key the player should use to initiate this action
        """
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)


class MoveNorth(Action):
    def __init__(self):
        super().__init__(method=Player.move_north, name='Move north', hotkey='n')


class MoveSouth(Action):
    def __init__(self):
        super().__init__(method=Player.move_south, name='Move south', hotkey='s')


class MoveEast(Action):
    def __init__(self):
        super().__init__(method=Player.move_east, name='Move east', hotkey='e')


class MoveWest(Action):
    def __init__(self):
        super().__init__(method=Player.move_west, name='Move west', hotkey='w')


class ViewInventory(Action):
    """Prints the player's inventory"""
    def __init__(self):
        super().__init__(method=Player.print_inventory, name='View inventory', hotkey='i')


class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attack", hotkey='a', enemy=enemy)


class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Flee", hotkey='f', tile=tile)
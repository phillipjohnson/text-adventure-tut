"""
A simple text adventure designed as a learning experience for new programmers.
"""
__author__ = 'Phillip Johnson'
from adventuretutorial.player import Player


class World:
    """A singleton that provides access to the world space."""
    _instance = None

    def __init__(self):
        self._world = {}
        self.load_tiles()

    @staticmethod
    def instance():
        """Returns the singleton instance"""
        if World._instance is None:
            World._instance = World()
        return World._instance

    def tile_exists(self, x, y):
        """Returns the tile at the given coordinates or None if there is no tile.

        :param x: the x-coordinate in the worldspace
        :param y: the y-coordinate in the worldspace
        :return: the tile at the given coordinates or None if there is no tile
        """
        return self._world.get((x, y))

    def load_tiles(self):
        """Parses a file that describes the world space into the World object"""
        with open('resources/map.txt', 'r') as f:
            rows = f.readlines()
        x_max = len(rows[0].split('\t'))
        for y in range(len(rows)):
            cols = rows[y].split('\t')
            for x in range(x_max):
                tile_name = cols[x].replace('\n', '')
                self._world[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)


def game_loop():
    player = Player()
    world = World.instance()
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print("Choose an action:\n")
            available_actions = room.available_actions(player)
            for a in available_actions:
                print(a)
            action_input = input('Action: ')
            for a in available_actions:
                if action_input == a.hotkey:
                    a.execute()


if __name__ == "__main__":
    game_loop()
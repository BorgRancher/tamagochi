"""engine.py
This module holds the core class to run and manage the game at runtime
"""
import pyxel
from core import Draw, Animation, Collision


class Tamagotchi:
    """ Tamagotchi game class manager using Pyxel library as the engine """

    def __init__(self):
        # setup mouse and screen
        self.screen = (100, 100)
        self.room = {'w': self.screen[0], 'h': self.screen[1] - 22, 'current': 0}  # minus the room wall height
        pyxel.init(self.screen[0], self.screen[1], caption="Tamagotchi")
        pyxel.mouse(False)

        # setup character
        self.player = {'x': 0, 'y': 25, 'w': 17, 'h': 22, 'direction': -1}

        # load assets/collisions/animations
        self.collision = Collision()
        self.draw_manager = Draw(collision=self.collision)
        self.animation = Animation()

    def run(self):
        """ Start pyxel engine """
        pyxel.run(self.update, self.draw)

    def check_colliders(self, move_x: int = 0, move_y: int = 0) -> bool:
        """
        Checks collision in future position of player/character
        :param move_x: how many steps to move on the x origin
        :param move_y: how many steps to move on the y origin
        :return: True if colliding else False
        """
        results = self.collision.does_player_collide(
            player_x=self.player['x'] + move_x,
            player_y=self.player['y'] + move_y,
            player_h=self.player['h'],
            player_w=self.player['w']
        )
        return results

    def move_character(self):
        """
        Character movement controller
        """
        self.player['direction'] = -1
        if pyxel.btn(pyxel.KEY_LEFT):
            if 0 <= self.player['x'] - 1 <= self.room['w'] and not self.check_colliders(move_x=-1):
                self.player['x'] -= 1
                self.player['direction'] = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            if 0 <= self.player['x'] + 1 <= self.room['w'] - self.player['w'] and not self.check_colliders(move_x=1):
                self.player['x'] += 1
                self.player['direction'] = 1
        if pyxel.btn(pyxel.KEY_UP):
            if 0 <= self.player['y'] - 1 <= self.room['h'] and not self.check_colliders(move_y=-1):
                self.player['y'] -= 1
                self.player['direction'] = 2
        if pyxel.btn(pyxel.KEY_DOWN):
            if 0 <= self.player['y'] + 1 <= self.room['h'] and not self.check_colliders(move_y=1):
                self.player['y'] += 1
                self.player['direction'] = 3

    def change_room(self):
        """
        Game room change controller
        rooms = 0:bedroom, 1:kitchen, 2:bathroom
        """
        if pyxel.btnp(pyxel.KEY_1):
            self.room['current'] = 0
        if pyxel.btnp(pyxel.KEY_2):
            self.room['current'] = 1
        if pyxel.btnp(pyxel.KEY_3):
            self.room['current'] = 2

    def update(self):
        """ Game logic """
        self.move_character()
        self.change_room()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        """ Pyxel update screen changes """
        # clear screen
        pyxel.cls(0)

        # draw assets in current room
        self.draw_manager.draw_room(room=self.room['current'])

        # # draw player
        frame = self.animation.get_walk_animation(direction=self.player['direction'])
        self.draw_manager.draw_player(x=self.player['x'], y=self.player['y'], frame=frame)

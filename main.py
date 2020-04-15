# python modules:
import random
# kivy modules:
from kivy.app import App
from kivy import properties as kp
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Line, Ellipse
from kivy.factory import Factory
    # uix:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
# mine:
import settings


class GameOverPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__()
        print("kwargs", kwargs)
        self.size_hint = 0.5, 0.5
        self.title = "%s WIN" % kwargs.get("who_win", "")

        new_game_button = Button(text="New Game")
        new_game_button.bind(on_press=self.dismiss)
        new_game_button.bind(on_press=kwargs["game"].new_game)
        self.add_widget(new_game_button)


class Game(Screen):
    all_crosses = kp.ListProperty()
    all_circles = kp.ListProperty()
    player = kp.StringProperty("")
    mob = kp.StringProperty("")
    game_over = kp.BooleanProperty(False)
    who_is_first = kp.StringProperty("mob")

    def __init__(self):
        super().__init__()
        self.bind(size=self.draw_lines)
        self.bind(size=self.draw_crosses)
        self.bind(size=self.draw_circles)
        self.new_game()

    def new_game(self, *args):
        print("\nnew_game", args)
        self.all_circles = []
        self.all_crosses = []
        self.draw_lines()
        self.game_over = False
        self.who_is_first = "player" if self.who_is_first == "mob" else "mob"
        print("self.who_is_first", self.who_is_first)
        if self.who_is_first == "player":
            self.player = "cross"
            self.mob = "circle"
        elif self.who_is_first == "mob":
            print("is mob")
            self.player = "circle"
            self.mob = "cross"
            new_coord = self.calc_next_mob_coord()
            self.draw_symbol("cross", new_coord)
        print("self.player", self.player)

    def calc_lines(self):
        X = self.width
        Y = self.height
        x = X / 3
        y = Y / 3
        return [
            [x, 0, x, Y],
            [2 * x, 0, 2 * x, Y],
            [0, y, X, y],
            [0, 2 * y, X, 2 * y],
        ]

    def draw_lines(self, *args):
        print("draw_lines()", self.size)
        self.canvas.clear()
        lines = self.calc_lines()
        with self.canvas:
            for line in lines:
                Line(points=line)

    def calc_cross(self, coord_x, coord_y):
        X = self.width
        Y = self.height
        x = X / 3
        y = Y / 3
        offset_x = coord_x * x
        offset_y = coord_y * y
        return [
            [offset_x, offset_y, x + offset_x, y + offset_y],
            [x + offset_x, offset_y, offset_x, y + offset_y]
        ]

    def draw_crosses(self, *args):
        with self.canvas:
            for cross_coord in self.all_crosses:
                print("cross_coord", cross_coord)
                lines = self.calc_cross(*cross_coord)
                for line in lines:
                    Line(points=line)

    def calc_circle(self, coord_x, coord_y):
        # print("calc_circle(%s, %s)" % (coord_x, coord_y))
        # print(self.size)
        X = self.width
        Y = self.height
        x = X / 3
        y = Y / 3
        # print(x, y)
        offset_x = coord_x * x
        offset_y = coord_y * y
        return (offset_x, offset_y, x, y)

    def draw_circles(self, *args):
        print("draw_circles()", args, self.all_circles)
        with self.canvas:
            for circle_coord in self.all_circles:
                Line(ellipse=self.calc_circle(*circle_coord))

    def calc_coord(self, pos_x, pos_y):
        X = self.width
        Y = self.height
        x = X / 3
        y = Y / 3
        coord_x = pos_x // x
        coord_y = pos_y // y
        return coord_x, coord_y

    def draw_symbol(self, symbol, new_coord):
        print("\ndraw_symbol(%s, %s)" % (symbol, new_coord))

        if symbol == "cross":
            coords = self.all_crosses
            function = self.draw_crosses
        elif symbol == "circle":
            coords = self.all_circles
            function = self.draw_circles

        if new_coord in self.all_crosses + self.all_circles:
            return True
        coords.append(new_coord)
        function()
        if self.check_if_win(coords):
            print("\n\n%s win\n\n\n" % symbol)
            Factory.GameOverPopup(game=self, who_win=symbol).open()
            self.game_over = True
            return True
        return False


    def on_touch_down(self, *args):
        print("on_touch_down", args[0].pos)
        print("self.all_circles", self.all_circles)
        if self.game_over:
            return

        pos = args[0].pos

        # Player:
        new_coord = self.calc_coord(*pos)
        print("self.player", self.player)
        if self.draw_symbol(self.player, new_coord):
            return

        # Mob:
        new_coord = self.calc_next_mob_coord()
        self.draw_symbol(self.mob, new_coord)

    def calc_next_mob_coord(self):
        print("calc_next_mob_coord()")
        avail_coords = [(x, y) for x in range(3) for y in range(3)]
        print("avail_coords", avail_coords)
        print("self.all_crosses + self.all_circles", self.all_crosses + self.all_circles)
        for coord in self.all_crosses + self.all_circles:
            print("coord", coord)
            avail_coords.remove(coord)
        print("avail_coords", avail_coords)
        if avail_coords:
            choosed_coord = random.choice(avail_coords)
            print("choosed_coord", choosed_coord)
            return choosed_coord

    def check_if_win(self, who):
        print("check_if_win(%s)" % who)
        all_possible_wins = [
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)]
        ]
        if len(who) < 3:
            return False
        for possible_win in all_possible_wins:
            # print("possible_win", possible_win)
            for possible_coord in possible_win:
                # print("possible_coord", possible_coord)
                # print(possible_coord not in who, possible_coord, who)
                if possible_coord not in who:
                    break
            else:
                # print(possible_win)
                return True
        return False


class GameApp(App):

    def build(self):
        self.game = Game()
        Window.size = settings.SIZE
        print(Window.size)
        self.game.size = settings.SIZE
        self.game.draw_lines()
        return self.game


if __name__ == "__main__":
    game_app = GameApp()
    game_app.run()
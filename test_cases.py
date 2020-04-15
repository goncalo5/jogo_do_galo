import time
import unittest
import main

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.all_coords = [(x, y) for x in range(3) for y in range(3)]

    def test_calc_lines(self):
        game = main.Game()
        # print(game.size)
        game.size = (300, 300)
        # print(game.size)
        sol = [
            [100, 0, 100, 300],
            [200, 0, 200, 300],
            [0, 100, 300, 100],
            [0, 200, 300, 200],
        ]
        self.assertEqual(game.calc_lines(), sol)

    def test_calc_cross(self):
        game = main.Game()
        # print(game.size)
        game.size = (300, 300)
        # print(game.size)
        sol = [
            [0, 0, 100, 100],
            [100, 0, 0, 100],
        ]
        self.assertEqual(game.calc_cross(0, 0), sol)
        sol = [
            [100, 100, 200, 200],
            [200, 100, 100, 200],
        ]
        self.assertEqual(game.calc_cross(1, 1), sol)

    def test_calc_circle(self):
        game = main.Game()
        # print(game.size)
        game.size = (300, 300)
        # print(game.size)
        sol = (0, 0, 100, 100)
        self.assertEqual(game.calc_circle(0, 0), sol)
        sol = (100, 100, 100, 100)
        self.assertEqual(game.calc_circle(1, 1), sol)

    def test_calc_coord(self):
        game = main.Game()
        game.size = (300, 300)
        sol = (0, 0)
        self.assertEqual(game.calc_coord(55, 13), sol)
        self.assertEqual(game.calc_coord(55, 310), None)
        self.assertEqual(game.calc_coord(310, 10), None)

    def test_calc_next_mob_coord(self):
        game = main.Game()
        game.all_crosses = [(0, 0)]
        self.assertNotEqual(game.calc_next_mob_coord(), (0, 0))
        self.assertIn(game.calc_next_mob_coord(), self.all_coords)
        game.all_crosses = [(0, 0), (1, 1)]
        game.all_circles = [(1, 0)]
        self.assertNotIn(game.calc_next_mob_coord(), [(0, 0), (1, 1), (1, 0)])
        game.all_crosses = [(1, 0), (2, 0), (0, 1), (2, 2), (1, 2)]
        game.all_circles = [(1, 1), (0, 2), (2, 1), (0, 0)]
        self.assertEqual(game.calc_next_mob_coord(), None)

    def test_check_if_win_by_coords(self):
        print("\ntest_check_if_win_by_coords")
        game = main.Game()
        game.all_crosses = [(0, 0), (1, 1), (2, 2)]
        self.assertEqual(game.check_if_win_by_coords(game.all_crosses), True)
        game.all_crosses = [(0, 0), (1, 1), (2, 2), (1, 0)]
        self.assertEqual(game.check_if_win_by_coords(game.all_crosses), True)
        game.all_crosses = [(0, 0), (1, 1)]
        self.assertEqual(game.check_if_win_by_coords(game.all_crosses), False)
        game.all_crosses = [(0, 0), (1, 0), (1, 1)]
        self.assertEqual(game.check_if_win_by_coords(game.all_crosses), False)
        game.all_crosses = [(0, 0), (1, 0), (1, 1), (2, 2)]
        self.assertEqual(game.check_if_win_by_coords(game.all_crosses), True)
        game.all_crosses = [(0, 0), (1, 0), (2, 0)]
        self.assertEqual(game.check_if_win_by_coords(game.all_crosses), True)
        game.all_crosses = [(0, 0), (2, 2), (1, 0), (2, 0)]
        self.assertEqual(game.check_if_win_by_coords(game.all_crosses), True)
        game.all_crosses = [(2, 0), (1, 2), (0, 2)]
        self.assertEqual(game.check_if_win_by_coords(game.all_crosses), False)
        game.all_circles = [(2, 0), (1, 2), (0, 2)]
        self.assertEqual(game.check_if_win_by_coords(game.all_circles), False)

    def test_check_if_win_by_who(self):
        print("\ntest_check_if_win_by_who")
        game = main.Game()
        print(game.all_circles)
        game.player = "cross"
        game.mob = "circle"
        game.all_crosses = [(0, 0), (1, 1), (2, 2)]
        self.assertEqual(game.check_if_win_by_who("player"), True)
        game.all_crosses = [(0, 0), (1, 1), (2, 2), (1, 0)]
        self.assertEqual(game.check_if_win_by_who("player"), True)
        game.all_crosses = [(0, 0), (1, 1)]
        self.assertEqual(game.check_if_win_by_who("player"), False)
        game.all_circles = [(0, 0), (1, 1), (2, 2)]
        self.assertEqual(game.check_if_win_by_who("mob"), True)
        game.all_circles = [(0, 0), (1, 1), (2, 2), (1, 0)]
        self.assertEqual(game.check_if_win_by_who("mob"), True)
        game.all_circles = [(0, 0), (1, 1)]
        self.assertEqual(game.check_if_win_by_who("mob"), False)


if __name__ == '__main__':
    unittest.main()
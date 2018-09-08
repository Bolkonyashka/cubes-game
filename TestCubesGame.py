import unittest
import Cubes
from tkinter import *


class TestCubesMethods(unittest.TestCase):

    def setUp(self):
        game_map = []
        size = 40
        for i in range(0, 5):
            game_map.append([0] * 5)

        root = Tk()
        root.title("Cubes")
        c = Canvas(root, width=15 * size + 400, height=15 * size, bg="lightblue")
        c.pack()

        self.game = Cubes.Game(game_map, c, size, 5)

    def test_click_on_group1(self):
        #  -----> y
        #  !
        #  !
        #  !
        #  v
        #  X
        self.game.map = [[0, 0, 0, 0, 3],
                         [0, 0, 0, 0, 3],
                         [0, 0, 0, 2, 3],
                         [0, 0, 0, 1, 1],
                         [0, 0, 0, 1, 1]]
        self.game.mouse_down(160, 120)
        res = [[0, 0, 0, 0, 3],
               [0, 0, 0, 0, 3],
               [0, 0, 0, 2, 3],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]

        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])

        self.assertEqual(self.game.scores, 64)

    def test_click_on_group2(self):
        self.game.scores = 0
        self.game.map = [[0, 0, 0, 0, 3],
                         [0, 0, 0, 3, 3],
                         [0, 0, 4, 2, 3],
                         [0, 0, 5, 1, 1],
                         [0, 0, 0, 1, 1]]
        self.game.mouse_down(33, 200)
        res = [[0, 0, 0, 4, 2],
               [0, 0, 5, 1, 1],
               [0, 0, 0, 1, 1],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]

        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])

        self.assertEqual(self.game.scores, 64)

    def test_click_on_group3(self):
        self.game.scores = 0
        self.game.map = [[0, 0, 0, 0, 3],
                         [1, 3, 3, 3, 3],
                         [0, 3, 4, 2, 3],
                         [4, 3, 3, 3, 1],
                         [0, 0, 0, 3, 3]]
        self.game.mouse_down(33, 200)
        res = [[0, 0, 0, 0, 1],
               [0, 0, 0, 4, 2],
               [0, 0, 0, 4, 1],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]

        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])

        self.assertEqual(self.game.scores, 1728)

    def test_click_on_group4(self):
        self.game.scores = 0
        self.game.map = [[0, 0, 0, 0, 2],
                         [1, 3, 3, 3, 3],
                         [0, 3, 4, 2, 3],
                         [4, 3, 3, 3, 1],
                         [0, 0, 0, 3, 3]]
        self.game.mouse_down(33, 200)
        res = [[0, 0, 0, 0, 2],
               [1, 3, 3, 3, 3],
               [0, 3, 4, 2, 3],
               [4, 3, 3, 3, 1],
               [0, 0, 0, 3, 3]]

        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])

        self.assertEqual(self.game.scores, 0)

    def test_click_on_group5(self):
        self.game.scores = 0
        self.game.map = [[0, 0, 0, 3, 3],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]]
        self.game.mouse_down(33, 200)
        res = [[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]

        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])
        self.assertTrue(self.game.game_end)
        self.assertEqual(self.game.scores, 8)

    def test_backlight1(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [1, 3, 3, 3, 3],
                         [0, 3, 4, 2, 3],
                         [4, 3, 3, 3, 1],
                         [0, 0, 0, 3, 3]]
        self.game.backlight(33, 200)
        self.assertEqual(self.game.possibleScores, 1728)

    def test_backlight2(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [1, 3, 3, 3, 3],
                         [0, 3, 4, 2, 2],
                         [4, 3, 3, 3, 1],
                         [0, 0, 0, 3, 3]]
        self.game.backlight(102, 199)
        self.assertEqual(self.game.possibleScores, 8)

    def test_backlight3(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [1, 3, 3, 2, 3],
                         [0, 3, 4, 2, 2],
                         [4, 3, 3, 3, 1],
                         [0, 0, 0, 3, 3]]
        self.game.backlight(102, 199)
        self.assertEqual(self.game.possibleScores, 27)

    def test_leaderboard(self):
        self.game.leaders_table_load("leaders//test.txt")
        self.assertEqual(self.game.minLeaderScores, 18399)

    def test_loadgame(self):
        self.game.text.insert(1.0, "loadtest")
        e = Event
        self.game.load_game(e)
        self.assertEqual(self.game.scores, 4400)

    def test_game_end1(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]]
        self.game.game_end_founder()
        self.assertTrue(self.game.game_end)

    def test_game_end2(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [0, 0, 0, 0, 3],
                         [0, 0, 0, 5, 4],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]]
        self.game.game_end_founder()
        self.assertTrue(not self.game.game_end)

    def test_game_end3(self):
        self.game.map = [[0, 0, 0, 2, 3],
                         [0, 0, 0, 0, 2],
                         [0, 0, 0, 2, 3],
                         [0, 0, 0, 0, 4],
                         [0, 0, 0, 4, 1]]
        self.game.game_end_founder()
        self.assertTrue(self.game.game_end)

    def test_game_end4(self):
        self.game.map = [[0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]]
        self.game.game_end_founder()
        self.assertTrue(self.game.game_end)

    def test_shift_columns1(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 4, 4],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]]
        self.game.shift_columns_search()
        res = [[0, 0, 0, 0, 3],
               [0, 0, 0, 4, 4],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]
        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])

    def test_shift_columns2(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 4, 4, 4]]
        self.game.shift_columns_search()
        res = [[0, 0, 0, 0, 3],
               [0, 0, 4, 4, 4],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]
        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])

    def test_shift_columns3(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 2],
                         [0, 0, 0, 0, 0],
                         [0, 0, 4, 4, 4]]
        self.game.shift_columns_search()
        res = [[0, 0, 0, 0, 3],
               [0, 0, 0, 0, 2],
               [0, 0, 4, 4, 4],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]
        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])

    def test_shift_columns4(self):
        self.game.map = [[0, 0, 0, 0, 3],
                         [0, 0, 0, 0, 1],
                         [0, 0, 0, 0, 2],
                         [0, 0, 0, 0, 1],
                         [0, 0, 4, 4, 4]]
        self.game.shift_columns_search()
        res = [[0, 0, 0, 0, 3],
               [0, 0, 0, 0, 1],
               [0, 0, 0, 0, 2],
               [0, 0, 0, 0, 1],
               [0, 0, 4, 4, 4]]
        for i in range(0, 5):
            for j in range(0, 5):
                self.assertEqual(self.game.map[i][j], res[i][j])

    def test_save_game(self):
        self.game.scores = 18400
        self.game.minLeaderScores = 4084
        leaders_tab = open("leaders/test.txt", "r")
        data = leaders_tab.readlines()
        leaders_tab.close()
        self.game.leaders_table_load("leaders//test.txt")
        e = Event
        self.game.save_game(e, "test.txt", "test583")
        self.game.scores = 0
        self.assertEqual(self.game.minLeaderScores, 18400)
        leaders_tab = open("leaders/test.txt", "w")
        for d in data:
            leaders_tab.write(d)
        leaders_tab.close()

if __name__ == '__main__':
    unittest.main()

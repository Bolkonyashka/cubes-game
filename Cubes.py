from tkinter import *
from queue import Queue
import re
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game:
    def __init__(self, game_map, c, size, field_size):
        self.map = game_map
        self.oldMap = []
        for i in range(0, field_size):
            self.oldMap.append([0] * field_size)
        self.c = c
        self.size = size
        self.cubes = []
        for i in range(0, field_size):
            self.cubes.append([0] * field_size)
        self.colorList = {1: "red", 2: "blue", 3: "green", 4: "purple",
                          5: "yellow"}
        self.backLightList = {1: "salmon", 2: "deepskyblue", 3: "palegreen",
                              4: "mediumslateblue", 5: "lemonchiffon"}
        self.lightedCubes = []
        self.passedPoints = []
        for i in range(0, field_size):
            self.passedPoints.append([0] * field_size)
        self.scores = 0
        self.possibleScores = 0
        self.label1 = Label(self.c)
        self.label2 = Label(self.c)
        self.nickName = ""
        self.text = Text(self.c)
        self.leadersList = []
        self.leadersLabel = Label(self.c)
        self.minLeaderScores = 0
        self.game_end = False
        self.field_size = field_size

    def rectang_painter(self, x, y, color_code, size):
        self.cubes[x][y] = self.c.create_rectangle(x * size, y * size,
                                                   x * size + size,
                                                   y * size + size,
                                                   fill=self.colorList[color_code])

    def back_light_painter(self, x, y, color_code, size):
        self.lightedCubes.append(self.c.create_rectangle(x * size, y * size,
                                                         x * size + size,
                                                         y * size + size,
                                                         fill=self.backLightList[color_code]))

    def restarter(self, event):
        self.game_end = False
        random.seed()
        for j in range(0, 15):
            for i in range(0, 15):
                self.map[i][j] = random.randint(1, 5)
        self.scores = 0
        for j in range(0, 15):
            for i in range(0, 15):
                if self.oldMap[i][j] != 0:
                    self.c.delete(self.cubes[i][j])
                self.rectang_painter(i, j, self.map[i][j], self.size)
                self.oldMap[i][j] = self.map[i][j]
        self.label1.config(text="Счет:\n" + str(self.scores))

    def map_painter(self, size):
        self.c.create_rectangle(15 * size, 0, 15 * size + 400, 15 * size,
                                fill="lightblue3")
        for j in range(0, 15):
            for i in range(0, 15):
                self.oldMap[i][j] = self.map[i][j]
                self.rectang_painter(i, j, self.map[i][j], size)

        but1 = Button(self.c, text="Рестарт", width=9, height=2, bg="white",
                      fg="lightblue4", font="arial 20")
        but1.place(x=size * 15 + 5, y=260)
        but2 = Button(self.c, text="Сохранить", width=9, height=2, bg="white",
                      fg="lightblue4", font="arial 20")
        but2.place(x=size * 15 + 5, y=360)
        but3 = Button(self.c, text="Загрузить", width=9, height=2, bg="white",
                      fg="lightblue4", font="arial 20")
        but3.place(x=size * 15 + 5, y=460)

        self.label1 = Label(self.c, text="Счет:\n" + str(self.scores),
                            width=15, height=3,
                            bg="lightblue", fg="lightblue4", font="arial 25")
        self.label1.place(x=size * 15 + 5, y=5)
        self.label2 = Label(self.c, text="Возможные очки:\n" +
                            str(self.possibleScores), width=15, height=3,
                            bg="lightblue", fg="lightblue4", font="arial 25")
        self.label2.place(x=size * 15 + 5, y=130)
        label3 = Label(self.c, text="Ваш ник:", width=10, height=1,
                       bg="lightblue3", fg="lightblue4", font="arial 20")
        label3.place(x=size * 15 + 205, y=260)
        self.leaders_table_load("leaders//leaders.txt")

        self.text = Text(self.c, width=10, height=1, bg="white",
                         fg="lightblue4", font="arial 20")
        self.text.place(x=size * 15 + 205, y=300)

        but2.bind("<Button-1>", self.save_game)
        but3.bind("<Button-1>", self.load_game)
        but1.bind("<Button-1>", self.restarter)

        self.c.bind('<1>', self.mouse_down_event_analyser)
        self.c.bind('<Motion>', self.backlight_event_analyser)

    def leaders_table_load(self, path):
        self.c.delete(self.leadersLabel)
        leaders_tab = open(path, "r")
        self.leadersList = leaders_tab.readlines()
        lead_tab_text = "Лидеры:\n"
        counter = 1
        min_scores = 1000000
        for line in self.leadersList:
            scores = line[10:]
            lead_tab_text = lead_tab_text + str(counter) + "." + line[0:10] + " " + scores
            counter += 1
            if int(scores) < min_scores:
                min_scores = int(scores)

        self.leadersLabel = Label(self.c, text=lead_tab_text, width=20, height=10, bg="lightblue3",
                                  fg="lightblue4", font="arial 15")
        self.leadersLabel.place(x=self.size * 15 + 170, y=350)

        leaders_tab.close()
        self.minLeaderScores = min_scores

    def load_game(self, event):
        self.nickName = self.text.get("1.0", "1.10")
        if self.nickName == "":
            self.nickName = "none"
        try:
            save_file = open("saves//" + self.nickName + "Save.txt", "r")
        except IOError as e:
            print('Не удалось открыть файл')
        else:
            save_string = save_file.read()
            save_data = re.split(r"S", save_string)
            self.scores = int(save_data[0])
            counter = 0
            for i in range(0, self.field_size):
                for j in range(0, self.field_size):
                    self.map[i][j] = int(save_data[1][counter])
                    counter += 1
            save_file.close()
            self.map_refresh(self.size)

    def save_game(self, event, leaders_path="leaders.txt", nick=0):
        if nick == 0:
            self.nickName = self.text.get('1.0', '1.10')
        else:
            self.nickName = nick
        if self.nickName == "":
            self.nickName = "none"
        pattern = r'^[A-Za-zА-Яа-яЁё0-9]+$'
        if re.match(pattern, self.nickName):
            save_file = open("saves//" + self.nickName + "Save.txt", "w+")
            save_file.write(str(self.scores) + "S")
            for i in range(0, self.field_size):
                for j in range(0, self.field_size):
                    save_file.write(str(self.map[i][j]))
            save_file.close()
            downed_str = ""
            downed_position = 0
            if self.scores > self.minLeaderScores:
                for i in range(0, len(self.leadersList)):
                    if self.scores > int(self.leadersList[i][10:]):
                        downed_str = self.leadersList[i]
                        downed_position = i + 1
                        self.leadersList[i] = self.nickName + " " * (10 - len(self.nickName)) + str(self.scores) + "\n"
                        break
                if downed_position <= 4:
                    for j in range(downed_position, 5):
                        storage = self.leadersList[j]
                        self.leadersList[j] = downed_str
                        downed_str = storage
                lead_file = open("leaders//" + leaders_path, "w")
                for leader in self.leadersList:
                    lead_file.write(leader)
                lead_file.close()
                self.leaders_table_load("leaders//" + leaders_path)
        else:
            print('Неверный формат никнейма')

    def map_refresh(self, size):
        for j in range(0, self.field_size):
            for i in range(0, self.field_size):
                if self.map[i][j] != self.oldMap[i][j]:
                    self.c.delete(self.cubes[i][j])
                    if self.map[i][j] != 0:
                        self.rectang_painter(i, j, self.map[i][j], size)
                    self.oldMap[i][j] = self.map[i][j]
        self.label1.config(text="Счет:\n" + str(self.scores))
        self.game_end_founder()
        if self.game_end:
            self.game_end_painter()

    def backlight_event_analyser(self, event):
        self.backlight(event.x, event.y)

    def backlight(self, event_x, event_y):
        self.label2.config(text="Возможные очки:\n" + str(self.possibleScores))
        self.possibleScores = 0
        if len(self.lightedCubes) > 0:
                for k in range(0, len(self.lightedCubes)):
                    self.c.delete(self.lightedCubes[k])
                self.lightedCubes.clear()
        if event_x <= self.size * self.field_size and event_y <= self.size * self.field_size:
            current_possible_scores = 0
            same_cubes = self.same_cubes_search(event_x, event_y)
            if len(same_cubes) > 1:
                for i in same_cubes:
                    current_possible_scores += 1
                    self.back_light_painter(i.x, i.y, self.map[i.x][i.y],
                                            self.size)
                self.possibleScores = current_possible_scores * current_possible_scores * current_possible_scores

    def mouse_down_event_analyser(self, event):
        if event.x <= self.size * self.field_size and event.y <= self.size * self.field_size:
            self.mouse_down(event.x, event.y)

    def mouse_down(self, event_x, event_y):
        for j in range(0, self.field_size):
            for i in range(0, self.field_size):
                self.oldMap[i][j] = self.map[i][j]
        current_scores = 0
        self.possibleScores = 0
        self.label2.config(text="Возможные очки:\n" + str(self.possibleScores))
        for k in range(0, len(self.lightedCubes)):
            self.c.delete(self.lightedCubes[k])
        self.lightedCubes.clear()
        deleted_cubes = self.same_cubes_search(event_x, event_y)
        if len(deleted_cubes) > 1:
            for point in deleted_cubes:
                self.map[point.x][point.y] = 0
                current_scores += 1
            self.scores += current_scores * current_scores * current_scores
            for point in deleted_cubes:
                counter = 0
                for i in range(0, point.y + 1):
                    if self.map[point.x][point.y - i] == 0:
                        counter += 1
                        if point.y - i == 0:
                            break
                        else:
                            continue
                    self.map[point.x][point.y - i + counter] = self.map[point.x][point.y - i]
                for j in range(0, counter):
                    self.map[point.x][j] = 0
        self.shift_columns_search()
        self.map_refresh(self.size)

    def shift_columns_search(self):
        shift_columns = []
        for x in range(0, self.field_size):
            if self.map[x][self.field_size - 1] == 0:
                shift_columns.append(x)
        shift_columns.reverse()
        if len(shift_columns) > 0:
            for col in shift_columns:
                for x in range(col, self.field_size):
                    for y in range(0, self.field_size):
                        if x == self.field_size - 1:
                            self.map[x][y] = 0
                            continue
                        self.map[x][y] = self.map[x+1][y]

    def same_cubes_search(self, event_x, event_y):
        if event_x == self.size * self.field_size:
            event_x = self.size * self.field_size - 1
        if event_y == self.size * self.field_size:
            event_y = self.size * self.field_size - 1
        x, y = event_x, event_y
        map_x = x // self.size
        map_y = y // self.size
        current_color = self.map[map_x][map_y]
        q = Queue()
        same_cubes = []
        point = Point(map_x, map_y)
        q.put(point)
        while (not q.empty() and current_color != 0):
            point = q.get()
            if self.passedPoints[point.x][point.y] == -1:
                continue
            same_cubes.append(point)
            if point.x + 1 < self.field_size:
                if self.map[point.x + 1][point.y] == current_color:
                    q.put(Point(point.x + 1, point.y))
            if point.x - 1 >= 0:
                if self.map[point.x - 1][point.y] == current_color:
                    q.put(Point(point.x - 1, point.y))
            if point.y + 1 < self.field_size:
                if self.map[point.x][point.y + 1] == current_color:
                    q.put(Point(point.x, point.y + 1))
            if point.y - 1 >= 0:
                if self.map[point.x][point.y - 1] == current_color:
                    q.put(Point(point.x, point.y - 1))
            self.passedPoints[point.x][point.y] = -1
        for i in range(0, self.field_size):
            for j in range(0, self.field_size):
                self.passedPoints[i][j] = 0
        return same_cubes

    def game_end_founder(self):
        for i in range(0, self.field_size):
            for j in range(0, self.field_size):
                current_color = self.map[i][j]
                if current_color != 0:
                    if i + 1 < self.field_size:
                        if self.map[i + 1][j] == current_color:
                            return
                    if i - 1 >= 0:
                        if self.map[i - 1][j] == current_color:
                            return
                    if j + 1 < self.field_size:
                        if self.map[i][j + 1] == current_color:
                            return
                    if j - 1 >= 0:
                        if self.map[i][j - 1] == current_color:
                            return
        self.game_end = True

    def game_end_painter(self):
        self.label1.config(text="Игра окончена!\nСчет:\n" + str(self.scores))

    @staticmethod
    def game_starter():
        game_map = []
        size = 40
        for i in range(0, 15):
            game_map.append([0] * 15)

        root = Tk()
        root.title("Cubes")
        c = Canvas(root, width=15 * size + 400, height=15 * size,
                   bg="lightblue")
        c.pack()

        random.seed()

        for j in range(0, 15):
            for i in range(0, 15):
                game_map[i][j] = random.randint(1, 5)

        game = Game(game_map, c, size, 15)
        game.map_painter(size)
        root.mainloop()

if __name__ == '__main__':
    Game.game_starter()

import tkinter as tk
import random
import logging

# Настройка логирования
logging.basicConfig(filename='minesweeper.log', level=logging.INFO, format='%(asctime)s | %(message)s')


class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")

        # Уровень сложности и параметры поля
        self.difficulty = "Easy"
        self.width = 10
        self.height = 10
        self.mines = 10

        # Создание меню и начало новой игры
        self.create_menu()
        self.start_new_game()

    def create_menu(self):
        # Создание меню для выбора сложности и перезапуска игры
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        difficulty_menu = tk.Menu(menu)
        menu.add_cascade(label="Difficulty", menu=difficulty_menu)
        difficulty_menu.add_command(label="Easy", command=lambda: self.set_difficulty("Easy"))
        difficulty_menu.add_command(label="Medium", command=lambda: self.set_difficulty("Medium"))
        difficulty_menu.add_command(label="Hard", command=lambda: self.set_difficulty("Hard"))
        menu.add_command(label="Restart", command=self.start_new_game)

    def set_difficulty(self, level):
        # Установка уровня сложности и перезапуск игры
        self.difficulty = level
        if level == "Easy":
            self.width, self.height, self.mines = 10, 10, 10
        elif level == "Medium":
            self.width, self.height, self.mines = 15, 15, 30
        elif level == "Hard":
            self.width, self.height, self.mines = 20, 20, 60

        logging.info(f"Difficulty chosen: {self.difficulty}")
        self.start_new_game()

    def start_new_game(self):
        # Начало новой игры и создание игрового поля
        self.field = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.visible = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.buttons = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.game_over = False

        self.populate_mines()
        self.calculate_numbers()
        self.create_widgets()
        logging.info("New game started")

    def create_widgets(self):
        # Создание кнопок для игрового поля
        for y in range(self.height):
            for x in range(self.width):
                button = tk.Button(self.master, text=' ', width=3, bg='lightgray',
                                   command=lambda x=x, y=y: self.reveal_cell(x, y))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def populate_mines(self):
        #Заполнение поля минами
        mine_positions = random.sample(range(self.width * self.height), self.mines)
        for pos in mine_positions:
            x = pos % self.width
            y = pos // self.width
            self.field[y][x] = '*'

    def calculate_numbers(self):
        # Расчет чисел на поле, показывающих количество соседних мин
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x] == '*':
                    continue
                self.field[y][x] = str(self.count_adjacent_mines(x, y))

    def count_adjacent_mines(self, x, y):
        # Подсчет количества мин вокруг заданной клетки
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < self.width and 0 <= y + j < self.height:
                    if self.field[y + j][x + i] == '*':
                        count += 1
        return count

    def reveal_cell(self, x, y):
        # Открытие клетки при нажатии на кнопку
        if self.game_over:
            return

        if self.field[y][x] == '*':
            self.buttons[y][x].config(text='*', bg='red')
            self.game_over = True
            self.show_all_mines()
            self.show_message("Вы попали на мину! Игра окончена.")
            logging.info("Game end. Failed")
            return

        self.visible[y][x] = self.field[y][x]
        self.buttons[y][x].config(text=self.field[y][x], state='disabled', bg=self.get_color(self.field[y][x]))
        logging.info(f"Open case ({x}, {y}): {self.field[y][x]}")

        if self.field[y][x] == '0':
            self.reveal_adjacent_cells(x, y)

        if all(self.visible[y][x] != ' ' for y in range(self.height) for x in range(self.width) if
               self.field[y][x] != '*'):
            self.show_message("Поздравляем! Вы выиграли!")
            logging.info("Game end. Passed")

    def reveal_adjacent_cells(self, x, y):
        # Открытие соседних клеток, если открытая клетка пустая
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < self.width and 0 <= y + j < self.height:
                    if self.visible[y + j][x + i] == ' ':
                        self.reveal_cell(x + i, y + j)

    def show_all_mines(self):
        # Открытие всех мин на поле в случае поражения
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x] == '*':
                    self.buttons[y][x].config(text='*', bg='yellow')

    def get_color(self, value):
        # Возвращает цвет для отображения числа на кнопке
        if value == '0':
            return 'white'
        elif value == '1':
            return 'blue'
        elif value == '2':
            return 'green'
        elif value == '3':
            return 'red'
        elif value == '4':
            return 'darkblue'
        elif value == '5':
            return 'darkred'
        elif value == '6':
            return 'cyan'
        elif value == '7':
            return 'black'
        elif value == '8':
            return 'gray'
        return 'lightgray'

    def show_message(self, message):
        # Отображение сообщения о результате игры
        msg_box = tk.Toplevel(self.master)
        msg_box.title("Сообщение")
        tk.Label(msg_box, text=message).pack(padx=20, pady=20)
        tk.Button(msg_box, text="Закрыть", command=msg_box.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
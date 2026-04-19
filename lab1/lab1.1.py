import random
import os
import time
import sys

class SnakeGame:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.snake = [(width//2, height//2)]
        self.direction = (0, 1)  # Направление: (dx, dy)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
    def generate_food(self):
        while True:
            food = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if food not in self.snake:
                return food
    
    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.width, (head_y + dy) % self.height)
        
        # Проверка столкновения с собой
        if new_head in self.snake:
            self.game_over = True
            return
            
        self.snake.insert(0, new_head)
        
        # Проверка на поедание еды
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def change_direction(self, new_direction):
        # Не позволять менять направление на противоположное
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def display(self):
        # Очистка экрана
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Создание поля
        field = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        # Размещение еды
        food_x, food_y = self.food
        field[food_y][food_x] = 'O'
        
        # Размещение змейки (голова и тело)
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                field[y][x] = '@'  # Голова
            else:
                field[y][x] = 'o'  # Тело
        
        # Вывод поля
        print(f"Счет: {self.score}")
        print("+" + "-" * self.width + "+")
        for row in field:
            print("|" + "".join(row) + "|")
        print("+" + "-" * self.width + "+")
        print("Управление: W/A/S/D или стрелки. Q для выхода")
    
    def run(self):
        print("Добро пожаловать в игру Змейка!")
        print("Используйте клавиши WASD или стрелки для управления")
        input("Нажмите Enter, чтобы начать...")
        
        while not self.game_over:
            self.display()
            
            # Ожидание ввода пользователя
            try:
                import msvcrt  # Windows
                
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key == 'w' or key == 'к':
                        self.change_direction((0, -1))
                    elif key == 's' or key == 'ы':
                        self.change_direction((0, 1))
                    elif key == 'a' or key == 'ф':
                        self.change_direction((-1, 0))
                    elif key == 'd' or key == 'в':
                        self.change_direction((1, 0))
                    elif key == 'q':
                        break
            except ImportError:
                # Для Unix/Linux/MacOS
                import select
                import termios
                import tty
                
                def get_char():
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(sys.stdin.fileno())
                        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                            return sys.stdin.read(1).lower()
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
                char = get_char() or ''
                if char in ['w', 'к']:
                    self.change_direction((0, -1))
                elif char in ['s', 'ы']:
                    self.change_direction((0, 1))
                elif char in ['a', 'ф']:
                    self.change_direction((-1, 0))
                elif char in ['d', 'в']:
                    self.change_direction((1, 0))
                elif char == 'q':
                    break
            
            # Движение змейки
            self.move_snake()
            
            # Задержка для регулирования скорости игры
            time.sleep(0.2)
        
        # Конец игры
        self.display()
        print(f"Игра окончена! Ваш счет: {self.score}")

# Запуск игры
if __name__ == "__main__":
    game = SnakeGame()
    game.run()

import random
from random import choice


class Word:
    def __init__(self):
        self.sorted_list = []
        self.number = 0

    def complexity(self, value: int) -> 'Word':
        if value not in [1, 2, 3]:
            raise ValueError("Сложность должна быть 1, 2 или 3")

        if value == 1:
            self.number = random.randint(2, 5)
        elif value == 2:
            self.number = random.randint(6, 12)
        elif value == 3:
            self.number = random.randint(13, 24)
        return self

    def quick_word(self, value: int = None) -> str:  # быстрое создание слов необходимой сложности
        self.complexity(value)
        self.word_list()
        return choice(self.sorted_list)

    def word_list(self, number: int = None) -> list[str]:  # создаёт список из слов с определённой длиной
        if number is not None:
            self.number = number
        elif self.number == 0:
            self.number = random.randint(2, 24)

        with open("words.txt", 'r', encoding='utf-8') as f:  # Идём по документу
            # с помощью генератора заполняем список словами с необходимой длиной
            self.sorted_list = [line.split()[1] for line in f if line.split()[0] == str(self.number)]
        return self.sorted_list

    def random_word_list(self) -> str:  # вывод рандомного слова из списка
        self.word_list()
        return choice(self.sorted_list)


word = Word()
print(word.random_word_list())

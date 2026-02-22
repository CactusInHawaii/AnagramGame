import random
from random import choice


class Word:
    def __init__(self):
        self.sorted_list = []
        self.number = 0
        self.word = ""

    def __complexity(self, value: int) -> "Word":
        """Устанавливает длину слова в зависимости от уровня сложности (1, 2 или 3)."""
        if value not in {1, 2, 3}:
            raise ValueError("Сложность должна быть 1, 2 или 3")

        ranges = {1: (2, 5), 2: (6, 12), 3: (13, 24)}
        self.number = random.randint(*ranges[value])
        return self

    def __load_words(self, length: int = None) -> list[str]:
        """Загружает из файла words.txt список слов заданной длины."""
        if length is not None:
            self.number = length
        if self.number == 0:
            self.number = random.randint(2, 24)

        if not self.sorted_list:
            with open("words.txt", encoding="utf-8") as f:
                self.sorted_list = [
                    line.split()[1] for line in f if line.split()[0] == str(self.number)
                ]
        return self.sorted_list

    def quick_word(self, level: int = None) -> str:
        """Возвращает случайное слово (можно указать уровень сложности 1–3)."""
        if level is not None:
            self.__complexity(level)
        self.__load_words()
        return choice(self.sorted_list) if self.sorted_list else ""

    def anagram(self, word: str = None) -> str:
        """Возвращает анаграмму слова (если слово не передано — берёт случайное)."""
        if word is None:
            word = self.quick_word()
        shuffled = "".join(random.sample(word, len(word)))
        while shuffled == word:
            shuffled = "".join(random.sample(word, len(word)))
        return shuffled

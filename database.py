import sqlite3


class editor_bd:
    def __init__(self):
        # Подключение к БД
        self.conn = sqlite3.connect("words.db")
        self.cursor = self.conn.cursor()

        # Индекс для быстрой сортировки по очкам
        self.cursor.execute("""
                            CREATE INDEX IF NOT EXISTS idx_points
                                ON dictionary (points)
                            """)
        self.conn.commit()

    def add_word(self, word):
        """добавляет слово в таблицу"""
        try:
            with self.conn:
                self.cursor.execute(
                    """
                                    INSERT INTO dictionary (word, points, flag)
                                    VALUES (?, ?, ?)
                                    """,
                    (word, len(word), True),
                )
                self.__get_sorted_words()  # применить сортировку
        except sqlite3.IntegrityError:
            print(f"Слово '{word}' уже существует!")

    def __get_sorted_words(self):
        """приватный метод: сортирует таблицу"""
        with self.conn:
            self.cursor.execute("""
                                SELECT * FROM dictionary
                                ORDER BY points
                                """)
            return self.cursor

    def delete_word(self, word):
        """удаляет слово из таблицы"""
        with self.conn:
            self.cursor.execute(
                """
                DELETE FROM dictionary
                WHERE word = ?  # удаляем по точному совпадению
                """,
                (word,),
            )
            self.conn.commit()

            # Проверка, было ли удаление
            if self.cursor.rowcount > 0:
                print(f"Слово '{word}' удалено!")
            else:
                print(f"Слово '{word}' не найдено!")

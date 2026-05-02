import customtkinter as ctk
from words import Word

class UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Анаграммы")
        self.geometry("400x500")
        self.resizable(False, False)
        self.w = Word()
        self.counter = None
        self.entry = None
        self.score_label = None
        self.score = 0
        self.hint_text = ""
        self.hint_button = None
        self.check_button = None
        self.anagram_label = None
        self.total_hints = None
        self.word_array = None
        self.anagram = ""
        self.word = ""
        self.text_variable = ctk.StringVar()
        self.complexity =   None
        # Главный контейнер (будет менять экраны)
        self.current_frame = None

        # Показываем меню при запуске
        self.show_menu()

    def show_menu(self):
        self.clear_screen()  # убираем всё старое

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Анаграммы", font=("Arial", 28, "bold")).pack(pady=30)
        ctk.CTkButton(frame, text="Играть", width=200, command=self.show_complexity).pack(pady=10)
        ctk.CTkButton(frame, text="Выход", width=200, command=self.quit).pack(pady=10)

        self.current_frame = frame

    def show_complexity(self):
        self.clear_screen()
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Выберете сложность", font=("Arial", 24)).pack(pady=10)

        ctk.CTkButton(frame, text="Легко", width=200, command=lambda: self.start_game(1)).pack(pady=10)

        ctk.CTkButton(frame, text="Средне", width=200, command=lambda: self.start_game(2)).pack(pady=10)

        ctk.CTkButton(frame, text="Сложно", width=200, command=lambda: self.start_game(3)).pack(pady=10)

        ctk.CTkButton(frame, text="Назад в меню", width=200, command=self.show_menu).pack(pady=10)

        self.current_frame = frame

    def show_game(self):
        self.clear_screen()
        self.hint_text = ""
        self.text_variable = ctk.StringVar()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.score_label = ctk.CTkLabel(frame, text=f"Счёт: {self.score}", font=("Arial", 20))
        self.score_label.pack(pady=10)

        ctk.CTkLabel(frame, text=f"Анаграмма {len(self.word)} букв", font=("Arial", 22)).pack(pady=10)

        self.anagram_label = ctk.CTkLabel(frame, text=self.anagram, font=("Arial", 20))
        self.anagram_label.pack(pady=10)

        self.entry = ctk.CTkEntry(frame, textvariable = self.text_variable,width=200)
        self.entry.pack(pady=10)

        self.check_button = ctk.CTkButton(frame, text="Проверить", width=200, command=self.word_checker)
        self.check_button.pack(pady=10)

        self.hint_button = ctk.CTkButton(frame, text=f"Подсказка {self.counter}/{self.total_hints}", width=200, command=self.hint)
        self.hint_button.pack(pady=10)

        ctk.CTkButton(frame, text="Следующее слово", width=200, command=lambda:self.start_game(self.complexity)).pack(pady=10)

        ctk.CTkButton(
            frame, text="Назад в меню", width=200, command=self.show_menu
        ).pack(pady=10)

        self.current_frame = frame

    def hint(self):
        if self.counter > 0:
            self.score -= int(len(self.word) * 0.5)
            if self.score < 0: self.score = 0
            self.score_label.configure(text=f"Счёт: {self.score}")

            self.hint_text += self.word_array[self.total_hints - self.counter]
            self.counter -= 1
            self.hint_button.configure(text=f"Подсказка {self.counter}/{self.total_hints}")
            self.text_variable.set(self.hint_text)
            self.entry.icursor('end')

        if self.counter == 0:
            self.hint_button.configure(state="disabled")
            # self.check_button.configure(state="disabled")
            return


    def word_checker(self):
        if self.text_variable.get().strip().lower() == self.word:

            self.score+=len(self.word)
            self.score_label.configure(text=f"Счёт: {self.score}")
            self.start_game(self.complexity)
        else:
            self.text_variable.set("")

    def start_game(self, complexity,line_length=None):
        self.total_hints = 0
        self.counter=0
        self.complexity = complexity
        self.word = self.w.quick_word(self.complexity)
        self.anagram = self.w.anagram(self.word)
        self.counter = 2
        if len(self.word) % 2:
            line_length=len(self.word)//self.counter+1
        else:
            line_length=(len(self.word)//self.counter)

        self.total_hints = self.counter

        self.word_array = [self.word[i:i+line_length] for i in range(0,len(self.word),line_length)]
        self.show_game()


    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None


if __name__ == "__main__":
    app = UI()
    app.mainloop()
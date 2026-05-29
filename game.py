import customtkinter as ctk
from just_playback import Playback
from words import Word

class Game(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Анаграммы")
        self.geometry("400x500")
        self.resizable(False, False)

        # Инициализация переменных игры
        self.w = Word()
        self.score = 0
        self.text_hint = ""
        self.anagram = ""
        self.original_word = ""
        self.word = ""
        self.complexity = None
        self.counter = None
        self.total_hints = None
        self.word_array = None

        # Виджеты (будут присваиваться позже)
        self.current_frame = None
        self.score_label = None
        self.anagram_label = None
        self.entry = None
        self.check_button = None
        self.hint_button = None
        self.text_entry = ctk.StringVar()

        # Настройки звука и музыки
        self.music_value = ctk.BooleanVar(value=True)
        self.sound_button_value = ctk.BooleanVar(value=True)

        # Инициализация плееров
        self._click_player = Playback()
        self._click_player.load_file("click.mp3")
        self.volume_button = 0.1 #громкость звука при нажатии на кнопку

        self._music_player = Playback()
        self._music_player.load_file("music.mp3")
        self._music_player.loop_at_end(True)
        self._music_player.play()
        self._music_player.set_volume(0.1)

        # Запуск главного меню
        self.show_menu()

    def show_menu(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Анаграммы", font=("Arial", 28, "bold")).pack(pady=30)

        ctk.CTkButton(
            frame,
            text="Играть",
            width=200,
            command=lambda: [self.sound_button(), self.show_complexity()],
        ).pack(pady=10)

        ctk.CTkButton(frame, text="Настройки", width=200, command = lambda: [self.sound_button(), self.settings()]).pack(pady=10)

        ctk.CTkButton(frame, text="Выход", width=200, command=lambda: [self.sound_button(), self.quit()]).pack(pady=10)

        self.current_frame = frame

    def settings(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Настройки",font=("Arial", 28, "bold"), width=200).pack(pady=10)

        ctk.CTkCheckBox(frame, variable = self.music_value, text="Музыка",width=200,command = lambda: [self.sound_button(), self.music()]).pack(pady=10)

        ctk.CTkCheckBox(frame, variable = self.sound_button_value, text="Звук от кнопки", width=200,).pack(pady=10)

        self.back_to_menu(frame)

        self.current_frame = frame

    def music(self):
        self._music_player.resume() if self.music_value.get() else self._music_player.pause()

    def sound_button(self):
        if self.sound_button_value.get():
            self._click_player.play() #запуск звука
            self._click_player.set_volume(self.volume_button) #изменение громкости

    def show_complexity(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Выберете сложность", font=("Arial", 24)).pack(pady=10)

        ctk.CTkButton(frame, text="Легко", width=200, command=lambda: [self.sound_button(), self.start_game(1)]).pack(pady=10)

        ctk.CTkButton(frame, text="Средне", width=200, command=lambda: [self.sound_button(), self.start_game(2)]).pack(pady=10)

        ctk.CTkButton(frame,text="Сложно",width=200,command=lambda: [self.sound_button(), self.start_game(3)]).pack(pady=10)

        self.current_frame = frame

    def back_to_menu(self,frame):
        return ctk.CTkButton(frame,text="Назад в меню",width=200,command = lambda: [self.sound_button(), self.show_menu()]).pack(pady=10)

    def show_game(self):
        self.clear_screen()
        self.text_hint = ""
        self.text_entry = ctk.StringVar()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.score_label = ctk.CTkLabel(frame, text=f"Счёт: {self.score}", font=("Arial", 20))
        self.score_label.pack(pady=10)

        ctk.CTkLabel(frame, text=f"Анаграмма {len(self.original_word)} букв", font=("Arial", 22)).pack(pady=10)

        self.anagram_label = ctk.CTkLabel(frame, text=self.anagram, font=("Arial", 20))
        self.anagram_label.pack(pady=10)

        self.entry = ctk.CTkEntry(frame, textvariable = self.text_entry,width=200)
        self.entry.pack(pady=10)

        self.check_button = ctk.CTkButton(frame, text="Проверить", width=200, command=lambda: [self.sound_button(), self.word_checker()])
        self.check_button.pack(pady=10)

        self.hint_button = ctk.CTkButton(frame, text=f"Подсказка {self.counter}/{self.total_hints}", width=200, command=lambda: [self.sound_button(), self.hint()])
        self.hint_button.pack(pady=10)

        ctk.CTkButton(frame, text="Следующее слово", width=200, command=lambda:[self.sound_button(), self.start_game(self.complexity)]).pack(pady=10)

        self.back_to_menu(frame)

        self.current_frame = frame

    def hint(self):
        if self.counter > 0:
            part_word = self.word_array[self.total_hints - self.counter]
            self.text_hint += part_word

            if len(self.original_word) > 3:
                self.word = self.word.replace(part_word, "",1)
                text_anagram = self.text_hint + self.w.anagram(self.word)
                self.anagram_label.configure(text = text_anagram)

            self.counter -= 1

            self.hint_button.configure(text=f"Подсказка {self.counter}/{self.total_hints}")
            self.text_entry.set(self.text_hint)
            self.entry.icursor('end')

        if self.counter == 0:
            self.hint_button.configure(state="disabled")
            return


    def word_checker(self):
        if self.text_entry.get().strip().lower() == self.original_word:
            self.score+= len(self.original_word) - len(self.text_hint)
            self.score_label.configure(text=f"Счёт: {self.score}")
            self.start_game(self.complexity)
        else:
            self.text_entry.set(self.text_hint)
            self.entry.icursor('end')

    def start_game(self, complexity,line_length=None):
        self.total_hints = 0
        self.counter=0
        self.complexity = complexity
        self.original_word = self.w.quick_word(self.complexity)
        self.word = self.original_word
        self.anagram = self.w.anagram(self.original_word)
        self.counter = 2

        if len(self.original_word) % 2:
            line_length= len(self.original_word) // self.counter + 1
        else:
            line_length=(len(self.original_word) // self.counter)

        self.total_hints = self.counter

        self.word_array = [self.original_word[i:i + line_length] for i in range(0,len(self.original_word),line_length)]
        self.show_game()


    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None


if __name__ == "__main__":
    app = Game()
    app.mainloop()
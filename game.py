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
        self.hint_text = ""
        self.anagram = ""
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
        self.text_variable = ctk.StringVar()

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

        ctk.CTkButton(frame, text="Играть", width=200, command = lambda :[self.show_complexity(), self.sound_button()]).pack(pady=10)

        ctk.CTkButton(frame, text="Настройки", width=200, command = self.settings).pack(pady=10)

        ctk.CTkButton(frame, text="Выход", width=200, command=self.quit).pack(pady=10)

        self.current_frame = frame

    def settings(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Настройки",font=("Arial", 28, "bold"), width=200).pack(pady=10)

        ctk.CTkCheckBox(frame, variable = self.music_value, text="Музыка",width=200,command = self.music).pack(pady=10)

        ctk.CTkCheckBox(frame, variable = self.sound_button_value, text="Звук от кнопки", width=200,).pack(pady=10)

        self.back_to_menu(frame)

        self.current_frame = frame

    def music(self):
        self._music_player.resume() if self.music_value.get() else self._music_player.pause()

    def sound_button(self):
        self.sound_button_value and self._click_player.play() #запуск звука
        self._click_player.set_volume(self.volume_button) #изменение громкости

    def show_complexity(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Выберете сложность", font=("Arial", 24)).pack(pady=10)

        ctk.CTkButton(frame, text="Легко", width=200, command=lambda: self.start_game(1)).pack(pady=10)

        ctk.CTkButton(frame, text="Средне", width=200, command=lambda: self.start_game(2)).pack(pady=10)

        ctk.CTkButton(frame,text="Сложно",width=200,command=lambda: self.start_game(3)).pack(pady=10)

        self.back_to_menu(frame)

        self.current_frame = frame

    def back_to_menu(self,frame):
        return ctk.CTkButton(frame,text="Назад в меню",width=200,command = self.show_menu).pack(pady=10)

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

        self.back_to_menu(frame)

        self.current_frame = frame

    def hint(self):
        if self.counter > 0:
            self.score -= int(len(self.word) * 0.5)

            self.score = max(0, self.score)
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
    app = Game()
    app.mainloop()
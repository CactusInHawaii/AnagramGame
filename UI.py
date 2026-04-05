import customtkinter as ctk


class UI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Анаграммы")
        self.geometry("400x300")
        self.resizable(False, False)

        # Главный контейнер (будет менять экраны)
        self.current_frame = None

        # Показываем меню при запуске
        self.show_menu()

    def show_menu(self):
        self.clear_screen()  # убираем всё старое

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Анаграммы", font=("Arial", 28, "bold")).pack(pady=30)
        ctk.CTkButton(frame, text="Играть", width=200, command=self.show_game).pack(
            pady=10
        )
        ctk.CTkButton(frame, text="Выход", width=200, command=self.quit).pack(pady=10)

        self.current_frame = frame

    def show_game(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Тут твоя анаграмма!", font=("Arial", 24)).pack(
            pady=30
        )
        ctk.CTkButton(
            frame, text="Назад в меню", width=200, command=self.show_menu
        ).pack(pady=10)

        self.current_frame = frame

    def clear_screen(self):
        # Удаляем всё, что было на экране
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None


if __name__ == "__main__":
    app = UI()
    app.mainloop()
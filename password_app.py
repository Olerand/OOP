import tkinter as tk
from tkinter import messagebox
from password_utils import PasswordUtils

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        self.light_theme = {
            'bg': "#e0f7fa",  # Голубой
            'fg': "#006064",  # Темно-морской
            'btn_bg': "#00acc1",  # Сине-зеленый
            'entry_bg': "#ffffff",  # Белый
            'button_fg': "white"
        }

        self.current_theme = self.light_theme
        self.root.configure(bg=self.current_theme['bg'])

        # Заголовок
        title_label = tk.Label(root, text="Генератор паролей", font=("Arial", 18, "bold"), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        title_label.pack(pady=10)

        # Поле длины пароля
        length_frame = tk.Frame(root, bg=self.current_theme['bg'])
        length_frame.pack(pady=5)
        tk.Label(length_frame, text="Длина пароля:", font=("Arial", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg']).pack(side="left", padx=5)
        self.length_entry = tk.Entry(length_frame, width=5, font=("Arial", 12), bg=self.current_theme['entry_bg'])
        self.length_entry.pack(side="left", padx=5)
        self.length_entry.insert(0, "8")  # Значение по умолчанию

        # Опции
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=True)

        options_frame = tk.Frame(root, bg=self.current_theme['bg'])
        options_frame.pack(pady=10)
        tk.Checkbutton(options_frame, text="Включить заглавные буквы", variable=self.include_uppercase,
                       font=("Arial", 11), bg=self.current_theme['bg'], fg=self.current_theme['fg'], selectcolor=self.current_theme['entry_bg']).pack(anchor="w", pady=2)
        tk.Checkbutton(options_frame, text="Включить цифры", variable=self.include_numbers,
                       font=("Arial", 11), bg=self.current_theme['bg'], fg=self.current_theme['fg'], selectcolor=self.current_theme['entry_bg']).pack(anchor="w", pady=2)
        tk.Checkbutton(options_frame, text="Включить специальные символы", variable=self.include_special,
                       font=("Arial", 11), bg=self.current_theme['bg'], fg=self.current_theme['fg'], selectcolor=self.current_theme['entry_bg']).pack(anchor="w", pady=2)

        # Поле для ввода ключевых слов
        self.custom_keywords_label = tk.Label(root, text="Ключевые слова (через пробел):", font=("Arial", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.custom_keywords_label.pack(pady=5)
        self.custom_keywords_entry = tk.Entry(root, width=50, font=("Arial", 12), bg=self.current_theme['entry_bg'])
        self.custom_keywords_entry.pack(pady=5)

        # Кнопка генерации
        self.generate_button = tk.Button(root, text="Сгенерировать пароль", command=self.generate_password,
                                         font=("Arial", 12), bg=self.current_theme['btn_bg'], fg=self.current_theme['button_fg'], relief="flat", padx=10, pady=5)
        self.generate_button.pack(pady=10)

        # Поле вывода результата (с переносом строк)
        self.result_label = tk.Label(root, text="", font=("Arial", 14), wraplength=750, fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.result_label.pack(pady=10)

        # Поле времени взлома
        self.crack_time_label = tk.Label(root, text="", font=("Arial", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.crack_time_label.pack(pady=5)

        # Кнопка копирования пароля
        self.copy_button = tk.Button(root, text="Копировать", command=self.copy_to_clipboard,
                                     font=("Arial", 12), bg=self.current_theme['btn_bg'], fg=self.current_theme['button_fg'], relief="flat", padx=10, pady=5, state=tk.DISABLED)
        self.copy_button.pack(pady=10)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            include_uppercase = self.include_uppercase.get()
            include_numbers = self.include_numbers.get()
            include_special = self.include_special.get()
            custom_keywords = self.custom_keywords_entry.get()

            password = PasswordUtils.generate_password(length, include_uppercase, include_numbers, include_special, custom_keywords)
            password_strength = PasswordUtils.evaluate_password(password)
            crack_time = PasswordUtils.calculate_crack_time(password, include_uppercase, include_numbers, include_special)

            self.result_label.config(text=f"Пароль: {password}\nНадежность: {password_strength}")
            self.crack_time_label.config(text=f"Время взлома: {crack_time}")
            self.copy_button.config(state=tk.NORMAL)

            # Сохраняем пароль в файл
            PasswordUtils.save_password_to_file(password, custom_keywords)

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def copy_to_clipboard(self):
        password = self.result_label.cget("text").split("\n")[0].split(": ")[1]
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
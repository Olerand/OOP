import tkinter as tk
from tkinter import messagebox
from password_utils import PasswordUtils

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("��������� �������")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        self.light_theme = {
            'bg': "#e0f7fa",  # �������
            'fg': "#006064",  # �����-�������
            'btn_bg': "#00acc1",  # ����-�������
            'entry_bg': "#ffffff",  # �����
            'button_fg': "white"
        }

        self.current_theme = self.light_theme
        self.root.configure(bg=self.current_theme['bg'])

        # ���������
        title_label = tk.Label(root, text="��������� �������", font=("Arial", 18, "bold"), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        title_label.pack(pady=10)

        # ���� ����� ������
        length_frame = tk.Frame(root, bg=self.current_theme['bg'])
        length_frame.pack(pady=5)
        tk.Label(length_frame, text="����� ������:", font=("Arial", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg']).pack(side="left", padx=5)
        self.length_entry = tk.Entry(length_frame, width=5, font=("Arial", 12), bg=self.current_theme['entry_bg'])
        self.length_entry.pack(side="left", padx=5)
        self.length_entry.insert(0, "8")  # �������� �� ���������

        # �����
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=True)

        options_frame = tk.Frame(root, bg=self.current_theme['bg'])
        options_frame.pack(pady=10)
        tk.Checkbutton(options_frame, text="�������� ��������� �����", variable=self.include_uppercase,
                       font=("Arial", 11), bg=self.current_theme['bg'], fg=self.current_theme['fg'], selectcolor=self.current_theme['entry_bg']).pack(anchor="w", pady=2)
        tk.Checkbutton(options_frame, text="�������� �����", variable=self.include_numbers,
                       font=("Arial", 11), bg=self.current_theme['bg'], fg=self.current_theme['fg'], selectcolor=self.current_theme['entry_bg']).pack(anchor="w", pady=2)
        tk.Checkbutton(options_frame, text="�������� ����������� �������", variable=self.include_special,
                       font=("Arial", 11), bg=self.current_theme['bg'], fg=self.current_theme['fg'], selectcolor=self.current_theme['entry_bg']).pack(anchor="w", pady=2)

        # ���� ��� ����� �������� ����
        self.custom_keywords_label = tk.Label(root, text="�������� ����� (����� ������):", font=("Arial", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.custom_keywords_label.pack(pady=5)
        self.custom_keywords_entry = tk.Entry(root, width=50, font=("Arial", 12), bg=self.current_theme['entry_bg'])
        self.custom_keywords_entry.pack(pady=5)

        # ������ ���������
        self.generate_button = tk.Button(root, text="������������� ������", command=self.generate_password,
                                         font=("Arial", 12), bg=self.current_theme['btn_bg'], fg=self.current_theme['button_fg'], relief="flat", padx=10, pady=5)
        self.generate_button.pack(pady=10)

        # ���� ������ ���������� (� ��������� �����)
        self.result_label = tk.Label(root, text="", font=("Arial", 14), wraplength=750, fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.result_label.pack(pady=10)

        # ���� ������� ������
        self.crack_time_label = tk.Label(root, text="", font=("Arial", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.crack_time_label.pack(pady=5)

        # ������ ����������� ������
        self.copy_button = tk.Button(root, text="����������", command=self.copy_to_clipboard,
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

            self.result_label.config(text=f"������: {password}\n����������: {password_strength}")
            self.crack_time_label.config(text=f"����� ������: {crack_time}")
            self.copy_button.config(state=tk.NORMAL)

            # ��������� ������ � ����
            PasswordUtils.save_password_to_file(password, custom_keywords)

        except ValueError as e:
            messagebox.showerror("������", str(e))

    def copy_to_clipboard(self):
        password = self.result_label.cget("text").split("\n")[0].split(": ")[1]
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("�����", "������ ���������� � ����� ������")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
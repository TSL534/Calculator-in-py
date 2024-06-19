import tkinter as tk
from tkinter import ttk
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("320x500")
        self.root.resizable(False, False)

        self.light_mode = True
        self.configure_light_mode()
        self.create_widgets()

    def configure_light_mode(self):
        self.BUTTON_STYLE = {
            'font': ("Helvetica", 18),
            'padding': 10,
            'borderwidth': 0,
            'relief': "flat"
        }
        self.COLORS = {
            'bg': "#ffffff",
            'btn_bg': "#ffffff",
            'btn_fg': "#000000",
            'btn_active_bg': "#d9d9d9",
            'btn_pressed_bg': "#bfbfbf",
            'entry_bg': "#f0f0f0",
            'entry_fg': "#000000"
        }
        self.root.configure(bg=self.COLORS['bg'])
        self.apply_styles()

    def configure_dark_mode(self):
        self.BUTTON_STYLE = {
            'font': ("Helvetica", 18),
            'padding': 10,
            'borderwidth': 0,
            'relief': "flat"
        }
        self.COLORS = {
            'bg': "#2e2e2e",
            'btn_bg': "#4f4f4f",
            'btn_fg': "#ffffff",
            'btn_active_bg': "#5a5a5a",
            'btn_pressed_bg': "#6b6b6b",
            'entry_bg': "#3e3e3e",
            'entry_fg': "#ffffff"
        }
        self.root.configure(bg=self.COLORS['bg'])
        self.apply_styles()

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TEntry", foreground=self.COLORS['entry_fg'], background=self.COLORS['entry_bg'],
                        fieldbackground=self.COLORS['entry_bg'], borderwidth=0, font=("Helvetica", 18))
        style.configure("TButton", **self.BUTTON_STYLE, background=self.COLORS['btn_bg'], foreground=self.COLORS['btn_fg'])
        style.map("TButton", background=[('pressed', self.COLORS['btn_pressed_bg']), ('active', self.COLORS['btn_active_bg'])])

    def create_widgets(self):
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self.root, textvariable=self.entry_var, style="TEntry", justify='right', validate='key')
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=20)
        self.entry.bind("<Return>", self.evaluate_expression)
        self.entry['validatecommand'] = (self.entry.register(self.validate_entry), '%P')

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('√', 5, 0), ('C', 5, 1)
        ]

        for (text, row, col) in buttons:
            self.create_button(text, row, col)

        self.toggle_button = ttk.Button(self.root, text="L/D", command=self.toggle_mode, style="Toggle.TButton")
        self.toggle_button.grid(row=5, column=3, padx=5, pady=5, sticky="nsew")

        self.label = tk.Label(self.root, text="Made by TSL", font=("Helvetica", 12), bg=self.COLORS['bg'], fg=self.COLORS['btn_fg'])
        self.label.grid(row=6, column=0, columnspan=4, pady=10)

        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
            if i < 4:
                self.root.grid_columnconfigure(i, weight=1)

    def create_button(self, text, row, col):
        command = None
        if text == '=':
            command = self.evaluate_expression
        elif text == 'C':
            command = self.clear_entry
        elif text == '√':
            command = self.calculate_square_root
        else:
            command = lambda t=text: self.append_to_expression(t)

        btn = ttk.Button(self.root, text=text, command=command)
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def toggle_mode(self):
        if self.light_mode:
            self.configure_dark_mode()
        else:
            self.configure_light_mode()
        self.light_mode = not self.light_mode
        self.label.configure(bg=self.COLORS['bg'], fg=self.COLORS['btn_fg'])

    def evaluate_expression(self, event=None):
        try:
            expression = self.entry.get()
            result = eval(expression)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, 'Error')

    def append_to_expression(self, char):
        current_text = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, current_text + char)

    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def calculate_square_root(self):
        try:
            expression = self.entry.get()
            result = math.sqrt(float(expression))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, 'Error')

    def validate_entry(self, new_value):
        if new_value == "":
            return True
        allowed_chars = "0123456789+-*/()."
        for char in new_value:
            if char not in allowed_chars:
                return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ModernCalculator(root)
    root.mainloop()

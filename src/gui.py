"""Графический терминал на tkinter."""
import tkinter as tk

BG = "#111111"
FG = "#dddddd"
PROMPT_FG = "#77ff77"
FONT = ("Courier", 11)
TEXT_HEIGHT = 28
TEXT_WIDTH = 100


class Terminal:
    """Окно, имитирующее терминал: журнал вывода и строка ввода."""

    def __init__(self, root, shell, title, banner=""):
        self.root = root
        self.shell = shell
        self.history = []
        self.hist_pos = 0
        root.title(title)
        self._build_widgets()
        self.write(banner)
        self.refresh_prompt()

    def _build_widgets(self):
        """Создаёт журнал, приглашение и строку ввода."""
        self.log = tk.Text(
            self.root, bg=BG, fg=FG, font=FONT, state="disabled",
            wrap="word", height=TEXT_HEIGHT, width=TEXT_WIDTH)
        self.log.pack(fill="both", expand=True)
        row = tk.Frame(self.root, bg=BG)
        row.pack(fill="x")
        self.prompt = tk.Label(row, bg=BG, fg=PROMPT_FG, font=FONT)
        self.prompt.pack(side="left")
        self.entry = tk.Entry(
            row, bg=BG, fg=FG, insertbackground=FG, font=FONT,
            relief="flat")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.bind("<Up>", lambda _e: self.history_move(-1))
        self.entry.bind("<Down>", lambda _e: self.history_move(1))
        self.entry.focus_set()

    def write(self, text):
        """Добавляет текст в журнал."""
        self.log.config(state="normal")
        self.log.insert(tk.END, text)
        self.log.see(tk.END)
        self.log.config(state="disabled")
        self.root.update_idletasks()

    def refresh_prompt(self):
        """Обновляет текст приглашения."""
        self.prompt.config(text=self.shell.prompt())

    def on_enter(self, _event):
        """Выполняет введённую строку."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.write(self.shell.prompt() + line + "\n")
        if line.strip():
            self.history.append(line)
        self.hist_pos = len(self.history)
        self.show_result(self.shell.execute(line))

    def show_result(self, result):
        """Печатает результат команды; при exit закрывает окно."""
        if result.out:
            self.write(result.out + "\n")
        if result.exit:
            self.root.destroy()
        else:
            self.refresh_prompt()

    def history_move(self, delta):
        """Листает историю команд стрелками вверх и вниз."""
        if not self.history:
            return
        last = len(self.history)
        self.hist_pos = max(0, min(last, self.hist_pos + delta))
        self.entry.delete(0, tk.END)
        if self.hist_pos < last:
            self.entry.insert(0, self.history[self.hist_pos])

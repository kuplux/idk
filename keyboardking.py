import tkinter as tk
import random
import time

class KeyboardKingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Keyboard King")
        self.score = 0
        self.rounds_left = 10
        self.current_color = None
        self.game_running = False

        # Menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.help_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Nápověda", command=self.show_help)
        self.help_menu.add_command(label="O hře", command=self.show_about)
        
        # Canvas
        self.canvas = tk.Canvas(self.master, width=600, height=400, bg='white')
        self.canvas.pack()

        # Score label
        self.score_label = tk.Label(self.master, text=f"Skóre: {self.score} | Kola zbývají: {self.rounds_left}")
        self.score_label.pack()

        # Game control
        self.rectangles = {
            'S': self.canvas.create_rectangle(50, 350, 100, 400, fill='gray'),
            'D': self.canvas.create_rectangle(150, 350, 200, 400, fill='gray'),
            'F': self.canvas.create_rectangle(250, 350, 300, 400, fill='gray'),
            'J': self.canvas.create_rectangle(350, 350, 400, 400, fill='gray'),
            'K': self.canvas.create_rectangle(450, 350, 500, 400, fill='gray'),
            'L': self.canvas.create_rectangle(550, 350, 600, 400, fill='gray'),
        }

        self.start_game()

    def start_game(self):
        self.score = 0
        self.rounds_left = 10
        self.game_running = True
        self.update_score_label()
        self.next_round()

    def next_round(self):
        if self.rounds_left > 0:
            self.rounds_left -= 1
            self.update_score_label()
            self.current_color = random.choice(list(self.rectangles.keys()))
            self.canvas.itemconfig(self.rectangles[self.current_color], fill='red')
            self.show_key_to_press(self.current_color)
            self.master.after(1000, self.reset_rectangles)
            self.fall_circle()
        else:
            self.end_game()

    def fall_circle(self):
        self.circle = self.canvas.create_oval(275, 0, 325, 50, fill='blue')
        for i in range(300):  # Circle falls down
            self.canvas.move(self.circle, 0, 1)
            self.master.update()
            time.sleep(0.01)
        self.canvas.delete(self.circle)
        self.next_round()

    def show_key_to_press(self, key):
        self.canvas.create_text(300, 50, text=f"Stiskněte: {key}", font=('Arial', 20), fill='black', tag="key_text")

    def reset_rectangles(self):
        for key, rect in self.rectangles.items():
            color = 'gray' if key != self.current_color else 'black'
            self.canvas.itemconfig(rect, fill=color)
        self.current_color = None
        self.canvas.delete("key_text")  # Remove the key press instruction

    def key_pressed(self, event):
        if self.game_running and event.char.upper() in self.rectangles:
            if event.char.upper() == self.current_color:
                self.score += 1
                self.canvas.itemconfig(self.rectangles[event.char.upper()], fill='black')
            self.update_score_label()

    def update_score_label(self):
        self.score_label.config(text=f"Skóre: {self.score} | Kola zbývají: {self.rounds_left}")

    def end_game(self):
        self.game_running = False
        self.canvas.create_text(300, 200, text="Konec hry!", font=('Arial', 24), fill='red')

    def show_help(self):
        help_window = tk.Toplevel(self.master)
        help_window.title("Nápověda")
        help_text = "Stiskněte správnou klávesu co nejrychleji, když se rozsvítí odpovídající obdélník."
        label = tk.Label(help_window, text=help_text, padx=20, pady=20)
        label.pack()

    def show_about(self):
        about_window = tk.Toplevel(self.master)
        about_window.title("O hře")
        about_text = "Verze: 1.0\nAutor:\n(Jan Vápeník)"
        label = tk.Label(about_window, text=about_text, padx=20, pady=20)
        label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = KeyboardKingGame(root)
    root.bind('<KeyPress>', game.key_pressed)
    root.mainloop()

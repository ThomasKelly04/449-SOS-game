import tkinter as tk
from tkinter import ttk
from tkinter import font
from typing import NamedTuple
from itertools import cycle
from game_logic import SOSGame, DEFAULT_PLAYERS, Move

# create game board
class SOSBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("SOS Game")
        self._cells: dict[tk.Button, tuple[int, int]] = {}
        self._game = game
        self._pos_to_bin: dict[tuple[int,int], tk.Button] = {}
        self.grid_frame: tk.Frame | None = None
        self.strike_canvas: tk.Canvas | None = None
        self.grid_frame = None
        self._create_menu()
        self.create_board_display()
        self.create_board_grid()


    def create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X, padx=8, pady=(8,0))
        self.display = tk.Label(
            master=display_frame,
            text="Play!",
            font=font.Font(size=28, weight="bold")
        )
        self.display.pack(side=tk.LEFT)
        # adding controls for picking S/O, board size, and starting game
        controls = tk.Frame(master=self)
        controls.pack(fill=tk.X, padx=8, pady=8)
        # S/O buttons

        self.mode_var = tk.StringVar(value=self._game.mode)
        tk.Label(controls, text="Mode").pack(side=tk.LEFT, padx=(12,6))
        tk.Radiobutton(controls, text="Simple", variable=self.mode_var, value="simple").pack(side=tk.LEFT)
        tk.Radiobutton(controls, text="General", variable=self.mode_var, value="general").pack(side=tk.LEFT)

        self.mode_var.trace_add("write", lambda *_: print("SELECTED MODE:", self.mode_var.get()))

        self.letter_var = tk.StringVar(value="S")
        tk.Label(controls, text="Place:").pack(side=tk.LEFT, padx=(0,6))
        tk.Radiobutton(controls, text="S", variable=self.letter_var, value="S").pack(side=tk.LEFT)
        tk.Radiobutton(controls, text="O", variable=self.letter_var, value="O").pack(side=tk.LEFT, padx=(6,12))

        tk.Label(controls, text="Board size:").pack(side=tk.LEFT, padx=(12,6))
        self.size_var = tk.IntVar(value=self._game.board_size)
        self.size_slider = tk.Scale(
            controls, from_=3, to=12, orient=tk.HORIZONTAL,
            variable=self.size_var, showvalue=True, length=200
        )
        self.size_slider.pack(side=tk.LEFT)

        

        ttk.Button(controls, text="Start New Game", command=self.start_new_game_with_size).pack(side=tk.LEFT, padx=12)
        ttk.Button(controls, text="play again", command=self.reset_board).pack(side=tk.LEFT)

    def create_board_grid(self):
        
        if self.grid_frame is not None:
            self.grid_frame.destroy()
            self._cells.clear()
            self._pos_to_bin.clear()

        self.grid_frame = tk.Frame(master=self)
        self.grid_frame.pack(padx=8, pady=8)

        
        
        for row in range(self._game.board_size):
            self.grid_frame.rowconfigure(row, weight=1, minsize=50)
            self.grid_frame.columnconfigure(row, weight=1, minsize=75)
            for col in range (self._game.board_size):
                button = tk.Button(
                    master=self.grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                self._pos_to_bin[(row, col)] = button
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
                #self.strike_canvas = tk.Canvas(self.grid_frame, highlightthickness=0, bg=self.cget("bg"))
        #self.strike_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

    def play(self, event):
        print("MODE:", self._game.mode)
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]

        chosen_letter = self.letter_var.get()
        move = Move(row, col, chosen_letter)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn, chosen_letter, self._game.current_player.color)
            self._game.process_move(move)
            new_sos = self._game.last_new_sos
            if new_sos:
                self._draw_strikes(new_sos, self._game.current_player.color)
            if self._game.is_tied():
                if self._game.mode == "general":
                    msg=f"Tie! Scores = {self._score_text()}"
                else:
                    msg = "tied game!"
                self._update_display(msg = msg, color ="red")
            elif self._game.has_winner():
                if self._game.mode == "simple":
                    msg = f'Winner: {self._game.current_player.label}!'
                    color = self._game.current_player.color
                else:
                    msg = f'Winner: {self._game.winner_label}! Final scores - {self._score_text()}'
                    color = "green"
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def start_new_game_with_size(self):
        size = int(self.size_var.get())
        mode = self.mode_var.get()
        self._game = SOSGame(players=DEFAULT_PLAYERS, board_size=size, mode = mode)
        print("NEW GAME MODE:", self._game.mode)
        self._update_display(msg=f"New {size}x{size} game! Player {self._game.current_player.label} starts.")
        self.create_board_grid()

    def _update_button(self, clicked_btn, letter, color):
        clicked_btn.config(text=letter, fg = color)

    def _update_display(self, msg, color='black'):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def reset_board(self):
        mode = self.mode_var.get()
        size = int(self.size_var.get())
        self._game.reset_game(mode = mode, board_size=size)
        if self.strike_canvas:
            self.strike_canvas.delete("all")
        self._update_display(msg="ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text='')
            button.config(fg='black')
    
    def _cell_center(self, r: int, c: int):
        btn = self._pos_to_bin[(r, c)]
        x = btn.winfo_x() + btn.winfo_width() // 2
        y = btn.winfo_y() + btn.winfo_height() // 2
        return x, y

    def _draw_strikes(self, triples, color: str):
        for triple in triples:
            for (r, c) in triple:
                btn = self._pos_to_bin[(r, c)]
                f = font.Font(font=btn["font"])
                f.configure(overstrike=1)
                btn.config(font=f, fg=color)
    
    def _score_text(self) -> str:
        return " | ".join(f"{label}: {score}" for label, score in self._game.scores.items())
    

    

# run the gui
def main():
    game = SOSGame()
    board = SOSBoard(game)
    board.mainloop()

if __name__ ==  "__main__":
    main()

import tkinter as tk
from tkinter import ttk
from tkinter import font
from typing import NamedTuple
from itertools import cycle

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE=6
DEFAULT_PLAYERS=(
    Player(label="A", color="Blue"),
    Player(label="B", color="Red"),
)



class SOSGame:
    DIRECTIONS = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1),
        (-1, -1), (1, 1),
        (-1, 1), (1, -1),
        ]
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE, mode: str = "simple"):
        assert mode in {"simple", "general"}, "mode must be 'simple' or 'general'"
        
        self._players = cycle(players)
        self.players = players
        self.mode = mode
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo=[]
        self._current_moves = [
            [Move(r, c) for c in range(self.board_size)]
            for r in range(self.board_size)
        ]
        self._has_winner = False
        self._game_over = False
        self._winning_combos = []
        self.winner_label = None
        self.scores = {p.label: 0 for p in players}
        self._seen_sos = set()
        self.last_new_sos = []

        self._setup_board()

    

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()
        
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]
    def is_valid_move(self, move):
        if self._game_over or (self._has_winner and self.mode == "simple"):
            return False
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    def process_move(self, move):
        if not self.is_valid_move(move):
            self.last_new_sos = []
            return []
        r, c, ch = move
        self._current_moves[r][c] = move
        new_sos = self._find_new_sos_from_move(move)
        self.last_new_sos = new_sos
        if new_sos:
            if self.mode == "simple":
                self._has_winner = True
                self._game_over = True
                self.winner_label = self.current_player.label
                self.winner_combo = new_sos[-1]
            else:
                self.scores[self.current_player.label] += len(new_sos)
        if self.mode == "general":
            if all(m.label for row in self._current_moves for m in row):
                self._game_over = True
                sorted_scores = sorted(self.scores.items(), key=lambda kv: kv[1], reverse=True)
                if len(sorted_scores) >= 2 and sorted_scores[0][1] > sorted_scores[1][1]:
                    self._has_winner = True
                    self.winner_label = sorted_scores[0][0]
                else:
                    self._has_winner = False
                    self.winner_label = None
        return new_sos
    def is_over(self) -> bool:
        return self._game_over
    
    def has_winner(self):
        return self._has_winner
    def is_tied(self):
        if self.mode == "simple":
            full = all(m.label for row in self._current_moves for m in row)
            return full and not self._has_winner
        else:
            if not self._game_over:
                return False
            vals = list(self.scores.values())
            return len(vals) >= 2 and vals[0] == vals[1]

        
    def toggle_player(self):
        self.current_player = next(self._players)
    def reset_game(self, *, mode: str | None = None, board_size: int | None = None):
        if mode is not None:
            assert mode in {"simple", "general"}
            self.mode = mode
        if board_size is not None:
            self.board_size = int(board_size)
        self._current_moves = [
            [Move(r, c) for c in range(self.board_size)]
            for r in range(self.board_size)
        ]
        self._has_winner = False
        self._game_over = False
        self.winner_combo = []
        self.winner_label = None
        self._seen_sos.clear()
        self.last_new_sos = []
        self.scores = {p.label: 0 for p in self.players}
    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.board_size and 0 <= c < self.board_size
    def _cell_label(self, r: int, c: int) -> str:
        return self._current_moves[r][c].label
    def _find_new_sos_from_move(self, move: Move):
        r, c, ch = move
        new_triples = []
        if ch == "O":
            for dr, dc in self.DIRECTIONS:
                r1, c1 = r - dr, c - dc
                r2, c2 = r + dr, c + dc
                if self._in_bounds(r1, c1) and self._in_bounds(r2, c2):
                    if self._cell_label(r1, c1) == "S" and self._cell_label(r2, c2) == "S":
                        triple = [(r1, c1), (r, c), (r2, c2)]
                        key = frozenset(triple)
                        if key not in self._seen_sos:
                            self._seen_sos.add(key)
                            new_triples.append(triple)
        if ch == "S":
            for dr, dc in self.DIRECTIONS:
                r_mid, c_mid = r + dr, c + dc
                r_end, c_end = r + 2*dr, c + 2*dc
                if self._in_bounds(r_mid, c_mid) and self._in_bounds(r_end, c_end):
                    if self._cell_label(r_mid, c_mid) == "O" and self._cell_label(r_end, c_end) == "S":
                        triple = [(r, c), (r_mid, c_mid), (r_end, c_end)]
                        key = frozenset(triple)
                        if key not in self._seen_sos:
                            self._seen_sos.add(key)
                            new_triples.append(triple)
        return new_triples
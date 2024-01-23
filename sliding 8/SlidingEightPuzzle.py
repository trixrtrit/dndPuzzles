import time
import tkinter as tk
from tkinter import messagebox
import random


class SlidingEightPuzzle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sliding Eight Puzzle")
        self.winning_condition = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.tiles = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        random.shuffle(self.tiles)
        if not self.is_solvable(self.tiles):
            while not self.is_solvable(self.tiles):
                random.shuffle(self.tiles)
        self.grid_frames = []
        self.empty_tile_index = self.tiles.index(0)
        self.timer_started = False
        self.start_time = 0
        self.moves = 0
        self.init_ui()
        self.init_timer()

    def init_ui(self):
        for i in range(len(self.tiles)):
            tile = self.tiles[i]
            button = tk.Button(self, text=str(tile) if tile != 0 else "",
                               width=10, height=5, command=lambda tile_pos=i: self.move_tile(tile_pos))
            button.grid(row=i // 3, column=i % 3)
            self.grid_frames.append(button)
        self.timer_label = tk.Label(self, text="00:00:00")
        self.timer_label.grid(row=3, column=0, columnspan=3)
        self.moves_label = tk.Label(self, text="Moves: ")
        self.moves_label.grid(row=4, column=0, columnspan=3)

    def init_timer(self):
        self.elapsed_time = 0
        self.update_timer()

    def start_timer(self):
        if not self.timer_started:
            self.timer_started = True
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()

    def stop_timer(self):
        self.timer_started = False

    def update_timer(self):
        if self.timer_started:
            self.elapsed_time = time.time() - self.start_time
            elapsed_formatted = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))
            self.timer_label.config(text=elapsed_formatted)
            self.after(1000, self.update_timer)

    def update_move_counter(self):
        if self.timer_started:
            self.moves += 1
            self.moves_label.config(text="Moves: " + str(self.moves))
    def move_tile(self, index):
        self.start_timer()
        if self.is_valid_move(index):
            self.tiles[self.empty_tile_index], self.tiles[index] = self.tiles[index], self.tiles[self.empty_tile_index]
            self.empty_tile_index = index
            self.update_move_counter()
            self.refresh_board()
            self.is_winner()

    def is_valid_move(self, index):
        row_diff = abs(index // 3 - self.empty_tile_index // 3)
        col_diff = abs(index % 3 - self.empty_tile_index % 3)
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)

    def refresh_board(self):
        for i, tile in enumerate(self.tiles):
            self.grid_frames[i].config(text=str(tile) if tile != 0 else "")

    def is_winner(self):
        if self.tiles == self.winning_condition:
            self.disable_buttons()
            messagebox.showinfo("Congratulations!", "You've solved the puzzle!")
            self.stop_timer()

    def disable_buttons(self):
        for button in self.grid_frames:
            button.config(state='disabled')

    def count_inversions(self, tiles):
        inv_count = 0
        tiles_flat = [tile for tile in tiles if tile != 0]
        for i in range(len(tiles_flat)):
            for j in range(i + 1, len(tiles_flat)):
                if tiles_flat[i] > tiles_flat[j]:
                    inv_count += 1
        return inv_count

    def is_solvable(self, tiles):
        return self.count_inversions(tiles) % 2 == 0



if __name__ == "__main__":
    game = SlidingEightPuzzle()
    game.mainloop()

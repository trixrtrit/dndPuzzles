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

        self.empty_tile_index = self.tiles.index(0)
        self.grid_frames = []
        self.init_ui()

    def init_ui(self):
        for i in range(len(self.tiles)):
            tile = self.tiles[i]
            button = tk.Button(self, text=str(tile) if tile != 0 else "",
                               width=10, height=5, command=lambda tile_pos=i: self.move_tile(tile_pos))
            button.grid(row=i // 3, column=i % 3)
            self.grid_frames.append(button)

    def move_tile(self, index):
        if self.is_valid_move(index):
            self.tiles[self.empty_tile_index], self.tiles[index] = self.tiles[index], self.tiles[self.empty_tile_index]
            self.empty_tile_index = index
            self.refresh_board()
            self.is_winner()

    def is_valid_move(self, index):
        row_diff = abs(index // 3 - self.empty_tile_index // 3)
        col_diff = abs(index % 3 - self.empty_tile_index % 3)
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)

    def refresh_board(self):
        print(f"Refreshing board")
        for i, tile in enumerate(self.tiles):
            self.grid_frames[i].config(text=str(tile) if tile != 0 else "")

    def is_winner(self):
        if self.tiles == self.winning_condition:
            messagebox.showinfo("Congratulations!", "You've solved the puzzle!")

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

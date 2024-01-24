import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import ProcessImage as procImg


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
        self.image_path = './owl.png'
        self.img_tiles = procImg.process_image(self.image_path)
        self.geometry("800x800")
        self.init_ui()
        self.init_timer()

    def init_ui(self):
        self.tile_frames = []
        self.tile_labels = []
        self.tk_img_tiles = [ImageTk.PhotoImage(image=tile) for tile in self.img_tiles]
        tile_size = (100, 100)

        for i in range(len(self.tiles)):
            frame = tk.Frame(self, width=tile_size[0], height=tile_size[1])
            frame.grid(row=i // 3, column=i % 3)
            frame.grid_propagate(False)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)

            if self.tiles[i] != 0:
                label = tk.Label(frame, image=self.tk_img_tiles[self.tiles[i] - 1])
            else:
                label = tk.Label(frame, background='black')  # Empty tile
            label.grid(sticky="nsew")
            label.bind("<Button-1>", lambda event, tile_pos=i: self.move_tile(tile_pos))

            self.tile_frames.append(frame)
            self.tile_labels.append(label)
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
        for i, tile_index in enumerate(self.tiles):
            if tile_index != 0:
                self.tile_labels[i].config(image=self.tk_img_tiles[tile_index - 1])
            else:
                self.tile_labels[i].config(image='', background='black')

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

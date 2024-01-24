import time
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import random
import sliding_puzzle.ProcessImage as procImg
import sliding_puzzle.ListImages as listImgs


class SlidingEightPuzzle(tk.Tk):
    def __init__(self, difficulty=3, image_path=None):
        super().__init__()
        self.title("Sliding Eight Puzzle")
        self.difficulty = difficulty
        self.grid_size = difficulty * difficulty
        if image_path is None:
            self.image_files = listImgs.list_images('./symbols')
            self.wins_needed = len(self.image_files)
        else:
            self.image_files = [image_path]
            self.wins_needed = 1
        self.current_image_index = 0
        self.current_wins = 0
        self.grid_frames = []
        self.geometry("800x800")
        self.starting_state = None
        self.setup_game()

    def setup_game(self):
        self.tiles = [i for i in range(1, self.grid_size)] + [0]
        self.winning_condition = self.tiles[:]
        random.shuffle(self.tiles)
        while not self.is_solvable(self.tiles):
            random.shuffle(self.tiles)
        self.starting_state = self.tiles[:]
        self.empty_tile_index = self.tiles.index(0)
        self.img_tiles = procImg.process_image(
            self.image_files[self.current_image_index],
            grid_size=(self.difficulty, self.difficulty)
        )
        self.timer_started = False
        self.start_time = 0
        self.moves = 0
        self.init_ui()
        self.init_timer()

    def init_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Button(self, text="Reset", command=lambda: self.reset_game()).grid(row=self.difficulty + 2, column=0, columnspan=3)
        self.tile_frames = []
        self.tile_labels = []
        self.tk_img_tiles = [ImageTk.PhotoImage(image=tile) for tile in self.img_tiles]
        tile_size = (100, 100)

        for i in range(self.grid_size):
            frame = tk.Frame(self, width=tile_size[0], height=tile_size[1])
            frame.grid(row=i // self.difficulty, column=i % self.difficulty)
            frame.grid_propagate(False)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)

            if self.tiles[i] != 0:
                label = tk.Label(frame, image=self.tk_img_tiles[self.tiles[i] - 1])
            else:
                label = tk.Label(frame, background='black')
            label.grid(sticky="nsew")
            label.bind("<Button-1>", lambda event, tile_pos=i: self.move_tile(tile_pos))

            self.tile_frames.append(frame)
            self.tile_labels.append(label)
        self.timer_label = tk.Label(self, text="00:00:00")
        self.timer_label.grid(row=self.difficulty, column=0, columnspan=3)
        self.moves_label = tk.Label(self, text="Moves: ")
        self.moves_label.grid(row=self.difficulty + 1, column=0, columnspan=3)

    def reset_game(self):
        self.stop_timer()
        for i in range(len(self.starting_state)):
            self.tiles[i] = self.starting_state[i]
        self.current_wins = 0
        self.current_image_index = 0
        self.moves = 0
        self.empty_tile_index = self.tiles.index(0)
        self.img_tiles = procImg.process_image(
            self.image_files[self.current_image_index],
            grid_size=(self.difficulty, self.difficulty)
        )
        self.init_ui()

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
        print(index)
        self.start_timer()
        if self.is_valid_move(index):
            self.tiles[self.empty_tile_index], self.tiles[index] = self.tiles[index], self.tiles[self.empty_tile_index]
            self.empty_tile_index = index
            self.update_move_counter()
            self.refresh_board()
            self.is_winner()

    def is_valid_move(self, index):
        row_diff = abs(index // self.difficulty - self.empty_tile_index // self.difficulty)
        col_diff = abs(index % self.difficulty - self.empty_tile_index % self.difficulty)
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
            self.current_wins += 1
            self.current_image_index += 1
            self.stop_timer()
            self.load_next_image()

    def load_next_image(self):
        if self.current_wins < self.wins_needed:
            self.image_path = self.image_files[self.current_image_index]
            self.setup_game()
        else:
            self.stop_timer()
            self.disable_buttons()
            messagebox.showinfo("Congratulations!", "You've beat the challenge!")

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
        if self.difficulty == 3:
            return self.count_inversions(tiles) % 2 == 0
        else:
            inversions = self.count_inversions(tiles)
            empty_tile_row = self.find_empty_tile_row(tiles, self.grid_size)
            if (empty_tile_row % 2 == 0 and inversions % 2 != 0) or (empty_tile_row % 2 != 0 and inversions % 2 == 0):
                return True
            return False

    def find_empty_tile_row(self, tiles, grid_size):
        empty_tile_index = tiles.index(0)
        row_from_top = empty_tile_index // grid_size
        row_from_bottom = grid_size - row_from_top - 1
        return row_from_bottom

import tkinter as tk
from tkinter import filedialog, messagebox
from sliding_eight_puzzle import SlidingEightPuzzle
import shutil


class GameLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Select Difficulty")
        self.geometry("300x250")
        self.image_path = None
        tk.Button(self, text="Easy (3x3) grid", command=lambda: self.start_game(3)).pack(pady=5)
        tk.Button(self, text="Medium (4x4) grid", command=lambda: self.start_game(4)).pack(pady=5)
        tk.Button(self, text="Hard (5x5) grid", command=lambda: self.start_game(5)).pack(pady=5)
        tk.Button(self, text="Add and Use Your Own Picture", command=self.use_custom_picture).pack(pady=10)

    def start_game(self, difficulty):
        self.destroy()
        game = SlidingEightPuzzle(difficulty=difficulty, image_path=self.image_path)
        game.mainloop()

    def use_custom_picture(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=(("JPEG files", "*.jpg;*.jpeg"), ("PNG files", "*.png"), ("All files", "*.*"))
        )
        if file_path:
            self.image_path = file_path
        else:
            messagebox.showinfo("No Image Selected", "Please select an image to use for the puzzle.")


if __name__ == '__main__':
    launcher = GameLauncher()
    launcher.mainloop()

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
from All_Functions import (
    llama_request,
    extract_prompts_and_Process_results,
    process_results_further,
    send_SD_requests,
)
from imager2 import Images_for_Chunks


# Function to delete the contents of a but not the folder itself
def delete_contents(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


delete_contents("VN_Images")
delete_contents("generated_images")


colab_ngrok_url_llama = "http://56c4-34-125-169-239.ngrok-free.app"
colab_ngrok_SD = "http://59d3-34-125-203-124.ngrok-free.app/"
file_path = "The Bet.txt"

Result_text = llama_request(file_path, colab_ngrok_url_llama)
image_prompts, processed_results = extract_prompts_and_Process_results(Result_text)
send_SD_requests(image_prompts, colab_ngrok_SD)


processed_results = process_results_further(processed_results)
chunk_number = 1
index = 0
for text in processed_results:
    Images_for_Chunks(text, chunk_number, f"generated_images/{index}.png")
    chunk_number += 1
    index += 1

# Initialize pygame mixer for playing background music
pygame.mixer.init()


class VisualNovelApp:
    def __init__(self, root, image_directory):
        self.root = root
        self.root.title("Visual Novel")
        self.image_directory = image_directory

        # Get a list of image files in the specified directory
        self.image_files = sorted(
            [
                f
                for f in os.listdir(image_directory)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
            ]
        )
        self.current_image_index = 0

        # Load and display the first image
        self.load_image()

        # Load and play background music
        pygame.mixer.music.load("mixkit-hazy-after-hours-132.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop infinitely

        # Create navigation buttons
        self.prev_button = ttk.Button(
            root, text="Previous", style="NavButton.TButton", command=self.prev_image
        )
        self.prev_button.pack(side=tk.LEFT, padx=10)
        self.next_button = ttk.Button(
            root, text="Next", style="NavButton.TButton", command=self.next_image
        )
        self.next_button.pack(side=tk.RIGHT, padx=10)

        # Bind arrow keys for navigation
        self.root.bind("<Left>", self.prev_image)
        self.root.bind("<Right>", self.next_image)

        # Style for navigation buttons
        style = ttk.Style()
        style.configure("NavButton.TButton", font=("Helvetica", 12), padding=5)

        # Bind F11 key to toggle full screen
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.fullscreen = False

    def load_image(self):
        if self.image_files:
            image_path = os.path.join(
                self.image_directory, self.image_files[self.current_image_index]
            )
            image = Image.open(image_path)
            image.thumbnail(
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
            )
            photo = ImageTk.PhotoImage(image)

            if hasattr(self, "image_label"):
                self.image_label.config(image=photo)
                self.image_label.image = photo
            else:
                self.image_label = ttk.Label(self.root, image=photo)
                self.image_label.pack()
                self.image_label.photo = photo

    def prev_image(self, event=None):
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(
                self.image_files
            )
            self.load_image()

    def next_image(self, event=None):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(
                self.image_files
            )
            self.load_image()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        self.load_image()

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)
        self.load_image()


if __name__ == "__main__":
    image_directory = "VN_Images"
    root = tk.Tk()
    app = VisualNovelApp(root, image_directory)
    root.mainloop()

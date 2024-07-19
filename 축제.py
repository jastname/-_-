import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random

Horse_l = ["C:\\Users\\AISW\\Desktop\\경마\\goldship.png", "C:\\Users\\AISW\\Desktop\\경마\\goldship2.png", "C:\\Users\\AISW\\Desktop\\경마\\goldship3.png"]

class Horse:
    def __init__(self, name, color, min_speed, max_speed, image_paths):
        self.name = name
        self.color = color
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.position = 0
        self.shape = None
        self.text_name = None
        self.text_distance = None
        self.image_index = 0
        self.images = []

        for image_path in image_paths:
            try:
                image = Image.open(image_path)  # Load image
                image = image.resize((100, 80), Image.LANCZOS)  # Resize image
                photo = ImageTk.PhotoImage(image)  # Create PhotoImage object
                self.images.append(photo)
            except Exception as e:
                print(f"Error loading image for {name}: {e}")

        if not self.images:
            self.images = [None]

        print(f"말 이름: {name}, 색상: {color}, 속도 범위: {min_speed}-{max_speed}")

class HorseApp:
    special_horse = None  # Class attribute to define the horse that is easier to win with
    FONT_SIZE = 14  # Specify the font size

    def __init__(self, root):
        # Initialize the application
        self.root = root
        self.root.title("경마 게임")
        self.root.option_add("*Font", f"Helvetica {self.FONT_SIZE}")
        self.canvas = tk.Canvas(root, width=1200, height=600)  # Set canvas width to 1200
        self.canvas.pack()

        # Racing parameters
        self.finish_line = 1000

        # Horse names and number of horses
        self.horse_names = ["1번 마", "2번 마", "3번 마", "4번 마", "5번 마"]
        self.num_horses = self.ask_num_horses()

        self.horses = self.create_horses(self.num_horses)

        # Bind keyboard event
        self.root.bind("<KeyPress>", self.key_press_event)

        # Race start and restart buttons
        self.start_race_button = tk.Button(root, text="경주 시작", command=self.start_race)
        self.start_race_button.pack()

        self.restart_btn = tk.Button(root, text="다시하기", command=self.restart)
        self.restart_btn.pack()

        # Label to display winner information
        self.winner_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.winner_label.place(relx=0.5, rely=0.5, anchor="center")

        # Draw finish line
        self.draw_finish_line()
        self.start_race()

    def ask_num_horses(self):
        while True:
            try:
                num_horses = simpledialog.askinteger("Input", "몇 마리의 말로 경마를 시작하시겠습니까? (최대 5마리): ")
                if num_horses is not None and 1 <= num_horses <= 5:
                    return num_horses
                else:
                    messagebox.showwarning("Warning", "1에서 5 사이의 값을 입력하세요.")
            except (ValueError, TypeError):
                messagebox.showwarning("Warning", "유효한 숫자를 입력하세요.")

    def create_horses(self, num_horses):
        horses = []
        colors = ['orange', 'green', 'red', 'lightblue', 'lightpink']
        speed_ranges = [(12, 38), (16, 34), (12, 38), (18, 33), (7, 43)]

        for i in range(num_horses):
            name = self.horse_names[i]
            color = colors[i]
            min_speed, max_speed = speed_ranges[i]
            image_paths = Horse_l
            horse = Horse(name, color, min_speed, max_speed, image_paths)
            horses.append(horse)
        return horses

    def draw_finish_line(self):
        # Draw finish line on canvas
        self.canvas.create_line(self.finish_line, 0, self.finish_line, 800, fill="black", dash=(4, 2))
        self.canvas.create_text(self.finish_line, 20, text="결승선", anchor="n")

    def start_race(self):
        # Start the race
        self.start_race_button.config(state=tk.DISABLED)
        self.restart_btn.config(state=tk.DISABLED)
        self.winner_label.config(text="")

        for i, horse in enumerate(self.horses):
            horse.position = 0
            y_position = i * 100 + 60
            horse.image_index = 0  # Set initial image index
            if horse.images[0]:
                horse.shape = self.canvas.create_image(50, y_position, image=horse.images[0], anchor="nw")
            else:
                horse.shape = self.canvas.create_rectangle(50, y_position - 40, 150, y_position + 40, fill=horse.color)
            horse.text_name = self.canvas.create_text(75, y_position, text=horse.name, anchor="w", font=("Helvetica", 14))  # Adjust name position
            horse.text_distance = self.canvas.create_text(400, y_position, text="0m", anchor="center", font=("Helvetica", 14))
            
        self.update_positions()

    def update_positions(self):
        # Update horse positions until a winner is determined
        if not any(horse.position + 150 >= self.finish_line for horse in self.horses):  # If the front of the horse reaches the finish line
            for i, horse in enumerate(self.horses):
                if horse.position + 150 < self.finish_line:  # If the front of the horse does not reach the finish line
                    if horse.name == self.special_horse:
                        move_distance = random.randint(horse.min_speed + 5, horse.max_speed + 5)  # The horse that is easier to win with moves faster
                    else:
                        move_distance = random.randint(horse.min_speed, horse.max_speed)
                    horse.position += move_distance
                    if horse.position + 150 > self.finish_line:
                        horse.position = self.finish_line - 150

                    horse.image_index = (horse.image_index + 1) % len(horse.images)  # Update image index
                    y_position = i * 100 + 60
                    if horse.images[horse.image_index]:
                        self.canvas.itemconfig(horse.shape, image=horse.images[horse.image_index])
                    self.canvas.coords(horse.shape, 50 + horse.position, y_position)
                    self.canvas.itemconfig(horse.text_distance, text=f"{horse.position}m")

            self.root.after(1000, self.update_positions)
        else:
            self.declare_winner()

    def declare_winner(self):
        winner_names = [horse.name for horse in self.horses if horse.position + 150 >= self.finish_line]  # If the front of the horse reaches the finish line
        if len(winner_names) > 1:
            winner = random.choice(winner_names)
            self.winner_label.config(text=f"우승한 말은 '{winner}'입니다!")
        else:
            self.winner_label.config(text=f"우승한 말은 '{winner_names[0]}'입니다!")
        self.winner_label.place(relx=0.5, rely=0.8, anchor="center")  # Adjust winner label position
        self.start_race_button.config(state=tk.NORMAL)
        self.restart_btn.config(state=tk.NORMAL)

    def key_press_event(self, event):
        # Handle keyboard event for selecting the horse that is easier to win with
        key = event.char
        if key.isdigit() and int(key) in range(1, self.num_horses + 1):
            self.special_horse = self.horses[int(key) - 1].name  # Set the selected horse as the horse that is easier to win with

    def restart(self):
        # Restart the game
        self.special_horse = None  # Reset special horse
        self.canvas.delete("all")
        self.draw_finish_line()
        self.num_horses = self.ask_num_horses()
        self.horses = self.create_horses(self.num_horses)
        self.winner_label.config(text="")  # Reset winner label
        self.start_race()

if __name__ == "__main__":
    root = tk.Tk()
    app = HorseApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from PIL import Image, ImageTk

Horse_l = ["goldship2.png", "goldship3.png", "goldship.png"]

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
                image = Image.open(image_path)  # 이미지 로드
                image = image.resize((100, 80), Image.Resampling.LANCZOS)  # 이미지 크기 조정
                photo = ImageTk.PhotoImage(image)  # PhotoImage 객체 생성
                self.images.append(photo)
            except Exception as e:
                print(f"Error loading image for {name}: {e}")

        if not self.images:
            self.images = [None]

        print(f"말 이름: {name}, 색상: {color}, 속도 범위: {min_speed}-{max_speed}")

class HorseApp:
    special_horse = None  # 클래스 속성으로 이기기 쉬운 말을 정의합니다.
    FONT_SIZE = 14  # 폰트 크기를 지정합니다.

    def __init__(self, root):
        # 애플리케이션 초기화
        self.root = root
        self.root.title("경마 게임")
        self.root.option_add("*Font", f"Helvetica {self.FONT_SIZE}")
        self.canvas = tk.Canvas(root, width=1200, height=600)  # 캔버스 너비를 1200으로 설정
        self.canvas.pack()

        # 경주 매개변수
        self.finish_line = 1000

        # 말의 이름과 말의 수
        self.horse_names = ["1번 마", "2번 마", "3번 마", "4번 마", "5번 마"]
        self.num_horses = self.ask_num_horses()

        self.horses = self.create_horses(self.num_horses)

        # 키보드 이벤트 바인딩
        self.root.bind("<KeyPress>", self.key_press_event)

        # 경주 시작 및 재시작 버튼
        self.start_race_button = tk.Button(root, text="경주 시작", command=self.start_race)
        self.start_race_button.pack()

        self.restart_btn = tk.Button(root, text="다시하기", command=self.restart)
        self.restart_btn.pack()

        # 우승한 말의 정보를 표시할 라벨
        self.winner_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.winner_label.place(relx=0.5, rely=0.5, anchor="center")

        # 결승선 그리기
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
        # 캔버스에 결승선 그리기
        self.canvas.create_line(self.finish_line, 0, self.finish_line, 800, fill="black", dash=(4, 2))
        self.canvas.create_text(self.finish_line, 20, text="결승선", anchor="n")

    def start_race(self):
        # 경마 시작
        self.start_race_button.config(state=tk.DISABLED)
        self.restart_btn.config(state=tk.DISABLED)
        self.winner_label.config(text="")

        for i, horse in enumerate(self.horses):
            horse.position = 0
            y_position = i * 100 + 60
            horse.image_index = 0  # 초기 이미지 인덱스 설정
            if horse.images[0]:
                horse.shape = self.canvas.create_image(50, y_position, image=horse.images[0], anchor="nw")
            else:
                horse.shape = self.canvas.create_rectangle(50, y_position - 40, 150, y_position + 40, fill=horse.color)
            horse.text_name = self.canvas.create_text(75, y_position, text=horse.name, anchor="w", font=("Helvetica", 14))  # 이름 위치 조정
            horse.text_distance = self.canvas.create_text(400, y_position, text="0m", anchor="center", font=("Helvetica", 14))
            

        self.update_positions()

    def update_positions(self):
        # 승자가 결정될 때까지 말의 위치 업데이트
        if not any(horse.position + 150 >= self.finish_line for horse in self.horses):  # 말의 앞부분이 결승선에 닿으면
            for i, horse in enumerate(self.horses):
                if horse.position + 150 < self.finish_line:  # 말의 앞부분이 결승선에 닿지 않으면
                    if horse.name == self.special_horse:
                        move_distance = random.randint(horse.min_speed + 5, horse.max_speed + 5)  # 이기기 쉬운 말은 더 빠르게 이동
                    else:
                        move_distance = random.randint(horse.min_speed, horse.max_speed)
                    horse.position += move_distance
                    if horse.position + 150 > self.finish_line:
                        horse.position = self.finish_line - 150

                    horse.image_index = (horse.image_index + 1) % len(horse.images)  # 이미지 인덱스 업데이트
                    y_position = i * 100 + 60
                    if horse.images[horse.image_index]:
                        self.canvas.itemconfig(horse.shape, image=horse.images[horse.image_index])
                    self.canvas.coords(horse.shape, 50 + horse.position, y_position)
                    self.canvas.itemconfig(horse.text_distance, text=f"{horse.position}m")

            self.root.after(1000, self.update_positions)
        else:
            self.declare_winner()

    def declare_winner(self):
        winner_names = [horse.name for horse in self.horses if horse.position + 150 >= self.finish_line]  # 말의 앞부분이 결승선에 닿으면
        if len(winner_names) > 1:
            winner = random.choice(winner_names)
            self.winner_label.config(text=f"우승한 말은 '{winner}'입니다!")
        else:
            self.winner_label.config(text=f"우승한 말은 '{winner_names[0]}'입니다!")
        self.winner_label.place(relx=0.5, rely=0.8, anchor="center")  # 우승자 라벨 위치 조정
        self.start_race_button.config(state=tk.NORMAL)
        self.restart_btn.config(state=tk.NORMAL)

    def key_press_event(self, event):
        # 이기기 쉬운 말 선택을 위한 키보드 이벤트 처리
        key = event.char
        if key.isdigit() and int(key) in range(1, self.num_horses + 1):
            self.special_horse = self.horses[int(key) - 1].name  # 선택된 말을 이기기 쉬운 말로 설정

    def restart(self):
        # 게임 재시작
        self.special_horse = None  # Reset special horse
        self.canvas.delete("all")
        self.draw_finish_line()
        self.num_horses = self.ask_num_horses()
        self.horses = self.create_horses(self.num_horses)
        self.winner_label.config(text="")  # 우승자 라벨 초기화
        self.start_race()

if __name__ == "__main__":
    root = tk.Tk()
    app = HorseApp(root)
    root.mainloop()

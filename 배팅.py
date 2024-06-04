import tkinter as tk
from tkinter import ttk

# 배팅 금액 설정
bet_amount = 500

# 배팅 내역 저장
bets = {1: [], 2: [], 3: [], 4: [], 5: []}
bettor_bets = {}

# 배팅 함수
def place_bet(horse_number, bettor_name):
    if bettor_name:  # 이름이 입력된 경우에만 배팅
        if bettor_name not in bettor_bets:
            bettor_bets[bettor_name] = []
        
        if len(bettor_bets[bettor_name]) < 2 and horse_number not in bettor_bets[bettor_name]:
            bets[horse_number].append(bettor_name)
            bettor_bets[bettor_name].append(horse_number)
            update_labels()
        else:
            status_var.set("1인당 최대 2마리의 말에만 배팅할 수 있습니다.")
    else:
        status_var.set("이름을 입력하세요")

# 라벨 업데이트 함수
def update_labels():
    total_bet_amount = sum(len(bettors) for bettors in bets.values()) * bet_amount
    for horse_number, label in labels.items():
        horse_bet_amount = len(bets[horse_number]) * bet_amount
        if horse_bet_amount > 0:
            dividend = (total_bet_amount * 0.8) / horse_bet_amount
        else:
            dividend = 0
        bettors = ", ".join(bets[horse_number])
        label.config(text=f"말 {horse_number}: {horse_bet_amount}원 (배팅자: {bettors}, 배율: {dividend:.2f})")

# 배팅 버튼 클릭 함수
def on_bet_button_click(horse_number):
    bettor_name = name_entry.get()
    place_bet(horse_number, bettor_name)

# 승리한 말 선택 함수
def set_winning_horse():
    try:
        winning_horse = int(winning_horse_entry.get())
        if winning_horse in bets:
            calculate_payout(winning_horse)
        else:
            status_var.set("올바른 말 번호를 입력하세요.")
    except ValueError:
        status_var.set("올바른 말 번호를 입력하세요.")

# 정산금 계산 함수
def calculate_payout(winning_horse):
    total_bet_amount = sum(len(bettors) for bettors in bets.values()) * bet_amount
    horse_bet_amount = len(bets[winning_horse]) * bet_amount
    number_of_bettors = len(bets[winning_horse])
    
    if horse_bet_amount > 0 and number_of_bettors > 0:
        dividend = (total_bet_amount * 0.8) / horse_bet_amount
        payout_per_person = dividend * bet_amount
    else:
        dividend = 0
        payout_per_person = 0

    # 정산금 라벨 업데이트
    payout_text = f"정산금 (해당 말의 배율 {dividend:.2f}):\n"
    for bettor in bets[winning_horse]:
        payout_text += f"{bettor}: {payout_per_person:.2f}원\n"
    payout_var.set(payout_text)

# 리셋 함수
def reset():
    global bets, bettor_bets
    bets = {1: [], 2: [], 3: [], 4: [], 5: []}
    bettor_bets = {}
    update_labels()
    payout_var.set("정산금:")
    status_var.set("")

# GUI 설정
root = tk.Tk()
root.title("배팅 보조 프로그램")

# 스타일 설정
style = ttk.Style()
style.theme_use("clam")

# 열 설정
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# 이름 입력 라벨 및 엔트리
name_label = ttk.Label(root, text="배팅자 이름:")
name_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# 배팅 버튼 및 라벨 생성
labels = {}
for i in range(1, 6):
    button = ttk.Button(root, text=f"말 {i} 배팅", command=lambda i=i: on_bet_button_click(i))
    button.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

    label = ttk.Label(root, text=f"말 {i}: 0원 (배팅자: 없음, 배율: 0.00)")
    label.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
    labels[i] = label

# 승리한 말 입력 라벨 및 엔트리
winning_horse_label = ttk.Label(root, text="승리한 말 번호:")
winning_horse_label.grid(row=6, column=0, padx=10, pady=5, sticky="ew")
winning_horse_entry = ttk.Entry(root)
winning_horse_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

# 승리한 말 설정 버튼
set_winning_horse_button = ttk.Button(root, text="승리한 말 설정", command=set_winning_horse)
set_winning_horse_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# 정산금 표시 라벨
payout_var = tk.StringVar()
payout_var.set("정산금:")
payout_label = ttk.Label(root, textvariable=payout_var)
payout_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# 리셋 버튼
reset_button = ttk.Button(root, text="리셋", command=reset)
reset_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# 상태 표시 라벨
status_var = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_var, foreground="red")
status_label.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# 규칙 설명
rules_label = ttk.Label(root, text="규칙:\n1. 1인당 배팅금액 500원\n2. 1인당 총 2마리의 말 배팅 가능", justify="left")
rules_label.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# GUI 루프 시작
root.mainloop()

print("프로그램이 종료되었습니다.")
print("최종 배팅 내역:")
total_bet_amount = sum(len(bettors) for bettors in bets.values()) * bet_amount
for horse, bettors in bets.items():
    horse_bet_amount = len(bettors) * bet_amount
    number_of_bettors = len(bettors)
    if horse_bet_amount > 0 and number_of_bettors > 0:
        dividend = (total_bet_amount * 0.8) / horse_bet_amount
        payout_per_person = dividend / number_of_bettors
    else:
        dividend = 0
        payout_per_person = 0
    print(f"말 {horse}: {horse_bet_amount}원 (배팅자: {', '.join(bettors)}, 배율: {payout_per_person:.2f})")

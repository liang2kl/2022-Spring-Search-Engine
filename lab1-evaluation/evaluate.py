import sys, os
from pathlib import Path

GOOGLE_DATA = [
    "1110010000", "1101000000",
    "1111111111", "1100010000",
    "1111111111", "1111011111",
    "1111111001", "1111111111",
    "1111111100", "1111111111"
]

BAIDU_DATA = [
    "1111111101", "1110000100",
    "1111111111", "1111111111",
    "1101011111", "1110100101",
    "1111110111", "1111111111",
    "1111111101", "1101001110"
]

PATH = Path(os.path.dirname(os.path.realpath(__file__))) / "result.txt"

def calculate_P_10(data):
    sum = 0
    for d in data:
        if d == "1":
            sum += 1
    return sum / len(data)

def calculate_AP(data):
    sum = 0
    total = 0
    for i in range(len(data)):
        if data[i] == "1":
            total += 1
            sum += total / (i + 1)
    return sum / total

def calculate_RR(data):
    for i in range(len(data)):
        if data[i] == "1":
            return 1 / (i + 1)
    return 0

def calculate_success_10(data):
    for i in range(len(data)):
        if data[i] == "1":
            return 1
    return 0

def evaluate(datas, func):
    print(func.__name__)
    sum = 0
    for data in datas:
        result = func(data)
        sum += result
        print(result, end=",")
    print(f"Mean: {sum / len(data)}", end="\n\n")

if __name__ == "__main__":
    sys.stdout = open(PATH, "w")
    functions = [calculate_AP, calculate_P_10, calculate_RR, calculate_success_10]
    # Google
    print("Google")
    for func in functions:
        evaluate(GOOGLE_DATA, func)

    # Baidu
    print("Baidu")
    for func in functions:
        evaluate(BAIDU_DATA, func)

from reader import Reader
from window import Window
import tkinter as tk

if __name__ == "__main__":
    url = "https://billwurtz.com/questions/random.php?"
    readRate = 150
    minReadTime = 5
    maxReadTime = 10

    reader = Reader(url, readRate, minReadTime, maxReadTime)
    window = Window("Bill Wurtz Q&A Reader", reader)
    window.mainloop()
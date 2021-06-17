import tkinter as tk

class Window(tk.Tk):
    def __init__(self, title, reader):
        tk.Tk.__init__(self)
        self._reader = reader

        self.title(title)
        self.geometry("300x100")

        btn_startReadingTimer = tk.Button(text="Start reading timer", command=reader.startReading)
        btn_readOnce = tk.Button(text="Read random Q&A now", command=reader.read)

        btn_startReadingTimer.grid(row=0, column=0)
        btn_readOnce.grid(row=0, column=1)
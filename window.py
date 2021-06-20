import tkinter as tk

class Window(tk.Tk):
    def __init__(self, title, size, reader):
        tk.Tk.__init__(self)
        self._reader = reader

        self.title(title)
        self.geometry(size)

        self._buttonSpacingX = 5
        self._buttonSpacingY = 5
        self._labelFrameIPaddingX = 10
        self._labelFrameIPaddingY = 10

        self._createOptions()
        self._createButtons()

    def _createButtons(self):
        self._buttonFrame = tk.Frame(self)
        self._runFrame = tk.LabelFrame(self._buttonFrame, text="Run")

        self._btn_startReadingTimer = tk.Button(self._runFrame, text="Start reading timer", command=self._startReading)
        self._btn_stopReadingTimer = tk.Button(self._runFrame, text="Stop reading timer", command=self._stopReading)
        self._btn_readOnce = tk.Button(self._runFrame, text="Read random Q&A now", command=self._reader.read)

        self._buttonFrame.pack()
        self._runFrame.grid(row=1, column=2, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        self._btn_startReadingTimer.grid(row=0, column=0, padx=self._buttonSpacingX, pady=self._buttonSpacingY)
        self._btn_stopReadingTimer.grid(row=0, column=1, padx=self._buttonSpacingX, pady=self._buttonSpacingY)
        self._btn_readOnce.grid(row=0, column=2, padx=self._buttonSpacingX, pady=self._buttonSpacingY)

    def _createOptions(self):
        self._voiceOptions = {
            "Female" : 0,
            "Male" : 1
        }

        self._configFrame = tk.Frame(self)

        self._askerFrame = tk.LabelFrame(self._configFrame, text="Asker")
        self._askerLabel = tk.Label(self._askerFrame, text="Asker's Voice")
        self._askerVoice = tk.StringVar()
        self._askerVoice.set("Female")
        self._voiceOptionsAsker = tk.OptionMenu(self._askerFrame, self._askerVoice, *self._voiceOptions.keys(), command=self._updateVoices)

        self._billFrame = tk.LabelFrame(self._configFrame, text="Bill")
        self._billLabel = tk.Label(self._billFrame, text="Bill's Voice")
        self._billVoice = tk.StringVar()
        self._billVoice.set("Male")
        self._voiceOptionsBill = tk.OptionMenu(self._billFrame, self._billVoice, *self._voiceOptions.keys(), command=self._updateVoices)

        self._configFrame.pack()
        #need to give a bit of space between each of the voice config label frames
        self._configFrame.grid_columnconfigure(2, minsize=100)

        self._askerFrame.grid(row=0, column=1, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        self._askerLabel.pack()
        self._voiceOptionsAsker.pack()

        self._billFrame.grid(row=0, column=3, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        self._billLabel.pack()
        self._voiceOptionsBill.pack()

    def _startReading(self):
        self._btn_startReadingTimer["state"] = "disabled"
        self._btn_stopReadingTimer["state"] = "normal"
        self._reader.startReading()

    def _stopReading(self):
        self._btn_startReadingTimer["state"] = "normal"
        self._btn_stopReadingTimer["state"] = "disabled"
        self._reader.stopReading()

    def _updateVoices(self):
        self._reader.askerVoiceIndex = self._voiceOptions[self._askerVoice.get()]
        self._reader.billVoiceIndex = self._voiceOptions[self._billVoice.get()]
import tkinter as tk

class Window(tk.Tk):
    def __init__(self, title, size, reader):
        tk.Tk.__init__(self)
        self._reader = reader

        self.title(title)
        self.geometry(size)

        self._buttonSpacingX = 5
        self._buttonSpacingY = 5
        self._labelFrameIPaddingX = 25
        self._labelFrameIPaddingY = 10
        
        self._voiceOptions = {
            "Female" : 0,
            "Male" : 1
        }

        self._createVoiceOptions()
        self._createButtons()
        
    def _createVoiceOptions(self):
        #outer-most frame
        configFrame = tk.Frame(self)

        #asker label frame and contents
        askerFrame = tk.LabelFrame(configFrame, text="Asker")
        askerLabel = tk.Label(askerFrame, text="Asker's Voice")
        askerVoice = tk.StringVar()
        askerVoice.set("Female")
        voiceOptionsAsker = tk.OptionMenu(askerFrame, askerVoice, *self._voiceOptions.keys(), command=self._updateAskerVoice)

        #bill label frame and contents
        billFrame = tk.LabelFrame(configFrame, text="Bill")
        billLabel = tk.Label(billFrame, text="Bill's Voice")
        billVoice = tk.StringVar()
        billVoice.set("Male")
        voiceOptionsBill = tk.OptionMenu(billFrame, billVoice, *self._voiceOptions.keys(), command=self._updateBillVoice)

        #putting it all together
        configFrame.pack()
        #need to give a bit of space between each of the voice config label frames
        configFrame.grid_columnconfigure(2, minsize=100)

        askerFrame.grid(row=0, column=1, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        askerLabel.pack()
        voiceOptionsAsker.pack()

        billFrame.grid(row=0, column=3, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        billLabel.pack()
        voiceOptionsBill.pack()

    def _createButtons(self):
        buttonFrame = tk.Frame(self)
        runFrame = tk.LabelFrame(buttonFrame, text="Run")

        self._btn_startReadingTimer = tk.Button(runFrame, text="Start reading timer", command=self._startReading)
        self._btn_stopReadingTimer = tk.Button(runFrame, text="Stop reading timer", command=self._stopReading)
        self._btn_readOnce = tk.Button(runFrame, text="Read random Q&A now", command=self._reader.read)

        buttonFrame.pack()
        runFrame.grid(row=1, column=2, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        self._btn_startReadingTimer.grid(row=0, column=0, padx=self._buttonSpacingX, pady=self._buttonSpacingY)
        self._btn_stopReadingTimer.grid(row=0, column=1, padx=self._buttonSpacingX, pady=self._buttonSpacingY)
        self._btn_readOnce.grid(row=0, column=2, padx=self._buttonSpacingX, pady=self._buttonSpacingY)

    ###########LISTENERS###############

    def _startReading(self):
        self._btn_startReadingTimer["state"] = "disabled"
        self._btn_stopReadingTimer["state"] = "normal"
        self._reader.startReading()

    def _stopReading(self):
        self._btn_startReadingTimer["state"] = "normal"
        self._btn_stopReadingTimer["state"] = "disabled"
        self._reader.stopReading()

    def _updateAskerVoice(self, value):
        self._reader.askerVoiceIndex = self._voiceOptions[value]
        
    def _updateBillVoice(self, value):
        self._reader.billVoiceIndex = self._voiceOptions[value]
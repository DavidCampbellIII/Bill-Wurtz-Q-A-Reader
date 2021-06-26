import tkinter as tk
import tkinter.font as font

class Window(tk.Tk):
    def __init__(self, title, size, reader):
        tk.Tk.__init__(self)
        self._reader = reader

        self.title(title)
        self.geometry(size)
        
        self._backgroundColor = "light blue"
        self._buttonColor = "cyan"
        self._textColor = "purple"
        self._largeFont = font.Font(family="Arial", size=30)
        self._smallFont = font.Font(family="Arial", size=20)

        self._buttonSpacingX = 5
        self._buttonSpacingY = 5
        self._labelFrameIPaddingX = 25
        self._labelFrameIPaddingY = 10
        
        self._voiceOptions = {
            "female" : 0,
            "male" : 1
        }
        
        self.configure(background=self._backgroundColor)

        self._createVoiceOptions()
        self._createButtons()
        
    def _createVoiceOptions(self):
        #outer-most frame
        configFrame = tk.Frame(self, bg=self._backgroundColor)

        #asker label frame and contents
        askerFrame = tk.LabelFrame(configFrame, text="asker", bg=self._backgroundColor, fg=self._textColor, font=self._largeFont)
        askerLabel = tk.Label(askerFrame, text="asker's voice", bg=self._backgroundColor, fg=self._textColor, font=self._smallFont)
        askerVoice = tk.StringVar()
        askerVoice.set("female")
        voiceOptionsAsker = tk.OptionMenu(askerFrame, askerVoice, *self._voiceOptions.keys(), command=self._updateAskerVoice)
        voiceOptionsAsker.configure(background=self._buttonColor, font=self._smallFont)
        
        #read rate frame and contents
        rateFrame = tk.LabelFrame(configFrame, text="read configuration", bg=self._backgroundColor, fg=self._textColor, font=self._largeFont)
        rateLabel = tk.Label(rateFrame, text="read rate", bg=self._backgroundColor, fg=self._textColor, font=self._smallFont)
        self._readRate = tk.IntVar()
        #default slider to whatever the read rate starts as
        self._readRate.set(self._reader.readRate)
        rateSlider = tk.Scale(rateFrame, from_=75, to=300, orient="horizontal", command=self._updateReadRate, variable=self._readRate, bg=self._buttonColor, font=self._smallFont)

        #bill label frame and contents
        billFrame = tk.LabelFrame(configFrame, text="bill", bg=self._backgroundColor, fg=self._textColor, font=self._largeFont)
        billLabel = tk.Label(billFrame, text="bill's voice", bg=self._backgroundColor, fg=self._textColor, font=self._smallFont)
        billVoice = tk.StringVar()
        billVoice.set("male")
        voiceOptionsBill = tk.OptionMenu(billFrame, billVoice, *self._voiceOptions.keys(), command=self._updateBillVoice)
        voiceOptionsBill.configure(background=self._buttonColor, font=self._smallFont)

        #putting it all together
        configFrame.pack()
        #need to give a bit of space between each of the voice config label frames
        configFrame.grid_columnconfigure(2, minsize=100)

        askerFrame.grid(row=0, column=1, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        askerLabel.pack()
        voiceOptionsAsker.pack()
        
        rateFrame.grid(row=0, column=2, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        rateLabel.pack()
        rateSlider.pack()

        billFrame.grid(row=0, column=3, ipadx=self._labelFrameIPaddingX, ipady=self._labelFrameIPaddingY)
        billLabel.pack()
        voiceOptionsBill.pack()

    def _createButtons(self):
        buttonFrame = tk.Frame(self, bg=self._backgroundColor)
        runFrame = tk.LabelFrame(buttonFrame, text="run", bg=self._backgroundColor, fg=self._textColor, font=self._largeFont)

        self._btn_startReadingTimer = tk.Button(runFrame, text="start reading timer", command=self._startReading, bg="lime", font=self._smallFont)
        self._btn_stopReadingTimer = tk.Button(runFrame, text="stop reading timer", command=self._stopReading, bg="red", font=self._smallFont)
        self._btn_readOnce = tk.Button(runFrame, text="read random q&a now", command=self._reader.read, bg="pink", font=self._smallFont)

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
        
    def _updateReadRate(self, _):
        self._reader.readRate = self._readRate.get()
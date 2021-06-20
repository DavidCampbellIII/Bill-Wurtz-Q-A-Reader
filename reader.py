import threading
import bs4 as bs
from urllib.request import urlopen, Request
import pyttsx3
import time
import random
from threading import Thread

class Reader(Thread):
    def __init__(self, url, readRate, minReadTime, maxReadTime):
        Thread.__init__(self, target=self.readOverTime)
        self._stop = threading.Event()
        
        self._speechEngine = pyttsx3.init()
        self._speechEngine.startLoop(False)
        #need to "say()" at least once so thread can start properly when reading over time
        self._speechEngine.say("")
        self._speechEngine.iterate()
        self._isReading = False

        self.url = url
        self.readRate = readRate
        self.minReadTime = minReadTime
        self.maxReadTime = maxReadTime
        self.askerVoiceIndex = 0
        self.billVoiceIndex = 1

    @property
    def readRate(self):
        return self._readRate

    @readRate.setter
    def readRate(self, value):
        self._readRate = value
        self._speechEngine.setProperty("rate", value)

    #open page via url and return souped text
    def loadPageText(self, url):
        request = Request(url=url)
        pageText = urlopen(request).read()
        parsedText = bs.BeautifulSoup(pageText, "lxml")
        return parsedText

    def findQuestionAnswerPairs(self, parsedText):
        pairs = {}
        questionH3 = parsedText.find("h3")
        question = "the question did not work"
        try:
            qco = questionH3.findChildren("qco")
            if len(qco) == 0:
                question = questionH3.findChildren("font")[0].text
            else:
                question = questionH3.findChildren("qco")[0].text
        except:
            print(f"Cannot find question as <qco> or <font>!\n{parsedText}")
        
        question = self.cleanText(question)
        answer = self.cleanText(questionH3.next_sibling)
        pairs[question] = answer
        return pairs

    def cleanText(self, answer):
        return answer.replace("\n", "").replace("\xa0", "").replace("\r", "").strip()

    def readQAPairs(self, pairs):
        print(pairs)
        for key in pairs:
            self.say(key, self.askerVoiceIndex)
            self.say(pairs[key], self.billVoiceIndex)

    def say(self, message, voiceIndex):
        voices = self._speechEngine.getProperty("voices")
        self._speechEngine.setProperty("voice", voices[voiceIndex].id)
        self._speechEngine.say(message)
        self._speechEngine.iterate()

    def startReading(self):
        self._isReading = True
        #start thread if this is our first time starting to read
        if not self.is_alive():
            self.start()

    def readOverTime(self):
        #thread should never actually stop, just stop reading at a time
        while True:
            time.sleep(0.1)
            #clear stop flag if already set
            if self._stop.is_set():
                self._stop.clear()
            while self._isReading:
                self.read()
                timeBeforeNext = random.randrange(self.minReadTime, self.maxReadTime)
                self._stop.wait(timeBeforeNext)

    def stopReading(self):
        self._isReading = False
        self._stop.set()

    def read(self):
        parsedText = self.loadPageText(self.url)
        qaPairs = self.findQuestionAnswerPairs(parsedText)
        self.readQAPairs(qaPairs)
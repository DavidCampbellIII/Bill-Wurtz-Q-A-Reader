import threading
import bs4 as bs
from urllib.request import urlopen, Request
import pyttsx3
import time
import random
import json
from threading import Thread

class Reader(Thread):
    def __init__(self, url, readRate, minReadTime, maxReadTime):
        Thread.__init__(self, target=self.readOverTime)
        self._stop = threading.Event()
        #so the thread can exit when the main program exits
        self.daemon = True
        
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
        self.bulkDownloadAmount = 100

    @property
    def readRate(self):
        return self._readRate

    @readRate.setter
    def readRate(self, value):
        self._readRate = value
        self._speechEngine.setProperty("rate", value)

    #open page via url and return souped text
    def _loadPageText(self, url):
        request = Request(url=url)
        pageText = urlopen(request).read()
        parsedText = bs.BeautifulSoup(pageText, "lxml")
        return parsedText

    def _findQuestionAnswerPairs(self, parsedText):
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
        
        question = self._cleanText(question)
        answer = self._cleanText(questionH3.next_sibling)
        pairs[question] = answer
        return pairs
    
    def _getQAPair(self):
        parsedText = self._loadPageText(self.url)
        return self._findQuestionAnswerPairs(parsedText)
    
    #TODO instead of loading each random page, open the main page and parse all questions at once.
    #that way, we can get way more questions, way faster, although they will only be the most recent ones
    def _downloadBulkQAs(self):
        start = time.time()
        pairs = {}
        for i in range(self.bulkDownloadAmount):
            print(f"Downloading bulk unit {i + 1}/{self.bulkDownloadAmount}")
            newPair = self._getQAPair()
            pairs.update(newPair)
        with open("cached_QAs.json", 'w', encoding="utf-8") as f:
            json.dump(pairs, f, ensure_ascii=False, indent=4)
        end = time.time()
        print(f"Bulk download of {self.bulkDownloadAmount} completed in {end - start} seconds")

    def _cleanText(self, answer):
        return answer.replace("\n", "").replace("\xa0", "").replace("\r", "").strip()

    def _readQAPairs(self, pairs):
        print(pairs)
        for key in pairs:
            self._say(key, self.askerVoiceIndex)
            self._say(pairs[key], self.billVoiceIndex)

    def _say(self, message, voiceIndex):
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
        qaPairs = self._getQAPair()
        self._readQAPairs(qaPairs)
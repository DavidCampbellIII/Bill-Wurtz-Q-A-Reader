import bs4 as bs
from urllib.request import urlopen, Request
import pyttsx3
import time
import random
from threading import Thread

class Reader(Thread):
    def __init__(self, url, readRate, minReadTime, maxReadTime):
        Thread.__init__(self, target=self.readOverTime)
        self.daemon = True
        
        self._speechEngine = pyttsx3.init()
        self.isReading = False

        self.url = url
        self.readRate = readRate
        self.minReadTime = minReadTime
        self.maxReadTime = maxReadTime

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
            self.say(key, 0)
            self.say(pairs[key], 1)

    def say(self, message, voiceIndex):
        voices = self._speechEngine.getProperty("voices")
        self._speechEngine.setProperty("voice", voices[voiceIndex].id)
        self._speechEngine.say(message)
        self._speechEngine.runAndWait()

    def startReading(self):
        self.isReading = True
        self.start()

    def readOverTime(self):
        while self.isReading:
            self.read()
            timeBeforeNext = random.randrange(5, 10)
            time.sleep(timeBeforeNext)

    def stopReading(self):
        self.isReading = False
        self.join()

    def read(self):
        parsedText = self.loadPageText(self.url)
        qaPairs = self.findQuestionAnswerPairs(parsedText)
        self.readQAPairs(qaPairs)
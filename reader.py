import bs4 as bs
from urllib.request import urlopen, Request
import pyttsx3
import time
import random
import tkinter

#open page via url and return souped text
def loadPageText(url):
    request = Request(url=url)
    pageText = urlopen(request).read()
    parsedText = bs.BeautifulSoup(pageText, "lxml")
    return parsedText

def findQuestionAnswerPairs(parsedText):
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
    
    question = cleanText(question)
    answer = cleanText(questionH3.next_sibling)
    pairs[question] = answer
    return pairs

def cleanText(answer):
    return answer.replace("\n", "").replace("\xa0", "").replace("\r", "").strip()

def readQAPairs(speechEngine, pairs):
    print(pairs)
    for key in pairs:
        say(speechEngine, key, 0)
        say(speechEngine, pairs[key], 1)

def say(speechEngine, message, voiceIndex):
    voices = speechEngine.getProperty("voices")
    speechEngine.setProperty("voice", voices[voiceIndex].id)
    speechEngine.say(message)
    speechEngine.runAndWait()

if __name__ == "__main__":
    print("it's working")
    url = "https://billwurtz.com/questions/random.php?"
    speechEngine = pyttsx3.init()
    speechEngine.setProperty("rate", 150)
    while True:
        parsedText = loadPageText(url)
        qaPairs = findQuestionAnswerPairs(parsedText)
        readQAPairs(speechEngine, qaPairs)
        timeBeforeNext = random.randrange(5, 10)
        time.sleep(timeBeforeNext)
from injector import inject
from jvcore import TextToSpeech

class Communicator:
    @inject
    def __init__(self, tts: TextToSpeech) -> None:
        self._tts = tts
    
    def say(self, text):
        self._tts.sayAndWait(text)
    
    def sayAndPrint(self, text):
        self.print(text)
        self.say(text)
    
    def print(self, text):
        print(text)

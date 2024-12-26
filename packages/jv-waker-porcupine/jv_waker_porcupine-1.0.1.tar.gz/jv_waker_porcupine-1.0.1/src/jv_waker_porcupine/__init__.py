from jvcore import Waker
from .porcupine_waker import PorcupineWaker

def getWaker()-> Waker:
    return PorcupineWaker()

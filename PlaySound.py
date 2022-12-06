<<<<<<< HEAD
from pygame import mixer

mixer.init()

def playSound(sound):
    mixer.music.load(sound)
=======
from pygame import mixer

mixer.init()

def playSound(sound):
    mixer.music.load(sound)
>>>>>>> b99091fdc91ce265928ea9f7a3718adcb922f526
    mixer.music.play(loops=0)
from pygame import mixer

mixer.init()

def playSound(sound):
    mixer.music.load(sound)
    mixer.music.play(loops=0)
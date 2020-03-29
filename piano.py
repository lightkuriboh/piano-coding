import os
import pyxhook
from os import listdir
from os.path import isfile, join
from pygame import mixer
import random

keys = [
    'space',
    'BackSpace',
    'Delete',
    'Shift_L',
    'slash',
    'plus',
    'minus',
    'asterisk',
    'Return',
    'Control_L',
    'Tab'
]
effects = []
keyNoteMap = {}
volume = 50.0

def initKeys():
    for char in range(26):
        keys.append(chr(ord('a') + char))


def initKeyMap():
    idxes = []
    for i in range(len(effects)):
        idxes.append(i)
    random.shuffle(idxes)
    for i in range(min(len(keys), len(effects))):
        keyNoteMap[keys[i]] = idxes[i]


def playNote(key):
    if key in keyNoteMap:
        effects[keyNoteMap[key]].play()
    for effect in effects:
        vol = effect.get_volume()
        effect.set_volume(min(1.0, vol * volume))


def getNotes():
    mypath = '/home/kuribohkute/workspace/piano/notes/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    answer = []
    for fileName in onlyfiles:
        answer.append(mypath + fileName)
    return answer


def initNotes(notesList):
    for note in notesList:
        effects.append(mixer.Sound(note))


def OnKeyPress(event):
    # print('{}\n'.format(event.Key))
    playNote(event.Key)


if __name__ == '__main__':
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = OnKeyPress

    new_hook.HookKeyboard()
    try:
        mixer.init()
        initKeys()
        notes = getNotes()
        initNotes(notes)
        initKeyMap()
        new_hook.start() 
    except KeyboardInterrupt: 
        pass
    except Exception as ex: 
        msg = 'Error while catching events:\n  {}'.format(ex) 
        print(msg)

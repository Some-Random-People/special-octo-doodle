import random

beat = []
with open('./beatmap_list.txt', 'r') as x:
    content = x.readlines()
    x.close()

def roll():
    for i in content:
        beat.append(i.strip("\n"))

    return beat[random.randint(0,len(beat) - 1)]
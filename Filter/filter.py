import random


def rerror(frame):
    frame = list(frame)
    length = len(frame)
    times = random.randint(1,50)
    for x in range(0,times):
        r = random.randint(0, length)
        frame[r] = 'f'
    return ''.join(frame)


def rloss(frame):
    length = len(frame)
    r = random.randint(0, length)
    frame = frame[0:r]
    return frame
from System import Random

class StimulusRandomizer():
    def __init__(self):
        self.random = Random()
        self.first = self.random.Next(2) == 1

    def next(self):
        self.first = self.random.Next(2) == 1

    def isFirst(self):
        return self.first

def CreateRandom():
    return StimulusRandomizer()

def GetFirstIntensity():
    if random.isFirst():
        return SndIs + x
    else:
        return SndIs


def GetSecondIntensity():
    if random.isFirst():
        retValue = SndIs
    else:
        retValue = SndIs + x

    random.next()
    return retValue


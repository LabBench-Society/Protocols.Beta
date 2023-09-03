from Serilog import Log
from LabBench.Interface.Instruments.Algometry import *
import traceback
import random

def Stimulate(tc, x):
    algometer = tc.Devices.Algometer
    chan = algometer.Channels[0]

    chan.SetStimulus(1, chan.CreateWaveform()
                     .Step(x, 1))
    algometer.ConfigurePressureOutput(0, ChannelID.CH01)
    algometer.StartStimulation(AlgometerStopCriterion.STOP_CRITERION_ON_BUTTON_PRESSED, True)

    return True

class ImageRepository:
    def __init__(self, tc):
        stimuli = tc.Assets.VisualStimuli
        self._images = {
                "Blank":                    stimuli.GetAsset("Blank.png"),
                "Marker":                   stimuli.GetAsset("Marker.png"),
                "MarkerWithFiducial":       stimuli.GetAsset("MarkerWithFiducial.png"),
                "High73":                   stimuli.GetAsset("High73.png"),
                "High79":                   stimuli.GetAsset("High79.png"),
                "High84":                   stimuli.GetAsset("High84.png"),
                "High88":                   stimuli.GetAsset("High88.png"),
                "High93":                   stimuli.GetAsset("High93.png"),
                "HighCue1":                 stimuli.GetAsset("HighCue1.png"),
                "HighCue2":                 stimuli.GetAsset("HighCue2.png"),
                "LearningRateExpectedPain": stimuli.GetAsset("LearningRateExpectedPainDE.png") 
                                            if tc.Language == "de" else 
                                            stimuli.GetAsset("LearningRateExpectedPainEn.png"),
                "Low27":                    stimuli.GetAsset("Low27.png"),
                "Low32":                    stimuli.GetAsset("Low32.png"),
                "Low40":                    stimuli.GetAsset("Low40.png"),
                "Low45":                    stimuli.GetAsset("Low45.png"),
                "Low51":                    stimuli.GetAsset("Low51.png"),
                "LowCue1":                  stimuli.GetAsset("LowCue1.png"),
                "LowCue2":                  stimuli.GetAsset("LowCue2.png"),
                "TestRateExpectedPain":     stimuli.GetAsset("TestRateExpectedPainDE.png") 
                                            if tc.Language == "de" else 
                                            stimuli.GetAsset("TestRateExpectedPainEN.png"),
                "TestRatePain":             stimuli.GetAsset("TestRatePainDE.png") 
                                            if tc.Language == "de" else 
                                            stimuli.GetAsset("TestRatePainEN.png")
            }
        
    def get(self, id):
        return self._images[id].Data
    
    def getHighCue(self, variant):
        if variant == 0:
            return self._images['HighCue1'].Data
        elif variant == 1:
            return self._images['HighCue2'].Data
        else:
            raise ValueError("Invalid cue variant: {variant}".format(variant = variant)) 
        
    def getLowCue(self, variant):
        if variant == 0:
            return self._images['LowCue1'].Data
        elif variant == 1:
            return self._images['LowCue2'].Data
        else:
            raise ValueError("Invalid cue variant: {variant}".format(variant = variant)) 
        
    def getHighFeedback(self, variant):
        if variant == 0:
            return self._images['High73'].Data
        elif variant == 1:
            return self._images['High79'].Data
        elif variant == 2:
            return self._images['High84'].Data
        elif variant == 3:
            return self._images['High88'].Data
        elif variant == 4:
            return self._images['High93'].Data
        else:
            raise ValueError("Invalid feedback variant: {variant}".format(variant = variant)) 
        
    
    def getLowFeedback(self, variant):
        if variant == 0:
            return self._images['Low27'].Data
        elif variant == 1:
            return self._images['Low32'].Data
        elif variant == 2:
            return self._images['Low40'].Data
        elif variant == 3:
            return self._images['Low45'].Data
        elif variant == 4:
            return self._images['Low51'].Data
        else:
            raise ValueError("Invalid feedback variant: {variant}".format(variant = variant))         
        
        
class LearningTrial:
    def __init__(self, high, variant):
        self.high = high
        self.variant = variant
        self.cue = random.randint(0, 4)
        
    def getCue(self, images):
        return images.getHighCue(self.variant) if self.high == 1 else images.getLowCue(self.variant)
                
    def getFeedback(self, images):
        if self.high == 1:
            return images.getHighFeedback(self.cue)
        else:
            return images.getLowFeedback(self.cue)      

class LearningTask:
    def __init__(self, tc):
        self._images = ImageRepository(tc)
        self._iteration = 0
        self.trials = []
        numberOfBlocks = tc.NumberOfLearningTrials / 4
        
        for n in range(numberOfBlocks):
            block = [LearningTrial(1, 0), 
                     LearningTrial(1, 1), 
                     LearningTrial(0, 0), 
                     LearningTrial(0, 1)]
            random.shuffle(block)
            
            for trial in block:
                self.trials.append(trial)
        
    def reset(self):
        Log.Information("Resetting learning task with {n} trials".format(n = len(self.trials)))
        
        self._iteration = 0
        return True
        
    def printTrial(self):
        if (self._iteration < len(self.trials)):
            current = self.trials[self._iteration]
            Log.Information("TRIAL (high = {high}, variant = {variant}, cue = {cue})".format(high = current.high, 
                                                                                             variant = current.variant, 
                                                                                             cue = current.cue))
        
    def nextTrial(self):
        self._iteration = self._iteration + 1
    
    def getImage(self, id):
        return self._images.get(id)
    
    def getCue(self):
        if (self._iteration >= len(self.trials)):
            raise ValueError("No trial for iteration: {n}".format(n = self._iteration))

        current = self.trials[self._iteration]
        return current.getCue(self._images)
    
    def getFeedback(self):
        if (self._iteration >= len(self.trials)):
            raise ValueError("No trial for iteration: {n}".format(n = self._iteration))

        current = self.trials[self._iteration]
        return current.getFeedback(self._images)

class TestTrial:
    def __init__(self, high, variant, correct):
        self.high = high
        self.variant = variant        
        self.correct = correct
        
    def getCue(self, images):
        return images.getHighCue(self.variant) if self.high == 1 else images.getLowCue(self.variant)
                
    def getIntensity(self, tc):
        if self.high == 1:
            return tc.THR30['PULSE'] if self.correct == 0 else tc.THR70['PULSE']
        elif self.high == 0:
            return tc.THR70['PULSE'] if self.correct == 0 else tc.THR30['PULSE']
        else:
            raise ValueError("Invalid high value: {high}".format(high = self.high))
    

class TestTask:
    def __init__(self, tc):
        self._images = ImageRepository(tc)
        self._iteration = 0
        self.trials = []
        numberOfBlocks = tc.NumberOfTestTrials / 4
        
        for n in range(numberOfBlocks):
            highCorrect = [0, 1]
            lowCorrect = [0, 1]
            random.shuffle(highCorrect)
            random.shuffle(lowCorrect)
            block = [TestTrial(1, 0, highCorrect[0]), 
                     TestTrial(1, 1, highCorrect[1]), 
                     TestTrial(0, 0, lowCorrect[0]), 
                     TestTrial(0, 1, lowCorrect[1])]
            random.shuffle(block)
            
            for trial in block:
                self.trials.append(trial)
        
    def reset(self):
        Log.Information("Resetting test task with {n} trials".format(n = len(self.trials)))
        
        self._iteration = 0
        return True
    
    def nextTrial(self):
        self._iteration = self._iteration + 1
    
    def getImage(self, id):
        return self._images.get(id)
    
    def getCue(self):
        if (self._iteration >= len(self.trials)):
            raise ValueError("No trial for iteration: {n}".format(n = self._iteration))

        current = self.trials[self._iteration]
        
        return current.getCue(self._images)
    
    def stimulate(self, tc):
        if (self._iteration >= len(self.trials)):
            raise ValueError("No trial for iteration: {n}".format(n = self._iteration))

        current = self.trials[self._iteration]
        intensity = current.getIntensity(tc)
        Stimulate(tc, intensity)
        
        return self._images.get("MarkerWithFiducial")    

def CreateLearningTask(tc):
    return LearningTask(tc)

def InitializeLearning(tc):
    tc.LEARNINGPHASE.Annotations.Add("high", [trial.high for trial in tc.LearningTask.trials])
    tc.LEARNINGPHASE.Annotations.Add("variant", [trial.high for trial in tc.LearningTask.trials])
    tc.LEARNINGPHASE.Annotations.Add("cue", [trial.high for trial in tc.LearningTask.trials])
    return tc.LearningTask.reset()

def RunLearning(tc, x):
    retValue = True
    
    try:
        display = tc.Devices.Display
        task = tc.LearningTask
        Log.Information("Running the learning task for step: {name}".format(name = tc.StimulusName))

        if (tc.StimulusName == "Marker"):
            display.Display(task.getImage("Marker"))
        elif (tc.StimulusName == "Cue"):
            display.Display(task.getCue())
        elif (tc.StimulusName == "RateExpected"):
            display.Display(task.getImage("LearningRateExpectedPain"))
        elif (tc.StimulusName == "Feedback"):
            display.Display(task.getFeedback())
        elif (tc.StimulusName == "Blank"):
            display.Display(task.getImage("Blank"))
            task.nextTrial()
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        retValue = False
        
    return retValue

def CreateTestTask(tc):
    return TestTask(tc)

def InitializeTest(tc):
    tc.TESTPHASE.Annotations.Add("high", [trial.high for trial in tc.TestTask.trials])
    tc.TESTPHASE.Annotations.Add("variant", [trial.high for trial in tc.TestTask.trials])
    tc.TESTPHASE.Annotations.Add("correct", [trial.correct for trial in tc.TestTask.trials])
    return tc.TestTask.reset()

def RunTest(tc, x):
    retValue = True
    
    try:
        display = tc.Devices.Display
        task = tc.TestTask

        if (tc.StimulusName == "Marker"):
            display.Display(task.getImage("Marker"))
        elif (tc.StimulusName == "Cue"):
            display.Display(task.getCue())
        elif (tc.StimulusName == "RateExpected"):
            display.Display(task.getImage("TestRateExpectedPain"))
        elif (tc.StimulusName == "Stimulate"):
            display.Display(task.stimulate(tc))
        elif (tc.StimulusName == "Rate"):
            display.Display(task.getImage("TestRatePain"))
        elif (tc.StimulusName == "Blank"):
            display.Display(task.getImage("Blank"))
            task.nextTrial()
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        retValue = False
        
    return retValue
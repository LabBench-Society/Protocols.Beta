from Serilog import Log
from LabBench.Interface.Instruments.Algometry import *

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
                "Marker",                   stimuli.GetAsset("Marker.png"),
                "MarkerWithFiducial",       stimuli.GetAsset("MarkerWithFiducial.png"),
                "High73",                   stimuli.GetAsset("High73.png"),
                "High79",                   stimuli.GetAsset("High79.png"),
                "High84",                   stimuli.GetAsset("High84.png"),
                "High88",                   stimuli.GetAsset("High88.png"),
                "High93",                   stimuli.GetAsset("High93.png"),
                "HighCue1",                 stimuli.GetAsset("HighCue1.png"),
                "HighCue2",                 stimuli.GetAsset("HighCue2.png"),
                "LearningRateExpectedPain", stimuli.GetAsset("LearningRateExpectedPainDE.png") 
                                            if tc.Language == "de" else 
                                            stimuli.GetAsset("LearningRateExpectedPainEn.png"),
                "Low27",                    stimuli.GetAsset("Low27.png"),
                "Low32",                    stimuli.GetAsset("Low32.png"),
                "Low40",                    stimuli.GetAsset("Low40.png"),
                "Low45",                    stimuli.GetAsset("Low45.png"),
                "Low51",                    stimuli.GetAsset("Low51.png"),
                "LowCue1",                  stimuli.GetAsset("LowCue1.png"),
                "LowCue2",                  stimuli.GetAsset("LowCue2.png"),
                "TestRateExpectedPain",     stimuli.GetAsset("TestRateExpectedPainDE.png") 
                                            if tc.Language == "de" else 
                                            stimuli.GetAsset("TestRateExpectedPainEN.png"),
                "TestRatePain",             stimuli.GetAsset("TestRatePainDE.png") 
                                            if tc.Language == "de" else 
                                            stimuli.GetAsset("TestRatePainEN.png")
            }
        
    def get(self, id):
        return self.images[id]
        
class LearningTask:
    def __init__(self, tc):
        self.images = ImageRepository(tc)
        
    def reset(self):
        return True
        
    def nextTrial():
        pass
    
    def getImage(self, id):
        return self.images.get(id)
    
    def getCue(self):
        return self.images.get("HighCue1")
    
    def getFeedback(self):
        return self.images.get("High88")

class TestTask:
    def __init__(self, tc):
        self.images = ImageRepository(tc)
        
    def reset(self):
        return True
    
    def nextTrial():
        pass
    
    def getImage(self, id):
        return self.images.get(id)
    
    def getCue(self):
        return self.images.get("HighCue1")
    
    def stimulate(self, tc):
        return self.images.get("MarkerWithFiducial")    

def CreateLearningTask(tc):
    return LearningTask(tc)

def InitializeLearning(tc):
    return tc.LearningTask.reset()

def RunLearning(tc, x):
    display = tc.Devices.Display
    task = tc.LearningTask

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
        
    return True

def CreateTestTask(tc):
    return TestTask(tc)

def InitializeTest(tc):
    return tc.TestTask.reset()

def RunTest(tc, x):
    display = tc.Devices.Display
    task = tc.TestTask

    if (tc.StimulusName == "Marker1"):
        display.Display(task.getImage("Marker"))
    elif (tc.StimulusName == "Cue"):
        display.Display(task.getCue())
    elif (tc.StimulusName == "RateExpected"):
        display.Display(task.getImage("TestRateExpectedPain"))
    elif (tc.StimulusName == "Marker2"):
        display.Display(task.getImage("Marker"))
    elif (tc.StimulusName == "Stimulate"):
        display.Display(task.stimulate(tc))
    elif (tc.StimulusName == "Marker3"):
        display.Display(task.getImage("Marker"))
    elif (tc.StimulusName == "Rate"):
        display.Display(task.getImage("TestRatePain"))
    elif (tc.StimulusName == "Blank"):
        display.Display(task.getImage("Blank"))
        task.nextTrial()
        
    return True
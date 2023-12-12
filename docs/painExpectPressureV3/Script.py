from Serilog import Log
from LabBench.Interface.Instruments.Algometry import *
import traceback
import random

def Stimulate(tc, x):
    algometer = tc.Devices.Algometer
    chan = algometer.Channels[0]

    chan.SetStimulus(1, chan.CreateWaveform()
                     .Step(x, 2))
    algometer.ConfigurePressureOutput(0, ChannelID.CH01)
    algometer.StartStimulation(AlgometerStopCriterion.STOP_CRITERION_ON_BUTTON_PRESSED, True)

    return True

class ImageRepository:
    def __init__(self, tc):
        stimuli = tc.Assets.VisualStimuli
    
        self.Cue = [
            [stimuli.GetAsset("LowCue1.png").Data, stimuli.GetAsset("LowCue2.png").Data],
            [stimuli.GetAsset("HighCue1.png").Data, stimuli.GetAsset("HighCue2.png").Data]
        ]
        self.Feedback = [
            [
                stimuli.GetAsset("Low27.png").Data,
                stimuli.GetAsset("Low32.png").Data,
                stimuli.GetAsset("Low40.png").Data,
                stimuli.GetAsset("Low45.png").Data,
                stimuli.GetAsset("Low51.png").Data,            
            ],
            [
                stimuli.GetAsset("High73.png").Data,
                stimuli.GetAsset("High79.png").Data,
                stimuli.GetAsset("High84.png").Data,
                stimuli.GetAsset("High88.png").Data,
                stimuli.GetAsset("High93.png").Data,
            ]
        ]
        self.Blank = stimuli.GetAsset("Blank.png").Data
        self.Marker = stimuli.GetAsset("Marker.png").Data
        self.MarkerWithFiducial = stimuli.GetAsset("MarkerWithFiducial.png").Data
        self.LearningRateExpectedPain = stimuli.GetAsset("LearningRateExpectedPainDE.png") if tc.Language == "de" else stimuli.GetAsset("LearningRateExpectedPainEn.png")
        self.TestRateExpectedPain = stimuli.GetAsset("TestRateExpectedPainDE.png") if tc.Language == "de" else stimuli.GetAsset("TestRateExpectedPainEN.png")
        self.TestRatePain = stimuli.GetAsset("TestRatePainDE.png") if tc.Language == "de" else stimuli.GetAsset("TestRatePainEN.png")

def CreateImageRepository(tc):
    return ImageRepository(tc)
   
class LearningTrial:
    def __init__(self, tc):
        self.high = tc.StimulusName[0] == "H"
        self.variant = tc.StimulusName[1] == "1"
        self.cue = random.randint(0, 4)
        self.rating = -1
  
def InitializeLearning(tc):
    tc.Defines.Set("LearningTrials", [])
    tc.Defines.Set("SavedLearningTrials", [])
    return True

def AbortLearningBlock(tc):
    tc.LearningTrials = tc.SavedLearningTrials
    return True

def LearningComplete(tc):
    tc.Current.Annotations.Add("high", [trial.high for trial in tc.LearningTrials])
    tc.Current.Annotations.Add("cue", [trial.cue for trial in tc.LearningTrials])
    tc.Current.Annotations.Add("variant", [trial.variant for trial in tc.LearningTrials])
    tc.Current.Annotations.Add("rating", [trial.rating for trial in tc.LearningTrials])
    tc.SavedLearningTrials = tc.LearningTrials.copy()
    return True

def LearningRatingPain(tc):
    tc.Devices.Display.Display(tc.Images.Marker)
    tc.LearningTrials[-1].rating = tc.Devices.Response.GetCurrentRating() 
    return 500

def RunLearning(tc, x):
    try:
        display = tc.Devices.Display
        trial = LearningTrial(tc)
        tc.LearningTrials.append(trial)

        display.Run(display.Sequence(tc)
                    .Display(tc.Images.Marker, 500)
                    .Display(tc.Images.Cue[trial.high][trial.cue], 2000)
                    .Display(tc.Images.LearningRateExpectedPain, 4000)
                    .Run(LearningRatingPain)
                    .Display(tc.Images.Feedback[trial.high][trial.variant], 3000)                    
                    )
        
        return True
 
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False

class TestTrial:
    def __init__(self, tc):
        self.high = tc.StimulusName[0] == "H"
        self.cue = tc.StimulusName[1] == "1"        
        self.correct = tc.StimulusName[2] == "C"
        self.ratingExpected
        self.ratingActual = -1;    

def InitializeTest(tc):
    tc.Defines.Set("TestTrials", [])
    tc.Defines.Set("SavedTestTrials", [])
    return True

def AbortTestBlock(tc):
    tc.TestTrials = tc.SavedTestTrials
    return True

def TestComplete(tc):
    tc.Current.Annotations.Add("high", [trial.high for trial in tc.TestTrials])
    tc.Current.Annotations.Add("cue", [trial.cue for trial in tc.TestTrials])
    tc.Current.Annotations.Add("correct", [trial.correct for trial in tc.TestTrials])
    tc.Current.Annotations.Add("ratingExpected", [trial.ratingExpected for trial in tc.TestTrials])
    tc.Current.Annotations.Add("ratingActual", [trial.ratingActual for trial in tc.TestTrials])
    tc.SavedTestTrials = tc.TestTrials.copy()
    return True

def TestRateExpectedPain(tc):
    tc.Devices.Display.Display(tc.Images.Marker)
    tc.TestTrials[-1].ratingExpected = tc.Devices.Response.GetCurrentRating() 
    return 500

def getIntensity(tc):
    trial = tc.TestTrials[-1]
    if trial.high == 1:
        return tc.THR30['PULSE'] if trial.correct == 0 else tc.THR70['PULSE']
    elif trial.high == 0:
        return tc.THR70['PULSE'] if trial.correct == 0 else tc.THR30['PULSE']
    else:
        raise ValueError("Invalid high value: {high}".format(high = trial.high))
    
def TestStimulate(tc):
    tc.Devices.Display.Display(tc.Images.Marker)
    Stimulate(tc, getIntensity(tc))
    return 2000

def TestRateActualPain(tc):
    tc.Devices.Display.Display(tc.Images.Blank)
    tc.TestTrials[-1].ratingActual = tc.Devices.Response.GetCurrentRating() 
    return 10

def RunTest(tc, x):
    try:
        display = tc.Devices.Display
        trial = TestTrial(tc)
        tc.TestTrials.append(trial)

        display.Run(display.Sequence()
                    .Display(tc.Images.Marker, 500)
                    .Display(tc.cue[trial.high][tc.cue[trial.cue]], 2000)
                    .Display(tc.Images.TestRateExpectedPain, 4000)
                    .Run(TestRateExpectedPain)
                    .Display(tc.Images.Marker, 500)
                    .Run(TestStimulate)
                    .Display(tc.Images.Marker, 500)
                    .Display(tc.Images.TestRatePain, 5000)
                    .Run(TestRateActualPain)
                    )
        return True
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False
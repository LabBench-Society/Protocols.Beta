from Serilog import Log
from LabBench.Interface.Instruments.Algometry import *
import traceback
import random

class IntensitySelector:
    def __init__(self, tc):
        self.tc = tc

    def PresentationIntensity(self):
        return 0 if self.tc.Session == "SES01" else 1
    
    def VAS30(self):
        return 0 if self.tc.Session == "SES01" else 1

    def VAS70(self):
        return 0 if self.tc.Session == "SES01" else 1

def CreateIntensitySelector(tc):
    return IntensitySelector(tc)

def Stimulate(tc, x):
    algometer = tc.Instruments.PressureAlgometer
    chan = algometer.Channels[0]

    chan.SetStimulus(1, chan.CreateWaveform()
                     .Step(x, 2))
    algometer.ConfigurePressureOutput(0, ChannelID.CH01)
    algometer.StartStimulation(AlgometerStopCriterion.STOP_CRITERION_ON_BUTTON_PRESSED, True)

    return True

def CreateLowCue(tc, variant):
    Xc = tc.ImageWidth/2
    Yc = tc.ImageHeight/2
    W = 400
    H = 400

    with tc.Image.GetCanvas(tc.ImageWidth, tc.ImageHeight, '#ffffff') as canvas:
        canvas.Color("#0000FF")
        canvas.Fill(True)
        canvas.Rectangle(Xc - W/2, Yc- H/2, Xc + W/2, Yc + H/2) # + level, 10 + level   1000, 600, 800, 400 
        canvas.Color("#ffffff")
        canvas.Fill(True)
        if variant == 1:
            canvas.Rectangle(Xc - W/2, Yc - H/2, Xc, Yc) # + level, 10 + level   1000, 600, 800, 400 
        else:
            canvas.Rectangle(Xc, Yc - H/2, Xc + W/2, Yc) # + level, 10 + level   1000, 600, 800, 400 

        return canvas.GetImage()

def CreateHighCue(tc, variant):
    Xc = tc.ImageWidth/2
    Yc = tc.ImageHeight/2
    W = 400
    H = 400

    with tc.Image.GetCanvas(tc.ImageWidth, tc.ImageHeight, '#ffffff') as canvas:
        canvas.Color("#0000FF")
        canvas.Fill(True)
        canvas.Rectangle(Xc - W/2, Yc- H/2, Xc + W/2, Yc + H/2) # + level, 10 + level   1000, 600, 800, 400  Ws/2
        canvas.Color("#ffffff")
        canvas.Fill(True)
        if variant == 1:
            canvas.Rectangle(Xc, Yc, Xc + W/2, Yc + H/2) # + level, 10 + level   1000, 600, 800, 400 
        else:
            canvas.Rectangle(Xc - W/2, Yc , Xc, Yc + H/2) #Ws, Hs/2, Ws + W/2, Hs   
        return canvas.GetImage()

def CreateFeedback(tc, level):
    Ws = 1920
    Hs = 1080


    with tc.Image.GetCanvas(Ws, Hs, '#ffffff') as canvas:
        canvas.Color("#0000FF")
        canvas.Fill(True)
        canvas.Rectangle(1100, 600, 900, 400 ) 

        canvas.Font("Roboto")
        canvas.TextSize(24)
        canvas.Color("#000000")

        canvas.Write(10,500, 'Level = {level}'.format(level = level))

        return canvas.GetImage()

class ImageRepository:
    def __init__(self, tc):
        stimuli = tc.Assets.VisualStimuli
    
        self.Cue = [
            [stimuli.LowCue1, stimuli.LowCue2],
            [stimuli.HighCue1, stimuli.HighCue2]
        ]
        self.Feedback = [
            [
                 stimuli.Low27,
                 stimuli.Low32,
                 stimuli.Low40,
                 stimuli.Low45,
                 stimuli.Low51],
            [
                 stimuli.High73,
                 stimuli.High79,
                 stimuli.High84,
                 stimuli.High88,
                 stimuli.High93]
        ]
        self.Blank = stimuli.Blank
        self.Marker = stimuli.Marker
        self.MarkerWithFiducial = stimuli.MarkerWithFiducial
        self.LearningRateExpectedPain = (stimuli.LearningRateExpectedPainDE 
                                         if tc.Language == "de" 
                                         else stimuli.LearningRateExpectedPainEn)
        self.TestRateExpectedPain = (stimuli.TestRateExpectedPainDE 
                                     if tc.Language == "de" 
                                     else stimuli.TestRateExpectedPainEN)
        self.TestRatePain = (stimuli.TestRatePainDE 
                             if tc.Language == "de" 
                             else stimuli.TestRatePainEN)

    def AlternativeCues(self, tc, alternative):
        if alternative:
            self.Cue = [
                [CreateLowCue(tc, 1), CreateLowCue(tc, 2)],
                [CreateHighCue(tc, 1), CreateHighCue(tc, 2)]
            ]
        else:
            stimuli = tc.Assets.VisualStimuli

            self.Cue = [
                [stimuli.LowCue1, stimuli.LowCue2],
                [stimuli.HighCue1, stimuli.HighCue2]
            ]


def CreateImageRepository(tc):
    return ImageRepository(tc)

class LearningTrial:
    def __init__(self, tc):
        self.high = 1 if tc.StimulusName[0] == "H" else 0
        self.variant = 1 if tc.StimulusName[1] == "1" else 0
        self.feedback = random.randint(0, 4)
        self.rating = -1
        Log.Information("LEARNING TRIAL [ high: {high}, variant: {high}, feedback: {feedback}]", self.high, self.variant, self.feedback)
  
def InitializeExampleLearning(tc):
    try:
        tc.Images.AlternativeCues(tc, True)
        tc.Defines.Set("LearningTrials", [])
        tc.Instruments.ImageDisplay.Default(tc.Images.Blank)
        Log.Information("Initialized learning task")
        return True
    
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False

def InitializeLearning(tc):
    try:
        tc.Images.AlternativeCues(tc, False)
        tc.Defines.Set("LearningTrials", [])
        tc.Instruments.ImageDisplay.Default(tc.Images.Blank)
        Log.Information("Initialized learning task")
        return True
    
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False

def LearningComplete(tc):
    try:        
        tc.LP.Annotations.Add("high", [trial.high for trial in tc.LearningTrials])
        tc.LP.Annotations.Add("variant", [trial.variant for trial in tc.LearningTrials])
        tc.LP.Annotations.Add("feedback", [trial.feedback for trial in tc.LearningTrials])
        tc.LP.Annotations.Add("rating", [trial.rating for trial in tc.LearningTrials])
        tc.LP.Annotations.Add("ratingLow", [trial.rating for trial in tc.LearningTrials if trial.high == 0])
        tc.LP.Annotations.Add("ratingHigh", [trial.rating for trial in tc.LearningTrials if trial.high == 1])

        Log.Information("Data added as annotations")
        
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return True

def LearningRatingPain(tc):
    try:        
        rating = tc.Instruments.Response.GetCurrentRating()
        tc.Instruments.ImageDisplay.Display(tc.Images.Marker)
        tc.LearningTrials[-1].rating = rating
        Log.Information("PAIN RATING: {rating}", rating) 
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return 500

def RunLearning(tc, x):
    try:
        display = tc.Instruments.ImageDisplay
        trial = LearningTrial(tc)
        tc.LearningTrials.append(trial)
       
        display.Run(display.Sequence(tc)
                    .Display(tc.Images.Marker, 500)
                    .Display(tc.Images.Cue[trial.high][trial.variant], 2000)
                    .Display(tc.Images.LearningRateExpectedPain, 4000)
                    .Run(LearningRatingPain)
                    .Display(tc.Images.Feedback[trial.high][trial.feedback], 3000)        
                    )
        
        return True
 
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False

class TestTrial:
    def __init__(self, tc):
        self.high = 1 if tc.StimulusName[0] == "H" else 0
        self.variant = 1 if tc.StimulusName[1] == "1" else 0        
        self.congruent = 1 if tc.StimulusName[2] == "C" else 0
        self.ratingExpected = -1
        self.ratingActual = -1;    

def InitializeTest(tc):
    try:
        tc.Images.AlternativeCues(tc, False)
        tc.Defines.Set("TestTrials", [])
        tc.Devices.ImageDisplay.Default(tc.Images.Blank)
        Log.Information("Initialized test task")
        return True

    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False

def InitializeExampleTest(tc):
    try:
        tc.Images.AlternativeCues(tc, True)
        tc.Defines.Set("TestTrials", [])
        tc.Devices.ImageDisplay.Default(tc.Images.Blank)
        Log.Information("Initialized test task")
        return True

    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False        

def TestComplete(tc):
    try:
        tc.TP.Annotations.Add("high", [trial.high for trial in tc.TestTrials])
        tc.TP.Annotations.Add("variant", [trial.variant for trial in tc.TestTrials])
        tc.TP.Annotations.Add("congruent", [trial.congruent for trial in tc.TestTrials])
        tc.TP.Annotations.Add("ratingExpected", [trial.ratingExpected for trial in tc.TestTrials])
        tc.TP.Annotations.Add("ratingActual", [trial.ratingActual for trial in tc.TestTrials])

        tc.TP.Annotations.Add("expectedHighCongruent", [trial.ratingExpected for trial in tc.TestTrials if trial.high == 1 and trial.congruent == 1])
        tc.TP.Annotations.Add("actualHighCongruent", [trial.ratingActual for trial in tc.TestTrials if trial.high == 1 and trial.congruent == 1])
        tc.TP.Annotations.Add("expectedHighIncongruent", [trial.ratingExpected for trial in tc.TestTrials if trial.high == 1 and trial.congruent == 0])
        tc.TP.Annotations.Add("actualHighIncongruent", [trial.ratingActual for trial in tc.TestTrials if trial.high == 1 and trial.congruent == 0])

        tc.TP.Annotations.Add("expectedLowCongruent", [trial.ratingExpected for trial in tc.TestTrials if trial.high == 0 and trial.congruent == 1])
        tc.TP.Annotations.Add("actualLowCongruent", [trial.ratingActual for trial in tc.TestTrials if trial.high == 0 and trial.congruent == 1])
        tc.TP.Annotations.Add("expectedLowIncongruent", [trial.ratingExpected for trial in tc.TestTrials if trial.high == 0 and trial.congruent == 0])
        tc.TP.Annotations.Add("actualLowIncongruent", [trial.ratingActual for trial in tc.TestTrials if trial.high == 0 and trial.congruent == 0])

        Log.Information("Data added as annotations")

    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return True

def TestRateExpectedPain(tc):
    try:
        ratingExpected = tc.Instruments.Response.GetCurrentRating() 
        tc.Instruments.ImageDisplay.Display(tc.Images.Marker)
        tc.TestTrials[-1].ratingExpected = ratingExpected
        Log.Information("Rating expected pain: {rating}", ratingExpected)
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return 500

def getIntensity(tc):
    trial = tc.TestTrials[-1]

    if trial.high == 1:
        intensity = tc.THR30['PULSE'] if trial.congruent == 0 else tc.THR70['PULSE']
    elif trial.high == 0:
        intensity = tc.THR70['PULSE'] if trial.congruent == 0 else tc.THR30['PULSE']
    else:
        raise ValueError("Invalid high value: {high}".format(high = trial.high))
    
    Log.Information("STIMULATE [ high: {high}, congruent: {congruent} ] with intensity: {intensity}kPa",
                    trial.high,
                    trial.congruent,
                    intensity)
    
    return intensity
    
def TestStimulate(tc):
    try:
        tc.Devices.ImageDisplay.Display(tc.Images.MarkerWithFiducial)
        Stimulate(tc, getIntensity(tc))
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return 2000

def TestRateActualPain(tc):
    try:
        ratingActual = tc.Instruments.Response.GetCurrentRating() 
        tc.Instruments.ImageDisplay.Display(tc.Images.Blank)
        tc.TestTrials[-1].ratingActual = ratingActual
        Log.Information("RATING ACTUAL PAIN: {rating}", ratingActual)        
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return 10

def RunTest(tc, x):
    try:
        display = tc.Instruments.ImageDisplay
        trial = TestTrial(tc)
        tc.TestTrials.append(trial)

        display.Run(display.Sequence(tc)
                    .Display(tc.Images.Marker, 500)
                    .Display(tc.Images.Cue[trial.high][trial.variant], 2000)
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
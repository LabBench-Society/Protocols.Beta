from Serilog import Log
import traceback
import random

class ImageRepository:
    def __init__(self, tc):
        stimuli = tc.Assets.VisualStimuli
    
        self.Cue = [
            [stimuli.GetImageFromArchive("LowCue1.png"), stimuli.GetImageFromArchive("LowCue2.png")],
            [stimuli.GetImageFromArchive("HighCue1.png"), stimuli.GetImageFromArchive("HighCue2.png")]
        ]
        self.Feedback = [
            [
                stimuli.GetImageFromArchive("Low27.png"),
                stimuli.GetImageFromArchive("Low32.png"),
                stimuli.GetImageFromArchive("Low40.png"),
                stimuli.GetImageFromArchive("Low45.png"),
                stimuli.GetImageFromArchive("Low51.png")],
            [
                stimuli.GetImageFromArchive("High73.png"),
                stimuli.GetImageFromArchive("High79.png"),
                stimuli.GetImageFromArchive("High84.png"),
                stimuli.GetImageFromArchive("High88.png"),
                stimuli.GetImageFromArchive("High93.png")]
        ]
        self.Blank = stimuli.GetImageFromArchive("Blank.png")
        self.Marker = stimuli.GetImageFromArchive("Marker.png")
        self.MarkerWithFiducial = stimuli.GetImageFromArchive("MarkerWithFiducial.png")
        self.LearningRateExpectedPain = (stimuli.GetImageFromArchive("LearningRateExpectedPainDE.png") 
                                         if tc.Language == "de" 
                                         else stimuli.GetImageFromArchive("LearningRateExpectedPainEn.png"))
        self.TestRateExpectedPain = (stimuli.GetImageFromArchive("TestRateExpectedPainDE.png") 
                                     if tc.Language == "de" 
                                     else stimuli.GetImageFromArchive("TestRateExpectedPainEN.png"))
        self.TestRatePain = (stimuli.GetAssGetImageFromArchive("TestRatePainDE.png") 
                             if tc.Language == "de" 
                             else stimuli.GetImageFromArchive("TestRatePainEN.png"))

def CreateImageRepository(tc):
    return ImageRepository(tc)
   
class LearningTrial:
    def __init__(self, tc):
        self.high = 1 if tc.StimulusName[0] == "H" else 0
        self.variant = 1 if tc.StimulusName[1] == "1" else 0
        self.feedback = random.randint(0, 4)
        self.rating = -1
        Log.Information("LEARNING TRIAL [ high: {high}, variant: {high}, feedback: {feedback}]", self.high, self.variant, self.feedback)
  
def InitializeLearning(tc):
    try:
        tc.Defines.Set("LearningTrials", [])
        tc.Devices.Display.Default(tc.Images.Blank)
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
        rating = tc.Devices.Response.GetCurrentRating()
        tc.Devices.Display.Display(tc.Images.Marker)
        tc.LearningTrials[-1].rating = rating
        Log.Information("PAIN RATING: {rating}", rating) 
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return 500

def RunLearning(tc, x):
    try:
        display = tc.Devices.Display
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
        tc.Defines.Set("TestTrials", [])
        tc.Devices.Display.Default(tc.Images.Blank)
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
        ratingExpected = tc.Devices.Response.GetCurrentRating()
        tc.Devices.Display.Display(tc.Images.Marker)
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
        tc.Devices.Display.Display(tc.Images.MarkerWithFiducial)
        tc.Devices.Stimulator.Generate(tc.stimulus)
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return 2000

def TestRateActualPain(tc):
    try:
        ratingActual = tc.Devices.Response.GetCurrentRating() 
        tc.Devices.Display.Display(tc.Images.Blank)
        tc.TestTrials[-1].ratingActual = ratingActual
        Log.Information("RATING ACTUAL PAIN: {rating}", ratingActual)        
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))

    return 10

def RunTest(tc, x):
    try:
        display = tc.Devices.Display
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
from Serilog import Log
from LabBench.Interface.Instruments.Algometry import *
import traceback
import random
import math

class ImageRepository:
    def __init__(self, tc):
        stimuli = tc.Assets.Images
    
        self.Cue01 = stimuli.GetImageFromArchive("Cue1.png")
        self.Cue02 = stimuli.GetImageFromArchive("Cue2.png")
        self.Cue03= stimuli.GetImageFromArchive("Cue3.png")
        self.Contract = stimuli.GetImageFromArchive("Contract.png")
        self.Blank = stimuli.GetImageFromArchive("Blank.png")
        self.Complete = stimuli.GetImageFromArchive("Complete.png")
        self.Ready = stimuli.GetImageFromArchive("Ready.png")
        self.Rest = stimuli.GetImageFromArchive("Rest.png")

        self.MVCInstruction = stimuli.GetImageFromArchive("MVCInstruction.png")
        self.MVCPostEffort = stimuli.GetImageFromArchive("MVCPostEffort.png")
        self.PainEffortInstruction01 = stimuli.GetImageFromArchive("PainEffortInstruction01.png")
        self.PainEffortInstruction02 = stimuli.GetImageFromArchive("PainEffortInstruction02.png")
        self.PainEffortInstruction03 = stimuli.GetImageFromArchive("PainEffortInstruction03.png")
        self.QuestionnaireInstruction = stimuli.GetImageFromArchive("QuestionnaireInstruction.png")
        self.RightLeg = stimuli.GetImageFromArchive("RightLeg.png")
        self.LeftLeg = stimuli.GetImageFromArchive("LeftLeg.png")

        self.SR1 = stimuli.GetImageFromArchive("SR1.png")
        self.SR2 = stimuli.GetImageFromArchive("SR2.png")
        self.TS = stimuli.GetImageFromArchive("TS.png")
        self.CPM = stimuli.GetImageFromArchive("CPM.png")

def InstructionSR1(tc):
    tc.Devices.Display.Display(tc.Images.SR1)
    return True

def InstructionSR2(tc):
    tc.Devices.Display.Display(tc.Images.SR2)
    return True

def InstructionTS(tc):
    tc.Devices.Display.Display(tc.Images.TS)
    return True

def InstructionCPM(tc):
    tc.Devices.Display.Display(tc.Images.CPM)
    return True

def InstructionMVC(tc):
    tc.Devices.Image.Display(tc.Images.MVCInstruction)
    return True

def InstructionPostEffort(tc):
    tc.Devices.Image.Display(tc.Images.MVCPostEffort)
    return True

def CreateImageRepository(tc):
    return ImageRepository(tc)


def IsMVCIncomplete(tc):
    diff = 100 * abs(tc.Current['M1'] - tc.Current['M2']) / ((tc.Current['M1'] + tc.Current['M2'])/2)
    return diff > 10

def InitializeEffortTrial(tc):
    tc.Defines.Set("DominantVAS", [])
    tc.Defines.Set("NonDominantVAS", [])
    Log.Information("INITIALIZE EFFORT TRIAL")

    return True

def CompleteEffortTrial(tc):
    Log.Information("COMPLETE EFFORT TRIAL")
    tc.Current.Annotations.Add("DominantVAS", [vas for vas in tc.DominantVAS])
    tc.Current.Annotations.Add("NonDominantVAS", [vas for vas in tc.NonDominantVAS])

    return True

def Start(tc):
    tc.Devices.Sound.Play(tc.Assets.GoSound)
    return 3000

def Stop(tc):
    tc.Devices.Sound.Play(tc.Assets.StopSound)
    return 50

def SamplePainDominant(tc):
    tc.Devices.Display.Display(tc.Images.Blank)
    rating = tc.Devices.Response.GetRatioRating()
    tc.DominantVAS.Add(rating)
    Log.Information("Pain dominant leg: {rating}".format(rating = rating))
    return 50

def SamplePainNonDominant(tc):
    tc.Devices.Display.Display(tc.Images.Blank)
    rating = tc.Devices.Response.GetRatioRating()
    tc.NonDominantVAS.Add(rating)
    Log.Information("Pain non-dominant leg: {rating}".format(rating = rating))
    return 50

def Instruct(tc,x):
    try:
        display = tc.Devices.Display

        if tc.StimulusName == "I1":
            display.Display(tc.Images.PainEffortInstruction01)
        elif tc.StimulusName == "I2":
            display.Display(tc.Images.PainEffortInstruction02)
        elif tc.StimulusName == "I3":
            display.Display(tc.Images.PainEffortInstruction03)
        elif tc.StimulusName == "I4":
            display.Display(tc.Images.Ready)
        elif tc.StimulusName == "I5":
            display.Display(tc.Images.Blank)

        return True
    
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False

#<choice value="0" label="L/S|H/S" />
#<choice value="1" label="H/S|L/S" />
#<choice value="2" label="L/S|S/H" />
#<choice value="3" label="H/S|S/L" />
#<choice value="4" label="S/L|S/H" />
#<choice value="5" label="S/H|S/L" />
#<choice value="6" label="S/L|H/S" />
#<choice value="7" label="S/H|L/S" />

def IntensityMatrix(SR):
    L = 0.4*SR.PTT
    H = 0.8*SR.PTT
    S = 5

    return [[L, S, H, S],
            [H, S, L, S],
            [L, S, S, H],
            [H, S, S, L],
            [S, L, S, H],
            [S, H, S, L],
            [S, L, H, S],            
            [S, H, L, S]]

def IntensitySES01B1(tc):
    return IntensityMatrix(tc.SES01SR01)[tc.SUBJECT['SETUP']][0]

def IntensitySES01B2(tc):
    return IntensityMatrix(tc.SES01SR01)[tc.SUBJECT['SETUP']][1]

def IntensitySES02B1(tc):
    return IntensityMatrix(tc.SES01SR01)[tc.SUBJECT['SETUP']][2]

def IntensitySES02B2(tc):
    return IntensityMatrix(tc.SES01SR01)[tc.SUBJECT['SETUP']][3]

def SetContract(tc):
    tc.Devices.Display.Default(tc.Images.Contract)
    return 0

def Stimulate(tc,x):
    try:
        display = tc.Devices.Display

        if tc.StimulusName == "START":
            display.Run(display.Sequence(tc)
                        .Display(tc.Images.Cue03, 250)
                        .Display(tc.Images.Cue02, 250)
                        .Display(tc.Images.Cue01, 250)
                        .Run(SetContract))
            algometer = tc.Devices.Algometer
            chan = algometer.Channels[0]

            chan.SetStimulus(1, chan.CreateWaveform()
                            .Step(x, 600))
            algometer.ConfigurePressureOutput(0, ChannelID.CH01)
            algometer.ConfigurePressureOutput(1, ChannelID.NONE)
            algometer.StartStimulation(AlgometerStopCriterion.STOP_CRITERION_ON_BUTTON_PRESSED, True)

        elif tc.StimulusName == "CONTRACT":
            display.Run(display.Sequence(tc)
                        .Run(Start)
                        .Run(Stop))

        if tc.StimulusName == "STOP":
            display.Display(tc.Images.Blank)
            display.Default(tc.Images.Blank)
            algometer = tc.Devices.Algometer.StopStimulation()

        elif tc.StimulusName == "PAINDominant":
            display.Run(display.Sequence(tc)
                        .Display(tc.Images.LeftLeg if tc.SUBJECT['HANDEDNESS'] == 1 else tc.Images.RightLeg, 4000)
                        .Run(SamplePainDominant))
            
        elif tc.StimulusName == "PAINNonDominant":
            display.Run(display.Sequence(tc)
                        .Display(tc.Images.RightLeg if tc.SUBJECT['HANDEDNESS'] == 1 else tc.Images.LeftLeg, 4000)
                        .Run(SamplePainNonDominant))

        return True
    
    except Exception as e:
        Log.Error("An exception {e}: {trace}".format(e = e, trace = traceback.format_exc()))
        return False
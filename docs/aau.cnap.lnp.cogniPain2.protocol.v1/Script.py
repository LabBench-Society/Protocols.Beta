import random

def CuffInstruction(tc):
    if not tc.SUBJECT.Completed:
        return 'Instructions.UnknownHandedCuffs'
    
    return 'Instructions.LeftHandedCuffs' if tc.SUBJECT['HANDEDNESS'] == 1 else 'Instructions.RightHandedCuffs'

def Stimulate(tc, x):
    algometer = tc.Instruments.PressureAlgometer

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(x, 3.0))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.CH01)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.NoChannel)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True)

    return True

def MaximumStimulate(tc):
    algometer = tc.Instruments.PressureAlgometer

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(100, 3.0))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.CH01)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.NoChannel)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True)

    return True
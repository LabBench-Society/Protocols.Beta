
def CuffInstruction(tc):
    if not tc.SUBJECT.Completed:
        return tc.Assets.Instructions.UnknownHandedCuffs
    
    return tc.Assets.Instructions.LeftHandedCuffs if tc.SUBJECT['HANDEDNESS'] == 1 else tc.Assets.Instructions.RightHandedCuffs

def Stimulate(tc, x):
    algometer = tc.Instruments.PressureAlgometer

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(x, 3.0))

    algometer.ConfigurePressureOutput("outlet-1", "channel-1")
    algometer.ConfigurePressureOutput("outlet-2", "none")
    algometer.StartStimulation('stop-when-button-pressed', True)

    return True

def MaximumStimulate(tc):
    algometer = tc.Instruments.PressureAlgometer

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(100, 3.0))

    algometer.ConfigurePressureOutput("outlet-1", "channel-1")
    algometer.ConfigurePressureOutput("outlet-2", "none")
    algometer.StartStimulation('stop-when-button-pressed', True)

    return True
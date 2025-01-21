
def StimulateArm(tc):
    algometer = tc.Instruments.PressureAlgometer

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Ramp(tc.Intensity, 2).Step(tc.Intensity, 13))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.CH01)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.NONE)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True)

    return True

def StimulateLeg(tc):
    algometer = tc.Instruments.PressureAlgometer

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Ramp(tc.Intensity, 2).Step(tc.Intensity, 13))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.NONE)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.CH01)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True)

    return True
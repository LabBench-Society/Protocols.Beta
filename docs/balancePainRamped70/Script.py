
def StimulateArm(tc):
    algometer = tc.Instruments.PressureAlgometer

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Increment(tc.Intensity / 2, 2).Step(tc.Intensity, 13))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.CH01)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.NoChannel)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True)

    return True

def StimulateLeg(tc):
    algometer = tc.Instruments.PressureAlgometer

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Increment(tc.Intensity / 2, 2).Step(tc.Intensity, 13))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.NoChannel)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.CH01)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True)

    return True

def StopStimulation(tc):
    algometer = tc.Instruments.PressureAlgometer
    algometer.StopStimulation()

    return True
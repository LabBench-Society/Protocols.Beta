

def Stimulate(tc):
    algometer = tc.Instruments.PressureAlgometer
    display = tc.Instruments.ImageDisplay

    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(0.7 * tc.NDLEG.PTT, 110 - (6 + tc.CPM.PTT)))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.NONE)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.CH02)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True, False)

    return True
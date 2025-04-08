

def Stimulate(tc):
    algometer = tc.Instruments.PressureAlgometer
    display = tc.Instruments.ImageDisplay
    intensity = 0.7 * tc.NDLEG.PTT
    time = 110 - (6 + tc.CPM.PTT)
    
    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(intensity, time))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.NoChannel)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.CH02)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True, False)
    tc.Log.Information("STIMULATION STARTED [ Intensity: {intensity}, Time: {time}]", intensity, time)

    display.Display(tc.Assets.CPAInstructions.COND)

    return True

def ConditioningTime(tc):
    try:
        return 110 - (6 + tc.CPM.PTT) + 15
    except Exception as e:
        return 125


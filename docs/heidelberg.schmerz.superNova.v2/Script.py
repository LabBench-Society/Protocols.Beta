

def Stimulate(tc):
    algometer = tc.Instruments.PressureAlgometer
    display = tc.Instruments.ImageDisplay
    intensity = 0.7 * tc.NDLEG.PTT
    time = 110 - tc.CPM.RunningTime
    
    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(intensity, time))

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.NoChannel)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.CH02)
    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True, False)
    tc.Log.Information("STIMULATION STARTED [ Intensity: {intensity}, Time: {time}]", intensity, time)

    display.Display(tc.Assets.CPAInstructions.COND)

    return True

def Stop(tc):
    algometer = tc.Instruments.PressureAlgometer
    algometer.StopStimulation()
    return True

def ConditioningTime(tc):
    try:
        time = 110 - tc.CPM.RunningTime + 15
        tc.Log.Information("TEST DUTATION [ Time: {time}]", time)
        return time
    except Exception as e:
        return 125


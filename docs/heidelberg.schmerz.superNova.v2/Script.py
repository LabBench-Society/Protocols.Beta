

def Stimulate(tc):
    algometer = tc.Instruments.PressureAlgometer
    display = tc.Instruments.ImageDisplay
    intensity = 0.7 * tc.NDLEG.PTT
    time = 110 - tc.CPM.RunningTime
    
    chan = algometer.Channels[0]
    chan.SetStimulus(1, chan.CreateWaveform().Step(intensity, time))
    chan = algometer.Channels[1]
    chan.SetStimulus(1, chan.CreateWaveform())

    algometer.ConfigurePressureOutput(0, algometer.ChannelIDs.NoChannel)
    algometer.ConfigurePressureOutput(1, algometer.ChannelIDs.CH01)

    algometer.StartStimulation(algometer.StopCriterions.WhenButtonPressed, True, False)
    tc.Log.Information("STIMULATION STARTED [ Intensity: {intensity}, Time: {time}]", intensity, time)

    display.Display(tc.Assets.CPAInstructions.COND)

    return True

def Stop(tc):
    try:
        algometer = tc.Instruments.PressureAlgometer
        algometer.StopStimulation()
    except:
        pass

    return True

def ConditioningTime(tc):
    try:
        time = 110 - tc.CPM.RunningTime + 15
        return time
    except Exception as e:
        return 125


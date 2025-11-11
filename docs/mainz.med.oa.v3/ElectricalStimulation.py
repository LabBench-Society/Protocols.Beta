
class ElectricalOffsetAnalgesia:
   def __init__(self, tc, conditioning, intensity, duration):
      self.tc = tc
      self.PreConditioning = duration[0]
      self.PreDuration = duration[1]
      self.StimulusDuration = duration[2]
      self.PostDuration = duration[3]
      self.Intensity = intensity
      self.CondPressure = conditioning

   def Duration(self):
      return self.PreConditioning + self.PreDuration + self.StimulusDuration + self.PostDuration + 4

   def Stimulate(self, sr):
      cpar = self.tc.Instruments.PressureAlgometer
      channel = cpar.Channels[0]

      PDT = sr.PDT
      PTT = sr.PTT

      CondIntensity = self.CondPressure * (PTT - PDT) + PDT
      Intensity = self.Intensity * (PTT - PDT) + PDT

      channel.SetStimulus(1, channel.CreateWaveform()
                        .Step(0,self.PreConditioning)
                        .Step(CondIntensity,self.PreDuration)
                        .Step(Intensity,self.StimulusDuration)
                        .Step(CondIntensity,self.PostDuration))
      cpar.ConfigurePressureOutput(0, cpar.ChannelIDs.CH01)
      cpar.ConfigurePressureOutput(1, cpar.ChannelIDs.NoChannel)
      cpar.StartStimulation(cpar.StopCriterions.WhenButtonPressed, True)

      return True

   def Control(self, sr):
      cpar = self.tc.Instruments.PressureAlgometer
      channel = cpar.Channels[0]

      PDT = sr.PDT
      PTT = sr.PTT

      CondIntensity = self.CondPressure * (PTT - PDT) + PDT

      channel.SetStimulus(1, channel.CreateWaveform()
                        .Step(self.PrecondIntensity * PDT,self.PreConditioning)
                        .Step(CondIntensity,self.PreDuration)
                        .Step(CondIntensity,self.StimulusDuration)
                        .Step(CondIntensity,self.PostDuration))
      cpar.ConfigurePressureOutput(0, cpar.ChannelIDs.CH01)
      cpar.ConfigurePressureOutput(1, cpar.ChannelIDs.NoChannel)
      cpar.StartStimulation(cpar.StopCriterions.WhenButtonPressed, True)

      return True
   
def CreatePressureIncreasingOffsetModulation(tc):
   return PressureOffsetAnalgesia(tc, 0.4, 1, [2, 10, 10, 10])

def CreatePressureDecreasingOffsetModulation(tc):
   return PressureOffsetAnalgesia(tc, 0.8, 0.2, [2, 10, 10, 10])

def StopPressure(tc):
   cpar = tc.Instruments.PressureAlgometer
   cpar.StopStimulation()
   return True

def SamplePressure(tc):
   cpar = tc.Instruments.PressureAlgometer
   return [cpar.Pressure[0]]

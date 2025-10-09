
class OffsetAnalgesia:
   def __init__(self, tc, version, vas):
      self.version = version
      self.tc = tc
      self.vas = vas

   def Stimulate(self, sr):
      cpar = self.tc.Instruments.PressureAlgometer
      channel = cpar.Channels[0]

      PDT = sr.PDT
      PTT = sr.PTT

      if 'THR' in self.version:
         CondIntensity = self.tc.CondPressure * (PTT - PDT) + PDT
      else:
         CondIntensity = sr.GetPressureFromPerception(self.vas)

      channel.SetStimulus(1, channel.CreateWaveform()
                        .Step(CondIntensity,self.tc.PreDuration)
                        .Step(PTT,self.tc.StimulusDuration)
                        .Step(CondIntensity,self.tc.PostDuration))
      cpar.ConfigurePressureOutput(0, cpar.ChannelIDs.CH01)
      cpar.ConfigurePressureOutput(1, cpar.ChannelIDs.CH01)
      cpar.StartStimulation(cpar.StopCriterions.WhenButtonPressed, True)

      return True

   def StimulateGap(self, sr):
      cpar = self.tc.Instruments.PressureAlgometer
      channel = cpar.Channels[0]

      PDT = sr.PDT
      PTT = sr.PTT

      if 'THR' in self.version:
         CondIntensity = self.tc.CondPressure * (PTT - PDT) + PDT
      else:
         CondIntensity = sr.GetPressureFromPerception(self.vas)

      channel.SetStimulus(1, channel.CreateWaveform()
                        .Step(CondIntensity,self.tc.PreDuration)
                        .Step(0, self.tc.StimulationGap)
                        .Step(PTT,self.tc.StimulusDuration)
                        .Step(0, self.tc.StimulationGap)
                        .Step(CondIntensity,self.tc.PostDuration))
      cpar.ConfigurePressureOutput(0, cpar.ChannelIDs.CH01)
      cpar.ConfigurePressureOutput(1, cpar.ChannelIDs.CH01)
      cpar.StartStimulation(cpar.StopCriterions.WhenButtonPressed, True)

      return True

   
def CreateThresholdVersion(tc):
   return OffsetAnalgesia(tc, 'THR', 0.0)

def CreateRatingVersion(tc):
   return OffsetAnalgesia(tc, 'VAS', tc.CondRating)

def Stop(tc):
   cpar = tc.Instruments.PressureAlgometer
   cpar.StopStimulation()
   return True

def Sample(tc):
   cpar = tc.Instruments.PressureAlgometer
   return [cpar.Pressure[0]]

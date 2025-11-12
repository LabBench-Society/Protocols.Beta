
class ElectricalOffsetModulation:
   def __init__(self, tc, conditioning, intensity, duration):
      self.tc = tc
      self.Duration = duration
      self.Intensity = intensity
      self.Conditioning = conditioning
      self.CurrentIntenisity = 0

   def Duration(self):
      return self.Duration[0] + self.Duration[1] + self.Duration[3] + self.Duration[4] + 4

   def UpdateIntensity(self, duration, intensity):
      self.CurrentIntenisity = intensity
      self.tc.Log.Information("Updating intensity to {}".format(intensity) )

      return duration

   def Stimulate(self, thr):
      PTT = thr.CH01

      schedule = self.tc.Scheduler.Create()
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[0], 0))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[1], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[2], PTT * self.Intensity))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[3], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(5, 0))
      self.tc.Scheduler.Run(schedule)

      return True

   def Control(self, thr):
      PTT = thr.CH01

      schedule = self.tc.Scheduler.Create()
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[0], 0))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[1], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[2], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(1000 * self.Duration[3], PTT * self.Conditioning))
      schedule.Add(lambda: self.UpdateIntensity(5, 0))
      self.tc.Scheduler.Run(schedule)

      return True
   
   def Sample(self):
      return [self.CurrentIntenisity]
   
   def Stop(self):
      return True
   
def CreateElectricalOffsetModulation(tc):
   return ElectricalOffsetModulation(tc, 1.5, 1.8, [2, 10, 10, 10])

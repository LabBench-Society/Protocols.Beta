import random
from collections import defaultdict

class Condition:
   _data = {
      1:  (3, "3-3", ["4-4", "5-5", "6-6", "7-7"]),
      2:  (4, "4-4", ["5-5", "6-6", "7-7"]),
      3:  (5, "5-5", ["6-6", "7-7"]),
      4:  (6, "6-6", ["7-7"]),
      5:  (4, "4-5", ["4-6", "4-7", "6-5", "7-5"]),
      6:  (5, "4-5", ["4-6", "4-7", "6-5", "7-5"]),
      7:  (5, "5-6", ["5-7", "7-6"]),
      8:  (6, "5-6", ["5-7", "7-6"]),
      9:  (3, "3-6", ["3-7", "4-6", "5-6", "7-6"]),
      10: (6, "3-6", ["3-7", "4-6", "5-6", "7-6"]),
      11: (4, "4-7", ["5-7", "6-7"]),
      12: (7, "4-7", ["5-7", "6-7"]),
      13: (4, "4-6", ["5-6", "7-6", "4-7"]),
      14: (6, "4-6", ["5-6", "7-6", "4-7"]),
      15: (3, "3-7", ["4-7", "5-7", "6-7"]),
      16: (7, "3-7", ["4-7", "5-7", "6-7"]),
   }

   _lure_pools = defaultdict(list)

   def __init__(self, condition: int):
      if condition not in self._data:
         raise ValueError(f"Invalid condition: {condition}")

      self.Condition = condition
      self.Stimulation, self.Target, lures = self._data[condition]

      self.Lure = self._next_lure(condition, lures)

      self.TargetLeft = random.choice([True, False]) 

      self.TargetIntensity = self.get_intensity(self.Target)
      self.TargetPositions = [0, 1]
      random.shuffle(self.TargetPositions)

      self.LureIntensity = self.get_intensity(self.Lure)
      self.LurePositions = [0, 1]
      random.shuffle(self.LurePositions)

   @classmethod
   def _next_lure(cls, condition, lures):
      pool = cls._lure_pools[condition]

      if not pool:
         pool.extend(lures)
         random.shuffle(pool)

      return pool.pop()
   
   def is_target_selected(self, leftPressed):      
      return self.TargetLeft if leftPressed else not self.TargetLeft

   def parse(self, cue: str):
      a, b = map(int, cue.split("-"))
      return [a, b]

   def get_intensity(self, cue: str) -> int:
      return random.choice(self.parse(cue))
   
   def plot(self, image):
      image.AlignCenter()
      image.AlignMiddle()
      image.Color("#FFFFFF")
      y = image.Height / 2
      xLeft = int(image.Width / 4)
      xRight = int(3 * image.Width / 4)
      target = self.parse(self.Target)
      lure = self.parse(self.Lure)




   def plot_selected(self, image, targetSelected):
      image.AlignCenter()
      image.AlignMiddle()
      image.Color("#FFFFFF")

   def __repr__(self):
      return (
         f"Condition({self.Condition}) -> "
         f"Stim={self.Stimulation}, "
         f"Target={self.Target} ({self.TargetIntensity}), "
         f"Lure={self.Lure} ({self.LureIntensity})"
      )
   
class ResponseTask:
   def __init__(self, tc):
      self.tc = tc
      self.currentRating = 0

   def Start(self, numberOfTrials = 9999):
      self.trials = [Condition(c) for c in range(1, 17) for _ in range(5)]
      random.shuffle(self.trials)

      if numberOfTrials < len(self.trials):
         self.trials = self.trials[:numberOfTrials]
      
      self.index = 0
      self.ratings = []     
      self.currentRating = 0
      self.targetSelected = [] 

      return True
   
   def Complete(self):
      data = self.tc.Current

      data.SetNumbers("ratings", self.ratings)
      data.SetBools("targetSelected", self.targetSelected)
      data.SetIntegers("conditions", [condition.Condition for condition in self.trials])
      data.SetString("targets", [condition.Target for condition in self.trials])
      data.SetString("lures", [condition.Lure for condition in self.trials])
      data.SetIntegers("targetIntensities", [condition.TargetIntensity for condition in self.trials])
      data.SetIntegers("lureIntensities", [condition.LureIntensity for condition in self.trials])
      
      return True

   def PlotRating(self, x, y):
      with self.tc.Image.GetCanvas(x, y, "#FFFFFF") as image:
         image.AlignCenter()
         image.AlignMiddle()
         image.Color("#000000")
         image.Write(x /2, y /2, "Rating: {r}".format(r = self.currentRating))
         return image.GetImage()
                
   def PlotChoices(self, condition: Condition):
      display = self.tc.Instruments.ImageDisplay

      with self.tc.Image.GetCanvas(display, "#000000") as image:
         condition.plot(image)
         return image.GetImage()
      
   def PlotSelected(self, condition: Condition, targetSelected: bool):
      display = self.tc.Instruments.ImageDisplay

      with self.tc.Image.GetCanvas(display, "#000000") as image:
         condition.plot_selected(image, targetSelected)
         return image.GetImage()

   def Stimulate(self, condition: Condition, targetSelected: bool):
      if targetSelected:
         self.tc.Log.Information("Target intensity: {intensity}", condition.TargetIntensity)
      else:
         self.tc.Log.Information("Lure intensity: {intensity}", condition.LureIntensity)      

   def Enter(self, srTest):
      self.tc.Keyboard.Clear();
      self.tc.Instruments.Button.Reset()

      id = self.tc.CurrentState.ID
      display = self.tc.Instruments.ImageDisplay
      condition = self.trials[self.index]

      if id == "CROSS":
         display.Display(self.tc.Assets.Images.Cross, 1500)
      if id == "SELECTION":
         self.PlotChoices(condition)
      if id == "DISPLAY":
         self.PlotSelected(condition, self.targetSelected[-1])
      if id == "STIMULATION":
         display.Display(self.tc.Assets.Images.Stimulating)
         self.Stimulate(condition, self.targetSelected[-1])
      if id == "RATING":
         self.tc.CurrentState.SetPlotter(lambda x,y : self.PlotRating(x, y))
      if id == "PAUSE":
         display.Display(self.tc.Assets.Images.Blank)
      if id == "REST":
         display.Display(self.tc.Assets.Images.Break)

      return True
     
   def Update(self):
      button = self.tc.Instruments.Button
      scale = self.tc.Instruments.RatioScale

      id = self.tc.CurrentState.ID
      condition = self.trials[self.index]

      if id == "CROSS":
         return "*" if self.tc.CurrentState.RunningTime < 2000 else "SELECTION"
      
      if id == "SELECTION":
         if button.IsLatched("1"):
            self.targetSelected.append(condition.is_target_selected(True))
            self.tc.Log.Information("Target selected: {selected}", self.targetSelected[-1])
            return "DISPLAY"
         if button.IsLatched("2"):
            self.targetSelected.append(condition.is_target_selected(False))
            self.tc.Log.Information("Target selected: {selected}", self.targetSelected[-1])
            return "DISPLAY"
         
      if id == "DISPLAY":
         return "*" if self.tc.CurrentState.RunningTime < 2000 else "STIMULATION"
      
      if id == "STIMULATION":
         return "*" if self.tc.CurrentState.RunningTime < 500 else "RATING"
      
      if id == "RATING":
         self.currentRating = scale.GetRatioRating()

         if button.IsLatched("1") or button.IsLatched("2"):
            self.ratings.append(self.currentRating)
            return "PAUSE"         
         
      if id == "PAUSE":
         return "*" if self.tc.CurrentState.RunningTime < 2000 else "CROSS"
      
      if id == "REST":
         return "*" if self.tc.CurrentState.RunningTime < 2000 else "CROSS"
         
      return "*"

def CreateTask(tc):
   return ResponseTask(tc)


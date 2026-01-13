import random 

class ResponseTask:
   def __init__(self, tc):
      self.tc = tc
      self.PromptDisplayTime = 250  # milliseconds
      self.ResponseTimeLimit = 8000  # milliseconds
      self.CueDisplayTime = 2000  # milliseconds
      self.StimulationTime = 2000  # milliseconds
      self.Cues = [(4,5),(3,6),(4,6),(3,7),(5,6),(4,7)]
      self.selected = random.choice(["Target", "Lure"])


   def CreateCueImage(self, target, lure):
      with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as canvas:
         w = self.tc.Instruments.ImageDisplay.Width
         h = self.tc.Instruments.ImageDisplay.Height
         canvas.AlignCenter()
         canvas.AlignMiddle()
         canvas.Color("#FFFFFF")
         canvas.Write(w/2, h/2, "Cues: {}/{}".format(target, lure))
         return canvas.GetImage()

   def CreateSelectedImage(self, cue):
      with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as canvas:
         w = self.tc.Instruments.ImageDisplay.Width
         h = self.tc.Instruments.ImageDisplay.Height
         canvas.AlignCenter()
         canvas.AlignMiddle()
         canvas.Color("#FFFFFF")
         canvas.Write(w/2, h/2, "Selected Cue: {}".format(cue))
         return canvas.GetImage()

   def PlotRating(self, x, y):
      with self.tc.Image.GetCanvas(x, y, "#FFFFFF") as canvas:
         canvas.AlignCenter()
         canvas.AlignMiddle()
         canvas.Color("#000000")
         canvas.Write(x /2, y /2, "Rating: {}".format(self.current))
         return canvas.GetImage()

   def Start(self):
      self.current = 0
      return True
   
   def Complete(self):
      return True
     
   def Enter(self):
      id = self.tc.CurrentState.ID

      if id == "Prompt":
         self.tc.Instruments.ImageDisplay.Display(self.tc.Images.Cross)
         return True
      if id == "Cue":
         self.tc.Instruments.ImageDisplay.Display(self.CreateCueImage("Target", "Lure"))
         self.tc.Instruments.Button.Reset()
         return True
      if id == "Display":
         self.tc.Instruments.ImageDisplay.Display(self.CreateSelectedImage("Selected cue"))
         return True
      if id == "Stimulate":
         self.tc.Instruments.ImageDisplay.Display(self.tc.Images.Stimulating)
         return True
      if id == "Rate":
         self.tc.Instruments.Button.Reset()
         return True
      if id == "Pause":
         return True

      return False
    
   def Leave(self):
      return True
   
   def Update(self):
      id = self.tc.CurrentState.ID

      if id == "Prompt":
         return "Cue" if self.tc.CurrentState.RunningTime > self.PromptDisplayTime else "*"
      
      if id == "Cue":
         state = self.tc.CurrentState
         self.tc.CurrentState.Status = "Remaining time: {} ms".format(self.ResponseTimeLimit - state.RunningTime)

         if self.tc.Instruments.Button.IsLatched("left"):
            return "Display"
         if self.tc.Instruments.Button.IsLatched("right"):
            return "Display"         
         if state.RunningTime > self.ResponseTimeLimit:
            return "Display"

         return "*"
      
      if id == "Display":
         return "Stimulate" if self.tc.CurrentState.RunningTime > self.CueDisplayTime else "*"
      
      if id == "Stimulate":
         return "Rate" if self.tc.CurrentState.RunningTime > self.StimulationTime else "*"
      
      if id == "Rate":
         self.current = self.tc.Instruments.Scale.GetCurrentRating()

         if self.tc.Instruments.Button.IsLatched("next"):
            return "Pause"
         
         return "*"   
         
      if id == "Pause":
         return "Prompt" if self.tc.CurrentState.RunningTime > 1000 else "*"
      
      return "abort"


def CreateTask(tc):
   return ResponseTask(tc)


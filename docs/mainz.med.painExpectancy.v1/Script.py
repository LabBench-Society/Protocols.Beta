import random 


class ResponseTask:
   class PromptState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc

      def Enter(self):
         self.tc.Instruments.ImageDisplay.Display(self.tc.Images.Cross)
         return True

      def Leave(self):
         return True

      def Update(self):
         return "Cue" if self.tc.CurrentState.RunningTime > self.owner.PromptDisplayTime else "*"

   class CueState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def CreateImage(self, target, lure):
         with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as canvas:
            w = self.tc.Instruments.ImageDisplay.Width
            h = self.tc.Instruments.ImageDisplay.Height
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Color("#FFFFFF")
            canvas.Write(w/2, h/2, "Cues: {}/{}".format(target, lure))
            return canvas.GetImage()

      def Enter(self):
         self.tc.Instruments.ImageDisplay.Display(self.CreateImage("Target", "Lure"))
         return True

      def Leave(self):
         self.tc.Keyboard.Clear();
         return True

      def Update(self):
         state = self.tc.CurrentState
         self.tc.CurrentState.Status = "Remaining time: {} ms".format(self.owner.ResponseTimeLimit - state.RunningTime)

         if self.tc.Keyboard.Pressed("LEFT"):
            return "Display"
         if self.tc.Keyboard.Pressed("RIGHT"):
            return "Display"         
         if state.RunningTime > self.owner.ResponseTimeLimit:
            return "Display"

         return "*"

   class DisplayState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc

      def CreateImage(self, cue):
         with self.tc.Image.GetCanvas(self.tc.Instruments.ImageDisplay, "#000000") as canvas:
            w = self.tc.Instruments.ImageDisplay.Width
            h = self.tc.Instruments.ImageDisplay.Height
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Color("#FFFFFF")
            canvas.Write(w/2, h/2, "Selected Cue: {}".format(cue))
            return canvas.GetImage()
         
      def Enter(self):
         self.tc.Instruments.ImageDisplay.Display(self.CreateImage("Selected cue"))
         return True

      def Leave(self):
         self.tc.Keyboard.Clear();
         return True

      def Update(self):
         return "Stimulate" if self.tc.CurrentState.RunningTime > self.owner.CueDisplayTime else "*"

   class StimulateState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def Enter(self):
         self.tc.Instruments.ImageDisplay.Display(self.tc.Images.Stimulating)
         return True

      def Leave(self):
         return True

      def Update(self):
         return "Rate" if self.tc.CurrentState.RunningTime > self.owner.StimulationTime else "*"

   class RateState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def PlotRating(self, x, y):
         with self.tc.Image.GetCanvas(x, y, "#FFFFFF") as canvas:
            canvas.AlignCenter()
            canvas.AlignMiddle()
            canvas.Color("#000000")
            canvas.Write(x /2, y /2, "Rating: {}".format(self.owner.current))
            return canvas.GetImage()

      def Enter(self):
         pass

      def Leave(self):
         pass

      def Update(self):
         pass

   class PauseState:
      def __init__(self, tc, owner):
         self.owner = owner
         self.tc = tc
         pass

      def Enter(self):
         pass

      def Leave(self):
         pass

      def Update(self):
         pass

   def __init__(self, tc):
      self.tc = tc
      self.states = {
         "Prompt": self.PromptState(tc, self),
         "Cue": self.CueState(tc, self),
         "Display": self.DisplayState(tc, self),
         "Stimulate": self.StimulateState(tc, self),
         "Rate": self.RateState(tc, self),
         "Pause": self.PauseState(tc, self),
      }
      self.PromptDisplayTime = 250  # milliseconds
      self.ResponseTimeLimit = 8000  # milliseconds
      self.CueDisplayTime = 2000  # milliseconds
      self.StimulationTime = 2000  # milliseconds
      self.Cues = [(4,5),(3,6),(4,6),(3,7),(5,6),(4,7)]

   def Start(self):
      return True
   
   def Complete(self):
      return True
     
   def Enter(self):
      return self.states[self.tc.CurrentState.ID].Enter()
    
   def Leave(self):
      return self.states[self.tc.CurrentState.ID].Leave()
   
   def Update(self):
      return self.states[self.tc.CurrentState.ID].Update()

def CreateTask(tc):
   return ResponseTask(tc)


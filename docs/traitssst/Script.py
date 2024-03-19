from Serilog import Log
from LabBench.Interface.Instruments.Response import ButtonID
from LabBench.Interface.Waveforms import Waveform
import traceback
import random

class ImageRepository:
    def __init__(self, tc):
        images = tc.Assets.Images

        self.Left = images.GetImageFromArchive("left.png")
        self.Right = images.GetImageFromArchive("right.png")
        self.StopLeft = images.GetImageFromArchive("stopLeft.png")
        self.StopRight = images.GetImageFromArchive("stopRight.png")
        self.Correct = images.GetImageFromArchive("correct.png")
        self.Wrong = images.GetImageFromArchive("wrong.png")
        self.Instruction = images.GetImageFromArchive("instructions.png")        
        self.GoInstruction = images.GetImageFromArchive("goInstructions.png")        
        self.FixationCross = images.GetImageFromArchive("fixation.png")

class UpDownAlgorithm:
    def __init__(self, tc, stepsize, initialDelay):
        self.lowerLimit = tc.LowDelayLimit
        self.highLimit = tc.HighDelayLimit
        self.delay = initialDelay
        self.stopSignalDelay = []
        self.stepsize = stepsize

        self.delays = []

    def Complete(self, result):
        result.Annotations.Add("sstDelays", self.delays)
        result.Annotations.Add("sstStopSignalDelay", self.stopSignalDelay)

    def Iterate(self, answer):
        if answer:
            self.delay = self.delay + self.stepsize
            
            if self.delay > self.highLimit:
                self.delay = self.highLimit
        else:
            self.delay = self.delay - self.stepsize
            
            if self.delay < self.lowerLimit:
                self.delay = self.lowerLimit
        
        self.stopSignalDelay.append(self.delay)

class PsiAlgorithm:
    def __init__(self, tc):
        self.lowerLimit = tc.LowDelayLimit
        self.highLimit = tc.HighDelayLimit
        self.delays = []
        self.method = tc.Create(tc.Psychophysics.PsiMethod()
                                                .NumberOfTrials(tc.Trials)
                                                .Function(tc.Psychophysics.Functions.Quick(Beta=1, Lambda=0.02, Gamma=0))
                                                .Alpha(X0=tc.AlphaX0,X1=1.0,N = tc.AlphaN)
                                                .Beta(X0=tc.BetaX0,X1=tc.BetaX1,N = tc.BetaN)
                                                .Intensity(X0 = tc.IntensityX0,X1 = 1.0,N = tc.IntensityN))
        
        self.delay = self.Transform(self.method.Setup())     
        self.alpha = []
        self.beta = []
        self.ConfidenceLevel = tc.ConfidenceLevel
        self.alphaConfidence = []
        self.betaConfidence = []
        self.stopSignalDelay = []
        self.delays = []

    def Transform(self, x):
        return (self.highLimit - self.lowerLimit) * (1 - x) + self.lowerLimit
    
    def Complete(self, result):
        result.Annotations.Add("sstLowerLimit", self.lowerLimit)
        result.Annotations.Add("sstHighLimit", self.highLimit)
        result.Annotations.Add("sstDelays", self.delays)
        result.Annotations.Add("sstStopSignalDelay", self.stopSignalDelay)
        result.Annotations.Add("sstAlpha", self.alpha)        
        result.Annotations.Add("sstAlphaLower", [x[0] for x in self.alphaConfidence])        
        result.Annotations.Add("sstAlphaUpper", [x[1] for x in self.alphaConfidence])        
        result.Annotations.Add("sstBeta", self.beta)   
        result.Annotations.Add("sstBetaLower", [x[0] for x in self.betaConfidence])        
        result.Annotations.Add("sstBetaUpper", [x[1] for x in self.betaConfidence])                

    def Iterate(self, answer):
        self.delays.append(self.delay)

        self.delay = self.Transform(self.method.Iterate(answer))      

        alpha = self.method.EstimateAlpha()
        self.alpha.append(alpha)
        self.beta.append(self.method.EstimateBeta())
        self.alphaConfidence.append(self.method.EstimateAlphaConfidenceInterval(self.ConfidenceLevel))
        self.betaConfidence.append(self.method.EstimateBetaConfidenceInterval(self.ConfidenceLevel))
        self.stopSignalDelay.append(self.Transform(alpha))
        

class StopSignalTask:
    def __init__(self, tc, algorithm):
        self.display = tc.Devices.ImageDisplay
        self.response = tc.Devices.Response
        self.images = tc.Images
        self.algorithm = algorithm
        self.feedbackTime = tc.FeedbackTime
        self.responseTimeout = tc.ResponseTimeout
        self.feedbackDelay = tc.FeedbackDelay
                   
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.result = tc.Current
            
        Log.Information("Stop Signal Task [ CREATED ]")
    
    def Complete(self):
        self.result.Annotations.Add("sstGoSignals", self.goSignals)
        self.result.Annotations.Add("sstAnswer", self.answer)
        self.result.Annotations.Add("sstTime", self.time)
        self.algorithm.Complete(self.result)
        Log.Information("Stop Signal Task [ SAVED ]")

    def Go(self):
        self.response.Reset()
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        if self.signal == 0:
            self.display.Display(self.images.Left)
        else:
            self.display.Display(self.images.Right)                      
       
        Log.Information("STOP-SIGNAL TESTING DELAY [ Delay: {delay} ]".format(delay = self.algorithm.delay))

        return self.algorithm.delay
        
    def Stop(self):
        if self.signal == 0:
            self.display.Display(self.images.StopLeft)
        else:
            self.display.Display(self.images.StopRight)    

        return self.responseTimeout - self.algorithm.delay
            
    def Feedback(self):
        if self.response.LatchedActive != ButtonID.BUTTON_NONE:
            self.answer.append(0)
            self.time.append(self.response.ReactionTime)
        else:           
            self.answer.append(1)
            self.time.append(-1)

        self.algorithm.Iterate(True if self.answer[-1] == 1 else False)

        Log.Information("STOP-SIGNAL RESPONSE [ Correct: {answer}, sstDelay: {stopSignalDelay}, New Delay: {delay} ]", 
                        self.answer[-1], 
                        self.algorithm.stopSignalDelay[-1], 
                        self.algorithm.delay)

        if self.answer[-1] == 1:
            self.display.Display(self.images.Correct)
        else:
            self.display.Display(self.images.Wrong)

        return self.feedbackTime

class GoSignalTask:
    def __init__(self, tc):       
        self.tc = tc
        self.display = tc.Devices.ImageDisplay
        self.response = tc.Devices.Response
        self.images = tc.Images

        self.goDelay = tc.HighDelayLimit
        self.goSignals = [] # 0: left, 1: right
        self.answer = []
        self.time = []
        
        self.feedbackTime = tc.FeedbackTime
        self.responseTimeout = tc.ResponseTimeout
        self.feedbackDelay = tc.FeedbackDelay
        
        self.result = tc.Current
            
        Log.Information("Go Signal Task Created")
        
    def Complete(self):
        self.result.Annotations.Add("gtSignals", self.goSignals)
        self.result.Annotations.Add("gtAnswer", self.answer)
        self.result.Annotations.Add("gtTime", self.time)
    
    def Go(self):
        self.response.Reset()        
        self.signal = random.randint(0,1)
        self.goSignals.append(self.signal)
        
        if self.signal == 0:
            self.display.Display(self.images.Left)
        else:
            self.display.Display(self.images.Right)                      
       
        return self.responseTimeout
                  
    def Feedback(self):
        button = self.response.LatchedActive
        self.time.append(self.response.ReactionTime)
        
        if button == ButtonID.BUTTON_NONE:
            self.answer.append(0)
        else:         
            if self.signal == 0: # Left
                if button == ButtonID.LEFT: # Correct
                    self.answer.append(1)
                else: # wrong
                    self.answer.append(0)
                    
            else: # Right
                if button == ButtonID.RIGHT: # Correct
                    self.answer.append(1)
                else: # wrong
                    self.answer.append(0)
                        
        Log.Information("GO RESPONSE [ Button: {button}, Signal: {signal}, Correct: {answer}, Time: {time}]", 
                         button, 
                         "left" if self.signal == 0 else "right", 
                         self.answer[-1],
                         self.time[-1])

        if self.answer[-1] == 1:
            self.display.Display(self.images.Correct)
        else:
            self.display.Display(self.images.Wrong)

        return self.feedbackTime
 
def CreateImages(tc):
    return ImageRepository(tc)

def GoInstructions(tc):
    tc.Devices.ImageDisplay.Display(tc.Images.GoInstruction)
    return True

def Instructions(tc):
    tc.Devices.ImageDisplay.Display(tc.Images.Instruction)
    return True

def GoInitialize(tc):
    tc.Defines.Set("GoTask", GoSignalTask(tc))
    return True

def UpDownInitialize(tc):
    tc.Defines.Set("StopTask", StopSignalTask(tc, UpDownAlgorithm(tc, 100, 150)))
    tc.Defines.Set("GoTask", GoSignalTask(tc))
    return True

def PsiInitialize(tc):
    tc.Defines.Set("StopTask", StopSignalTask(tc, PsiAlgorithm(tc)))
    tc.Defines.Set("GoTask", GoSignalTask(tc))
    return True

def GoComplete(tc):
    tc.GoTask.Complete()
    return True

def Complete(tc):
    tc.StopTask.Complete()
    tc.GoTask.Complete()
    return True

def Go(task):
    return task.Go()
    
def Stop(task):
    return task.Stop()
    
def Feedback(task):
    return task.Feedback()
    
def Stimulate(tc, x):   
    display = tc.Devices.ImageDisplay
    
    if tc.StimulusName == "STOP":
        display.Run(display.Sequence(tc.StopTask)
                    .Display(tc.Images.FixationCross, tc.FixationDelay)
                    .Run(Go)
                    .Run(Stop)
                    .Display(tc.Images.FixationCross, tc.FeedbackDelay)
                    .Run(Feedback))
        
    elif tc.StimulusName == "GO":
        display.Run(display.Sequence(tc.GoTask)
                    .Display(tc.Images.FixationCross, tc.FixationDelay)
                    .Run(Go)
                    .Display(tc.Images.FixationCross, tc.FeedbackDelay)
                    .Run(Feedback))
    else:
        Log.Error("Unknown stimulus: {name}".format(name = tc.StimulusName))

    return True


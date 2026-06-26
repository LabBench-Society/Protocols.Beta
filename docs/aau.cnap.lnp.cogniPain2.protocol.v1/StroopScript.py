import random

def GetWords(tc):
    if tc.Language == 'DA':
        return {'b': 'BLÅ','y': 'GUL','r': 'RØD','g': 'GRØN'}
    
    if tc.Language == 'DE':
        return {'b': 'BLAU', 'y': 'GELB', 'r': 'ROT', 'g': 'GRÜN'}
    
    return {'b': 'BLUE','y': 'YELLOW','r': 'RED','g': 'GREEN'}

def StroopNeutralStimulate(tc, x):
    display = tc.Instruments.ImageDisplay
    name =  tc.StimulusName
    triggerGenerator = tc.Instruments.TriggerGenerator

    with tc.Image.GetCanvas(display) as canvas:
        tlk = tc.Triggers

        canvas.Fill(True)
        canvas.Color(tc.StroopColors[name[0]])
        canvas.Circle(display.Width/2, display.Height/2, display.Height/8)

        trigger = tlk.CreateTrigger(10).TriggerOut().Interface(1)
        triggerGenerator.GenerateTriggerSequence("port1", tlk.Sequence().Add(trigger))
        display.Display(canvas, tc.StroopDisplayTime, True)
        
    return True

def StroopStimulate(tc, x):
    display = tc.Instruments.ImageDisplay
    name =  tc.StimulusName
    triggerGenerator = tc.Instruments.TriggerGenerator

    with tc.Image.GetCanvas(display) as canvas:
        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(200)

        canvas.Color(tc.StroopColors[name[0]])
        canvas.Write(display.Width/2, display.Height/2, tc.StroopWords[name[1]])

        tlk = tc.Triggers
        triggerCode = 1 if name[0] == name[1] else 2
        trigger = tlk.CreateTrigger(10).TriggerOut().Interface(triggerCode)
        triggerGenerator.GenerateTriggerSequence("port1", tlk.Sequence().Add(trigger))
        display.Display(canvas, tc.StroopDisplayTime, True)
        
    return True

def IsCorrect(tc, result):
    if (result.Stimulus[0] == 'b'):
        return True if result.Response == 1 else False
    elif (result.Stimulus[0] == 'y'):
        return True if result.Response == 2 else False
    elif (result.Stimulus[0] == 'r'):
        return True if result.Response == 3 else False
    elif (result.Stimulus[0] == 'g'):
        return True if result.Response == 4 else False
    else:
        tc.Log.Error("Invalid stimulus name: " + result.Stimulus)
        return False
    
def StroopEvaluate(tc):
    tc.Current.Annotations.SetBools("correct", [IsCorrect(tc, s) for s in tc.Current.Stimulations])   
    return True
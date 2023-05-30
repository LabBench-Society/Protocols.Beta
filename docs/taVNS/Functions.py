
def GetIntensity(tc):
    index = tc.T03['MULT']
    retValue = tc.T02['PULSE']

    if index == 1:
        retValue = retValue * 1
    elif index == 2:
        retValue = retValue * 1.5
    elif index == 3:
        retValue = retValue * 2.0
    elif index == 4:
        retValue = retValue * 3.0    
    
    return retValue

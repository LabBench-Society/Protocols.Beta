def GetIntensity(tc, x):
    intensities = [tc.T02['PULSE'], 
                   (tc.T03['PULSE'] - tc.T02['PULSE'])*(1/3) + tc.T02['PULSE'], 
                   (tc.T03['PULSE'] - tc.T02['PULSE'])*(2/3) + tc.T02['PULSE'], 
                   tc.T03['PULSE']]
    index = (int)(x)
    return intensities[index]




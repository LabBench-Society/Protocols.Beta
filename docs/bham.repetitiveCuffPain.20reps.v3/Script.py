def GetInstructions(tc):
    instruction = tc.Assets.Instructions

    if not tc.CONFIGURATION.Completed:
        tc.Assets.Instructions.Default

    if tc.CONFIGURATION.Cuff:
        return tc.Assets.Instructions.LeftCuff
    else:
        return tc.Assets.Instructions.RightCuff

# Stroop-taak (SOMIMOVE-protocol)
# Gebaseerd op aau.cnap.lnp.cogniPain2.protocol.v2 (LabBench 6.0), zonder EEG-triggers.
# Stimulusnaam = kleur_woord, bv. "rood_groen" = het woord GROEN in rode letters.

def Kleur(naam):
    return naam.split("_")[0]   # kleur van de letters

def Woord(naam):
    return naam.split("_")[1]   # betekenis van het woord

# Geheugensteun onderaan het scherm: vier gekleurde bolletjes in dezelfde
# kruisvorm als de joystickknoppen (boven = rood, onder = blauw,
# links = geel, rechts = groen).
def TekenLegende(canvas, display, tc):
    cx = display.Width / 2
    cy = display.Height * 0.82
    d = display.Height * 0.07
    r = display.Height * 0.025

    canvas.Fill(True)
    for kleur, dx, dy in [('rood', 0, -d), ('blauw', 0, d), ('geel', -d, 0), ('groen', d, 0)]:
        canvas.Color(tc.StroopColors[kleur])
        canvas.Circle(cx + dx, cy + dy, r)

def StroopStimulate(tc, x, legende=False):
    display = tc.Instruments.ImageDisplay
    naam = tc.StimulusName

    with tc.Image.GetCanvas(display) as canvas:
        if legende:
            TekenLegende(canvas, display, tc)

        canvas.AlignCenter()
        canvas.AlignMiddle()
        canvas.Font("Roboto")
        canvas.TextSize(200)

        canvas.Color(tc.StroopColors[Kleur(naam)])
        canvas.Write(display.Width/2, display.Height/2, Woord(naam).upper())

        display.Display(canvas, tc.StroopDisplayTime, False)

    return True

# Correct antwoord = de knop van de KLEUR van de letters.
# Nummers zoals LabBench ze geeft (getest 4/11/2026, TEST026):
# links = 1 = geel, boven = 2 = rood, onder = 3 = blauw, rechts = 4 = groen
JUISTE_KNOP = {'geel': 1, 'rood': 2, 'blauw': 3, 'groen': 4}

# Antwoorden sneller dan dit (ms) zijn gokjes en tellen niet mee voor de reactietijd
MIN_RT = 200

def IsCorrect(tc, result):
    kleur = Kleur(result.Stimulus)

    if kleur in JUISTE_KNOP:
        return result.Response == JUISTE_KNOP[kleur]

    tc.Log.Error("Ongeldige stimulusnaam: " + result.Stimulus)
    return False

# Afronden op 1 decimaal (ook voor negatieve getallen); -1 en -999 blijven zoals ze zijn
def Afronden(x):
    if x == -1 or x == -999:
        return x
    return int(x * 10 + (0.5 if x >= 0 else -0.5)) / 10.0

def Percentage(lijst):
    return 100.0 * sum(1 for c in lijst if c) / len(lijst) if len(lijst) > 0 else -1

def Gemiddelde(waarden):
    return sum(waarden) / len(waarden) if len(waarden) > 0 else -1

def StroopEvaluate(tc):
    trials = list(tc.Current.Stimulations)
    correct = [IsCorrect(tc, s) for s in trials]

    # Per trial: was het antwoord correct?
    tc.Current.Annotations.SetBools("correct", correct)

    # Samenvatting
    n = len(trials)
    n_geen_antwoord = sum(1 for s in trials if s.Response <= 0)
    n_te_snel = sum(1 for s in trials if 0 <= s.ReactionTime < MIN_RT)

    # Reactietijden: enkel correcte antwoorden en niet sneller dan MIN_RT
    def Bruikbaar(s, c):
        return c and s.ReactionTime >= MIN_RT

    rt_congruent = [s.ReactionTime for s, c in zip(trials, correct)
                    if Bruikbaar(s, c) and Kleur(s.Stimulus) == Woord(s.Stimulus)]
    rt_incongruent = [s.ReactionTime for s, c in zip(trials, correct)
                      if Bruikbaar(s, c) and Kleur(s.Stimulus) != Woord(s.Stimulus)]

    rt_con = Gemiddelde(rt_congruent)
    rt_incon = Gemiddelde(rt_incongruent)
    interferentie = rt_incon - rt_con if rt_con >= 0 and rt_incon >= 0 else -1

    # Relatieve interferentie (%): (RT incongruent - RT congruent) / RT congruent x 100
    # corrigeert voor iemand die overal trager reageert
    rel_interferentie = 100.0 * (rt_incon - rt_con) / rt_con if rt_con > 0 and rt_incon >= 0 else -1

    tc.Current.Annotations.SetNumber("aantalTrials", Afronden(n))
    tc.Current.Annotations.SetNumber("aantalGeenAntwoord", Afronden(n_geen_antwoord))
    tc.Current.Annotations.SetNumber("aantalTeSnel", Afronden(n_te_snel))
    # Accuratesse (%): correct / alle woorden van die soort x 100
    # (woorden zonder antwoord tellen als fout)
    con = [c for s, c in zip(trials, correct) if Kleur(s.Stimulus) == Woord(s.Stimulus)]
    incon = [c for s, c in zip(trials, correct) if Kleur(s.Stimulus) != Woord(s.Stimulus)]

    tc.Current.Annotations.SetNumber("accuratesse", Afronden(Percentage(correct)))
    tc.Current.Annotations.SetNumber("accCongruent", Afronden(Percentage(con)))
    tc.Current.Annotations.SetNumber("accIncongruent", Afronden(Percentage(incon)))

    # Fout-interferentie (%-punten): foutpercentage incongruent - foutpercentage congruent
    # (foutpercentage = 100 - accuratesse); > 0 = meer fouten bij incongruente woorden
    acc_con = Percentage(con)
    acc_incon = Percentage(incon)
    fout_interferentie = (100 - acc_incon) - (100 - acc_con) if acc_con >= 0 and acc_incon >= 0 else -999
    tc.Current.Annotations.SetNumber("foutInterferentie", Afronden(fout_interferentie))
    tc.Current.Annotations.SetNumber("rtCongruent", Afronden(rt_con))
    tc.Current.Annotations.SetNumber("rtIncongruent", Afronden(rt_incon))
    tc.Current.Annotations.SetNumber("interferentie", Afronden(interferentie))
    tc.Current.Annotations.SetNumber("relInterferentie", Afronden(rel_interferentie))

    # Inverse Efficiency Score (ms): RT / proportie correct, per conditie
    # (lager = betere prestatie); IES-interferentie = IES incongruent - IES congruent
    def IES(rt, acc):
        return rt / (acc / 100.0) if rt >= 0 and acc > 0 else -1

    ies_con = IES(rt_con, acc_con)
    ies_incon = IES(rt_incon, acc_incon)
    ies_interferentie = ies_incon - ies_con if ies_con >= 0 and ies_incon >= 0 else -999

    tc.Current.Annotations.SetNumber("iesCongruent", Afronden(ies_con))
    tc.Current.Annotations.SetNumber("iesIncongruent", Afronden(ies_incon))
    tc.Current.Annotations.SetNumber("iesInterferentie", Afronden(ies_interferentie))

    return True

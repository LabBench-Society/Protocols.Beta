# Script.py - hulpfuncties voor het SOMIMOVE QST-protocol

DREMPEL_KPA = 5.0   # maximaal PDT-verschil tussen twee opeenvolgende oefenramps


def _pdt(context, ramp_nummer):
    """Geeft de PDT van oefenramp FAMx terug, of None als die ramp
    (nog) niet voltooid is of geen geldige PDT heeft."""
    try:
        resultaat = getattr(context, "FAM%d" % ramp_nummer)
        if not resultaat.Completed:
            return None
        pdt = resultaat.PDT
        if pdt is None or pdt != pdt or pdt <= 0:   # pdt != pdt vangt NaN op
            return None
        return pdt
    except Exception:
        return None


def FamNodig(context, deze_ramp):
    """Voor oefenramp 4 en 5: geeft True als deze ramp nog uitgevoerd moet worden,
    en False als de familiarisatie al stabiel was (PDT-verschil < 5 kPa)."""
    for k in range(3, deze_ramp):
        a = _pdt(context, k - 1)
        b = _pdt(context, k)
        if a is not None and b is not None and abs(b - a) < DREMPEL_KPA:
            return False
    return True


def FamNaRamp(context, ramp_nummer):
    """(Vorige poging, wordt niet meer gebruikt in het protocol.)"""
    return True

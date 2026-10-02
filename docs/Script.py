# Script.py - hulpfuncties voor het SOMIMOVE QST-protocol

DREMPEL_KPA = 5.0   # maximaal PDT-verschil tussen twee opeenvolgende oefenramps


def _pdt(context, ramp_nummer):
    """Geeft de PDT van oefenramp FAMx terug, of None als die ramp niet is uitgevoerd."""
    try:
        return getattr(context, "FAM%d" % ramp_nummer).PDT
    except Exception:
        return None


def FamNaRamp(context, ramp_nummer):
    """Wordt uitgevoerd wanneer oefenramp 3, 4 of 5 voltooid is.
    Schrijft in het logboek van Runner of de familiarisatie stabiel is."""
    a = _pdt(context, ramp_nummer - 1)
    b = _pdt(context, ramp_nummer)

    if a is None or b is None:
        context.Log.Warning("FAMILIARISATIE: PDT van ramp " + str(ramp_nummer - 1) +
                            " of " + str(ramp_nummer) + " ontbreekt, stopregel kan niet berekend worden.")
        return True

    verschil = abs(b - a)
    waarden = ("PDT ramp {0} = {1:.1f} kPa, ramp {2} = {3:.1f} kPa, verschil {4:.1f} kPa"
               ).format(ramp_nummer - 1, a, ramp_nummer, b, verschil)

    if verschil < DREMPEL_KPA:
        context.Log.Warning("FAMILIARISATIE VOLTOOID: " + waarden +
                            " (< 5 kPa). Ga naar de experimentele ramp.")
    elif ramp_nummer >= 5:
        context.Log.Warning("FAMILIARISATIE NIET STABIEL NA 5 RAMPS: " + waarden +
                            " (>= 5 kPa). Maximum bereikt: ga naar de experimentele ramp.")
    else:
        context.Log.Warning("FAMILIARISATIE NOG NIET STABIEL: " + waarden +
                            " (>= 5 kPa). Voer de volgende oefenramp uit.")
    return True

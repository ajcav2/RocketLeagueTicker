def getRank(tier,division):
    if (tier == 0):
        return "unranked"
    elif (tier == 1):
        t = "B1"
    elif (tier == 2):
        t = "B2"
    elif (tier == 3):
        t = "B3"
    elif (tier == 4):
        t = "S1"
    elif (tier == 5):
        t = "S2"
    elif (tier == 6):
        t = "S3"
    elif (tier == 7):
        t = "G1"
    elif (tier == 8):
        t = "G2"
    elif (tier == 9):
        t = "G3"
    elif (tier == 10):
        t = "P1"
    elif (tier == 11):
        t = "P2"
    elif (tier == 12):
        t = "P3"
    elif (tier == 13):
        t = "C1"
    elif (tier == 14):
        t = "C2"
    elif (tier == 15):
        t = "C3"
    elif (tier == 16):
        return " GC "
    else:
        t = "err"

    if (division == 0):
        d = "D1"
    elif (division == 1):
        d = "D2"
    elif (division == 2):
        d = "D3"
    elif (division == 3):
        d = "D4"
    else:
        d = "err"

    return (t + d)

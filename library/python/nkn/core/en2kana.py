import enum


class Symbol(enum.IntEnum):
    AA = enum.auto()
    AA0 = enum.auto()
    AA1 = enum.auto()
    AA2 = enum.auto()
    AE = enum.auto()
    AE0 = enum.auto()
    AE1 = enum.auto()
    AE2 = enum.auto()
    AH = enum.auto()
    AH0 = enum.auto()
    AH1 = enum.auto()
    AH2 = enum.auto()
    AO = enum.auto()
    AO0 = enum.auto()
    AO1 = enum.auto()
    AO2 = enum.auto()
    AW = enum.auto()
    AW0 = enum.auto()
    AW1 = enum.auto()
    AW2 = enum.auto()
    AY = enum.auto()
    AY0 = enum.auto()
    AY1 = enum.auto()
    AY2 = enum.auto()
    B = enum.auto()
    CH = enum.auto()
    D = enum.auto()
    DH = enum.auto()
    EH = enum.auto()
    EH0 = enum.auto()
    EH1 = enum.auto()
    EH2 = enum.auto()
    ER = enum.auto()
    ER0 = enum.auto()
    ER1 = enum.auto()
    ER2 = enum.auto()
    EY = enum.auto()
    EY0 = enum.auto()
    EY1 = enum.auto()
    EY2 = enum.auto()
    F = enum.auto()
    G = enum.auto()
    HH = enum.auto()
    IH = enum.auto()
    IH0 = enum.auto()
    IH1 = enum.auto()
    IH2 = enum.auto()
    IY = enum.auto()
    IY0 = enum.auto()
    IY1 = enum.auto()
    IY2 = enum.auto()
    JH = enum.auto()
    K = enum.auto()
    L = enum.auto()
    M = enum.auto()
    N = enum.auto()
    NG = enum.auto()
    OW = enum.auto()
    OW0 = enum.auto()
    OW1 = enum.auto()
    OW2 = enum.auto()
    OY = enum.auto()
    OY0 = enum.auto()
    OY1 = enum.auto()
    OY2 = enum.auto()
    P = enum.auto()
    R = enum.auto()
    S = enum.auto()
    SH = enum.auto()
    T = enum.auto()
    TH = enum.auto()
    UH = enum.auto()
    UH0 = enum.auto()
    UH1 = enum.auto()
    UH2 = enum.auto()
    UW = enum.auto()
    UW0 = enum.auto()
    UW1 = enum.auto()
    UW2 = enum.auto()
    V = enum.auto()
    W = enum.auto()
    Y = enum.auto()
    Z = enum.auto()
    ZH = enum.auto()


def str2symbol(s: str):
    if s in dir(Symbol):
        return eval('Symbol.%s' % s)
    return None


if __name__ == '__main__':
    for sy in Symbol:
        print(sy, int(sy))
    a = str2symbol('AA')
    print(a, int(a))

    pass
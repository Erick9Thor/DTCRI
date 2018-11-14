import math


# ========================= Entropia =============================================================================
# s = llista num elements per clase : [num elements de clase 1, num elements de clase 2, ...]
def entropia(s):
    tot = 0.0
    entr = 0.0
    for e in s:
        tot = tot + e
    for e in s:
        if (e == 0):
            entr += 0
        else:
            entr = entr - ((e / tot) * math.log(e / tot, 2))

    return entr


# ========================= Gain ================================================================================
# #s = llista num elements per clase : [num elements de clase 1, num elements de clase 2, ...]
# g = entropia de s
# s = numero de mostres (|S|)
# a = llista num elements per clase per cada valor de atribut X
#			: [[elems c1, elems c2,...],[elems c1, elems c2,...],...]
def gain(g, s, a):
    gn = g
    s = float(s)
    # g = entropia(s)

    # countS = 0.0	# Comptar el numero de mostres (|S|)
    # for i in s:
    # countS = countS + i

    countA = []  # Comptar el num de mostres per a cada valor del atribut (|Sv|)
    for e in a:
        countA.append(0)
        for v in e:
            countA[-1] = countA[-1] + v

    if (s != 0.0):
        for i in range(len(a)):
            gn = gn - (countA[i] / s) * entropia(a[i])

    # return float(g)
    return round(gn, 12)


# ========================= Split Info =============================================================================
# #s = llista num elements per clase : [num elements de clase 1, num elements de clase 2, ...]
# s = numero de mostres (|S|)
# a = llista num elements per clase per cada valor de atribut X
#			: [[elems c1, elems c2,...],[elems c1, elems c2,...],...]	
def splitInfo(s, a):
    si = 0.0
    s = float(s)

    # countS = 0.0	# Comptar el numero de mostres (|S|)
    # for i in s:
    # countS = countS + i

    countA = []  # Comptar el num de mostres per a cada valor del atribut (|Sv|)
    for e in a:
        countA.append(0)
        for v in e:
            countA[-1] = countA[-1] + v

    if (s != 0.0):
        for sv in countA:
            if (sv != 0.0):
                si = si + ((sv / s) * math.log(sv / s, 2))

    return -si


# ========================= Gain Ratio =============================================================================
# #s = llista num elements per clase : [num elements de clase 1, num elements de clase 2, ...]
# s = numero de mostres (|S|)
# g = entropia de s
# a = llista num elements per clase per cada valor de atribut X
#			: [[elems c1, elems c2,...],[elems c1, elems c2,...],...]	
def gainRatio(g, s, a):
    g = gain(g, s, a)
    s = splitInfo(s, a)

    if (g == 0 or s == 0):
        return 0.0
    else:
        return g / s

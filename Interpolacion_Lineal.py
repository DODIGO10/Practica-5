
def interpolacion_Lineal(vector):
    Nvector = vector[:]
    Nvector.sort()
    Quartiles = [-1 for _ in range(3)]

    for i in range(3):
        posQn = busqueda_Quartil((i + 1), len(Nvector))
        if(posQn.is_integer()):
            Qi = Nvector[posQn]
        else:
            Qi = Nvector[int(posQn)] + ((int(posQn) - posQn) * (Nvector[int(posQn) + 1] - Nvector[int(posQn)]))

        Quartiles[i] = Qi

    result = IQR(Quartiles[0], Quartiles[2])

    return result

def busqueda_Quartil(pos, lenVector):
    Qn = (pos * (lenVector + 1)) / 4
    return Qn

def IQR(q1,q3):
    IQR = q3 - q1
    return IQR

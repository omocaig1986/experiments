def computePb(l, mi, k):
    ro = float(l) / float(mi)
    if ro == 1.0:
        ro -= 0.00001
    #print("l is %f, k is %d ,ro is %f" % (l, k, ro))
    return ((1-ro)*pow(ro, k))/(1-pow(ro, k+1))


def delay(l, mi, k):
    ro = float(l)/float(mi)
    pb = computePb(l, mi, k)
    k = int(k)

    if ro == 1.0:
        ro -= 0.00001

    total = 0.0
    for i in range(1, k + 1):
        total += i*pow(ro, i)

    return (((1-ro)/(1-pow(ro, k+1)))*total)/(float(l)*(1-pb))


def generatePbArray(lambda_array, k, mi):
    out = []
    for l in lambda_array:
        out.append(computePb(l, mi, k))
    return out


def generateDelayArray(lambda_array, k, mi):
    out = []
    for l in lambda_array:
        out.append(delay(l, mi, k))
    return out

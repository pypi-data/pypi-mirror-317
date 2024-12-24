def algebric_progression_part(a1,d,n):
    return a1+(n-1)*d

def algebric_progression_sum(a1,d,n):
    return n*(a1+(a1+(n-1)*d))/2

def geometric_progression_part(a1,q,n):
    return a1*q**(n-1)

def geometric_progression_sum(a1,q,n):
    if q == 1:
        return a1 * n
    else:
        return a1 * (1 - q**n) / (1 - q)

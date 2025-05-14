def nibutan_u(y, d):
    """f(mid)>=dの境界の元を探す二分探索"""
    def f(x): return # <関数の式> #
    ok,ng=10**13,-1
    while abs(ok-ng) > 1:
        mid = (ok+ng)//2
        if f(mid) >= d:
            ok = mid
        else:
            ng = mid
    return ok

def nibutan_b(y, d):
    """f(mid)<=dの境界の元を探す二分探索"""
    def f(x): return # <関数の式> #
    ok,ng=-1,10**14
    while abs(ok-ng) > 1:
        mid = (ok+ng)//2
        if f(mid) <= d:
            ok = mid
        else:
            ng = mid
    return ok
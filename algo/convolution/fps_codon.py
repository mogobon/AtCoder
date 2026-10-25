# Codon FPS library (998244353)
# Tested with Codon 0.19.0, Linux x86_64, release build.
# Coefficients are in ascending order and normalized to [0, MOD).
# The supplied user prelude is included below. Existing function names are preserved.
# See VERIFICATION.md for per-function coverage and contracts.
# This is a port of this library:
# https://github.com/lif4635/harurun-s-library/blob/main/library_codon/convolution/FPS.py

import sys
II = lambda : int(input())
LI = lambda : [int(a) for a in input().split()]
SI = lambda : input().rstrip()
LLI = lambda n : [[int(a) for a in input().split()] for _ in range(n)]
LSI = lambda n : [input().rstrip() for _ in range(n)]
LI_1 = lambda : [int(a)-1 for a in input().split()]
from bisect import bisect_right, bisect_left
from collections import defaultdict
from heapq import heappop, heappush, heapify
DD = defaultdict
BSL = bisect_left
BSR = bisect_right
inf = 1001001001001001001
mod = 998244353
@extend
class int:
    @llvm
    def __mod__(self, v: int) -> int:
        %ini = srem i64 %self, %v
        %added = add i64 %ini, %v
        %fin = srem i64 %added, %v
        ret i64 %fin
    @llvm
    def __floordiv__(self, v: int) -> int:
        %quot = sdiv i64 %self, %v
        %rem = srem i64 %self, %v
        %sgn = xor i64 %self, %v
        %is_neg = icmp slt i64 %sgn, 0
        %notzero = icmp ne i64 %rem, 0
        %flag = and i1 %is_neg, %notzero
        %adj = select i1 %flag, i64 -1, i64 0
        %fin = add i64 %quot, %adj
        ret i64 %fin
    def bit_length(self) -> int:
        return 64-abs(self).__ctlz__()
    def bit_count(self) -> int:
        return self.__ctpop__()
@extend
class list:
    def pb(self, v: T): self.append(v)
    def eb(self, v: T): self.extend(v)
    def __str__(self): return " ".join(map(str, self))
@extend
class float:
    def __str__(self): return f"{self:.15f}"
def _override_pow():
    _builtin_pow = pow
    def codon_pow(base, exp, mod = None):
        if mod is None: return _builtin_pow(base, exp)
        if exp < 0:
            a, b, x, y = base, mod, 1, 0
            while b:
                q = a // b
                a, b, x, y = b, a - q * b, y, x - q * y
            if abs(a) != 1:
                raise ValueError('base is not invertible for the given modulus')
            base, exp = a * x, - exp
        v = _builtin_pow(base, exp, mod)
        return v + mod if (mod < 0 < v) or (v < 0 < mod) else v
    return codon_pow
pow = _override_pow()

# https://github.com/atcoder/ac-library/blob/master/atcoder/convolution.hpp
MOD = 998244353
IMAG = 911660635
IIMAG = 86583718
INV2 = 499122177
rate2 = [0, 911660635, 509520358, 369330050, 332049552, 983190778, 123842337, 238493703, 975955924, 603855026, 856644456, 131300601, 842657263, 730768835, 942482514, 806263778, 151565301, 510815449, 503497456, 743006876, 741047443, 56250497, 867605899, 0]
irate2 = [0, 86583718, 372528824, 373294451, 645684063, 112220581, 692852209, 155456985, 797128860, 90816748, 860285882, 927414960, 354738543, 109331171, 293255632, 535113200, 308540755, 121186627, 608385704, 438932459, 359477183, 824071951, 103369235, 0]
rate3 = [0, 372528824, 337190230, 454590761, 816400692, 578227951, 180142363, 83780245, 6597683, 70046822, 623238099, 183021267, 402682409, 631680428, 344509872, 689220186, 365017329, 774342554, 729444058, 102986190, 128751033, 395565204, 0]
irate3 = [0, 509520358, 929031873, 170256584, 839780419, 282974284, 395914482, 444904435, 72135471, 638914820, 66769500, 771127074, 985925487, 262319669, 262341272, 625870173, 768022760, 859816005, 914661783, 430819711, 272774365, 530924681, 0]

# https://judge.yosupo.jp/submission/55648
def butterfly(a: list[int]):
    n = len(a)
    h = (n - 1).bit_length()
    le = 0
    while le < h:
        if h - le == 1:
            p = 1 << (h - le - 1)
            rot = 1
            for s in range(1 << le):
                offset = s << (h - le)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p] * rot
                    a[i + offset] = (l + r) % MOD
                    a[i + offset + p] = (l - r) % MOD
                rot *= rate2[(~s & -~s).bit_length()]
                rot %= MOD
            le += 1
        else:
            p = 1 << (h - le - 2)
            rot = 1
            for s in range(1 << le):
                rot2 = rot * rot % MOD
                rot3 = rot2 * rot % MOD
                offset = s << (h - le)
                for i in range(p):
                    a0 = a[i + offset]
                    a1 = a[i + offset + p] * rot
                    a2 = a[i + offset + p * 2] * rot2
                    a3 = a[i + offset + p * 3] * rot3
                    a1na3imag = (a1 - a3) % MOD * IMAG
                    a[i + offset] = (a0 + a2 + a1 + a3) % MOD
                    a[i + offset + p] = (a0 + a2 - a1 - a3) % MOD
                    a[i + offset + p * 2] = (a0 - a2 + a1na3imag) % MOD
                    a[i + offset + p * 3] = (a0 - a2 - a1na3imag) % MOD
                rot *= rate3[(~s & -~s).bit_length()]
                rot %= MOD
            le += 2

def butterfly_inv(a: list[int]):
    n = len(a)
    h = (n - 1).bit_length()
    le = h
    while le:
        if le == 1:
            p = 1 << (h - le)
            irot = 1
            for s in range(1 << (le - 1)):
                offset = s << (h - le + 1)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p]
                    a[i + offset] = (l + r) % MOD
                    a[i + offset + p] = (l - r) * irot % MOD
                irot *= irate2[(~s & -~s).bit_length()]
                irot %= MOD
            le -= 1
        else:
            p = 1 << (h - le)
            irot = 1
            for s in range(1 << (le - 2)):
                irot2 = irot * irot % MOD
                irot3 = irot2 * irot % MOD
                offset = s << (h - le + 2)
                for i in range(p):
                    a0 = a[i + offset]
                    a1 = a[i + offset + p]
                    a2 = a[i + offset + p * 2]
                    a3 = a[i + offset + p * 3]
                    a2na3iimag = (a2 - a3) * IIMAG % MOD
                    a[i + offset] = (a0 + a1 + a2 + a3) % MOD
                    a[i + offset + p] = (a0 - a1 + a2na3iimag) * irot % MOD
                    a[i + offset + p * 2] = (a0 + a1 - a2 - a3) * irot2 % MOD
                    a[i + offset + p * 3] = (a0 - a1 - a2na3iimag) * irot3 % MOD
                irot *= irate3[(~s & -~s).bit_length()]
                irot %= MOD
            le -= 2

def intt(a):
    if len(a) <= 1: return
    butterfly_inv(a)
    iv = pow(len(a), MOD - 2, MOD)
    for i, x in enumerate(a): a[i] = x * iv % MOD

def multiply(s: list[int], t: list[int]):
    n = len(s)
    m = len(t)
    if n == 0 or m == 0: return []
    if min(n, m) <= 60:
        a = [0] * (n + m - 1)
        for i in range(n):
            for j in range(m):
                a[i + j] = (a[i + j] + s[i] * t[j]) % MOD
        return a
    a = s.copy()
    b = t.copy()
    z = 1 << (n + m - 2).bit_length()
    a += [0] * (z - n)
    b += [0] * (z - m)
    butterfly(a)
    butterfly(b)
    for i in range(z):
        a[i] *= b[i]
        a[i] %= MOD
    butterfly_inv(a)
    a = a[:n + m - 1]
    iz = pow(z, MOD - 2, MOD)
    return [v * iz % MOD for v in a]

def pow2(s: list[int]):
    n = len(s)
    if n == 0: return []
    l = (n << 1) - 1
    if n <= 60:
        a = [0] * l
        for i, x in enumerate(s):
            for j, y in enumerate(s):
                a[i + j] = (a[i + j] + x * y) % MOD
        return [x % MOD for x in a]
    z = 1 << (l - 1).bit_length()
    a = s + [0] * (z - n)
    butterfly(a)
    for i, x in enumerate(a): a[i] = x * x % MOD
    butterfly_inv(a)
    a[l:] = []
    iz = pow(z, MOD - 2, MOD)
    return [x * iz % MOD for x in a]

def shrink(a: list[int]):
    while a and not a[-1]: a.pop()

def fps_add(a: list[int], b: list[int]):
    if len(a) < len(b):
        res = b.copy()
        for i, x in enumerate(a):
            res[i] += x
    else:
        res = a.copy()
        for i, x in enumerate(b):
            res[i] += x
    return [x-MOD if MOD <= x else x for x in res]

def fps_sub(a: list[int], b: list[int]):
    if len(a) < len(b):
        res = b.copy()
        for i, x in enumerate(a):
            res[i] -= x
        return [MOD-x if 0 < x else -x for x in res]
    else:
        res = a.copy()
        for i, x in enumerate(b):
            res[i] -= x
        return [x if 0 <= x else x+MOD for x in res]

def fps_neg(a: list[int]):
    return [MOD-x if x else 0 for x in a]

def fps_div(a: list[int], b: list[int]) -> list[int]:
    g = b.copy()
    shrink(g)
    if not g: raise ValueError("division by zero polynomial")
    f = a.copy()
    shrink(f)
    if len(f) < len(g): return []
    n = len(f) - len(g) + 1
    if len(g) > 64:
        return multiply(f[::-1][:n], fps_inv(g[::-1], n))[:n][::-1]
    coef = pow(g[-1], MOD - 2, MOD)
    res = [0] * n
    for i in range(n - 1, -1, -1):
        x = f[i + len(g) - 1] * coef % MOD
        res[i] = x
        for j in range(len(g)):
            f[i + j] = (f[i + j] - x * g[j]) % MOD
    return res

def fps_mod(a: list[int], b: list[int]) -> list[int]:
    res = fps_sub(a, multiply(fps_div(a, b),  b))
    while res and not res[-1]: res.pop()
    return res

def fps_divmod(a: list[int], b: list[int]):
    q = fps_div(a, b)
    r = fps_sub(a, multiply(q, b))
    while r and not r[-1]: r.pop()
    return q, r

def fps_eval(a: list[int], x: int) -> int:
    r = 0
    x %= MOD
    for i in range(len(a) - 1, -1, -1):
        r = (r * x + a[i]) % MOD
    return r

def fps_inv(a: list[int], deg: int=-1):
    # assert(self[0] != 0)
    if deg == -1: deg = len(a)
    if deg == 0: return []
    res = [0] * deg
    res[0] = pow(a[0], MOD - 2, MOD)
    d = 1
    iv = INV2
    while d < deg:
        d2 = d << 1
        f = [0] * d2
        fl = min(len(a), d2)
        f[:fl] = a[:fl]
        g = [0] * d2
        g[:d] = res[:d]
        butterfly(g)
        butterfly(f)
        for i in range(d2): f[i] = f[i] * g[i] % MOD
        butterfly_inv(f)
        f[:d] = [0] * d
        for i in range(d, d2): f[i] = f[i] * iv % MOD
        butterfly(f)
        for i in range(d2): f[i] = f[i] * g[i] % MOD
        butterfly_inv(f)
        for i in range(d, min(d2, deg)): res[i] = (MOD-f[i]) * iv % MOD
        d <<= 1
        iv = iv * INV2 % MOD
    return res

def fps_pow(a: list[int], k: int, deg=-1) -> list[int]:
    n = len(a)
    if deg == -1: deg = n
    if k == 0:
        if not deg: return []
        res = [0] * deg
        res[0] = 1
        return res
    if deg == 0: return []
    for i, x in enumerate(a):
        if i and k > (deg - 1) // i: return [0] * deg
        if x:
            iz = pow(x, MOD - 2, MOD)
            res = [x * iz % MOD for x in a[i:]]
            res = fps_log(res, deg)
            res = [x * (k % MOD) % MOD for x in res]
            res = fps_exp(res, deg)
            coef = pow(x, k, MOD)
            res = [0] * (i * k) + [x * coef % MOD for x in res]
            if len(res) < deg:
                return res + [0] * (deg - len(res))
            return res[:deg]
        if k > (deg - 1) // (i + 1): break
    return [0] * deg

def fps_exp(a: list[int], deg: int=-1):
    # assert a[0] == 0
    if deg == -1: deg = len(a)
    if deg == 0: return []
    inv = [0, 1]
    def inplace_integral(f: list[int]) -> list[int]:
        n = len(f)
        while len(inv) <= n:
            j, k = divmod(MOD, len(inv))
            inv.append((-inv[k] * j) % MOD)
        return [0] + [x * inv[i + 1] % MOD for i, x in enumerate(f)]

    b = [1, (a[1] if 1 < len(a) else 0)]
    c = [1]
    z1: list[int] = []
    z2 = [1, 1]
    m = 2
    while m < deg:
        y = b + [0] * m
        butterfly(y)
        z1 = z2
        z = [y[i] * p % MOD for i, p in enumerate(z1)]
        intt(z)
        z[:m >> 1] = [0] * (m >> 1)
        butterfly(z)
        for i, p in enumerate(z1): z[i] = z[i] * (-p) % MOD
        intt(z)
        c[m >> 1:] = z[m >> 1:]
        z2 = c + [0] * m
        butterfly(z2)
        tmp = min(len(a), m)
        x = a[:tmp] + [0] * (m - tmp)
        x = fps_diff(x)
        x.append(0)
        butterfly(x)
        for i, p in enumerate(x): x[i] = y[i] * p % MOD
        intt(x)
        for i, p in enumerate(b):
            if not i: continue
            x[i - 1] -= p * i % MOD
        x += [0] * m
        for i in range(m - 1): x[m + i], x[i] = x[i], 0
        butterfly(x)
        for i, p in enumerate(z2): x[i] = x[i] * p % MOD
        intt(x)
        x.pop()
        x = inplace_integral(x)
        x[:m] = [0] * m
        for i in range(m, min(len(a), m << 1)): x[i] += a[i]
        butterfly(x)
        for i, p in enumerate(y): x[i] = x[i] * p % MOD
        intt(x)
        b[m:] = x[m:]
        m <<= 1
    return b[:deg]

def fps_log(a: list[int], deg=-1) -> list[int]:
    # assert(a[0] == 1)
    if deg == -1: deg = len(a)
    if deg == 0: return []
    return fps_integral(multiply(fps_diff(a), fps_inv(a, deg))[:deg - 1])

def fps_integral(a: list[int]):
    n = len(a)
    res = [0] * (n + 1)
    if n: res[1] = 1
    for i in range(2, n + 1):
        j, k = divmod(MOD, i)
        res[i] = (-res[k] * j) % MOD
    for i, x in enumerate(a): res[i + 1] = res[i + 1] * x % MOD
    return res

def fps_diff(a: list[int]):
    return [i * x % MOD for i, x in enumerate(a) if i]

def LinearRecurrence(n: int, p: list[int], q: list[int]):
    """
    [x^n]P(x)/Q(x)
    """
    # assert len(p) < len(q)
    shrink(q)
    while n:
        q2 = q[:]
        for i in range(1,len(q2),2): q2[i] = (-q2[i])%MOD
        s = multiply(p,q2)
        t = multiply(q,q2)
        p = s[n & 1::2]
        q = t[::2]
        n >>= 1
    return (p[0] if p else 0) * pow(q[0], -1, MOD) % MOD

def fps_compsite(f: list[int], g: list[int]):
    """
    g(f(x)) mod x^n
    """
    # assert len(f) == len(g)
    def trans_multiply(s, t):
        n = len(s)
        m = len(t)
        l = 1 << (max(n, m) - 1).bit_length()
        a = s + [0] * (l - n)
        b = t + [0] * (l - m)
        a = [a[0]] + [a[l - i] for i in range(1, l)]
        butterfly(a)
        butterfly(b)
        iz = pow(l, MOD-2, MOD)
        for i, x in enumerate(b):
            a[i] = a[i] * x % MOD * iz % MOD
        butterfly_inv(a)
        a = [a[0]] + [a[l - i] for i in range(1, l)]
        return a[:n - m + 1]
    
    n = len(f)
    if n == 0: return []
    l = 1 << (n - 1).bit_length()
    a = [(-x) % MOD for x in f] + [0] * (2 * l - n)
    b = g + [0] * (l - n) 
    
    def _inner(q, n, k):
        if n == 1:
            p = [0] * (2 * k)
            p[0::2] = b[::-1]
            return p
        siz = 2 * n * k
        r = [MOD - x if i & 1 else x for i,x in enumerate(q)]
        qq = multiply(q, r)
        qq.append(0)
        for i in range(0, siz, 2):
            qq[siz+i] = (qq[siz+i] + 2 * q[i]) % MOD
        nq = [0] * siz
        for j in range(2 * k):
            for i in range(n >> 1):
                nq[n * j + i] = qq[2 * n * j + 2 * i]
        np = _inner(nq, n >> 1, k << 1)
        
        pq = [0] * (2 * siz)
        for j in range(2 * k):
            for i in range(n >> 1):
                pq[2 * n * j + 2 * i + 1] = np[n * j + i]
        
        p = [pq[siz + i] for i in range(siz)]
        pq.pop()
        x = trans_multiply(pq, r)
        p = [(p[i] + x[i]) % MOD for i in range(siz)]
        return p
    
    p = _inner(a, l, 1)
    p = p[l-1::-1]
    return p[:n]

def fps_compsitional_inv(calc, deg):
    """
    input
    calc(g, d) = f(g(x)) mod x^d を計算する
    fps_compsite よりも良い計算量のものが存在するならば書く
    
    output
    g(x) mod x^deg s.t. f(g(x)) = x 
    """
    if deg == 0: return []
    if deg == 1: return [0]
    c = (deg - 1).bit_length()
    g = calc([0, 1], 2)
    g[1] = pow(g[1], -1, MOD)
    d = 2
    while d < deg:
        d <<= 1
        fg = calc(g, d + 1)
        fdg = multiply(fps_diff(fg), fps_inv(fps_diff(g), d))
        fdg[d:] = []
        fg[1] = (fg[1] - 1) % MOD
        g = fps_sub(g, multiply(fg, fps_inv(fdg)))
        g[d:] = []
    g[deg:] = []
    return g

INVMOD = [1,1]
def SubsetSum(d: list[int]) -> list[int]:
    """
    product: ( 1 + x^i ) ^ d[i]
    
    d[w] = 重さ w が d[w] 種類 1 個ずつある
    r[w] = 重さが w になるような選び方
    """
    n = len(d)
    for i in range(len(INVMOD), n):
        INVMOD.append(-INVMOD[MOD%i] * (MOD//i) % MOD)
    res = [0] * n
    sgn = [-1, 1]
    for i in range(1, n):
        if d[i]:
            tmp = (d[i] % MOD) * i % MOD
            for j in range(i, n, i):
                res[j] = (res[j] + tmp * INVMOD[j] * sgn[(j//i)&1]) % MOD
    res = fps_exp(res, n)
    return res

def MultisetSum(d: list[int]) -> list[int]:
    """
    product: ( 1 / ( 1 - x^i ) ) ^ d[i]
    
    d[w] = 重さ w が d[w] 種類 inf 個ずつある
    r[w] = 重さが w になるような選び方
    """
    n = len(d)
    for i in range(len(INVMOD), n):
        INVMOD.append(-INVMOD[MOD%i] * (MOD//i) % MOD)
    res = [0] * n
    for i in range(1, n):
        if d[i]:
            tmp = (d[i] % MOD) * i % MOD
            for j in range(i, n, i):
                res[j] = (res[j] + tmp * INVMOD[j]) % MOD
    res = fps_exp(res, n)
    return res

fac = [1, 1]
finv = [1, 1]
def tayler_shift(a: list[int], c: int) -> list[int]:
    global fac, finv
    n = len(a)
    if n == 0: return []
    c %= MOD
    l = len(fac)
    fac += [0] * (n - l)
    finv += [0] * (n - l)
    for i in range(l, n):
        fac[i] = fac[i-1] * i % MOD
    finv[n-1] = pow(fac[n-1], MOD-2, MOD)
    for i in reversed(range(l, n-1)):
        finv[i] = finv[i+1] * (i+1) % MOD
    
    r = [x * fac[i] % MOD for i, x in enumerate(a)]
    b = [0] * n
    b[0] = 1
    for i in range(1, n):
        b[i] = b[i-1] * c % MOD * finv[i] % MOD * fac[i-1] % MOD
    r.reverse()
    res = multiply(r, b)[:n]
    return [x * finv[i] % MOD for i, x in enumerate(res[::-1])]

def ntt2d(a: list[list[int]]):
    n, m = len(a), len(a[0])
    h = (n - 1).bit_length()
    le = 0
    while le < h:
        if h - le == 1:
            p = 1 << (h - le - 1)
            rot = 1
            for s in range(1 << le):
                offset = s << (h - le)
                for i in range(p):
                    for j in range(m):
                        l = a[i + offset][j]
                        r = a[i + offset + p][j] * rot
                        a[i + offset][j] = (l + r) % MOD
                        a[i + offset + p][j] = (l - r) % MOD
                rot *= rate2[(~s & -~s).bit_length()]
                rot %= MOD
            le += 1
        else:
            p = 1 << (h - le - 2)
            rot = 1
            for s in range(1 << le):
                rot2 = rot * rot % MOD
                rot3 = rot2 * rot % MOD
                offset = s << (h - le)
                for i in range(p):
                    for j in range(m):
                        a0 = a[i + offset][j]
                        a1 = a[i + offset + p][j] * rot
                        a2 = a[i + offset + p * 2][j] * rot2
                        a3 = a[i + offset + p * 3][j] * rot3
                        a1na3imag = (a1 - a3) % MOD * IMAG
                        a[i + offset][j] = (a0 + a2 + a1 + a3) % MOD
                        a[i + offset + p][j] = (a0 + a2 - a1 - a3) % MOD
                        a[i + offset + p * 2][j] = (a0 - a2 + a1na3imag) % MOD
                        a[i + offset + p * 3][j] = (a0 - a2 - a1na3imag) % MOD
                rot *= rate3[(~s & -~s).bit_length()]
                rot %= MOD
            le += 2
    n, m = m, n
    h = (n - 1).bit_length()
    le = 0
    while le < h:
        if h - le == 1:
            p = 1 << (h - le - 1)
            rot = 1
            for s in range(1 << le):
                offset = s << (h - le)
                for i in range(p):
                    for j in range(m):
                        l = a[j][i + offset]
                        r = a[j][i + offset + p] * rot
                        a[j][i + offset] = (l + r) % MOD
                        a[j][i + offset + p] = (l - r) % MOD
                rot *= rate2[(~s & -~s).bit_length()]
                rot %= MOD
            le += 1
        else:
            p = 1 << (h - le - 2)
            rot = 1
            for s in range(1 << le):
                rot2 = rot * rot % MOD
                rot3 = rot2 * rot % MOD
                offset = s << (h - le)
                for i in range(p):
                    for j in range(m):
                        a0 = a[j][i + offset]
                        a1 = a[j][i + offset + p] * rot
                        a2 = a[j][i + offset + p * 2] * rot2
                        a3 = a[j][i + offset + p * 3] * rot3
                        a1na3imag = (a1 - a3) % MOD * IMAG
                        a[j][i + offset] = (a0 + a2 + a1 + a3) % MOD
                        a[j][i + offset + p] = (a0 + a2 - a1 - a3) % MOD
                        a[j][i + offset + p * 2] = (a0 - a2 + a1na3imag) % MOD
                        a[j][i + offset + p * 3] = (a0 - a2 - a1na3imag) % MOD
                rot *= rate3[(~s & -~s).bit_length()]
                rot %= MOD
            le += 2

def intt2d(a : list[list[int]]):
    n, m = len(a), len(a[0])
    h = (n - 1).bit_length()
    le = h
    while le:
        if le == 1:
            p = 1 << (h - le)
            irot = 1
            for s in range(1 << (le - 1)):
                offset = s << (h - le + 1)
                for i in range(p):
                    for j in range(m):
                        l = a[i + offset][j]
                        r = a[i + offset + p][j]
                        a[i + offset][j] = (l + r) % MOD
                        a[i + offset + p][j] = (l - r) * irot % MOD
                irot *= irate2[(~s & -~s).bit_length()]
                irot %= MOD
            le -= 1
        else:
            p = 1 << (h - le)
            irot = 1
            for s in range(1 << (le - 2)):
                irot2 = irot * irot % MOD
                irot3 = irot2 * irot % MOD
                offset = s << (h - le + 2)
                for i in range(p):
                    for j in range(m):
                        a0 = a[i + offset][j]
                        a1 = a[i + offset + p][j]
                        a2 = a[i + offset + p * 2][j]
                        a3 = a[i + offset + p * 3][j]
                        a2na3iimag = (a2 - a3) * IIMAG % MOD
                        a[i + offset][j] = (a0 + a1 + a2 + a3) % MOD
                        a[i + offset + p][j] = (a0 - a1 + a2na3iimag) * irot % MOD
                        a[i + offset + p * 2][j] = (a0 + a1 - a2 - a3) * irot2 % MOD
                        a[i + offset + p * 3][j] = (a0 - a1 - a2na3iimag) * irot3 % MOD
                irot *= irate3[(~s & -~s).bit_length()]
                irot %= MOD
            le -= 2
    n, m = m, n
    h = (n - 1).bit_length()
    le = h
    while le:
        if le == 1:
            p = 1 << (h - le)
            irot = 1
            for s in range(1 << (le - 1)):
                offset = s << (h - le + 1)
                for i in range(p):
                    for j in range(m):
                        l = a[j][i + offset]
                        r = a[j][i + offset + p]
                        a[j][i + offset] = (l + r) % MOD
                        a[j][i + offset + p] = (l - r) * irot % MOD
                irot *= irate2[(~s & -~s).bit_length()]
                irot %= MOD
            le -= 1
        else:
            p = 1 << (h - le)
            irot = 1
            for s in range(1 << (le - 2)):
                irot2 = irot * irot % MOD
                irot3 = irot2 * irot % MOD
                offset = s << (h - le + 2)
                for i in range(p):
                    for j in range(m):
                        a0 = a[j][i + offset]
                        a1 = a[j][i + offset + p]
                        a2 = a[j][i + offset + p * 2]
                        a3 = a[j][i + offset + p * 3]
                        a2na3iimag = (a2 - a3) * IIMAG % MOD
                        a[j][i + offset] = (a0 + a1 + a2 + a3) % MOD
                        a[j][i + offset + p] = (a0 - a1 + a2na3iimag) * irot % MOD
                        a[j][i + offset + p * 2] = (a0 + a1 - a2 - a3) * irot2 % MOD
                        a[j][i + offset + p * 3] = (a0 - a1 - a2na3iimag) * irot3 % MOD
                irot *= irate3[(~s & -~s).bit_length()]
                irot %= MOD
            le -= 2
    iv = pow(n * m, MOD - 2, MOD)
    for i in range(m):
        for j in range(n):
            a[i][j] = a[i][j] * iv % MOD

def multiply2d(s: list[list[int]], t: list[list[int]]):
    hs, ws = len(s), len(s[0])
    ht, wt = len(t), len(t[0])
    h = 1 << (hs + ht - 2).bit_length()
    w = 1 << (ws + wt - 2).bit_length()
    a = [row.copy() for row in s]
    b = [row.copy() for row in t]
    for i in range(hs):
        a[i] += [0] * (w - ws)
    for i in range(ht):
        b[i] += [0] * (w - wt)
    a += [[0]*w for i in range(h - hs)]
    b += [[0]*w for i in range(h - ht)]
    ntt2d(a)
    ntt2d(b)
    for i in range(h):
        for j in range(w):
            a[i][j] *= b[i][j]
            a[i][j] %= MOD
    intt2d(a)
    a = a[:hs + ht - 1]
    for i in range(hs + ht - 1):
        a[i][ws + wt - 1:] = []
    return a

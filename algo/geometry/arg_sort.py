# 偏角ソート（正のx軸を始点に反時計回り）
# ABC481 E: https://atcoder.jp/contests/abc481/tasks/abc481_e
# 下部は同問題の使用例。pの各点は原点ではなく、
# 異なる2点と原点が一直線上に並ばないことを前提とする。

import sys


def quick_sort(a, less):
    """less(a, b)がTrueならaを先に置く。aを直接変更し、Noneを返す。
    lessは狭義の順序（自分自身との比較はFalse）を満たすこと。
    平均O(N log N)、最悪O(N^2)。追加領域O(log N)。不安定ソート。
    """
    if len(a) < 2:
        return

    stack = [(0, len(a) - 1)]

    while stack:
        l, r = stack.pop()

        while l < r:
            pivot = a[(l + r) // 2]
            i, j = l, r

            while i <= j:
                while less(a[i], pivot):
                    i += 1
                while less(pivot, a[j]):
                    j -= 1

                if i <= j:
                    a[i], a[j] = a[j], a[i]
                    i += 1
                    j -= 1

            # 大きい側を保留し、小さい側を先に処理する
            if j - l < r - i:
                if i < r:
                    stack.append((i, r))
                r = j
            else:
                if l < j:
                    stack.append((l, j))
                l = i


def half(p):
    x, y = p
    return 0 if y > 0 or (y == 0 and x > 0) else 1


def angle_less(a, b):
    ha = half(a)
    hb = half(b)
    if ha != hb:
        return ha < hb
    return a[0] * b[1] - a[1] * b[0] > 0


def solve(p):
    quick_sort(p, angle_less)
    n = len(p)
    p += p  # 360度をまたぐ区間も扱う

    ans = 0
    r = 0

    for l in range(n):
        r = max(r, l + 1)
        x, y = p[l]

        while r < l + n:
            nx, ny = p[r]
            if x * ny - y * nx <= 0:
                break
            r += 1

        ans = max(ans, r - l)

    return ans


input = sys.stdin.buffer.readline
t = int(input())

for _ in range(t):
    n = int(input())
    p = [tuple(map(int, input().split())) for _ in range(n)]
    ans = solve(p)
    print(ans)

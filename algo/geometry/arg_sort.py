# https://github.com/mogobon/AtCoder/blob/main/algo/geometry/arg_sort.py
# Verify: https://atcoder.jp/contests/abc481/submissions/80396791
# 偏角ソート（正のx軸を始点に反時計回り）
# ABC481 E: https://atcoder.jp/contests/abc481/tasks/abc481_e

import sys


def quick_sort(lst, comparision, left=0, right=-1):
    if len(lst) == 0:
        return
    if right == -1:
        right = len(lst) - 1

    que = [(left, right)]
    while que:
        i, j = que.pop()
        left, right = i, j
        dpivot = lst[(i + j) // 2]

        while i <= j:
            while comparision(lst[i], dpivot) < 0:
                i += 1
            while comparision(dpivot, lst[j]) < 0:
                j -= 1
            if i <= j:
                lst[i], lst[j] = lst[j], lst[i]
                i += 1
                j -= 1

        if left < j:
            que.append((left, j))
        if i < right:
            que.append((i, right))


def half(p):
    x, y = p
    return 0 if y > 0 or (y == 0 and x > 0) else 1


def angle_less(a, b):
    ha = half(a)
    hb = half(b)

    if ha != hb:
        return -1 if ha < hb else 1

    cross = a[0] * b[1] - a[1] * b[0]

    if cross > 0:
        return -1
    if cross < 0:
        return 1
    return 0


def solve(p):
    quick_sort(p, angle_less)
    n = len(p)
    p += p

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

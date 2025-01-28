# RLE暗号文を出力するだけ
# s =input()
# n = len(s)
# i = 0; j = 0
# while i < n:
#     cnt = 0
#     while j < n and s[i] == s[j]:
#         cnt += 1
#         j += 1
#     print(s[i]+str(cnt), end="")
#     i = j

def encode(s):
    n = len(s)
    i = 0
    j = 0
    code = []
    while i < n:
        cnt = 0
        while j < n and s[i] == s[j]:
            j += 1
            cnt += 1
        code.append([s[i],cnt])
        i = j
    return code

def decode(c):
    n = len(c)
    s = []
    for i in range(n):
        char = c[i][0]; rep = c[i][1]
        for _ in range(rep):
            s.append(char)
    return s

n,k=map(int,input().split())
s = input()
c = encode(s)
# 結果はリストで返ってくる
# print(*c) 
# for i in range(len(c)):
#     char = c[i][0]
#     num = str(c[i][1])
#     print(char+num,end="")
# print()

print(*c)
# char+num をまとめて処理
print("".join(f"{char}{num}" for char, num in c))

cnt = 0
# for i in range(len(c)):
#     char = c[i][0]
#     if char == '1':
#         cnt += 1
#     if cnt == k:
#         c[i],c[i-1] = c[i-1],c[i]
#         break
# enumerate を使って上を書き換え
for i,(char,_) in enumerate(c):
    if char == '1': 
        cnt += 1
    if cnt == k:
        c[i],c[i-1] = c[i-1],c[i]
        break

# print(*c)

s = decode(c)
# for s in s: print(s,end="")
# print()

print(*c)
# char+num をまとめて処理
print("".join(f"{char}{num}" for char, num in c))

# デコードした文字列を出力
print("".join(decode(c)))


## for1重ループに改善版 ###

# n,k = map(int,input().split())
# s = input()

# def encode(s):
#     c = []
#     for ss in s:
#         if c and c[-1][0] == ss: c[-1][1] += 1
#         else: c.append([ss,1])
#     return c

# def decode(c):
#     s = []
#     for char,num in c:
#         for _ in range(num): s.append(char)
#     return s

# c = encode(s)
# cnt = 0
# for i,(char,num) in enumerate(c):
#     if char == '1':
#         cnt += 1
#     if cnt == k:
#         c[i],c[i-1] = c[i-1],c[i]

# s = decode(c)

# print("".join(s))





print("".join(decode(c)))

print("".join(f"{char}{num}" for char, num in c))
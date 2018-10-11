# Codeforces 999A
def getints():
    return [int(tok) for tok in input().split()]


n, k = getints()
a = getints()
l = -1
r = -2
for i, x in enumerate(a):
    if x > k:
        if l < 0:
            l = i
        r = i
print(n - (r - l + 1))
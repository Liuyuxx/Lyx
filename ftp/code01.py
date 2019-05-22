list01 = [1,2,3,3,4]
myset = set(list01)
print(myset)
for i in myset:
    print("the %d has found %d"%(i,list01.count(i)))

from collections import Counter
print(Counter(list01))

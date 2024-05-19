# [A - 旅人](https://atcoder.jp/contests/joi2010ho/tasks/joi2010ho_a)


* 最初の提出結果と、そのコード

|![image](https://github.com/jamad/jamad.github.io/assets/949913/f3d30e2f-c41c-4b05-bff3-bc3317215ead)|
|-|
 

```
n,m=map(int,input().split())
DIST=[0]
for i in range(n-1):
  d=int(input())
  DIST.append(DIST[-1]+d)

#DIST.pop(0)

#print(DIST)
#print(MOVE)

MOVE=[]

k=0
ans=0
for i in range(m):
  move=int(input())
  dest=k+move
  ans+=abs(DIST[dest]-DIST[k])
  k=dest

print(ans)
  
```

* 二回目

|![image](https://github.com/jamad/jamad.github.io/assets/949913/713534e6-78a1-4c05-a128-361c15ea0597)|
|-|


```
n,m=map(int,input().split())
DIST=[0]
for i in range(n-1):
  d=int(input())
  DIST.append(DIST[-1]+d)

current=previous=0
ans=0
for i in range(m):
  current=previous+int(input())
  ans+=abs(DIST[current]-DIST[previous])
  previous=current
print(ans%(10**5))
```

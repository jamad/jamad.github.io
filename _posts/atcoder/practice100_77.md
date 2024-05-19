＃ [A - 旅人](https://atcoder.jp/contests/joi2010ho/tasks/joi2010ho_a)


* 最初の提出結果と、そのコード 

![image](https://github.com/jamad/jamad.github.io/assets/949913/f3d30e2f-c41c-4b05-bff3-bc3317215ead)

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


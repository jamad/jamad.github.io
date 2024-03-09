<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

* [このページの edit](https://github.com/jamad/jamad.github.io/tree/master/_posts)

# 二重ループのbreakは初めて知った
* 競プロでよく使うけど空で書けないフレーズ `https://qiita.com/do_an/items/e5a202cac4fc69fe849d`

# 自分のvisualgo を codepen とかで作れるのではないかと思っている
* `https://visualgo.net/`

# segment tree
*　`\practicePython\atcoder\segment_tree.py` 
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/cb543a80-693b-4a52-b6dc-b87ed818f03b)
* `https://algo-logic.info/segment-tree/`より。概念を掴めた。 ![image](https://github.com/jamad/jamad.github.io/assets/949913/16e4304b-ff75-45d6-97fd-42d06255fc62)


# 間違えたことがあるもの
*  `(1,-1)[x]`　の9文字を短く表現する方法。
    *  結局`1-2*v`の5文字がベスト。 `-1**x` の5文字だと常に `-1` を返してしまうので間違い。正しい表記は7文字 `(-1)**x`で長い。

# メモ
* グラフで木の高さの最小値（木の半径と呼ばれる）は　およそ木の直径の半分 下記のコードでいうところの`(GetDiam(G)+1)//2`
   * 木の直径は任意の点から最も遠い点をゲットし、そこを起点として再び最も遠い点までの距離
      * `https://algo-method.com/submissions/1276401`
* nCr のベストな説明
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/9e4b9ee6-f28c-49fd-8c35-14d005a44441)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/f2343670-f9d8-4d1d-81da-473a29ee31e3)


## (atcoder では使えなかったもの、、、)
* `import gmpy2`   example : [xのn乗根 root(x,n)](https://www.codewars.com/kata/reviews/572af8eb9e69bf1329000036/groups/65b02c5766e84700012b952f)  , [is_prime(x)](https://www.codewars.com/kata/reviews/6117f77c0c70a70001ae2313/groups/611824f1497d5e0001725ef1) , [next_prime(x)](https://www.codewars.com/kata/reviews/6117f77c0c70a70001ae2313/groups/61f8e2aa398ead00015bb9e2)

# available lib at codewars 

* `import math` example :  [lcm(a,b)](https://atcoder.jp/contests/abc341/submissions/50431482) , factorial(x)
* `import collections` example :  Counter(A)
* `import numpy` example : [.base_reprで5進法に変換](https://atcoder.jp/contests/abc336/submissions/49343419) , [np.zerosにレンジで値を加える](https://atcoder.jp/contests/abc338/submissions/49767251) よりも [imos法の方が速かったので注意](https://atcoder.jp/contests/abc338/submissions/49771980)
* `import re` example : [`re.sub('c|[a-z]?C[a-z]?','',x)`](https://www.codewars.com/kata/reviews/62b769aaef340600014f7f3a/groups/64a69b6dfbed130001b5bae1)
* `import haslib` example : [`sha256(x.encode()).hexdigest()`](https://www.codewars.com/kata/reviews/587fb72807076d73c200068a/groups/588752311fe4490415000261)
* `import datetime` exmaple : [`(date(2024,1,1)+timedelta(x)).strftime("%B, %-d")`](https://www.codewars.com/kata/reviews/602d5f49265b840001f3ca4d/groups/6030b82e99b32b0001557fea)
* `import itertools` example : [zip_longest with fillvalue=''](https://www.codewars.com/kata/reviews/6274c394871b6200017aefd2/groups/6274dd3af229f5000178ed96) , [groupby](https://www.codewars.com/kata/reviews/63617a951a7c220001edfeba/groups/63b612398bc05e00011695a0)


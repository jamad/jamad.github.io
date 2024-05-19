<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

* [このページの edit](https://github.com/jamad/jamad.github.io/tree/master/_posts)

# bitDP
* 

## 二重ループをbreakできるtipsは初めて知った　確かにbreakしなかった場合は  else:continue を通るよなあ 
* 競プロでよく使うけど空で書けないフレーズ `https://qiita.com/do_an/items/e5a202cac4fc69fe849d`
```
for i in range(10):
    for j in range(10):
        for k in range(10):
            if 25< i*j*k:
                ng=(i,j,k)
                break
            ok=(i,j,k)

        else:continue
        break

    else:continue
    break

print(ok) # (1, 3, 8)
print(ng) # (1, 3, 9)
```

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



---

<h2 id="全探索：全列挙"><a href="#全探索：全列挙" class="headerlink" title="全探索：全列挙"></a>全探索：全列挙</h2><ol>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/08/itp1-7b/">ITP1 7B 組み合わせの数</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/09/abc106b/">ABC106B 105</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/10/abc122b/">ABC122B ATCoder</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/15/paken2019-3c/">パ研杯2019 3C カラオケ</a></p></li>
</ol>
<h2 id="全探索：工夫して通り数を減らす全列挙"><a href="#全探索：工夫して通り数を減らす全列挙" class="headerlink" title="全探索：工夫して通り数を減らす全列挙"></a>全探索：工夫して通り数を減らす全列挙</h2><ol start="5">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/11/abc095c/">ABC095C Half and Half</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/16/sumitrust2019d/">三井住友信託銀行プログラミングコンテスト2019D Lucky PIN</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/07/joi2007hoc/">JOI2007本戦C 最古の遺跡</a></p></li>
    <li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/08/s8pc6b/">Square869120Countest#6B - AtCoder Market</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/10/joi2008yod/">JOI2008予選4 星座探し</a></p></li>
</ol>
<h2 id="全探索：ビット全探索"><a href="#全探索：ビット全探索" class="headerlink" title="全探索：ビット全探索"></a>全探索：ビット全探索</h2><ol start="10">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/12/alds1-5a/">ALDS1 5A 総当たり</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/13/abc128c/">ABC128C Switches</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/14/abc002d/">ABC002D 派閥</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/19/joi2008yoe/">JOI2008予選5 おせんべい</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/29/s8pc4b/">Square869120Contest#4B Buildings are Colorful!</a></p></li>
</ol>
<h2 id="全探索：順列全探索"><a href="#全探索：順列全探索" class="headerlink" title="全探索：順列全探索"></a>全探索：順列全探索</h2><ol start="15">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/09/abc145c/">ABC145C Average Length</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/28/abc150c/">ABC150C Count Order</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/09/alds1-13a/">ALDS1 13A 8クイーン問題</a></p></li>
</ol>
<h2 id="二分探索"><a href="#二分探索" class="headerlink" title="二分探索"></a>二分探索</h2><ol start="18">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/17/alds1-4b/">ALDS1 4B 二分探索</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/17/joi2009hob/">JOI2009本選2 ピザ</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/11/abc077c/">ABC077C Snuke Festival</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/12/abc023d/">ABC023D 射撃王</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/27/arc054b/">ARC054B ムーアの法則</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/25/joi2008hoc/">JOI2008本選C ダーツ</a></p></li>
</ol>
<h2 id="深さ優先探索"><a href="#深さ優先探索" class="headerlink" title="深さ優先探索"></a>深さ優先探索</h2><ol start="24">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/24/alds1-11b/">ALDS1 11B 深さ優先探索</a> </p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/01/aoj1160/">AOJ1160 島はいくつある？</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/15/abc138d/">ABC138D Ki</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/02/joi2009yod/">JOI2009予選D 薄氷渡り</a></p></li>
</ol>
<h2 id="幅優先探索"><a href="#幅優先探索" class="headerlink" title="幅優先探索"></a>幅優先探索</h2><ol start="28">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/18/alds1-11c/">ALDS1 11C 幅優先探索</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/16/abc007c/">ABC007C 幅優先探索</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/30/joi2011yoe/">JOI2011予選E チーズ</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/06/joi2012yoe/">JOI2012予選E イルミネーション</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/07/aoj1166/">AOJ1166 迷図と命ず</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/17/abc088d/">ABC088D Grid Repainting</a></p></li>
</ol>
<h2 id="動的計画法：ナップザック-DP"><a href="#動的計画法：ナップザック-DP" class="headerlink" title="動的計画法：ナップザック DP"></a>動的計画法：ナップザック DP</h2><ol start="34">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/11/alds1-10a/">ALDS1 10A フィボナッチ数列</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/13/dpl1b/">DPL1B 0-1ナップザック問題</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/13/dpl1c/">DPL1C ナップザック問題</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/14/dpl1a/">DPL1A コイン問題</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/20/alds1-10c/">ALDS1 10C 最長共通部分列</a></p></li>
</ol>
<h3 id="ナップサックDPまたはその亜種"><a href="#ナップサックDPまたはその亜種" class="headerlink" title="ナップサックDPまたはその亜種"></a>ナップサックDPまたはその亜種</h3><ol start="39">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/08/joi2011yod/">JOI2011予選D 1年生</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/09/joi2012yod/">JOI2012予選D パスタ</a></p></li>
    <li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/10/joi2013yod/">JOI2013予選D 暑い日々</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/11/joi2015yod/">JOI2015予選D シルクロード</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/12/paken2019-3d/">パ研杯2019 3D パ研軍旗</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/13/aoj1167/">AOJ1167 ポロック予想</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/16/aoj2199/">AOJ2199 Differential Pulse Code Modulation</a></p></li>
</ol>
<h2 id="動的計画法：区間-DP"><a href="#動的計画法：区間-DP" class="headerlink" title="動的計画法：区間 DP"></a>動的計画法：区間 DP</h2><ol start="46">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/15/alds1-10b/">ALDS1 10B 連鎖行列積</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/16/joi2015hob/">JOI2015本選B ケーキの切り分け２</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/17/aoj1611/">AOJ1611 ダルマ落とし</a></p></li>
</ol>
<h2 id="動的計画法：bit-DP"><a href="#動的計画法：bit-DP" class="headerlink" title="動的計画法：bit DP"></a>動的計画法：bit DP</h2><ol start="49">
<li><a href="https://kakedashi-engineer.appspot.com/2020/05/21/dpl2a/">DPL2A 巡回セールスマン問題</a></li>
</ol>
<h2 id="動的計画法：その他"><a href="#動的計画法：その他" class="headerlink" title="動的計画法：その他"></a>動的計画法：その他</h2><ol start="53">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/21/dpl1d/">DPL1D 最長増加部分列</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/18/abc006d/">ABC006D トランプ挿入ソート</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/19/abc134e/">ABC134E Sequence Decomposing</a></p></li>
</ol>
<h2 id="最短経路問題：ダイクストラ法"><a href="#最短経路問題：ダイクストラ法" class="headerlink" title="最短経路問題：ダイクストラ法"></a>最短経路問題：ダイクストラ法</h2><ol start="56">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/25/grl1a/">GRL1A 単一始点最短経路</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/23/joi2008yof/">JOI2008予選F 船旅</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/26/joi2016yoe/">JOI2016予選E ゾンビ島</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/25/joi2014yoe/">JOI2014予選E タクシー</a></p></li>
</ol>
<h2 id="最短経路問題：ワーシャルフロイド法"><a href="#最短経路問題：ワーシャルフロイド法" class="headerlink" title="最短経路問題：ワーシャルフロイド法"></a>最短経路問題：ワーシャルフロイド法</h2><ol start="60">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/31/grl1c/">GRL1C 全点対間最短経路</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/20/abc012d/">ABC012D バスと避けられない運命</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/21/abc079d/">ABC079D Wall</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/21/abc079d/">ABC074D Restoring Road Network</a></p></li>
</ol>
<h2 id="最小全域木問題"><a href="#最小全域木問題" class="headerlink" title="最小全域木問題"></a>最小全域木問題</h2><ol start="64">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/28/grl2a/">GRL2A 最小全域木</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/28/abc065d/">ABC065D Built?</a></p></li>
</ol>
<h2 id="高速な素数判定法"><a href="#高速な素数判定法" class="headerlink" title="高速な素数判定法"></a>高速な素数判定法</h2><ol start="68">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/30/ntl1a/">NTL1A 素因数分解</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/29/abc084d/">ABC084D 2017-like Number</a></p></li>
</ol>
<h2 id="高速なべき乗計算"><a href="#高速なべき乗計算" class="headerlink" title="高速なべき乗計算"></a>高速なべき乗計算</h2><ol start="70">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/30/ntl1b/">NTL1B べき乗</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/04/30/s8pc1e/">Square869120Countest#1E - 散歩 (E869120 and Path Length)</a></p></li>
</ol>
<h2 id="逆元を使う問題"><a href="#逆元を使う問題" class="headerlink" title="逆元を使う問題"></a>逆元を使う問題</h2><ol start="72">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/01/abc034c/">ABC034C 経路</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/02/abc145d/">ABC145D Knight</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/03/abc021d/">ABC021D 多重ループ</a></p></li>
</ol>
<h2 id="累積和"><a href="#累積和" class="headerlink" title="累積和"></a>累積和</h2><ol start="76">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/16/nikkei2019final-a/">全国統一プログラミング王決定戦本戦A Abundant Resources</a></p>
</li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/04/joi2010hoa/">JOI2010本選A 旅人</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/20/joi2011hoa/">JOI2011本戦A 惑星探索</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/04/abc106d/">ABC106D AtCoder Express 2</a></p></li>
</ol>
<ol start="80">
<li><a href="https://kakedashi-engineer.appspot.com/2020/05/05/gigacode2019d/">GigaCode2019D 家の建設</a></li>
</ol>
<h3 id="いもす法"><a href="#いもす法" class="headerlink" title="いもす法"></a>いもす法</h3><ol start="81">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/05/abc014c/">ABC014C AtColor</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/26/aoj2013/">AOJ2013 大崎</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/21/joi2015hoa/">JOI2015本選A 鉄道旅行</a></p></li>
</ol>
<h2 id="Union-Find"><a href="#Union-Find" class="headerlink" title="Union-Find"></a>Union-Find</h2><ol start="85">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/18/dsl1a/">DSL1A 互いに素な集合</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/06/abc075c/">ABC075C Bridge</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/19/abc120d/">ABC120D Decayed Bridge</a></p></li>
</ol>
<h2 id="その他のテクニック"><a href="#その他のテクニック" class="headerlink" title="その他のテクニック"></a>その他のテクニック</h2><h3 id="圧縮"><a href="#圧縮" class="headerlink" title="圧縮"></a>圧縮</h3><ol start="88">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/08/joi2008hoa/">JOI2008本戦A 碁石ならべ</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/09/joi2013hoa/">JOI2013本選1 電飾</a></p></li>
</ol>
<h3 id="単純な幾何計算"><a href="#単純な幾何計算" class="headerlink" title="単純な幾何計算"></a>単純な幾何計算</h3><ol start="90">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/14/s8pc5b/">Square869120Contest#5B - Emblem</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/16/abc144d/">ABC144D Water Bottle</a></p></li>
</ol>
<h2 id="実装問題"><a href="#実装問題" class="headerlink" title="実装問題"></a>実装問題</h2><ol start="93">
<li><a href="https://kakedashi-engineer.appspot.com/2020/05/16/aoj1193/">AOJ1193 連鎖消滅パズル</a></li>
</ol>
<h2 id="数学的な問題"><a href="#数学的な問題" class="headerlink" title="数学的な問題"></a>数学的な問題</h2><ol start="95">
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/19/abc149b/">ABC149B Greedy Takahashi</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/22/abc139d/">ABC139D ModSum</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/05/06/abc150d/">ABC150D Semi Common Multiple</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/04/sumitrust2019e/">三井住友信託銀行プログラミングコンテスト2019E Colorful Hats 2</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/05/ddcc2020qual-d/">DDCC2020予選D Digit Sum Replace</a></p></li>
<li><p><a href="https://kakedashi-engineer.appspot.com/2020/06/03/tenka1-2018d/">Tenka1 Programmer Beginner Contest 2018D Crossing</a></p></li>

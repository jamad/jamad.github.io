<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

* [このページの edit](https://github.com/jamad/jamad.github.io/tree/master/_posts)


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
<p><strong>アルゴリズム（12 個）</strong></p>

<ul>
<li>全探索（bit 全探索、順列全探索を含む）</li>
<li>二分探索</li>
<li>深さ優先探索（DFS）</li>
<li>幅優先探索（BFS）</li>
<li>動的計画法（bitDP などを含む）</li>
<li>ダイクストラ法（最短経路問題）</li>
<li>ワーシャルフロイド法（最短経路問題）</li>
<li>クラスカル法（最小全域木問題）</li>
<li>高速な素数判定法</li>
<li>べき乗を高速に計算するアルゴリズム</li>
<li>逆元を計算するアルゴリズム</li>
<li>累積和</li>
</ul>

<p><strong>データ構造（3 個）</strong></p>

<ul>
<li>グラフ（グラフ理論）</li>
<li>木</li>
<li>Union-Find</li>
</ul>

<table>
<thead>
<tr>
<th></th>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>全探索</td>
<td>二分探索</td>
<td>深さ優先探索 (DFS)</td>
<td>幅優先探索 (BFS)</td>
</tr>
<tr>
<td>動的計画法 (DP)</td>
<td>ダイクストラ法</td>
<td>ワーシャルフロイド法</td>
<td>クラスカル法</td>
</tr>
<tr>
<td>高速な素数判定法</td>
<td>べき乗を高速に計算する手法</td>
<td>逆元を計算する手法</td>
<td>累積和</td>
</tr>
</tbody>
</table>

# 2-3. 分野別　初中級者が解くべき過去問精選 100 問
* [記事へのリンク](https://qiita.com/e869120/items/eb50fdaece12be418faa#2-3-%E5%88%86%E9%87%8E%E5%88%A5%E5%88%9D%E4%B8%AD%E7%B4%9A%E8%80%85%E3%81%8C%E8%A7%A3%E3%81%8F%E3%81%B9%E3%81%8D%E9%81%8E%E5%8E%BB%E5%95%8F%E7%B2%BE%E9%81%B8-100-%E5%95%8F)

* AtCoder 水色コーダー を少ない問題数で達成するために、適切な100 問
* 分野ごとに問題が分けられています。また、アルゴリズムの確認問題から応用問題まで幅広い層の問題がありますので、是非解いてみることをおすすめします。
* 難しい問題もあるので、水色コーダーを目指す人は 100 問中 70 問正解を目安に頑張ってください。
* 100 問全部解けたら、水色コーダー どころか 青色コーダー くらいの実力

<h4>
<span id="全探索全列挙" class="fragment"></span><a href="#%E5%85%A8%E6%8E%A2%E7%B4%A2%E5%85%A8%E5%88%97%E6%8C%99"><i class="fa fa-link"></i></a>全探索：全列挙</h4>

<h4>
<span id="全探索工夫して通り数を減らす全列挙" class="fragment"></span><a href="#%E5%85%A8%E6%8E%A2%E7%B4%A2%E5%B7%A5%E5%A4%AB%E3%81%97%E3%81%A6%E9%80%9A%E3%82%8A%E6%95%B0%E3%82%92%E6%B8%9B%E3%82%89%E3%81%99%E5%85%A8%E5%88%97%E6%8C%99"><i class="fa fa-link"></i></a>全探索：工夫して通り数を減らす全列挙</h4>
<strong>7</strong>　<a href="https://atcoder.jp/contests/joi2007ho/tasks/joi2007ho_c" rel="nofollow noopener" target="_blank">JOI 2007 本選 3 - 最古の遺跡</a>　面白いです。Python3 だと想定解法が TLE する可能性があります。<br>


<h4>
<span id="全探索ビット全探索" class="fragment"></span><a href="#%E5%85%A8%E6%8E%A2%E7%B4%A2%E3%83%93%E3%83%83%E3%83%88%E5%85%A8%E6%8E%A2%E7%B4%A2"><i class="fa fa-link"></i></a>全探索：ビット全探索</h4>
<strong>14</strong>　<a href="https://atcoder.jp/contests/s8pc-4/tasks/s8pc_4_b" rel="nofollow noopener" target="_blank">Square869120Contest #4 B - Buildings are Colorful!</a>　工夫も必要で、一筋縄では解けない難問ですが、解けば確実に力がつきます。</p>

<h4>
<span id="全探索順列全探索" class="fragment"></span><a href="#%E5%85%A8%E6%8E%A2%E7%B4%A2%E9%A0%86%E5%88%97%E5%85%A8%E6%8E%A2%E7%B4%A2"><i class="fa fa-link"></i></a>全探索：順列全探索</h4>
<strong>17</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_13_A&amp;lang=ja" rel="nofollow noopener" target="_blank">ALDS_13_A - 8 クイーン問題</a>　面白いです。</p>

<h4>
<span id="二分探索-1" class="fragment"></span><a href="#%E4%BA%8C%E5%88%86%E6%8E%A2%E7%B4%A2-1"><i class="fa fa-link"></i></a>二分探索</h4>
<strong>21</strong>　<a href="https://atcoder.jp/contests/abc023/tasks/abc023_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 023 D - 射撃王</a>　教育的に良いです。<br>
<strong>22</strong>　<a href="https://atcoder.jp/contests/arc054/tasks/arc054_b" rel="nofollow noopener" target="_blank">AtCoder Regular Contest 054 B - ムーアの法則</a>　微分して二分法をすると解けます。<a href="https://qiita.com/ganariya/items/1553ff2bf8d6d7789127" id="reference-6eb6dc9afa0310a9ec9e">三分探索</a>と話が繋がってくるので、それも調べてみると良いと思います。<br>
<strong>23</strong>　<a href="https://atcoder.jp/contests/joi2008ho/tasks/joi2008ho_c" rel="nofollow noopener" target="_blank">JOI 2008 本選 3 - ダーツ</a>　工夫して二分探索する、チャレンジ問題です。</p>

<h4>
<span id="深さ優先探索" class="fragment"></span><a href="#%E6%B7%B1%E3%81%95%E5%84%AA%E5%85%88%E6%8E%A2%E7%B4%A2"><i class="fa fa-link"></i></a>深さ優先探索</h4>
<strong>26</strong>　<a href="https://atcoder.jp/contests/abc138/tasks/abc138_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 138 D - Ki</a>　木構造の問題の多くは、深さ優先探索を使います。<br>
<strong>27</strong>　<a href="https://atcoder.jp/contests/joi2009yo/tasks/joi2009yo_d" rel="nofollow noopener" target="_blank">JOI 2009 予選 4 - 薄氷渡り</a>　深さ優先探索は、木構造だけではありません、ということを教えてくれる問題です。再帰関数を使って解けます。</p>

<h4>
<span id="幅優先探索" class="fragment"></span><a href="#%E5%B9%85%E5%84%AA%E5%85%88%E6%8E%A2%E7%B4%A2"><i class="fa fa-link"></i></a>幅優先探索</h4>
<strong>31</strong>　<a href="https://atcoder.jp/contests/joi2012yo/tasks/joi2012yo_e" rel="nofollow noopener" target="_blank">JOI 2012 予選 5 - イルミネーション</a>　少し実装が重いですが、頑張れば解けます。<br>
<strong>32</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1166&amp;lang=jp" rel="nofollow noopener" target="_blank">AOJ 1166 - 迷図と命ず</a>　実装が少し重いです。<br>
<strong>33</strong>　<a href="https://atcoder.jp/contests/abc088/tasks/abc088_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 088 D - Grid Repainting</a>　これが解ければ、幅優先探索に慣れたと思って良いです。</p>

<h4>
<span id="動的計画法ナップザック-dp" class="fragment"></span><a href="#%E5%8B%95%E7%9A%84%E8%A8%88%E7%94%BB%E6%B3%95%E3%83%8A%E3%83%83%E3%83%97%E3%82%B6%E3%83%83%E3%82%AF-dp"><i class="fa fa-link"></i></a>動的計画法：ナップザック DP</h4>
<strong>36</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DPL_1_C&amp;lang=ja" rel="nofollow noopener" target="_blank">DPL_1_C - ナップザック問題</a>　基本問題です。<br>
<strong>38</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_10_C&amp;lang=ja" rel="nofollow noopener" target="_blank">ALDS_10_C - 最長共通部分列</a>　基本問題です。</p>
<p>(ここから先は、どのような DP で解けるのかは書きませんが、全部ナップザック DP またはその亜種で解くことができます。)</p>
<strong>40</strong>　<a href="https://atcoder.jp/contests/joi2012yo/tasks/joi2012yo_d" rel="nofollow noopener" target="_blank">JOI 2012 予選 4 - パスタ</a><br>
<strong>41</strong>　<a href="https://atcoder.jp/contests/joi2013yo/tasks/joi2013yo_d" rel="nofollow noopener" target="_blank">JOI 2013 予選 4 - 暑い日々</a><br>
<strong>42</strong>　<a href="https://atcoder.jp/contests/joi2015yo/tasks/joi2015yo_d" rel="nofollow noopener" target="_blank">JOI 2015 予選 4 - シルクロード</a><br>
<strong>43</strong>　<a href="https://atcoder.jp/contests/pakencamp-2019-day3/tasks/pakencamp_2019_day3_d" rel="nofollow noopener" target="_blank">パ研杯2019 D - パ研軍旗</a><br>
<strong>44</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1167&amp;lang=jp" rel="nofollow noopener" target="_blank">AOJ 1167 - ポロック予想</a><br>
<strong>45</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=2199&amp;lang=jp" rel="nofollow noopener" target="_blank">AOJ 2199 - 差分パルス符号変調</a></p>

<h4>
<span id="動的計画法区間-dp" class="fragment"></span><a href="#%E5%8B%95%E7%9A%84%E8%A8%88%E7%94%BB%E6%B3%95%E5%8C%BA%E9%96%93-dp"><i class="fa fa-link"></i></a>動的計画法：区間 DP</h4>
<p><strong>46</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_10_B&amp;lang=ja" rel="nofollow noopener" target="_blank">ALDS_10_B - 連鎖行列積</a>　基本問題です。<br>
<strong>47</strong>　<a href="https://atcoder.jp/contests/joi2015ho/tasks/joi2015ho_b" rel="nofollow noopener" target="_blank">JOI 2015 本選 2 - ケーキの切り分け 2</a>　<mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="31" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D442 TEX-I"></mjx-c></mjx-mi><mjx-mo class="mjx-n"><mjx-c class="mjx-c28"></mjx-c></mjx-mo><mjx-msup><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D441 TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: 0.363em; margin-left: 0.054em;"><mjx-mn class="mjx-n" size="s"><mjx-c class="mjx-c32"></mjx-c></mjx-mn></mjx-script></mjx-msup><mjx-mo class="mjx-n"><mjx-c class="mjx-c29"></mjx-c></mjx-mo></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>O</mi><mo stretchy="false">(</mo><msup><mi>N</mi><mn>2</mn></msup><mo stretchy="false">)</mo></math></mjx-assistive-mml></mjx-container> の区間 DP です。<br>
<strong>48</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1611&amp;lang=jp" rel="nofollow noopener" target="_blank">AOJ 1611 ダルマ落とし</a>　<mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="32" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D442 TEX-I"></mjx-c></mjx-mi><mjx-mo class="mjx-n"><mjx-c class="mjx-c28"></mjx-c></mjx-mo><mjx-msup><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D441 TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: 0.363em; margin-left: 0.054em;"><mjx-mn class="mjx-n" size="s"><mjx-c class="mjx-c33"></mjx-c></mjx-mn></mjx-script></mjx-msup><mjx-mo class="mjx-n"><mjx-c class="mjx-c29"></mjx-c></mjx-mo></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>O</mi><mo stretchy="false">(</mo><msup><mi>N</mi><mn>3</mn></msup><mo stretchy="false">)</mo></math></mjx-assistive-mml></mjx-container> の区間 DP です。</p>

<h4>
<span id="動的計画法bit-dp" class="fragment"></span><a href="#%E5%8B%95%E7%9A%84%E8%A8%88%E7%94%BB%E6%B3%95bit-dp"><i class="fa fa-link"></i></a>動的計画法：bit DP</h4>
<p><strong>49</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DPL_2_A&amp;lang=ja" rel="nofollow noopener" target="_blank">DPL_2_A - 巡回セールスマン問題</a>　基本問題です。<br>
<strong>50</strong>　<a href="https://atcoder.jp/contests/s8pc-1/tasks/s8pc_1_g" rel="nofollow noopener" target="_blank">Square869120Contest #1 G - Revenge of Traveling Salesman Problem</a>　巡回セールスマン問題を少し変えた問題です。<br>
<strong>51</strong>　<a href="https://atcoder.jp/contests/joi2014yo/tasks/joi2014yo_d" rel="nofollow noopener" target="_blank">JOI 2014 予選 4 - 部活のスケジュール表</a>　bitDP に含まれるか微妙ですが、一応入れておきます。<br>
<strong>52</strong>　<a href="https://atcoder.jp/contests/joi2017yo/tasks/joi2017yo_d" rel="nofollow noopener" target="_blank">JOI 2017 予選 4 - ぬいぐるみの整理</a>　少し難しいですが、是非挑戦してみてください。</p>

<h4>
<span id="動的計画法その他" class="fragment"></span><a href="#%E5%8B%95%E7%9A%84%E8%A8%88%E7%94%BB%E6%B3%95%E3%81%9D%E3%81%AE%E4%BB%96"><i class="fa fa-link"></i></a>動的計画法：その他</h4>

<p>その他の DP として代表的なものは、<a href="https://qiita.com/python_walker/items/d1e2be789f6e7a0851e5" id="reference-ac70cdcbe0878491c5d4">最長増加部分列問題 (LIS)</a> です。<br>
<strong>53</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DPL_1_D&amp;lang=ja" rel="nofollow noopener" target="_blank">DPL_1_D - 最長増加部分列</a><br>
<strong>54</strong>　<a href="https://atcoder.jp/contests/abc006/tasks/abc006_4" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 006 D - トランプ挿入ソート</a><br>
<strong>55</strong>　<a href="https://atcoder.jp/contests/abc134/tasks/abc134_e" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 134 E - Sequence Decomposing</a>　チャレンジ問題です。</p>

<h4>
<span id="最短経路問題ダイクストラ法" class="fragment"></span><a href="#%E6%9C%80%E7%9F%AD%E7%B5%8C%E8%B7%AF%E5%95%8F%E9%A1%8C%E3%83%80%E3%82%A4%E3%82%AF%E3%82%B9%E3%83%88%E3%83%A9%E6%B3%95"><i class="fa fa-link"></i></a>最短経路問題：ダイクストラ法</h4>
<strong>58</strong>　<a href="https://atcoder.jp/contests/joi2016yo/tasks/joi2016yo_e" rel="nofollow noopener" target="_blank">JOI 2016 予選 5 - ゾンビ島</a>　前述の幅優先探索も使います。実装がやや重めです。<br>
<strong>59</strong>　<a href="https://atcoder.jp/contests/joi2014yo/tasks/joi2014yo_e" rel="nofollow noopener" target="_blank">JOI 2014 予選 5 - タクシー</a></p>

<h4>
<span id="最短経路問題ワーシャルフロイド法" class="fragment"></span><a href="#%E6%9C%80%E7%9F%AD%E7%B5%8C%E8%B7%AF%E5%95%8F%E9%A1%8C%E3%83%AF%E3%83%BC%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%95%E3%83%AD%E3%82%A4%E3%83%89%E6%B3%95"><i class="fa fa-link"></i></a>最短経路問題：ワーシャルフロイド法</h4>

<p><strong>60</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=GRL_1_C&amp;lang=ja" rel="nofollow noopener" target="_blank">GRL_1_C - 全点対間最短経路</a>　基本問題です。<br>
<strong>61</strong>　<a href="https://atcoder.jp/contests/abc012/tasks/abc012_4" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 012 D - バスと避けられない運命</a><br>
<strong>62</strong>　<a href="https://atcoder.jp/contests/abc079/tasks/abc079_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 079 D - Wall</a><br>
<strong>63</strong>　<a href="https://atcoder.jp/contests/abc074/tasks/arc083_b" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 074 D - Restoring Road Network</a>　ちょっと数学的考察が必要で難しいですが、是非解いてみましょう。</p>

<h4>
<span id="最小全域木問題" class="fragment"></span><a href="#%E6%9C%80%E5%B0%8F%E5%85%A8%E5%9F%9F%E6%9C%A8%E5%95%8F%E9%A1%8C"><i class="fa fa-link"></i></a>最小全域木問題</h4>

<p><strong>64</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=GRL_2_A&amp;lang=ja" rel="nofollow noopener" target="_blank">GRL_2_A - 最小全域木</a>　基本問題です。<br>
<strong>65</strong>　<a href="https://atcoder.jp/contests/joisc2010/tasks/joisc2010_finals" rel="nofollow noopener" target="_blank">JOI 2010 春合宿 - Finals</a>　(<a href="https://www.ioi-jp.org/camp/2010/2010-sp-tasks/2010-sp-day3_22.pdf" rel="nofollow noopener" target="_blank">問題pdf</a>) JOI 春合宿の問題ですが、比較的簡単です。<br>
<strong>66</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1127" rel="nofollow noopener" target="_blank">AOJ 1127 - Building a Space Station</a><br>
<strong>67</strong>　<a href="https://atcoder.jp/contests/abc065/tasks/arc076_b" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 065 D - Built?</a>　やや難しいです。単純に最小全域木を求めると、<mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="33" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D441 TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>N</mi></math></mjx-assistive-mml></mjx-container> 頂点 <mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="34" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msup><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D441 TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: 0.363em; margin-left: 0.054em;"><mjx-mn class="mjx-n" size="s"><mjx-c class="mjx-c32"></mjx-c></mjx-mn></mjx-script></mjx-msup></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>N</mi><mn>2</mn></msup></math></mjx-assistive-mml></mjx-container> 辺になりますが、なんとそれを減らすことができます。</p>

<h4>
<span id="高速な素数判定法-1" class="fragment"></span><a href="#%E9%AB%98%E9%80%9F%E3%81%AA%E7%B4%A0%E6%95%B0%E5%88%A4%E5%AE%9A%E6%B3%95-1"><i class="fa fa-link"></i></a>高速な素数判定法</h4>

<p><strong>68</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=NTL_1_A&amp;lang=ja" rel="nofollow noopener" target="_blank">NTL_1_A - 素因数分解</a>　基本問題です。<br>
<strong>69</strong>　<a href="https://atcoder.jp/contests/abc084/tasks/abc084_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 084 D - 2017-like Number</a></p>

<h4>
<span id="高速なべき乗計算" class="fragment"></span><a href="#%E9%AB%98%E9%80%9F%E3%81%AA%E3%81%B9%E3%81%8D%E4%B9%97%E8%A8%88%E7%AE%97"><i class="fa fa-link"></i></a>高速なべき乗計算</h4>

<p><strong>70</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=NTL_1_B&amp;lang=ja" rel="nofollow noopener" target="_blank">NTL_1_B - べき乗</a><br>
<strong>71</strong>　<a href="https://atcoder.jp/contests/s8pc-1/tasks/s8pc_1_e" rel="nofollow noopener" target="_blank">Square869120Contest #1 E - 散歩</a><br>
※ べき乗だけを使う問題は少ないですが、<mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="35" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45B TEX-I"></mjx-c></mjx-mi><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D436 TEX-I"></mjx-c></mjx-mi><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45F TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>n</mi><mi>C</mi><mi>r</mi></math></mjx-assistive-mml></mjx-container> などを求める際に、逆元とセットで出てくることが多いです。例えば、<mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="36" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D44E TEX-I"></mjx-c></mjx-mi><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D465 TEX-I"></mjx-c></mjx-mi><mjx-mo class="mjx-n" space="4"><mjx-c class="mjx-c2261"></mjx-c></mjx-mo><mjx-mn class="mjx-n" space="4"><mjx-c class="mjx-c31"></mjx-c></mjx-mn><mjx-mtext class="mjx-n"><mjx-c class="mjx-cA0"></mjx-c></mjx-mtext><mjx-mo class="mjx-n"><mjx-c class="mjx-c28"></mjx-c></mjx-mo><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45A TEX-I"></mjx-c></mjx-mi><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45C TEX-I"></mjx-c></mjx-mi><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D451 TEX-I"></mjx-c></mjx-mi><mjx-mtext class="mjx-n"><mjx-c class="mjx-cA0"></mjx-c></mjx-mtext><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45D TEX-I"></mjx-c></mjx-mi><mjx-mo class="mjx-n"><mjx-c class="mjx-c29"></mjx-c></mjx-mo></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mi>x</mi><mo>≡</mo><mn>1</mn><mtext>&nbsp;</mtext><mo stretchy="false">(</mo><mi>m</mi><mi>o</mi><mi>d</mi><mtext>&nbsp;</mtext><mi>p</mi><mo stretchy="false">)</mo></math></mjx-assistive-mml></mjx-container> の解は <mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="37" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msup><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D44E TEX-I"></mjx-c></mjx-mi><mjx-script style="vertical-align: 0.363em;"><mjx-texatom size="s" texclass="ORD"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45D TEX-I"></mjx-c></mjx-mi><mjx-mo class="mjx-n"><mjx-c class="mjx-c2212"></mjx-c></mjx-mo><mjx-mn class="mjx-n"><mjx-c class="mjx-c32"></mjx-c></mjx-mn></mjx-texatom></mjx-script></mjx-msup><mjx-mtext class="mjx-n"><mjx-c class="mjx-cA0"></mjx-c></mjx-mtext><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45A TEX-I"></mjx-c></mjx-mi><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45C TEX-I"></mjx-c></mjx-mi><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D451 TEX-I"></mjx-c></mjx-mi><mjx-mtext class="mjx-n"><mjx-c class="mjx-cA0"></mjx-c></mjx-mtext><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45D TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>a</mi><mrow data-mjx-texclass="ORD"><mi>p</mi><mo>−</mo><mn>2</mn></mrow></msup><mtext>&nbsp;</mtext><mi>m</mi><mi>o</mi><mi>d</mi><mtext>&nbsp;</mtext><mi>p</mi></math></mjx-assistive-mml></mjx-container> となります。（<mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="38" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mi class="mjx-i"><mjx-c class="mjx-c1D45D TEX-I"></mjx-c></mjx-mi></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>p</mi></math></mjx-assistive-mml></mjx-container> が素数の場合）</p>

<h4>
<span id="逆元を使う問題" class="fragment"></span><a href="#%E9%80%86%E5%85%83%E3%82%92%E4%BD%BF%E3%81%86%E5%95%8F%E9%A1%8C"><i class="fa fa-link"></i></a>逆元を使う問題</h4>

<p><strong>72</strong>　<a href="https://atcoder.jp/contests/abc034/tasks/abc034_c" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 034 C - 経路</a>　nCr を求めるだけの基本問題です。<br>
<strong>73</strong>　<a href="https://atcoder.jp/contests/abc145/tasks/abc145_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 145 D - Knight</a><br>
<strong>74</strong>　<a href="https://atcoder.jp/contests/abc021/tasks/abc021_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 021 D - 多重ループ</a><br>
<strong>75</strong>　<a href="https://atcoder.jp/contests/abc149/tasks/abc149_f" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 149 F - Surrounded Nodes</a>　チャレンジ問題です。解けなくても、「そういう特殊な出力形式の問題ってあるんだな」と感じてほしいです。</p>

<h4>
<span id="累積和-1" class="fragment"></span><a href="#%E7%B4%AF%E7%A9%8D%E5%92%8C-1"><i class="fa fa-link"></i></a>累積和</h4>

<p><strong>76</strong>　<a href="https://atcoder.jp/contests/nikkei2019-final/tasks/nikkei2019_final_a" rel="nofollow noopener" target="_blank">全国統一プログラミング王決定戦本戦 A - Abundant Resources</a>　基本です。累積和を使わなくても解けますが、是非使って解いてみてください。<br>
<strong>77</strong>　<a href="https://atcoder.jp/contests/joi2010ho/tasks/joi2010ho_a" rel="nofollow noopener" target="_blank">JOI 2010 本選 1 - 旅人</a><br>
<strong>78</strong>　<a href="https://atcoder.jp/contests/joi2011ho/tasks/joi2011ho1" rel="nofollow noopener" target="_blank">JOI 2011 本選 1 - 惑星探査</a>　二次元累積和です。<br>
<strong>79</strong>　<a href="https://atcoder.jp/contests/abc106/tasks/abc106_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 106 D - AtCoder Express 2</a><br>
<strong>80</strong>　<a href="https://atcoder.jp/contests/gigacode-2019/tasks/gigacode_2019_d" rel="nofollow noopener" target="_blank">GigaCode 2019 D - 家の建設</a></p>

<p>(ここから先は、「いもす法」というアルゴリズムを使う場合があります。)</p>

<p><strong>81</strong>　<a href="https://atcoder.jp/contests/abc014/tasks/abc014_3" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 014 C - AtColor</a>　基本問題です。<br>
<strong>82</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=2013" rel="nofollow noopener" target="_blank">AOJ 2013 - 大崎</a><br>
<strong>83</strong>　<a href="https://atcoder.jp/contests/joi2015ho/tasks/joi2015ho_a" rel="nofollow noopener" target="_blank">JOI 2015 本選 1 - 鉄道運賃</a><br>
<strong>84</strong>　<a href="https://atcoder.jp/contests/joi2012ho/tasks/joi2012ho4" rel="nofollow noopener" target="_blank">JOI 2012 本選 4 - 釘</a>　チャレンジ問題です。</p>

<h4>
<span id="union-find-1" class="fragment"></span><a href="#union-find-1"><i class="fa fa-link"></i></a>Union-Find</h4>

<p><strong>85</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_1_A&amp;lang=ja" rel="nofollow noopener" target="_blank">DSL_1_A - 互いに素な集合</a>　基本問題です。<br>
<strong>86</strong>　<a href="https://atcoder.jp/contests/abc075/tasks/abc075_c?lang=ja" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 075 C - Bridge</a>　深さ優先探索による連結成分の個数の数え上げでも解けますが、Union-Find でも解いてみましょう。<br>
<strong>87</strong>　<a href="https://atcoder.jp/contests/abc120/tasks/abc120_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 120 D - Decayed Bridge</a>　一個の考察ステップがあり、少し難しいですが、解くことで得られる力は大きいと思います。</p>

<h4>
<span id="その他のテクニック" class="fragment"></span><a href="#%E3%81%9D%E3%81%AE%E4%BB%96%E3%81%AE%E3%83%86%E3%82%AF%E3%83%8B%E3%83%83%E3%82%AF"><i class="fa fa-link"></i></a>その他のテクニック</h4>

<p>「圧縮」によって解ける問題たちです。</p>

<p><strong>88</strong>　<a href="https://atcoder.jp/contests/joi2008ho/tasks/joi2008ho_a" rel="nofollow noopener" target="_blank">JOI 2008 本選 1 - 碁石ならべ</a><br>
<strong>89</strong>　<a href="https://atcoder.jp/contests/joi2013ho/tasks/joi2013ho1" rel="nofollow noopener" target="_blank">JOI 2013 本選 1 - 電飾</a></p>

<p>「単純な幾何計算」によって解ける問題たちです。標準ライブラリに存在する、2 乗根・三角関数などを使うと解けます。</p>

<p><strong>90</strong>　<a href="https://atcoder.jp/contests/s8pc-5/tasks/s8pc_5_b" rel="nofollow noopener" target="_blank">Square869120Contest #5 B - Emblem</a><br>
<strong>91</strong>　<a href="https://atcoder.jp/contests/abc144/tasks/abc144_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 144 D - Water Bottle</a>　本記事では触れていませんが、<a href="https://ja.wikipedia.org/wiki/%E9%80%86%E4%B8%89%E8%A7%92%E9%96%A2%E6%95%B0" rel="nofollow noopener" target="_blank">三角関数の逆関数</a>を使って解くことができます。 </p>

<h4>
<span id="実装問題" class="fragment"></span><a href="#%E5%AE%9F%E8%A3%85%E5%95%8F%E9%A1%8C"><i class="fa fa-link"></i></a>実装問題</h4>

<p>考察に比べて実装がとても重い問題です。練習になると思います。</p>

<p><strong>92</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1193&amp;lang=jp" rel="nofollow noopener" target="_blank">AOJ 1193 - 連鎖消滅パズル</a><br>
<strong>93</strong>　<a href="https://atcoder.jp/contests/s8pc-3/tasks/s8pc_3_b" rel="nofollow noopener" target="_blank">Square869120Contest #3 B - 石落としゲーム</a><br>
<strong>94</strong>　<a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=1149&amp;lang=jp" rel="nofollow noopener" target="_blank">AOJ 1149 - ケーキカット</a></p>

<h4>
<span id="数学的な問題" class="fragment"></span><a href="#%E6%95%B0%E5%AD%A6%E7%9A%84%E3%81%AA%E5%95%8F%E9%A1%8C"><i class="fa fa-link"></i></a>数学的な問題</h4>

<p>AtCoder の問題の一部では、解くために数学的な考察を必要とします。上級編にも繋げていくために、水色コーダーを目指している人は「数学的考察って何なのか」「数学的考察ってどんな感じで使うのか」くらいは知っておくと良いと思うので、これを感じられる問題の代表例を紹介しておきます。</p>

<p><strong>95</strong>　<a href="https://atcoder.jp/contests/abc149/tasks/abc149_b" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 149 B - Greedy Takahashi</a>　200-300 点問題で出る数学的問題は大体そんな感じです。（<a href="http://www2.kobe-u.ac.jp/%7Eky/da2/haihu04.pdf" rel="nofollow noopener" target="_blank">貪欲法アルゴリズム</a>に繋がってきます。）<br>
<strong>96</strong>　<a href="https://atcoder.jp/contests/abc139/tasks/abc139_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 139 D - ModSum</a>　考察一個です。<br>
<strong>97</strong>　<a href="https://atcoder.jp/contests/abc150/tasks/abc150_d" rel="nofollow noopener" target="_blank">AtCoder Beginner Contest 150 D - Semi Common Multiple</a><br>
<strong>98</strong>　<a href="https://atcoder.jp/contests/sumitrust2019/tasks/sumitb2019_e" rel="nofollow noopener" target="_blank">三井住友信託銀行プログラミングコンテスト2019 予選 E - Colorful Hats 2</a><br>
<strong>99</strong>　<a href="https://atcoder.jp/contests/ddcc2020-qual/tasks/ddcc2020_qual_d" rel="nofollow noopener" target="_blank">DDCC2020 予選 D - Digit Sum Replace</a>　これも考察一個です。<br>
<strong>100</strong>　<a href="https://atcoder.jp/contests/tenka1-2018-beginner/tasks/tenka1_2018_d" rel="nofollow noopener" target="_blank">Tenka1 Programmer Beginner Contest D - Crossing</a>　やや難しいですが、頑張って解いてください。</p>

<hr>

<p>これが全部解けたら、自信をもって「水色コーダー相当の実力」があるといってよいです。<br>

---


# 分野別　初中級者が解くべき過去問精選 100 問 

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

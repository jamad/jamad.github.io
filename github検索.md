# [github検索ページ](https://jamad.github.io/github%E6%A4%9C%E7%B4%A2) そして　[ソースの.md](https://github.com/jamad/jamad.github.io/blob/master/github%E6%A4%9C%E7%B4%A2.md)

# github もしくは gistでの文字列検索ボタン  数行のコードで機能を作れたの素晴らしい！　そして入力フィールドも共通でいいんだ！
* [テストしたcodepen](https://codepen.io/jamad/pen/GRbKQxm)

|<input id="iT1" placeholder="検索用文字列を入力">|
|-|
|<button onclick="window.open('https://github.com/search?q=user%3Ajamad+'+encodeURIComponent(iT1.value),'_blank')">user:jamad でgithubを検索</button>|
|<button onclick="window.open('https://gist.github.com/search?q=user%3Ajamad+'+encodeURIComponent(iT1.value),'_blank')">user:jamad でgistを検索</button>|


# the following is a quicktest for svg tag

<svg width="100%" height="200">
  <circle cx="0" cy="100" r="20" fill="blue">
    <animate attributeName="cx" from="0" to="100%" dur="5s" repeatCount="indefinite" />
  </circle>
</svg>

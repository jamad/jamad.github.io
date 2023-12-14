<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

## このページ(index.html)の更新方法 
1. [index.md](https://github.com/jamad/jamad.github.io/edit/master/index.md)　から編集 (index.html が既存だと index.md が上書きできないので削除)
2. jekyllの自動更新を数分待つ おそらく確認は[ここ](https://github.com/jamad/jamad.github.io/actions)でできる
3. [jamad.github.io](https://jamad.github.io/) を確認する Chromeなら `ctrl+shift+R` でキャッシュクリアするのが吉

## note
* どうも1st line の記述が全てのブログポストに複製されるように思える  だがリンクである必要があるみたいだ　>> いや違うな。別の記事のタイトルが表示された
* [jamad.github.io](https://jamad.github.io/) の場合は複製されなかった
* `## jamad.github.io`　だと複製された
* `### jamad.github.io`　も複製された (結局これを使うことにした)
* `#### jamad.github.io` だと複製されなくなった

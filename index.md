#### jamad.github.io


* どうも1st line の記述が全てのブログポストに複製されるように思える  だがリンクである必要があるみたいだ
* [jamad.github.io](https://jamad.github.io/) の場合は複製されなかった
* `## jamad.github.io`　だと複製された
* `### jamad.github.io`　も複製された 


## このページの更新方法 
1. [index.md](https://github.com/jamad/jamad.github.io/edit/master/index.md)　から編集
2. jekyllの自動更新を数分待つ おそらく確認は[ここ](https://github.com/jamad/jamad.github.io/actions)でできる
3. [jamad.github.io](https://jamad.github.io/) を確認する Chromeなら ctrl+shift+R でキャッシュクリアするのが吉

### /assets/css/theme.css へのリンクを張ってみる .scss も.css にコンバートされるようだ
<link rel="stylesheet" type="text/css" href="/assets/css/theme.css">
* https://github.com/jamad/jamad.github.io/blob/master/assets/css/theme.scss を編集してjelyllがコンバートするまで暫し待つ （34行付近） $background-pattern: 'subtle-grey.png'; 


## github pages を作成する上での注意点
* index.html が既存だと index.md が上書きできない。なので削除するべし。






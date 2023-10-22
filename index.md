Jamad Blogs


* どうも1st line の記述が全てのブログポストに複製されるように思えるので　 コメントにしてみた


## このページの更新方法 
1. [index.md](https://github.com/jamad/jamad.github.io/edit/master/index.md)　から編集
2. jekyllの自動更新を数分待つ
3. [jamad.github.io](https://jamad.github.io/) を確認する Chromeなら ctrl+shift+R でキャッシュクリアするのが吉

### /assets/css/theme.css へのリンクを張ってみる .scss も.css にコンバートされるようだ
<link rel="stylesheet" type="text/css" href="/assets/css/theme.css">
* https://github.com/jamad/jamad.github.io/blob/master/assets/css/theme.scss を編集してjelyllがコンバートするまで暫し待つ （34行付近） $background-pattern: 'subtle-grey.png'; 


## github pages を作成する上での注意点
* index.html が既存だと index.md が上書きできない。なので削除するべし。



```![Image](src)```
![Image](https://jamad.github.io/jam_clock_icon.png)

```<img src="https://jamad.github.io/jam_clock_icon.png" width="64">```
<img src="https://jamad.github.io/jam_clock_icon.png" width="64">

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Doc
[documentation](https://help.github.com/categories/github-pages-basics/) 

### HTML tag test - center doesn't work

`<center>center text</center>`
<center>center text</center>

`<p style="text-align: center;">test</p>`
<p style="text-align: center;">test</p>

`<div style="text-align: center;"><img src="https://jamad.github.io/jam_clock_icon.png" width="64"></div>`
<div style="text-align: center;"><img src="https://jamad.github.io/jam_clock_icon.png" width="64"></div>




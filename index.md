
---

# Jamad Blogs
* 恐らく、上記の#タグは全てのブログポストに影響を及ぼす 

### /assets/css/theme.css へのリンクを張ってみる .scss も.css にコンバートされるようだ (でも、もしかしてindex.md を変更しないとコンバートされない？ cacheをリセットする必要があるのか？ )
<link rel="stylesheet" type="text/css" href="/assets/css/theme.css">
* https://github.com/jamad/jamad.github.io/blob/master/assets/css/theme.scss を編集してjelyllがコンバートするまで暫し待つ （34行付近） $background-pattern: 'subtle-grey.png'; 

#### github pages 
#### ここのページ[jamad.github.io](https://jamad.github.io/) を更新する手順
* [編集のためのリンクを開く](https://github.com/jamad/jamad.github.io/edit/master/index.md)　 



## github pages を作成する上での注意点
* index.html が既存だと index.md が上書きできない。なので削除するべし。


# Tips for GitHub Pages (日本語)
1. index.mdファイルを　[editor on GitHub](https://github.com/jamad/jamad.github.io/edit/master/index.md)　で編集する
2. jekyll が index.md から　index.html　を自動作成するのを数分待つ
3. https://jamad.github.io/ が index.md　で更新された内容を表示する


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




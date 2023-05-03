# Github Pages Jamad

## github pages を更新するには　例：https://jamad.github.io/
* [編集のためのリンクを開く](https://github.com/jamad/jamad.github.io/edit/master/index.md)　 

## theme の変更
* まず、themeはここに見つかった　https://pages.github.com/themes/
*  既存ファイル　jamad.github.io/blob/master/_config.yml　を編集することで変更できた
* `theme: jekyll-theme-slate` を削除すると思ったような結果にならなかったので、残した
* ![image](https://user-images.githubusercontent.com/949913/235970625-b782ce4b-6a42-4bf3-afc4-aae9fb470109.png)

|Theme Name|Theme Visual|
|-|-|
|Architect|![image](https://user-images.githubusercontent.com/949913/235971245-22d71837-a12f-4ff6-a522-9b4065643c0e.png)|
|Cayman|![image](https://user-images.githubusercontent.com/949913/235978166-dddbd7ea-96a2-4435-961f-6db689774c3a.png)|
|Dinky|![image](https://user-images.githubusercontent.com/949913/235984076-cd5e938c-7d74-4872-bd40-2ba60a926b86.png)|






## github pages を作成する上での注意点
* index.html が既存だと index.md が上書きできない。なので削除するべし。


# Tips for GitHub Pages (日本語)
1. index.mdファイルを　[editor on GitHub](https://github.com/jamad/jamad.github.io/edit/master/index.md)　で編集する
2. jekyll が index.md から　index.html　を自動作成するのを数分待つ
3. https://jamad.github.io/ が index.md　で更新された内容を表示する

# Tips for GitHub Pages (English)
1. Edit index.md by [editor on GitHub](https://github.com/jamad/jamad.github.io/edit/master/index.md)
1. wait for several minutes while [Jekyll](https://jekyllrb.com/) rebuild index.html from index.md
1. https://jamad.github.io/ displays the content by index.md


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

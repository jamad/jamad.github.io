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
|Hacker|![image](https://user-images.githubusercontent.com/949913/236018878-31f80437-3935-4a48-a8ba-e942881b7939.png)|
|Leap day|![image](https://user-images.githubusercontent.com/949913/236020058-1ba2a718-3eea-414c-9020-91ab7e5ec86d.png)|
|Merlot|![image](https://user-images.githubusercontent.com/949913/236022003-e59d6cba-ace8-4a42-86ce-d6f90061f377.png)|
|Midnight |![image](https://user-images.githubusercontent.com/949913/236022948-501d2ea3-97c1-4238-b021-25f80e46c236.png)|









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

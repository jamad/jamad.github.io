# Jamad Blogs
* 恐らく、上記の#タグは全てのブログポストに影響を及ぼす 

### /assets/css/theme.css へのリンクを張ってみる .scss も.css にコンバートされるようだ (でも、もしかしてindex.md を変更しないとコンバートされない？ cacheをリセットする必要があるのか？ )
<link rel="stylesheet" type="text/css" href="/assets/css/theme.css">
* https://github.com/jamad/jamad.github.io/blob/master/assets/css/theme.scss を編集してjelyllがコンバートするまで暫し待つ （34行付近） $background-pattern: 'subtle-grey.png'; 

#### github pages 
#### ここのページ[jamad.github.io](https://jamad.github.io/) を更新する手順
* [編集のためのリンクを開く](https://github.com/jamad/jamad.github.io/edit/master/index.md)　 

#### TODO
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/4e22c35f-d8aa-4aea-b25e-107689b893ed)
* ここを参考にして、背景をカスタマイズしよう
* `http://pavelmakhov.com/jekyll-clean-dark/2016/09/customizations/`
* _posts フォルダをダウンロードして　アップロードしてみた。
* _config.yml を参考にして、適当に変更してみた
* まだ思った通りになっていない　下記を参考にしよう
* https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/adding-a-theme-to-your-github-pages-site-using-jekyll
* https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site


#### theme を変更する手順 
* themeのある場所　https://pages.github.com/themes/
* 既存ファイル　[jamad.github.io/blob/master/_config.yml](https://github.com/jamad/jamad.github.io/edit/master/_config.yml)　を編集することで変更できた
* 変更例
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/ea23f161-5d3e-4a37-9b79-7af01c4819e6)
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/1a8d09c4-e937-4a14-ae06-9f7b0b4fcce1)
* `theme: jekyll-theme-slate` を削除すると思ったような結果にならなかったので、残した
* ![image](https://user-images.githubusercontent.com/949913/235970625-b782ce4b-6a42-4bf3-afc4-aae9fb470109.png)

|Theme Name|Theme Visual|
|-|-|
|[Cayman](https://pages-themes.github.io/cayman/)| <img height="60" src="https://user-images.githubusercontent.com/949913/235978166-dddbd7ea-96a2-4435-961f-6db689774c3a.png">|
|[Architect](https://pages-themes.github.io/architect/)|　<img height="60" src="https://user-images.githubusercontent.com/949913/235971245-22d71837-a12f-4ff6-a522-9b4065643c0e.png">|
|[Dinky](https://pages-themes.github.io/dinky/)|　<img height="60" src="https://user-images.githubusercontent.com/949913/235984076-cd5e938c-7d74-4872-bd40-2ba60a926b86.png">|　
|[Hacker](https://pages-themes.github.io/hacker/)|　<img height="60" src="https://user-images.githubusercontent.com/949913/236018878-31f80437-3935-4a48-a8ba-e942881b7939.png">|　
|[Leap day](https://pages-themes.github.io/leap-day/)|　<img height="60" src="https://user-images.githubusercontent.com/949913/236020058-1ba2a718-3eea-414c-9020-91ab7e5ec86d.png">|　
|[Merlot](https://pages-themes.github.io/merlot/)|　<img height="60" src="https://user-images.githubusercontent.com/949913/236022003-e59d6cba-ace8-4a42-86ce-d6f90061f377.png">|　
|Midnight |　<img height="60" src="https://user-images.githubusercontent.com/949913/236022948-501d2ea3-97c1-4238-b021-25f80e46c236.png">|　
|Slate|　<img height="60" src="https://user-images.githubusercontent.com/949913/236025082-bb9b0641-e1ff-4499-9ce8-75c06533cf70.png">|


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




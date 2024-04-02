<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

---

layout: post
title: front matter
date: 2023-12-12

---

## 上記は、front matter のテスト --- の前後には改行があった方がいい？　タイトルは front matter に変わってはいない。.mdのファイル名のままだ。 

# `で囲まれたブロックがiPhoneで読めなかったのを修正した時のメモ
* まずはinspectorで右記のような情報をゲット　![image](https://github.com/jamad/jamad.github.io/assets/949913/21df9df4-5514-4120-a692-a6ff64f692a1)
* それを参考に右記のようなコードを記述　![image](https://github.com/jamad/jamad.github.io/assets/949913/d2ed96e7-ae37-4b05-b2f5-e510ec0acb00)
* 同様にしてボタンの文字もiOSのSafariで読めるようにした　![image](https://github.com/jamad/jamad.github.io/assets/949913/6f34ef6e-2b32-4e58-ad77-b3b8b5de56ae)

### History
* 2023-12-12 theme.scss は使っていないので削除
* 2023-10-24 最新の状態では　href="/assets/css/styles.css" として .css を利用している。複数の.css があれば複数の記事それぞれで異なるスタイルをアサインできるということ

###  .scss はまたいつか試してみよう   （chatgpt に相談するのが吉）


# 背景画像を設定するためにしたこと

### /assets/css/styles.css へのリンクを.md内に記述することで背景画像が表示される
```
<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">
```

#### theme 主に 背景のカスタマイズ
* [ここ](http://pavelmakhov.com/jekyll-clean-dark/2016/09/customizations/)を参考にした
* _config.yml を適当に変更してみた 
* https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/adding-a-theme-to-your-github-pages-site-using-jekyll
* https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

|filename|Blog post title|note|
|-|-|-|
|`2023-12-12-how to post a blog page.md`|`How to post a blog page`|空白は保持。先頭のみ大文字化|
|`2023-10-22-table-styles.md`|`Table Styles`|-での接続の場合-直後が大文字化|




* History
* changed the filename as `2023-12-12-how to post a blog page.md`
* changed the filename from 2023-10-23-blogpost.md to 2023-12-12-blogpost.md

# _postでないフォルダのテスト
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/f7d5af53-098a-4863-9393-327cd6619463)


# 基本
1. 記事を[ _postフォルダ内](https://github.com/jamad/jamad.github.io/tree/master/_posts)に　YYYY-MM-DD-title.md のファイル名で作成する title部分は日本語OKだった
1. ファイルには下記のようにヘッダーを入れる  ここのtitle文字列がトップページに表示される 
1. commit changes... しても即反映はされないので、 Jekyllがコンバート終了するまで数分待つ
1. ブラウザでは念のためキャッシュクリアして更新の確認をする　(chromeなら ctrl + shift + R )

```
---
layout: post
title: how to post a blog page
author: jamad
---
```

具体例：この記事の場合は下記のようにヘッダーを入れている 
![image](https://github.com/jamad/jamad.github.io/assets/949913/80e13766-cc52-4b49-90e5-287a919c6b5f)


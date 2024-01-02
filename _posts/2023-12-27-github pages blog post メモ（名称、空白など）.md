<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

# .md のファイル名と表示文字列の関係

|ファイル名|Blog post表示されたタイトル|備考|
|-|-|-|
|`2023-12-12-how to post a blog page.md`|`How to post a blog page`|空白は保持。<br>先頭のみ大文字化|
|`2023-10-22-table-styles.md`|`Table Styles`|-は空白に置換<br>-直後は大文字化|
|`2023-10-23-github_pages_theme.md`|`Github_pages_theme`|_での接続の場合<br>そのまま表示|


# _postでないフォルダのテスト
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/f7d5af53-098a-4863-9393-327cd6619463)


# 基本
1. 記事を[ _postフォルダ内](https://github.com/jamad/jamad.github.io/tree/master/_posts)に　YYYY-MM-DD-title.md で作成する title部分は日本語もOK
1. commit changes... しても即反映はされない。Jekyllのコンバート完了を待つ（Actionsで確認可能）
1. ブラウザではキャッシュをクリアして更新の確認をするのが吉　(chromeなら ctrl + shift + R )

<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

# 2023-12-28 下記は終了しておいた方がいいかもしれないのでメモ
* https://github.com/skills/communicate-using-markdown


* example and [reference](https://guides.github.com/features/mastering-markdown/)

|syntax|result|
|-|-|
|```![Image](https://jamad.github.io/jam_clock_icon.png)```|![Image](https://jamad.github.io/jam_clock_icon.png)|
|```<img src="https://jamad.github.io/jam_clock_icon.png" width="64">```|<img src="https://jamad.github.io/jam_clock_icon.png" width="64">|


### Doc
* https://docs.github.com/en/pages/getting-started-with-github-pages


# テーブルの揃えのsyntax
### 一つのパイプでテーブル作れたぞ？ preview ではテーブルにならない。htmlのみ？

A|B

by `A|B`


##  [参考](https://kramdown.gettalong.org/syntax.html#tables)

| デフォルトは左詰めと同じ |左詰め | 中央揃え | 右詰め |
|-----------------|:-----------|:---------------:|---------------:|
| First body part |Second cell | Third cell      | fourth cell    |
| Second line     |foo         | **strong**      | baz            |
| Third line      |quux        | baz             | bar            |

```
|-|-|-|-|
|-  |:- |:-:|-: |
|abc|abc|abc|abc|
```

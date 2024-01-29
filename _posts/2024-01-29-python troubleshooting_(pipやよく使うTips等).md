<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# よく使うTips
* ファイルのあるパスを取得する方法
* 

# 問題と解決方法

* pipコマンド
* `pip install bs4` for beautifulsoup 

* problem `invalid character in identifier`  [例](https://github.com/jamad/myPygame/commit/de48df759a5f5d60929908afdcabc22b14cbc6d3)
  * investigation[参考はあるものの未解決](https://stackoverflow.com/questions/14844687/invalid-character-in-identifier)
 
---

* problem `error: (-2:Unspecified error) The function is not implemented.Rebuild the library with Windows, GTK+ 2.x or Cocoa support. `
  * investigation : helpful reference >> https://stackoverflow.com/questions/67120450/error-2unspecified-error-the-function-is-not-implemented-rebuild-the-libra
    * solution
      * `pip uninstall opencv-python`
      * `pip install opencv-python`
 


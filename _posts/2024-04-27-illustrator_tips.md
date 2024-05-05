# 画面上のActualSize表示が実寸と異なる問題
* メインのPCだと　正しく実寸で表示された　![image](https://github.com/jamad/jamad.github.io/assets/949913/5d27f4e4-0cec-4735-93d0-7722ac6f879d)　問題が発生する環境はM720QをHPZ17nで表示する場合だ。
* 問題の解決を試みる。＞＞ 結局、88%にして 実寸表示の代わりにすることにした。能書きよりも、結果が正しくなるものを見つけるのが一番早かったのだ。
* 以下、役に立たなかった能書き。
  * 72ppi で100%になるようにIllustratorが設定されているらしい。つまり x ppi ならば x/72*100 % にすればいいとのこと
  * WindowsPCの解像度をCMDで知る方法　`wmic path Win32_VideoController get CurrentHorizontalResolution,CurrentVerticalResolution`
  * だが、結局物理的に表示エリアのサイズを測るのがアナログのため、公式情報を得るのが一番早い。HP Z27n　のモニターの場合（2560 x 1440、PanelActiveArea　59.67 x 33.56 cm、てゆーかPPIが　108.8　と記載　）
  * 72 :100=108.8 : x なので、 x=72/108.8*100 かと思ったが、それだと６６％になる。108.8/72*100 だと１５１％になる。どちらも全然８８％からは程遠い。

# 全ての文字列を一括で置換する
* 「編集」＞「検索と置換」で実行できる　
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/99f49849-8901-420a-867c-f90a77538cdc)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/04a53f53-e388-41c4-9f46-a40d45cca52b)


# 用紙の向きの変更（A4縦をA4横に変更）が面倒だった。
* 解決方法は、Artboard をwindow から開き、右端の用紙のようなボタン（アートボードツールと呼ばれている？）を押してアートボードオプションと呼ばれるダイアログを開いたら見つかった。
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/73506b92-b3ec-4658-b8a1-79579f57d10e)



# 縦書きの文字を入力する方法　
* ファイル　`project_github\project_lasercutter\project2024Feb01_string_pierce\草稿.ai`
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/21550e1f-ec30-4399-9b83-3d0feadddf43)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/34a9f7ee-e112-455c-90ef-fc3dde514161)


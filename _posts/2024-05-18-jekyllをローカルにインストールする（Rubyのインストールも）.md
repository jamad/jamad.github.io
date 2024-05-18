<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

# てゆーか　jekyll の前に Ruby をインストールする必要あるんかい！


|手順|参考画像|
|-|-|
|ruby が入っているかを確認したら、入ってなかった|![image](https://github.com/jamad/jamad.github.io/assets/949913/dc437b23-81ff-4f23-bc0b-b3155ae0b2ac)|
|ダウンロードサイトへ行き、おすすめのバージョンをダウンロード|![image](https://github.com/jamad/jamad.github.io/assets/949913/31bad4b1-6d26-4cae-a968-9fe2e2b1ba8f)|
|exeをダウンロードしたら警告が|![image](https://github.com/jamad/jamad.github.io/assets/949913/642d8693-305c-41f1-b477-d2cab9da4981)|
|KeepAnywayを選択|![image](https://github.com/jamad/jamad.github.io/assets/949913/fb40fda2-f80a-4a8a-9e11-d89b6dd3c47c)|
|インストールは全てデフォルト。パスの追加がオンを確認した|![image](https://github.com/jamad/jamad.github.io/assets/949913/27d42233-920e-4274-89c7-8e7fa8f1cda1)|
|Finish直前のオプションもデフォルトがオンになっているのを確認した|![image](https://github.com/jamad/jamad.github.io/assets/949913/b57bc822-3f27-4235-a5eb-d0232c30a0f4)|
|こんなのが起動するので、最初はデフォルトのままEnterでいいらしい <br><br>MSYS2 base system: 基本的なUnixライクな環境<br><br>MINGW development toolchain: CおよびC++のコンパイラ等の開発ツール|![image](https://github.com/jamad/jamad.github.io/assets/949913/50292012-c971-47fa-81b4-89902c9e8457)|
|後に分かったが ridk install を実行すると同様に起動できるようだ|![image](https://github.com/jamad/jamad.github.io/assets/949913/cf428a5d-ee0d-4a9f-b30a-c9450be80eb5)|
|インストールが終わるとメッセージが。Enterを押したら閉じた。|![image](https://github.com/jamad/jamad.github.io/assets/949913/2c337a3b-7201-4499-b2d6-594014d97068)|
|ちゃんとインストールされていることを確認した|![image](https://github.com/jamad/jamad.github.io/assets/949913/c2ff6be5-27ae-4bbd-a6b0-94b6eee43dd8)|
|gemのインストールも確認した|![image](https://github.com/jamad/jamad.github.io/assets/949913/67fa8bab-cf3d-4d68-8948-50c856303e4f)|
|"C:\Ruby32-x64\msys64\mingw64.exe"　を起動して　pacman -V を確認した|![image](https://github.com/jamad/jamad.github.io/assets/949913/ea52e651-b34d-481b-a50e-5b67213ad638)|
|ridk enable　はした方が良かった。何故なら mingw64.exe が　Startメニューに見つからないから。cmdで実行できた方が楽だ。|![image](https://github.com/jamad/jamad.github.io/assets/949913/69f2822a-3a4c-467f-93ed-27d59bdbdd88)|
|cmd で pacman -V の実行を確認できた|![image](https://github.com/jamad/jamad.github.io/assets/949913/fe55aef7-ca5f-4d3d-b712-474d56e435a2)|
|でも mingw64 は cygwin みたいで使いやすいかも！|![image](https://github.com/jamad/jamad.github.io/assets/949913/02b065a4-1f5f-409a-b3e9-dbaf8ae9b6b5)|





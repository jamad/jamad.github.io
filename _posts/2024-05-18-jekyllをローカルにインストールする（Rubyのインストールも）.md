<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

# （二回目以降）インストール後にすべきアクション
* 先日、環境を作成したので、実際に運用しようとした時のメモ

|手順|参考画像|
|-|-|
|cmd にて`ruby -v`を確認|ruby 3.2.4 と表示されたので `ridk install` する必要も無し|
|cmd にて`ridk enable` と続けた　| `pacman -V`　で正しいアスキーアートが出力されることを確認した|
|mingw64　を起動して `explorer .` で開いたhomeで cmd し直してから　`bundle exec jekyll s` |しばらく待つ|



# （初回）てゆーか　jekyll の前に Ruby をインストールする必要あるんかい！

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
|gemコマンドが利用できるようになったので、まずは bundler を入れる。 python のpip みたいなもののようだ　gem install bundler|![image](https://github.com/jamad/jamad.github.io/assets/949913/5694505a-4a64-4bfa-a4e7-13128222f2cf)|
|rootがどこか分からなかったが、C:\Ruby32-x64\msys64\home\jamad　であることが分かった|![image](https://github.com/jamad/jamad.github.io/assets/949913/f9ee4fe0-ec4e-4a0a-b3a1-8e8057f3eb68)|
|そこにGemfile　を作成し　インストール内容を記述した|![image](https://github.com/jamad/jamad.github.io/assets/949913/915dfb15-1fd7-4e69-a6c2-b049734e5fa8) <br> ![image](https://github.com/jamad/jamad.github.io/assets/949913/b9987910-e7d7-4112-ab28-fd71da9349e4)|
|そこで　cmdを開き、bundler のコマンドを実行した|![image](https://github.com/jamad/jamad.github.io/assets/949913/0e7b00ed-bdf3-48c4-b255-c4c55bf2e40d)|
|インストールが終了した時の様子はこんな感じ　|![image](https://github.com/jamad/jamad.github.io/assets/949913/f8513b31-e3ec-48f8-a70d-bc8cfdcd9194)|
|実行するコマンドは`bundle config set path 'vendor/bundle'` 更に`bundle install` なぜなら`bundle install --path vendor/bundle`はdeprecatedだから|![image](https://github.com/jamad/jamad.github.io/assets/949913/d03b70c8-372e-4d39-ae6b-37ceb31061d8)|
|エラーに遭遇| `<internal:C:/Ruby32-x64/lib/ruby/3.2.0/rubygems/core_ext/kernel_require.rb>:38:in `require': cannot load such file -- webrick (LoadError)` |
|解決方法は　webrickを明示的にインストールすることだった |![image](https://github.com/jamad/jamad.github.io/assets/949913/a1569bbc-c50a-4ce2-9071-07974e5a1c52)|
|`bundle install`を実行しなおしたら `bundle exec jekyll s`でエラー出なくなった！|![image](https://github.com/jamad/jamad.github.io/assets/949913/fbb3aa29-d1a2-48e1-9dbe-cc0e7d4789d0)|
|`http://127.0.0.1:4000/`にアクセスすると、こんな状態だった|![image](https://github.com/jamad/jamad.github.io/assets/949913/ade23b5d-d21f-4a13-9774-eef744196c4c)|
|jekyll のバージョンを`bundle exec jekyll -v`で確認できた|![image](https://github.com/jamad/jamad.github.io/assets/949913/e6479c95-d687-4a6d-9a5e-3ea3a2e19ece)|
|新規プロジェクトを作成|![image](https://github.com/jamad/jamad.github.io/assets/949913/9c0847d1-c6cd-45d6-8c7f-18a9748c98af)|
|`bundle exec jekyll s` を実行したらまた別のエラーに遭遇|Could not find gem 'tzinfo-data mingw, x64_mingw, mswin, jruby' in cached gems or installed locally.|
|ああ、gemファイルを確認したら勝手に更新されているじゃないか|![image](https://github.com/jamad/jamad.github.io/assets/949913/fc48e5e1-129d-468f-a5b8-2d057cb5f187)|
|またインストールし直し|![image](https://github.com/jamad/jamad.github.io/assets/949913/f73b468b-46e2-4770-9eba-787f408af2da)|
|結局、また　gem "webrick"　を追加する必要があった。|![image](https://github.com/jamad/jamad.github.io/assets/949913/6ff5f39d-2704-450a-b6f7-e9cef025d851)|
|`bundle install`でインストールし直して　`bundle exec jekyll s` を実行して　http://127.0.0.1:4000/ にアクセスしたら、ついにページを閲覧できた！|![image](https://github.com/jamad/jamad.github.io/assets/949913/403fd1c7-ced8-4073-8373-2d80eb7681fe)|



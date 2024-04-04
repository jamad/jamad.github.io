<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">
 
たまたま見かけたライブラリだが、とても面白いと思ったのでメモしておく。
アイデアの具現化に集中できるよう、スコアやBGMやインプットなどの処理がライブラリで整えられているのが素晴らしい。

# 2024-04-02 もう少し慣れよう。wip
* [https://jamad.github.io/crisp_game_lib/?game002_abc](https://jamad.github.io/crisp_game_lib/?game002_abc)

# 2024-04-01 早速試してみた
* https://abagames.github.io/literate-diff-viewer/pinclimb/index.html?lang=ja は非常に丁寧なチュートリアル。なので、その手順通りに試してみた
* [https://jamad.github.io/crisp_game_lib/?game001_helloworld](https://jamad.github.io/crisp_game_lib/?game001_helloworld) によりゲームをプレイできた
* iphone でも期待通りプレイできた。<img src="https://github.com/jamad/jamad.github.io/assets/949913/b47cbeb7-5f1c-48ac-8106-1e10d38b70d9" width="20%" /> 
* ファイル構成は 最初だけ<img src="https://github.com/jamad/jamad.github.io/assets/949913/8f5cbb92-81b6-4ea7-9fff-690225abf7a7" width="25%" /> の配置が必要で、
  <img src="https://github.com/jamad/jamad.github.io/assets/949913/cce7632e-d5c1-4628-b8c8-6cbbe7d7ed97" width="25%" />のファイルだけで完結できる
* コードの更新は　[main.js](https://github.com/jamad/jamad.github.io/blob/master/crisp_game_lib/game001_helloworld/main.js) のEditでも可能だが、実際はVScodeで編集しつつ、ローカルのindex.htmlを開いた後に`index.html?game001_helloworld`としてRefreshして動作確認してからcommit という手順を繰り返した
* たまに、ブラウザをRefreshしてフリーズした場合はInspectorを表示してエラーメッセージを確認することでデバッグできた。
* 着色は　https://abagames.github.io/crisp-game-lib/ref_document/modules.html　を参考にしてcolorを見つけた。
* サウンドやピクセルレンダリング、画面サイズはoptionに記述するだけで設定できる。素晴らしい。


# 後で読みたいドキュメント
* https://github.com/abagames/crisp-game-lib/blob/master/README_ja.md
* https://abagames.github.io/joys-of-small-game-development/fun_to_make_small_games.html
* https://aba.hatenablog.com/entry/2021/08/08/195706 ワンボタンゲーム
* 凄い数のサンプルだ、、、　すごすぎる
  * <img src="https://github.com/jamad/jamad.github.io/assets/949913/c11f2beb-647d-428b-ab0c-3549e18ea615" width="25%" />
  * https://www.asahi-net.or.jp/~cs8k-cyu/browser.html
 
* また別のTutorial
 * https://github.com/JunoNgx/crisp-game-lib-tutorial



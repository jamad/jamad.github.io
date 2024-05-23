
# cmd での history に該当するコマンド
* `doskey /history` だった
* こんな感じで履歴が表示された。素晴らしい。
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/59e348ec-a2d5-4d72-b9f5-d4ddb8904b12)


# フォルダ内の全ファイル名の文字列を一括で変更
* `PS > Get-ChildItem | Rename-Item -NewName { $_.Name -replace "abc", "def" }` で　abcをdefに変更できる 


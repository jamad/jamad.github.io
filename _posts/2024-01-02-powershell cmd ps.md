# フォルダ内の全ファイル名の文字列を一括で変更
* `PS > Get-ChildItem | Rename-Item -NewName { $_.Name -replace "abc", "def" }` で　abcをdefに変更できる 


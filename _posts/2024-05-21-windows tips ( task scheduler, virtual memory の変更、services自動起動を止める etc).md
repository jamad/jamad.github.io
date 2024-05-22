# windows を軽くするために行ったこと
* wip
* 不要なプログラムを削除する
* 不要なファイルを削除する

# disk cleanup （役立たずな印象）

|メモ  |画像 |
|-|-|
|[old_temp_files_remover.py を作成してみたよ](https://gist.github.com/jamad/ca5da80a168e8a47bd080b5f55dffc87)　実行後にドライブが軽くなったのを確認した|![image](https://github.com/jamad/jamad.github.io/assets/949913/b5648b67-60a0-4488-8b26-6c73ab806c4c) |


# task scheduler  

|メモ  |画像 |
|-|-|
|まず自分で作成したものを明確にできるように、作成日時を冒頭に移動させた。|![image](https://github.com/jamad/jamad.github.io/assets/949913/1710a38c-ade5-495f-b782-029da2721d84)|
|History を確認することは重要　右のようになっていなければToggleすること|　　![image](https://github.com/jamad/jamad.github.io/assets/949913/6f66c2c6-eade-4624-a29a-034981e0d911)




# user account にアイコンを追加した時

|メモ  |画像 |
|-|-|
|画像の追加はここで行った|![image](https://github.com/jamad/jamad.github.io/assets/949913/0f4e780d-c0fe-4bd9-81f1-89282834ae8f)|
|画像を選択した時に、このような凄くエラーっぽいメッセージが出たが、実際には画像が追加された。バグか？|![image](https://github.com/jamad/jamad.github.io/assets/949913/a86f030c-6a46-40f9-a32b-8c35eca4e88e)|
|どうやらバグのようだ|　`https://windowsreport.com/microsoft-confirms-the-0x80070520-account-picture-error-in-windows-11-kb5036980/`|
|%appdata%\Microsoft\Windows\AccountPictures に.png を入れてみた。再起動前でも一応画像は見えていた|![image](https://github.com/jamad/jamad.github.io/assets/949913/47b1e712-1603-48bc-8e91-5458514f2c04)|



# startup にClockを入れた時の方法

|メモ  |画像 |
|-|-|
|%appdata%\Microsoft\Windows\Start Menu\Programs\Startup を開いて、そこにショートカットを作成したら　Startupに表示されるようになったぜ| ![image](https://github.com/jamad/jamad.github.io/assets/949913/cd8b98ac-f86e-4d62-a3e7-202bf855852e)|


# 入力方法がスウェーデン語しかなかったので日本語を追加する

|メモ  |画像 |
|-|-|
|この後に再起動が必要だった。|![image](https://github.com/jamad/jamad.github.io/assets/949913/342be92d-242f-40b9-bc02-96f570b50d99)|
|でも未だにログイン画面がスウェーデン語になったり日本語になったり安定しない。何でだろう？|-|


# Oculus のツールが自動的に起動しないように変更する

|メモ  |画像 |
|-|-|
|servicesを起動して|![image](https://github.com/jamad/jamad.github.io/assets/949913/6b1fa41e-c75d-4ce5-ae2c-a97c8236521f)|
|properties を変更し、manualになれば、次回からは起動しないはず。|![image](https://github.com/jamad/jamad.github.io/assets/949913/65b3a369-9021-4929-bf44-58f0236c2239)|

## virtual memory の変更

|メモ  |画像 |
|-|-|
| win + Pause/Break　＞＞　scroll down to click advanced system settings|![image](https://github.com/jamad/jamad.github.io/assets/949913/6992e4eb-f829-4801-a1ae-a462fc723a55)

<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

# 2023-12-17 更新
* [https://jamad.github.io/wasm/simple_button/](https://jamad.github.io/wasm/simple_button/)
* iOS の画面でもそれなりに合致するような解像度にした
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/72e8d875-ffcc-4506-8f16-b2ae58292628)
* [参考](https://github.com/pygame-web/pygbag)
* [ここもまた見よう](https://github.com/pygame-web/pygame-web.github.io/blob/main/wiki/pygbag-code/README.md)

# pygbag (wasm_webassembly) でpygameをdeploy
* 幾つかのメモ
* browserで勝手に拡大されて画像がぼける
* pygbagのヘルプを見る方法　`pygbag --help 'foldername'`

# まずは結果から。Github pagesでpygameをプレイできた　（問題点は、iOSだと　ReadyToStartを押しても反応せず、描画エリア外を押したら何故か開始するところ）

|playable pygame at [https://jamad.github.io/wasm/simplest_snakegame/](https://jamad.github.io/wasm/simplest_snakegame/)|![image](https://github.com/jamad/jamad.github.io/assets/949913/d0b4b29b-4b2d-4cc1-83ac-15b5289ea13d)|
|-|-|


# pygbag 前のコード変更

|作業のステップ|補足|
|-|-|
|main.py をファイル名にしてpygame作成 [original pygame](https://github.com/jamad/jamad.github.io/commit/b81478935a263176660824928385a67ddc909fb8?diff=unified&w=0)|![image](https://github.com/jamad/jamad.github.io/assets/949913/de710223-ef60-4c0f-96e6-358972bb7f12)|
|コードの加工が終わったら pygbagのステップへ進む　|[diff between before and after](https://github.com/jamad/jamad.github.io/commit/210a7ad0bcecc3d415990180ecc1b1a69433cbd8?diff=split&w=0)|
|加工の為のポイント| asyncio を import する <br> mainloop の構造を下記のように変更する|
  
```
async def main():
  while 1: # main loop
    ...
    await syncio.sleep(0)

asyncio.run(main())
```

## pygbag

|作業のステップ|補足|
|-|-|
|pygbag コマンドの実行|![image](https://github.com/jamad/jamad.github.io/assets/949913/490df2e4-9ed9-4a2e-89a0-89015d911c58)|
|ローカルでの動作を確認|![image](https://github.com/jamad/jamad.github.io/assets/949913/42c50d57-08bc-4688-82d0-87923f5385f9)|
|必要なファイルはbuildフォルダ内に生成されている|![image](https://github.com/jamad/jamad.github.io/assets/949913/63766277-7a2d-4d1f-9df9-27f998f6f002)|
|必要に応じてファイルの階層を変更してgithubにcommitすれば完了|![image](https://github.com/jamad/jamad.github.io/assets/949913/4cdef75e-1694-437f-8590-54c42b45199e)|

* [reference](https://www.youtube.com/watch?v=q25i2CCNvis)https://www.youtube.com/watch?v=q25i2CCNvis 

<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

* [このページの更新用　タイトルが変わるので親階層](https://github.com/jamad/jamad.github.io/tree/master/_posts)

### pinned notes
* numpy　の import は pygame の直後に行うようにした。
* browserで勝手に拡大されて画像がぼけるので、大きめの画面サイズで考える。
* pygbagのヘルプを見る方法　`pygbag --help 'foldername'`
* iOS の場合、なぜか　ReadyToStartのボタンから大きく外れたエリアを押さないと開始しない  `https://github.com/pygame-web/pygbag/issues/138#issue-2011645179`

## 2024-01-15 numpy sample 
* [https://jamad.github.io/wasm/2024-01-15-numpy/](https://jamad.github.io/wasm/2024-01-15-numpy/)
* <img src="https://github.com/jamad/jamad.github.io/assets/949913/df8627ea-41ee-41ac-be1d-a5c6ca6bc1d5" width="12.5%" />
* (問題とその解決)　当初、 実行しても何故か、何も起こらなかった（pygbag のコマンドでローカルサーバでのテストの時から）
  * 結局、`#import tkinter as tk` のようにtkinter を完全コメントアウトし、import を下記の順序にしたらコードが実行された
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/46010d5d-4354-44a3-bbee-0fbd0ad540e1)


## 2024-01-02 未完　movie size changer
* [https://jamad.github.io/wasm/2024-01-02-video_size_changer/](https://jamad.github.io/wasm/2024-01-02-video_size_changer/)
  

## 2023-12-23
* [https://jamad.github.io/wasm/2023-12-23-mandelbrot/](https://jamad.github.io/wasm/2023-12-23-mandelbrot)
* あれ？まだ黒いな  .py で実行した時は、下記のように表示されるのに。もしかしたらpygame.surfarray.pixels3d(screen)が良くないのか？
* <img src="https://github.com/jamad/jamad.github.io/assets/949913/6aecef9a-3df1-4481-900d-945d114e96ec" width="25%" />


* ちなみに、下記はpygame前のmatplotでの事前調査
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/0a2ccab2-3a5f-4559-97ce-0d00923f8fde)
* code

```
import pygame
import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iterations=30):
    z = 0
    for i in range(max_iterations):
        if 2<abs(z):return i
        z=z*z+c
    return max_iterations 

def mandelbrot_set(size=512):
    x=np.linspace(-2    ,1  ,size)
    y=np.linspace(-1.5  ,1.5,size)
    mset=np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            c=complex(x[j],y[i])
            mset[i,j]=mandelbrot(c)
    return mset

plt.imshow(mandelbrot_set(),cmap='hot')
plt.show()
```


* https://jamad.github.io/pygbag_test/
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/93a52565-d14e-44c4-b571-2e9b2e5920c7)


## 2023-12-19 メインを別ファイル化して作業しやすくした　(main.py は触らず、mygame.pyだけを更新)
### 更にモバイルで　指でタップして反応を得た！　player_pos = pygame.mouse.get_pos()　で指の位置ゲット
* [2023-12-19-swipe_action ](https://jamad.github.io/wasm/2023-12-19-swipe_action/index.html)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/3675df6f-c1d5-49b4-b064-d05683d78c32)
* [こちらも　メソッドを更新したらタッチの位置が正しくなった！](https://jamad.github.io/wasm/2023-12-19-touch_action/)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/b8010e57-35e8-4000-bd01-a378d9af49c4)


## 2023-12-18
* [2023-12-18-simpleclock iphone動作確認済](https://jamad.github.io/wasm/2023-12-18-simpleclock/)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/680a1d64-1320-4b0c-8ae5-3a18fb012427)

## 2023-12-17 更新
* [2023-12-17-simple_button](https://jamad.github.io/wasm/2023-12-17-simple_button/)
* iOS の画面でもそれなりに合致するような解像度にした
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/72e8d875-ffcc-4506-8f16-b2ae58292628)
* [参考](https://github.com/pygame-web/pygbag)
* [ここもまた見よう](https://github.com/pygame-web/pygame-web.github.io/blob/main/wiki/pygbag-code/README.md)


<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

# pygbag を使わなくても、python code を .html内部に記述すれば実行はできる (速度が十分かは未検証 更に不要な情報が見え隠れするのはNG )
* 入力したキーを表示するDemo
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/bed98232-1841-4a8f-af52-c1787b44dc7f)
* 加工後
* [after modding](https://jamad.github.io/wasm/pygame-web/pygame_simplest.html)
* 加工前
* [orignal](https://jamad.github.io/wasm/pygame-web/pygame_simplest.py)
* [参考](https://pygame-web.github.io/wiki/pygbag-code/)



## pygbag (wasm_webassembly) でpygameをdeploy

|playable pygame at [https://jamad.github.io/wasm/simplest_snakegame/](https://jamad.github.io/wasm/simplest_snakegame/)|![image](https://github.com/jamad/jamad.github.io/assets/949913/d0b4b29b-4b2d-4cc1-83ac-15b5289ea13d)|
|-|-|

## pygbag 前のコード変更

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


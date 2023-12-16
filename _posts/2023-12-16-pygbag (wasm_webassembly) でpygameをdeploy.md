# 結果
* playable pygame at [https://jamad.github.io/wasm/simplest_snakegame/](https://jamad.github.io/wasm/simplest_snakegame/)

# pygbag 前のコード変更

|作業のステップ|補足|
|-|-|
|main.py をファイル名にしてpygame作成 [original pygame](https://github.com/jamad/jamad.github.io/commit/b81478935a263176660824928385a67ddc909fb8?diff=unified&w=0)|![image](https://github.com/jamad/jamad.github.io/assets/949913/de710223-ef60-4c0f-96e6-358972bb7f12)|
|コードの加工　|[diff between before and after](https://github.com/jamad/jamad.github.io/commit/210a7ad0bcecc3d415990180ecc1b1a69433cbd8?diff=split&w=0)|
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
|-|![image](https://github.com/jamad/jamad.github.io/assets/949913/42c50d57-08bc-4688-82d0-87923f5385f9)|
|-|![image](https://github.com/jamad/jamad.github.io/assets/949913/63766277-7a2d-4d1f-9df9-27f998f6f002)|
|-|![image](https://github.com/jamad/jamad.github.io/assets/949913/4cdef75e-1694-437f-8590-54c42b45199e)|
|-|-|



* [reference](https://www.youtube.com/watch?v=q25i2CCNvis)https://www.youtube.com/watch?v=q25i2CCNvis 

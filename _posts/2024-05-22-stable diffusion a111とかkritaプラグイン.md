# krita の情報は `krita に関するメモ` に移動させよう

* C:\Users\j\AppData\Roaming\krita\ai_diffusion\ がデフォルトだったので、変えた。Cドライブの容量が減りすぎるから。
* vivox でkritaによる生成AIを実行しようと思ったが、そもそも comfiUI がインストールできない感じだ。RAMが８GBは少なすぎるな。今の時代。



# 20240522ymd  Krita のプラグインを試す。

|メモ |画像 |
|-|-|
|とりあえず最新版をインストール|![image](https://github.com/jamad/jamad.github.io/assets/949913/77fb1e14-2b84-43df-9bde-ba7d5fe1622d)|
|plugin（blenderと同様に解凍不要 ） を　`https://www.interstice.cloud/plugin` の手順でインストールしたらKrita再起動|![image](https://github.com/jamad/jamad.github.io/assets/949913/2d05fae0-6ef9-4b66-ae03-819055443ea5)|
|新規画像は512角を選んだ  |![image](https://github.com/jamad/jamad.github.io/assets/949913/a03694a1-eedb-4a17-9f49-5ff0431de334)|
|docker でAI画像生成があるのか。面白い。|![image](https://github.com/jamad/jamad.github.io/assets/949913/fb4dfe1d-1c86-49d4-8734-7bd9294f83ca)|
|dockerは、ほぼパネルなんだな。とにかくconfigureボタンを押してローカルを選択|![image](https://github.com/jamad/jamad.github.io/assets/949913/4c365130-dda1-4e5c-9fb1-d434b5c81323)|
|LocalなのでOKする前に、 サーバーをインストールする必要があった。かなり時間かかるぞ|![image](https://github.com/jamad/jamad.github.io/assets/949913/ac217c34-67c6-41ea-838b-2516404744e8)|
|起動したら 1,2,3,4 の順に変更したら`man in a black suit, standing in a well-lit hotel lobby`　の画像が生成された (参考 `https://www.youtube.com/watch?v=AF2VyqSApjA`)   |![image](https://github.com/jamad/jamad.github.io/assets/949913/ce4c9da6-cd47-4584-9349-a9d1c8950777)|
|次に、Vectorレイヤーを追加してから|![image](https://github.com/jamad/jamad.github.io/assets/949913/a4472a44-3f45-4e7c-99fc-bdeca9bd4806)|
|コントロールレイヤーを追加　（前回の操作により、自動的にVectorレイヤーが参照される ）　poseに切り替えた|![image](https://github.com/jamad/jamad.github.io/assets/949913/6b24b591-b4db-42b3-8dbb-a4407b1be384)|
|うーむ、骨を動かしていたらKritaがフリーズした。放置していたが、戻る気配がないな、、、ログは無いのか？|![image](https://github.com/jamad/jamad.github.io/assets/949913/cb52e0c8-775b-4f53-905a-7c065041266d)|
|後で、見てみよう|`https://youtu.be/AF2VyqSApjA`の続きと `https://www.youtube.com/watch?v=9UyNT_F18Do`|




# controlnet reference_only を使った時のメモ
* txt2img で prompt を通常通り設定
* controlnet に　image を追加 下記パラメータのみ変更した
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/8707a7c5-c630-450a-af53-45ecdd9d81b4)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/71e1df21-81ac-4dad-86e6-c38288b39ade)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/120b2304-53a0-48a2-ade0-6730eea761ce)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/0921146d-8e9a-4c94-a3c5-aa79f5ab7635)


# IP-adapter の使い方 (reference only は似ているが顔に特化しているらしい)
* 特に画像を追加する為に　Upload independent control image　が必要だった　![image](https://github.com/jamad/jamad.github.io/assets/949913/46809d9d-c459-498d-b085-bf09ef1363a7)
* 後は  extensions\sd-webui-controlnet\models に [.pth](https://huggingface.co/lllyasviel/sd_control_collection/tree/main) を入れた後に下記のように選択
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/48f73fe4-f7f2-4c60-afd2-2c6ddf0767d2)
* Controlweight はデフォルトか、それより小さい値がいいかも。0.7とか。0.25とか。試しに1.6にしてみた＞＞結果はイマイチだった。


# AUTOMATIC1111_webui_0824.zip を試す
* zip を解凍
* 1_セットアップ.bat　を実行し、ｙを押して暫く待つ
* 自動的にインターフェースが起動した状態になった

# ComfiUI 試したものの、結果がイマイチだったので一旦中止
* <img src="https://github.com/jamad/jamad.github.io/assets/949913/0ba82b15-1158-4c23-b78d-da46ecec53ce" width="20%">
* see `https://stable-diffusion-art.com/comfyui/#ComfyUI_vs_AUTOMATIC1111`
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/e2cbef15-90a6-45bd-ad19-f028c3be640e)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/6499fa30-35e8-4897-b634-89e43e21588d)

## troubleshooting

#### Problem 2024-01-19 `ValueError: max() arg is an empty sequence`
* reference `https://github.com/Gourieff/sd-webui-reactor/issues/273#issuecomment-1879502934`
* fixed by ![image](https://github.com/jamad/jamad.github.io/assets/949913/397ebcee-986e-41b6-abde-608a922ddb97)


#### Problem 2024-01-18 `TypeError: FaceSwapScript.process() missing 26 required positional arguments: 'img', 'enable', ...`
* 参考　`https://github.com/Gourieff/sd-webui-reactor#iv-attributeerror-faceswapscript-object-has-no-attribute-enable`
* オフに変更して　apply and quit した　![image](https://github.com/jamad/jamad.github.io/assets/949913/a5e96ee2-f3ca-49f3-81ae-0404e80481ac)
* エラー出なくなったので、解決したかな？


#### 解決済　Problem　2023-12-29  `Error: The 'insightface==0.7.3' distribution was not found and is required by the application`
* Solution
  * 準備として　insightface-0.7.3-cp310-cp310-win_amd64.whl　を下記の場所に置く。
    * ![image](https://github.com/jamad/jamad.github.io/assets/949913/7f27197c-63be-45f7-bb14-10196cac1bc8)
  * そして通常のstartのための.batを複製し、同様の手順で進んだ後にpipさせるようにしたらエラー出なくなった
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/f3439a84-243e-4121-bfa2-a24ced383c24)
  * 問題解決後は、通常のスタート.batを起動すると mov2mov のタブの中のControlNet下にReactorが表示された
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/10dbaa9a-ecc7-416c-8d06-c4c3bc639f3d)
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/bf9228c7-cf9e-4e7a-878d-a50947b6add8)






####  解決済　Problem　2023-12-29 `no module 'xformers'. Processing without...`
* Solution
  * 上と同様に
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/15106516-34a7-45dc-90b8-aae5ce137964)
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/5b067cd7-3eca-45bd-8311-77e5ca1a4aa3)

#### 未解決　Problem `No SDP backend available, likely because you are running in pytorch versions < 2.0. In fact, you are using PyTorch 1.13.1+cu117. You might want to consider upgrading.`
![image](https://github.com/jamad/jamad.github.io/assets/949913/f6480ec4-8862-43aa-bbdc-901ed4ee5315)
* Solution >> no, new error
 * 上と同様に  `venv\Scripts\python.exe -m pip install torch==2.0.0+cu118 --extra-index-url https://download.pytorch.org/whl/cu118`
 * ![image](https://github.com/jamad/jamad.github.io/assets/949913/1a7d72a7-228d-4305-9934-36674b9f42e8)
 * いや、待て、下記のエラーが新たに発生するようになったぞ

#### 解決中　Problem　2023-12-29 `python.exe - Entry Point Not Found , The procedure entry point ?get_warnAlways@Warning@c10@@YA_NXZ could not be located in the dynamic link library `
![image](https://github.com/jamad/jamad.github.io/assets/949913/c1b7d67a-2b79-4033-af5d-f300d9b17583)
* Solution
* 下記を試してみた
* pip install --upgrade torch==1.9.0
* pip install --upgrade torchvision==0.10.0

#### 解決済　Problem 2024-01-03 `modules.devices.NansException: A tensor with all NaNs was produced in Unet. This could be either because there's not enough precision to represent the picture, or because your video card does not support half type. Try setting the "Upcast cross attention layer to float32" option in Settings > Stable Diffusion or using the --no-half commandline argument to fix this. Use --disable-nan-check commandline argument to disable this check.`
* 結局、このargsにしたら　GPUを使い解像度も512くらいでも大丈夫だった　`set COMMANDLINE_ARGS= --autolaunch --disable-nan-check --lowvram --precision full --no-half --skip-torch-cuda-test`
* 尚、settingも下記のようにした
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/011b6749-6df5-4d30-9e52-ff6da0ee2e13)


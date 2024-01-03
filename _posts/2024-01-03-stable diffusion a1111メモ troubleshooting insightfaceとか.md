<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# AUTOMATIC1111_webui_0824.zip を試す
* zip を解凍
* 1_セットアップ.bat　を実行し、ｙを押して暫く待つ
* 自動的にインターフェースが起動した状態になった
* 


# ComfiUI 試したものの、結果がイマイチだったので一旦中止
* <img src="https://github.com/jamad/jamad.github.io/assets/949913/0ba82b15-1158-4c23-b78d-da46ecec53ce" width="20%">
* see `https://stable-diffusion-art.com/comfyui/#ComfyUI_vs_AUTOMATIC1111`

## troubleshooting

#### 解決済　Problem　2023-12-29  `Error: The 'insightface==0.7.3' distribution was not found and is required by the application`
* Solution
  * 通常のstartのための.batを複製し、同様の手順で進んだ後にpipさせるようにしたらエラー出なくなった
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/f3439a84-243e-4121-bfa2-a24ced383c24)
  * 問題解決後は、通常のスタート.batを起動すると mov2mov のタブの中のControlNet下にReactorが表示された
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/10dbaa9a-ecc7-416c-8d06-c4c3bc639f3d)
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/bf9228c7-cf9e-4e7a-878d-a50947b6add8)
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/e2cbef15-90a6-45bd-ad19-f028c3be640e)
  * ![image](https://github.com/jamad/jamad.github.io/assets/949913/6499fa30-35e8-4897-b634-89e43e21588d)






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
* 

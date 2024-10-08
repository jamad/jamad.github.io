
# WSL を使うために　windows を virtualization しないといけなかったのでメモ
* 目的は `https://github.com/openai/spinningup/issues/23` 
  

* まず 下記の２つはオンになっていることを確認。

![image](https://github.com/jamad/jamad.github.io/assets/949913/9579aac8-5958-48e7-a3f9-852c636d14bd)

* GPTからの情報の手順でBISOの設定を変更したら

![image](https://github.com/jamad/jamad.github.io/assets/949913/5b324f91-ee55-4c1c-8dbd-572c6e6e1733)

* 期待通りの結果になった。素晴らしい

![image](https://github.com/jamad/jamad.github.io/assets/949913/f5939a09-8c80-4c90-b03b-2362a13b637b)

* ubuntu を起動してみる

![image](https://github.com/jamad/jamad.github.io/assets/949913/e131b052-5051-4cfe-b90e-e11348a78718)

![image](https://github.com/jamad/jamad.github.io/assets/949913/e2ed3225-40ec-49af-98ba-e1242ce1afff)



おまけメモ

![image](https://github.com/jamad/jamad.github.io/assets/949913/b5946f82-c4a7-4483-854b-e33775cab184)

最後のラインに　追加して ctrl+O で保存し、ctrl+X でnanoをエスケープ

![image](https://github.com/jamad/jamad.github.io/assets/949913/bd6b2247-fa91-41f2-8f2a-70e40a0ac439)


windows の　Cドライブに該当する場所に移動するには　`cd /mnt/c` を実行する

![image](https://github.com/jamad/jamad.github.io/assets/949913/9fe40d8a-8fdc-4a6f-a01b-656dc0aeb9a6)

* 改めて　`https://spinningup.openai.com/en/latest/user/installation.html#installing-spinning-up`　の手順を実行してみる

![image](https://github.com/jamad/jamad.github.io/assets/949913/30bc1420-54b3-4e5c-9d30-2b87275a0d85)

* うーん、またエラーか

![image](https://github.com/jamad/jamad.github.io/assets/949913/1829d266-9ca9-4ba9-bcc3-279c1309230e)


GPTからの情報を試す

![image](https://github.com/jamad/jamad.github.io/assets/949913/c81d75d4-0dc0-4bca-afbc-8b7afcc7c27a)

エラーでてるやんけ　`E: Unable to locate package dos2unix`

GPT からの情報を試す

![image](https://github.com/jamad/jamad.github.io/assets/949913/71435c5f-2d59-46ec-bbe5-f1ef5b9e7c51)

おお、エラー出なくなった

![image](https://github.com/jamad/jamad.github.io/assets/949913/389f6748-f21c-4cfc-aaf9-1e1d7a22c57c)


でも、xclock をテストしたらエラーになったぞ。

![image](https://github.com/jamad/jamad.github.io/assets/949913/4479c621-4d11-4bd8-8569-f00f2c5639e2)


![image](https://github.com/jamad/jamad.github.io/assets/949913/598b0a26-6b30-439f-bd37-323128103a37)

サーバーが起動していることは確認した

![image](https://github.com/jamad/jamad.github.io/assets/949913/b1f28c17-c455-4b1e-9eb9-77d838832984)


firewall の確認もした

![image](https://github.com/jamad/jamad.github.io/assets/949913/36ca8f76-885f-42af-a3de-6680a4f597f9)


---

* とりあえず
* ` https://sourceforge.net/projects/xming/files/latest/download` から　Xming-6-9-0-31-setup.exe　を実行してみることにした


![image](https://github.com/jamad/jamad.github.io/assets/949913/5a4de3fb-f976-4fdf-806d-edc29e02edde)

![image](https://github.com/jamad/jamad.github.io/assets/949913/1ac2718f-4e89-4416-82e0-7cf91fe5e5d6)
![image](https://github.com/jamad/jamad.github.io/assets/949913/b56776af-99ed-42fb-a5ce-8fabcd18b1cc)

![image](https://github.com/jamad/jamad.github.io/assets/949913/87611f9a-fa06-4072-b930-3c6ae1911573)


* どうも　xming は WSLに必要なツールのようだ。

![image](https://github.com/jamad/jamad.github.io/assets/949913/79ee38f8-c7c9-4f2e-a627-6c3521314a5e)


# まとめ
* openai_gym を初めて聞いたので試していくうちに、`spinningup.openai.com` に教材があることを知る。そして windows は公式にサポートされていないので、WSL でLinux環境を作ることに。 

# 参考にする資料
* `https://qiita.com/ishizakiiii/items/75bc2176a1e0b65bdd16`
* `https://qiita.com/shu223/items/a9cfe9107447b327b564`
* `https://qiita.com/goodboy_max/items/f11bc4bd71e0e2e1cd37`
* `https://qiita.com/God_KonaBanana/items/c2cee09bc35cca722f2b`
* `https://qiita.com/nsd24/items/7758410128872d684e05`

* `https://spinningup.openai.com/en/latest/index.html` という学習サイトを知ったぞ。


## まず行ったのはpip

|![image](https://github.com/jamad/jamad.github.io/assets/949913/3085220e-1b09-47b1-9eaa-6021539b8982)|
|-|

|![image](https://github.com/jamad/jamad.github.io/assets/949913/73a03e1e-e323-4c4c-b2cf-0bd4389ad52d)|
|-|

* てゆーか、先にすべきはこっちだったかも？

|![image](https://github.com/jamad/jamad.github.io/assets/949913/36863790-682d-486b-8d4d-b1365aa7278e)|
|-|

|![image](https://github.com/jamad/jamad.github.io/assets/949913/a4684ea7-6b36-4ebd-ada0-2bbc52dae4c7)|
|-|

|![image](https://github.com/jamad/jamad.github.io/assets/949913/89d4473a-24ba-41c1-aed8-79fff2ca6d2b)|
|-|

* `cartpole.py` を見つけた。なぜなら　`https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py` がパスだから

|![image](https://github.com/jamad/jamad.github.io/assets/949913/5ff8705f-a2d0-484d-8acb-86d2cf73a9ae)|
|-|

* でも　`cartpole.py` を実行したが、何も起こらない。エラーすら発生しない。何故だろう？

|![image](https://github.com/jamad/jamad.github.io/assets/949913/7250c03f-c027-4ed9-93f1-9d6507032445)|
|-|

* デバッグメッセージを追加してみたが、どうやら2回起動している。そしてどちらも最終的にはCloseしているぞ？

|![image](https://github.com/jamad/jamad.github.io/assets/949913/9f195fe9-b78c-4916-9761-a9edde3517c1)|
|-|
  
* `pip3 install gym[all]`してみることに

  
---

* spinningup というサイトを知ったので、最初から、別のディレクトリを作成して試してみることに。 

|![image](https://github.com/jamad/jamad.github.io/assets/949913/9146a28b-ad18-4866-aae0-55676b301d28)|
|-|

* そして　`ERROR: No matching distribution found for tensorflow<2.0,>=1.8.0` に遭遇

|![image](https://github.com/jamad/jamad.github.io/assets/949913/75c25224-a551-4358-9474-22fd17dc2d72)|
|-|


* `D:\self_development_spinningup\spinningup>pip install tensorflow .` を試したら

![image](https://github.com/jamad/jamad.github.io/assets/949913/3fefc9c1-9445-442a-9b75-e74ed0196c91)

---

だめだ、公式のドキュメントに従おう
* そして `https://github.com/openai/spinningup/issues/23` を見つけた。Windowsで実行するには重要そうだぞ！ 
* まず admin で `wsl --install`
![image](https://github.com/jamad/jamad.github.io/assets/949913/1349d4b2-096f-458c-8317-f0245bd6eb27)



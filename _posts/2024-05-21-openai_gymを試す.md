https://gymnasium.farama.org/environments/classic_control/mountain_car/<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">


|起動できるゲームのリスト|　https://gist.github.com/jamad/03e13abf5e1ab122ba578020957bfdcf|
|-|-|
|てゆーか、[gym は　Gymnasium に移行している](https://github.com/openai/gym?tab=readme-ov-file#the-team-that-has-been-maintaining-gym-since-2021-has-moved-all-future-development-to-gymnasium-a-drop-in-replacement-for-gym-import-gymnasium-as-gym-and-gym-will-not-be-receiving-any-future-updates-please-switch-over-to-gymnasium-as-soon-as-youre-able-to-do-so-if-youd-like-to-read-more-about-the-story-behind-this-switch-please-check-out-this-blog-post)んだよな。また、そちらをやり直した方が将来的には近道なのかもしれない。|例えば　`Pooyan-v0`を試そうとして　`https://stackoverflow.com/q/63080326` に遭遇した。|
|`https://qiita.com/ishizakiiii/items/5eff79b59bce74fdca0d#q-learning` は図になっているので理解の助けになりそう|![image](https://github.com/jamad/jamad.github.io/assets/949913/31077af8-2715-4fb5-b2f8-cf9a8515ef45)|
|20240522ymd `pip install gymnasium`を実行した|![image](https://github.com/jamad/jamad.github.io/assets/949913/62399012-f5eb-48b0-be53-ad7da4364a33)|
|`InvertedDoublePendulum-v4`を試した時、mujoco のインストールは `pip install gymnasium[mujoco]`を指示通りに実行したが、まだエラーに遭遇した。<br><br>最終的に`pip install mujoco==2.3.7 `で解決したぞ|![image](https://github.com/jamad/jamad.github.io/assets/949913/c15e98a9-4dd8-4cfb-ad2b-514e84e9090c)|
|自動でなく手動でゲームをプレイするには`python C:\Users\jamad\.pyenv\pyenv-win\versions\3.10.9\Lib\site-packages\gymnasium\envs\box2d\car_racing.py`をすれば良かった|![image](https://github.com/jamad/jamad.github.io/assets/949913/397a6ffb-706d-4708-b9eb-6b86ab2ed0cd)<br>![image](https://github.com/jamad/jamad.github.io/assets/949913/83f6030b-9c35-4c21-b0c9-ae958cffffc4)|
|gymnasium の場合は　MountainCar-v0 のドキュメントは`https://gymnasium.farama.org/environments/classic_control/mountain_car`だった|![image](https://github.com/jamad/jamad.github.io/assets/949913/7403f42e-3945-48e8-acff-4b962fe3d271)|



 

# まとめ 2nd version
* 1stの流れからして、動くようになった最短の手順はおそらく下記のようになるだろう　（Windows11, Python 3.10.9, cmdにてコマンドを実行）
* `https://spinningup.openai.com/en/latest/user/installation.html#installing-spinning-up` の手順を`ERROR: No matching distribution found for tensorflow<2.0,>=1.8.0`に遭遇するまで進める
* [setup.py を変更](https://gist.github.com/jamad/49bfad5731e973d286438f622fdde972)　して　再び　`pip install -e .` を実行


# まとめ 1st version
* 結局、一番参考になった情報は　`https://stackoverflow.com/a/46739299`
  * メインマシンでも試した
  * `pip install -f https://github.com/Kojoley/atari-py/releases atari_py` してから
  * `pip install git+https://github.com/Kojoley/atari-py.git`　したが、これだけだと　`gym.error.NameNotFound: Environment SpaceInvaders doesn't exist.`
  * `pip install gym[atari]` をしたが、今度は`gym.error.Error: We're Unable to find the game "SpaceInvaders". Note: Gym no longer distributes ROMs`
  * なので、もう一度　`https://spinningup.openai.com/en/latest/user/installation.html#installing-spinning-up` の手順を行い　`ERROR: No matching distribution found for tensorflow<2.0,>=1.8.0`までを確認した
  * そして　setup.py の中を　`'tensorflow', 'torch',`のようにバージョンを削ったものにしてから、再び　`pip install -e .` を実行 `error: command 'swig.exe' failed: None` に遭遇
  * `pip install swig` を実行してから再び　`pip install -e .` を実行　`Failed to build matplotlib` に遭遇
  * setup.py の中を `'matplotlib',`のようにバージョンを削ったものにしてから、再び　`pip install -e .` を実行
  * この段階で、やっと`pip install -e .`のコマンドでエラーが出なくった　![image](https://github.com/jamad/jamad.github.io/assets/949913/49f1372d-0e90-4472-b671-3d3bea64c9db)
  * そして　`W:\openai_gym>python MountainCar-v0.py` のようにして　[ゲームの起動コード](https://gist.github.com/jamad/20d537edc3ab887dbb24e0f0432e6928)が作動するようになった　![image](https://github.com/jamad/jamad.github.io/assets/949913/7eefc88c-7615-4466-9e32-e65baf26f89e)


* `https://github.com/Kojoley/atari-py`
* invader 等が起動するようになった今、やっと
  * `https://github.com/openai/gym/wiki/Pendulum-v1`とか
  * `https://qiita.com/ishizakiiii/items/75bc2176a1e0b65bdd16`とか
  * `https://qiita.com/nsd24/items/7758410128872d684e05`とか
  * `https://uu64.hatenablog.jp/entry/2018/05/13/233959` に注目できるようになった
* `https://www.youtube.com/watch?v=gMgj4pSHLww` の動画も参考になるかもしれない (`https://gymnasium.farama.org/content/basic_usage/` という派生も今日知った)
* `https://github.com/pybox2d/pybox2d` も個別に興味がわいた


## 次の日 再びチャレンジ
* "D:\self_development_spinningup\spinningup\setup.py" の中でバージョンを削ってみた
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/40e316ab-947c-4335-bf73-36066e5b35a3)
* `pip install -e .`を実行したら　`error: command 'swig.exe' failed: None` に遭遇したので、`pip install swig` してみた
* `pip install -e .`を実行したら  ` ERROR: Failed building wheel for matplotlib` に遭遇したので　`==3.1.1` を削った　（"D:\self_development_spinningup\spinningup\setup.py"）
* 結局　![image](https://github.com/jamad/jamad.github.io/assets/949913/9381066c-dd92-4de9-ad90-2b067ac1ddcd)
* 先に進めたので `python -m spinup.run ppo --hid "[32,32]" --env LunarLander-v2 --exp_name installtest --gamma 0.999` を実行してみた。 
* 暫く経過して　エラーが発生　`ImportError: DLL load failed while importing MPI: The specified module could not be found.` なので　`pip install mpi4py`を実行したが `Requirement already satisfied: mpi4py`
* `https://stackoverflow.com/a/54907810` を見つけたので　`https://www.microsoft.com/en-us/download/details.aspx?id=105289` から`msmpisdk.msi` をダウンロードした
* `pip uninstall mpi4py` してから`msmpisdk.msi` を実行したが　今度は `ModuleNotFoundError: No module named 'mpi4py'` 認識されていないようだ。
* `https://stackoverflow.com/a/57781714` を見つけたので　色々試すが、解決方法は不明だった。
* `pip install -e .` をもう一度実行した。 そして`python -m spinup.run ppo --hid "[32,32]" --env LunarLander-v2 --exp_name installtest --gamma 0.999` を実行。 解決せず。
* だめだ、一旦中止する。
* ちょい待て　`https://stackoverflow.com/a/46739299` を見つけたので　`pip install git+https://github.com/Kojoley/atari-py.git` を実行してみた
* そして　![image](https://github.com/jamad/jamad.github.io/assets/949913/98134f3e-ca5c-43b5-a536-1eadb592ff9e)
* おお、起動できたぞ！　![image](https://github.com/jamad/jamad.github.io/assets/949913/fb2cd0cd-ce60-4586-9014-e48228dea8fa)
* env = gym.make('CartPole-v0') に変更すると別のゲームになった


---
# 以下は古い情報 (紛らわしくなる前に削除しよう)

* もう一度やってみる
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/3be28cf1-d452-4397-9b4a-032e0b28e2b7)
* やっぱり同じエラーだ

```
ERROR: Could not find a version that satisfies the requirement tensorflow<2.0,>=1.8.0 (from spinup) (from versions: 2.8.0rc1, 2.8.0, 2.8.1, 2.8.2, 2.8.3, 2.8.4, 2.9.0rc0, 2.9.0rc1, 2.9.0rc2, 2.9.0, 2.9.1, 2.9.2, 2.9.3, 2.10.0rc0, 2.10.0rc1, 2.10.0rc2, 2.10.0rc3, 2.10.0, 2.10.1, 2.11.0rc0, 2.11.0rc1, 2.11.0rc2, 2.11.0, 2.11.1, 2.12.0rc0, 2.12.0rc1, 2.12.0, 2.12.1, 2.13.0rc0, 2.13.0rc1, 2.13.0rc2, 2.13.0, 2.13.1, 2.14.0rc0, 2.14.0rc1, 2.14.0, 2.14.1, 2.15.0rc0, 2.15.0rc1, 2.15.0, 2.15.1, 2.16.0rc0, 2.16.1)
ERROR: No matching distribution found for tensorflow<2.0,>=1.8.0
```

*　今回試したのは  `Python 3.10.9` をキープするのを優先した作業
* `pip install --upgrade spinup`
* `pip install tensorflow`
* `pip install spinup`
* `pip install -e .`


---


# まとめ
* openai_gym と、その教材に該当する`spinningup.openai.com` を知る。
* だが windows は公式にサポートされていないので、WSL でLinux環境を作ることに。
* WSL をインストールしたが bash が使えない。下記のようなエラーでストップ中 

```
C:\Windows\System32>wsl --install
Ubuntu is already installed.
Launching Ubuntu...
Installing, this may take a few minutes...
WslRegisterDistribution failed with error: 0x80370102
Please enable the Virtual Machine Platform Windows feature and ensure virtualization is enabled in the BIOS.
For information please visit https://aka.ms/enablevirtualization
Press any key to continue...
```

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

* 再起動が必要なのかよ！
|![image](https://github.com/jamad/jamad.github.io/assets/949913/11d4c871-4a3d-472b-9da4-7c96779d1d3e)|
|-|

* 再起動した後に開けるよう　リンクをメモ 
* `https://spinningup.openai.com/en/latest/user/installation.html#installing-spinning-up`
* `https://github.com/openai/spinningup/issues/23`
* `https://qiita.com/coffee_g9/items/b5789a7e3b555122f079`

* 再起動してもエラーで進めない。

chatgpt に聞いたが　既に、オンになっている
  ![image](https://github.com/jamad/jamad.github.io/assets/949913/d3e768d0-e13b-4420-9954-e62477f27fff)

![image](https://github.com/jamad/jamad.github.io/assets/949913/a786e85f-cee4-43ab-bc9f-88726b05cf20)

後で試すことに。

でも、とにかくタスクマネージャーで確認したら、仮想化がオンになってないやんけ！
![image](https://github.com/jamad/jamad.github.io/assets/949913/2d4f5032-08d1-4c2c-be8c-3ea8c8f9b62d)

[BIOSの設定変更で、目的を達成できた。](https://github.com/jamad/jamad.github.io/blob/master/_posts/2024-05-20-windowsPC_virtualization%E3%82%92%E3%82%AA%E3%83%B3%E3%81%AB%E3%81%97%E3%81%A6ubuntu%E3%82%92%E5%88%A9%E7%94%A8%E5%8F%AF%E8%83%BD%E3%81%AB%E3%81%97%E3%81%9F.md)

---

別の方法を模索。gpt に聞いた時のメモ通りにやってみる　　　まずは、PRIME B450M-A のマシンにて　cmdで直接`pip install gym`

![image](https://github.com/jamad/jamad.github.io/assets/949913/81629b49-35fb-4f18-a588-69577e4a95a2)

![image](https://github.com/jamad/jamad.github.io/assets/949913/f3d036cd-31b5-445e-bc05-23fa2c39d705)


---

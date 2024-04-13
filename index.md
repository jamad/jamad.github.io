<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

* styleを適用している理由はiOSのデフォルトSafariでダークモードにならないから

* github . による dithub.dev モード（テンキーのピリオドでの起動が楽）はプレビューを見るのに便利(.md ファイルだけ？)　特に共有PCでのincognito mode とかで使えそう
  * 右上のここでpreviewを開けた　![image](https://github.com/jamad/jamad.github.io/assets/949913/373dca2f-3872-465f-9245-2d8693d9cddd)


# このindex.htmlの更新方法 
1. [index.md](https://github.com/jamad/jamad.github.io/edit/master/index.md)　から編集 (index.html が既存だと index.md が上書きできないので削除)
1. [jekyllのconversion完了を待つ](https://github.com/jamad/jamad.github.io/actions)
1. [https://jamad.github.io](https://jamad.github.io/)を再読み込みして確認。Chromeなら `ctrl+shift+R` でキャッシュクリア可能。

---

# 新規postの方法
* pc の場合 : [_posts](https://github.com/jamad/jamad.github.io/tree/master/_posts) > add file
* iOS app の場合 : profile > pinned repo > code > _posts > create file as yyyy-mm-dd-title.md > commit > wait

# コピーボタン各種
* [codepen](https://codepen.io/your-work/) で動作確認したhtmlを.mdに記述し、jekyllで実装するのが最も効率良い
  
<button onclick="copyT()" id="buttonlabel">dummy</button>

<script>
  str_to_copy=new Date().toISOString().slice(0,10)+'-';
  document.getElementById("buttonlabel").textContent='post用prefixのコピーボタン : '+str_to_copy;
  function copyT() {navigator.clipboard.writeText(str_to_copy);}
</script>

<button onclick="copyText2()"><span id="mystr">dummy</span></button>

<script>
  mystr= '<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">';
  document.getElementById("mystr").innerText ='CSSタグをコピーするボタン : '+mystr;
  function copyText2() { navigator.clipboard.writeText(mystr);}
</script>

<input type="text" id="my_userInput"> <button onclick="copyT2()" id="buttonlabel2">urlで画像をwidth=25%表示させるタグをコピーするボタン</button>
<script> 
 //example :  https://jamad.github.io/jam_clock_icon.png
 userInput = document.getElementById("my_userInput");
 // input要素の内容が変化した時に実行される関数を定義
 userInput.addEventListener("input", function() {  document.getElementById("buttonlabel2").textContent = `<img src="${userInput.value}" width="25%">`});
 function copyT2() {navigator.clipboard.writeText(document.getElementById("buttonlabel2").textContent);}
</script>

---

* javascript による簡易時計
<p id="tm"></p>
<script>
f=(x)=>String(x).padStart(2,'0');
g=(d=new Date())=>`${f(d.getHours())}:${f(d.getMinutes())}:${f(d.getSeconds())}`;
u=()=>document.getElementById('tm').textContent=g();
setInterval(u,1000);
</script>

---

* [日々のメモ](https://jamad.github.io/%E6%97%A5%E3%80%85%E3%81%AE%E3%83%A1%E3%83%A2)





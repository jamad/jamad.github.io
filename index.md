<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

<img height="160" alt="{FCE24642-BBA5-4C76-B288-096410F19060}" src="https://github.com/user-attachments/assets/c794ccb3-ddaf-449f-9c65-debe0b4931bd" />　[jamad.github.io/graviton/](https://jamad.github.io/graviton/)



todo here !

### note 
* the reason why I use style here is because I cannot read this page in  Dark mode on iOS Safari 

# このindex.htmlの更新方法 
1. [index.md](https://github.com/jamad/jamad.github.io/edit/master/index.md)　から編集 (index.html が既存だと index.md が上書きできないので削除)



# the following is a quicktest for svg tag

<svg width="100%" height="200">
  <circle cx="0" cy="100" r="20" fill="blue">
    <animate attributeName="cx" from="0" to="100%" dur="5s" repeatCount="indefinite" />
  </circle>
</svg>

* javascript による簡易時計
<p id="tm"></p>

<script>
  str_to_copy=new Date().toISOString().slice(0,10)+'-';
  document.getElementById("buttonlabel").textContent='post用prefixのコピーボタン : '+str_to_copy;
  function copyT() {navigator.clipboard.writeText(str_to_copy);}
  
  mystr= '<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">';
  document.getElementById("mystr").innerText ='CSSタグをコピーするボタン : '+mystr;
  function copyText2() { navigator.clipboard.writeText(mystr);}
  
  //example :  https://jamad.github.io/jam_clock_icon.png
  userInput = document.getElementById("my_userInput");
  userInput.addEventListener("input", function() {  document.getElementById("buttonlabel2").textContent = `<img src="${userInput.value}" width="25%">`}); // input要素の内容が変化した時に実行される関数を定義
  function copyT2() {navigator.clipboard.writeText(document.getElementById("buttonlabel2").textContent);}

  // 簡易時計
  f=(x)=>String(x).padStart(2,'0');
  g=(d=new Date())=>`${f(d.getHours())}:${f(d.getMinutes())}:${f(d.getSeconds())}`;
  u=()=>document.getElementById('tm').textContent=g();
  setInterval(u,1000);
</script>

---






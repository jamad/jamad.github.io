<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />


# https://codepen.io/jamad/pen/MWRgvqZ をここに表示してみる　
* expected result ![image](https://github.com/jamad/jamad.github.io/assets/949913/e23d4041-14a8-40be-952f-253c5128a7ea)
* css は `<style>`(body部分は全体に影響するので外した) , javascript は`<script>` に入れるように記述した。 ```html で　コード全体をマークしたら、ソースコード表示になってしまったので、外した。`コードここから` と  `コードここまで` で可視化してみた。

`コードここから`
<div class="health-bar">
  <div class="inner-bar" id="health"></div>
</div>

<style>
.health-bar {
  width: 200px;
  height: 10px;
  background-color: #500;
  border: 1px solid #666;
}

.inner-bar {
  width: 100%;
  height: 100%;
  background-color: #050;
  transition: width 0.5s ease;
}
</style>

<script>
let currentHealth = 100.0;
function takeDamage() {
  currentHealth -= 20;
  if (currentHealth <= 0) {
    currentHealth = 0;
  }
  updateHealthBar();
}
function updateHealthBar() {
  const healthBar = document.getElementById('health');
  healthBar.style.width = currentHealth + '%';
}

function damageLoop() {
  setInterval(function() {   
    if (currentHealth === 0) {
      currentHealth = 120; // 100 だと何故かフルにならないので
      updateHealthBar();
    }
    takeDamage();// can keep 0 health
  }, 1000);// every second
}

// ページが読み込まれたときにダメージループを開始
window.onload = function() {
  damageLoop();
};
</script> 

`コードここまで`


# my works
* [https://codepen.io/your-work/（Github でログイン）](https://codepen.io/your-work/)
* [文字列内の全ての{}を()に置き換え](https://codepen.io/jamad/pen/NWmwpVm)

# font awesome
* clicking the icon can copy it into the clipboard
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/71db6ccb-39a4-4fb0-99a3-99eb71c6b0c4)


# maze 2024-01-05
* [https://jamad.github.io/codepen_porting/maze](https://jamad.github.io/codepen_porting/maze)
* [by maze.md](https://github.com/jamad/jamad.github.io/blob/master/codepen_porting/maze.md)
* <img src="https://github.com/jamad/jamad.github.io/assets/949913/7a6d3d40-18c4-440d-9d1a-4a6f7bc4dae4" width="160" />
---

# image adjuster
* [https://jamad.github.io/mytools/image_adjuster](https://jamad.github.io/mytools/image_adjuster)
* <img src="https://github.com/jamad/jamad.github.io/assets/949913/e50d8a56-59ec-4641-ad1f-594abe37cba1" width="160" />
* 研究過程　[https://codepen.io/jamad/pen/RwdPbmw](https://codepen.io/jamad/pen/RwdPbmw)

# image filter
* [https://codepen.io/jamad/pen/ExMadmE](https://codepen.io/jamad/pen/ExMadmE)
* <img src="https://github.com/jamad/jamad.github.io/assets/949913/1cb81a0f-03ab-406e-9333-aa9ab63654f0" width="160" />

# 2024-01-04 https://codepen.io/jamad/pen/ZEPQrrQ

---

# practice
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/50f1390a-13fc-4a7d-a750-847e7034cbfa) 001 [https://codepen.io/jamad/pen/yLwBzrQ](https://codepen.io/jamad/pen/yLwBzrQ)

---

# 簡易メモ (Local storage を使ったメモ)
* [試作（完了）](https://codepen.io/jamad/pen/wvOBJwE?editors=1000)
* textarea に文字を入力してSaveするとmemoをkeyとしたlocalstrageというDictにValueが保存される
* clear ボタンは　textareaの中を消去するだけ
* loadボタンは　DictのValueをtextareaに表示する

<head><meta charset="UTF-8"></head>

<input id="clear" value="Clear" type="button" onclick="clearMemo()">
<textarea id="memo" rows="4" cols="32" name="memo"></textarea>
<input id="save" value="Save" type="button" onclick="saveMemo()"> 

<hr>
保存されたデータ
<input id="load" value="Load" type="button" onclick="loadMemo()"> 
<div id="display"></div>

<script>
  memoInput = document.getElementById("memo");
  clearMemo=()=>memoInput.value = "";
  
  displayDiv = document.getElementById("display");
  
  memoInput.value = localStorage.getItem("memo");
  if (memoInput.value)displayDiv.innerHTML = `${localStorage.getItem("memo")}`;
  
  function saveMemo() {
    localStorage.setItem("memo", memoInput.value);
    displayDiv.innerHTML=`${localStorage.getItem("memo")}`;
    if (localStorage.getItem("memo")=='') displayDiv.innerHTML = "No saved memo found yet!";
  }

  function loadMemo() {
    memoInput.value = localStorage.getItem("memo");
    if (memoInput.value==''){ displayDiv.innerHTML = "No saved memo found yet!";}
    else{displayDiv.innerHTML=`${memoInput.value}`;}
  }

</script>


---

# 2023-12-24  日時表示
* https://codepen.io/jamad/pen/yLwyMEe

<p id="mytime"></p>
<script>
opt=Object.fromEntries(['year','month','day','hour','minute','second'].map(k=>[k,'numeric']));
d=(t = new Date())=>t.toLocaleDateString('en-US',opt);
ut=()=> document.getElementById('mytime').innerHTML=d();
setInterval(ut, 500);
</script>

# 現在の日時を表示
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/18f44f87-42b1-4fa3-b91f-71726a1d20ee)
* https://codepen.io/jamad/pen/XWGJWro
```html
<span id="datetime"></span>
<script>
dateOptions=Object.fromEntries(['year','month','day','hour','minute','second'].map(key=>[key,'numeric']));
getdate=(today = new Date())=>today.toLocaleDateString('en-US', dateOptions);
const updateDateTime = () => document.getElementById('datetime').innerHTML =`${getdate()}`;
updateDateTime();
setInterval(updateDateTime, 1000);
</script>
```


# 現在の時刻を表示
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/6cd01629-0eeb-495f-99de-02c4de680648)
* https://codepen.io/jamad/pen/JjzoPGB

```html
現在の時間
<p id="time"></p>
<script>
getTime=(now=new Date())=>`${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;
updateTime=()=> document.getElementById('time').textContent=getTime();
updateTime();
setInterval(updateTime, 1000);
</script> 
```


# 現在の日付を表示
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/3e1f707b-83b3-4f6b-85ef-c47c83b4d59b)
* https://codepen.io/jamad/pen/eYXmOYE

```html
<span id="date"></span>
<script>
today= new Date();
options={year:'numeric', month:'numeric',day: 'numeric' };
document.getElementById("date").innerHTML = today.toLocaleDateString('en-US', options);
</script>
```

* need to learn more about this
* https://talk.jekyllrb.com/t/how-do-i-embed-javascript-in-jekyll/4374/29
  

<div id="repos">
    <div class="container">
        <!-- Filter controls -->
        <div class="field">
            <p class="control has-icons-left">
                <input class="search input" type="text" placeholder="Search repo names">
                <span class="icon is-left">
                    <i class="fas fa-search" aria-hidden="true"></i>
                </span>
            </p>
        </div>
    </div>
</div>



```
<span id="date"></span>
<script>
  window.onload = function() {
    var today = new Date();
    var options = { year: 'numeric', month: 'numeric', day: 'numeric' };
    document.getElementById("date").innerHTML = today.toLocaleDateString('en-US', options);
  }
</script> 
```


<button onclick="copyText()"><span id="mystr">dummy placeholder</span></button>

<script>
var mystr= new Date().toISOString().slice(0, 10) + '-';
document.getElementById("mystr").innerText =mystr;

// テキストエリア追加し、コピー後に削除
function copyText() {
  var textArea = document.createElement("textarea");
  document.body.appendChild(textArea);
  textArea.value = mystr;
  textArea.select();
  document.execCommand("copy");
  document.body.removeChild(textArea);
  alert("copied : " + mystr);
}
</script>


# .mdファイルでJavaScript実行できるのか！
 
# コードの実験をした場所　
* ver2 https://codepen.io/jamad/pen/ExMaxWq
* ver1 https://codepen.io/jamad/pen/ExMaxPz



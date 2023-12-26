<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# my works
* [https://codepen.io/your-work/](https://codepen.io/your-work/)

---

# image filter
* [https://codepen.io/jamad/pen/ExMadmE](https://codepen.io/jamad/pen/ExMadmE)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/1cb81a0f-03ab-406e-9333-aa9ab63654f0)

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

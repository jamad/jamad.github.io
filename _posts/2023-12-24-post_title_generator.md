<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

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

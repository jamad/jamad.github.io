
# github検索のテスト  https://codepen.io/jamad/pen/GRbKQxm 

`コードここから`

<input type="text" id="inputText" placeholder="検索文字列を入力">
<button onclick="openURL()">user:jamad でgithubを検索</button>
<script>
  function openURL() {
    const inputText = document.getElementById('inputText').value;
    const url = 'https://github.com/search?q=user%3Ajamad+' + encodeURIComponent(inputText);
    window.open(url, '_blank');//新規ページとして開く
  }
</script>

`コードここまで`



<input id="iT2" placeholder="検索文字列を入力">
<button onclick="window.open('https://github.com/search?q=user%3Ajamad+'+encodeURIComponent(iT2.value),'_blank')">user:jamad でgithubを検索</button>

<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

<p id="tm"></p>
<script>
f=(x)=>String(x).padStart(2,'0');
g=(d=new Date())=>`${f(d.getHours())}:${f(d.getMinutes())}:${f(d.getSeconds())}`;
u=()=>document.getElementById('tm').textContent=g();
setInterval(u,1000);
</script>

## codepen で動作確認して htmlを.md に実装し、jekyllでhtml 化する流れが今のところ最も効率が良い
* [https://codepen.io/your-work/](https://codepen.io/your-work/)

### 新規postの方法
* iOS app の場合
  * profile > pinned repo > code > _posts > create file as yyyy-mm-dd-title.md > commit > wait
* pc の場合
  * [_posts](https://github.com/jamad/jamad.github.io/tree/master/_posts) > add file
* TODO
  * CSSタグをコピーするボタンをここに作成
* 最初の行に記載するcssのtag

```
<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">
```

---

### このページ(index.html)の更新方法 
1. [index.md](https://github.com/jamad/jamad.github.io/edit/master/index.md)　から編集 (index.html が既存だと index.md が上書きできないので削除)
1. jekyllのconversionを待つ。進捗状況は[ここ](https://github.com/jamad/jamad.github.io/actions)で確認できる。
1. [このページを再読み込み](https://jamad.github.io/) して確認。Chromeなら `ctrl+shift+R` でキャッシュクリア可能。


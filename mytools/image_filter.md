<link rel="stylesheet" type="text/css" href="../assets/css/styles.css" />

# image filter
* example ![image](https://github.com/jamad/jamad.github.io/assets/949913/64ab77f8-5c1b-4851-839e-f4c553fce5a4)


 <main></main>

<script>
  const imageUrl = "https://raw.githubusercontent.com/dkzakka/dkzakka/main/dkzakka_icon.jpg";
  function createContents(filter) {
    const group = document.createElement('div');
    group.dataset.filter = `image-${filter}`;
    const header = document.createElement('h3');
    header.textContent = filter;
    const image = document.createElement('img');
    image.src = imageUrl;
    image.style.setProperty('--filter', filter === 'none' ? 'none' : filter);
    group.appendChild(header);
    group.appendChild(image);
    return group;
  }

  const main = document.querySelector('main');
  const filters = ["none", "grayscale(100%)", "saturate(200%)", "sepia(100%)", "invert(100%)", "opacity(50%)", "brightness(150%)", "contrast(200%)", "blur(5px)", "hue-rotate(180deg)"];
  filters.forEach(x=>main.appendChild(createContents(x)));
</script>

<style>
 main {
  display: flex;
  flex-wrap: wrap;
}

main div {
  margin: 10px;
  display: flex; /* 子要素を横に並べるために追加 */
  flex-direction: column; /* 子要素を縦に並べる指示を削除 */
  align-items: center; /* 要素を中央揃え */
  text-align: center; /* テキストを中央揃え */
}


/* 画像 */
main div img {
  width: 100%; /* 画像を親要素に合わせて調整 */
  max-width: 160px; /* 最大幅を指定 */
  height: auto; /* アスペクト比を保ったまま高さを自動調整 */
  filter: var(--filter); /* 画像に適用されるフィルターを定義 */
}

</style>


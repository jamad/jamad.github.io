# test for layout of auto generated contents

<main></main>

<style>
body { background: #222; color: #fff; }
main {display: flex;flex-wrap: wrap;}
main div { margin: 20px;}
</style>

<script>
function f(filter) {
  const group = document.createElement('div');
  group.dataset.filter = `image-${filter}`;
  const header = document.createElement('h5');
  header.textContent = filter;
  const image = document.createElement('img');
  image.src = "https://via.placeholder.com/120/0000FF/808080"; // 画像を表示するための img 要素
  image.style.width = '120px';
  image.style.filter = filter; 
  group.appendChild(header);
  group.appendChild(image);
  return group;
}
  const filters = ["grayscale(100%)", "sepia(100%)", "invert(100%)", "opacity(50%)"];
  filters.forEach(filter => document.querySelector('main').appendChild(f(filter)));
</script>

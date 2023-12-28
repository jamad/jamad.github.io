* test for layout of auto generated contents
* `<main>` だと　下記のようにレイアウトが崩れるので　`<section>` を使うようにしてみたら解決！
![image](https://github.com/jamad/jamad.github.io/assets/949913/ddf2fd91-2f50-4921-b339-c32aaf513664)


---
  <section></section>
  
  <style>
    body { background: #222; color: #fff; }
    section { display: flex; flex-wrap: wrap; }
    section div { margin: 20px; }
  </style>
  

  <script>
    function f(filter) {
      const group = document.createElement('div');
      group.dataset.filter = `image-${filter}`;
      const header = document.createElement('h5');
      header.textContent = filter;
      const image = document.createElement('img');
  
      // image.src = "https://via.placeholder.com/120/0000FF/808080"; // placeholder
      image.src = "https://picsum.photos/id/237/300/300.jpg"; // another placeholder
  
      image.style.width = '120px';
      image.style.filter = filter; 
      group.appendChild(header);
      group.appendChild(image);
      return group;
    }
  
    const filters = ["grayscale(100%)", "sepia(100%)", "invert(100%)", "opacity(50%)"];
    filters.forEach(filter => document.querySelector('section').appendChild(f(filter)));
  </script>

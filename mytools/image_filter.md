<link rel="stylesheet" type="text/css" href="../assets/css/styles.css" />

# image filter
* example ![image](https://github.com/jamad/jamad.github.io/assets/949913/64ab77f8-5c1b-4851-839e-f4c553fce5a4)



  <input type="file" accept="image/*" id="fileI" style="display: none">
  <div class="tgt" onclick="document.getElementById('fileI').click()">  <div class="img">Click Here to Display Image</div> </div>
  <main></main>

  <script>
    const img = document.querySelector('.img');
    const main = document.querySelector('main');
    const filters = ["none", "grayscale(100%)", "saturate(200%)", "sepia(100%)", "invert(100%)", "opacity(50%)", "brightness(150%)", "contrast(200%)", "blur(5px)", "hue-rotate(180deg)"];

    function dispI(x) {
      if (x && x.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(event) {
          img.style.backgroundImage = `url(${event.target.result})`;
          main.innerHTML = '';
          filters.forEach(filter => main.appendChild(createContents(event.target.result, filter)));
        };
        reader.readAsDataURL(x);
      } else {
        alert('Please select an image file.');
      }
    }

    document.getElementById('fileI').addEventListener('change', event => {
      dispI(event.target.files[0]);
    });

    function createContents(imageUrl, filter) {
      const group = document.createElement('div');
      group.dataset.filter = `image-${filter}`;
      const header = document.createElement('h3');
      header.textContent = filter;
      const image = document.createElement('img');
      image.src = imageUrl;
      image.style.width = '120px';
      image.style.filter = filter === 'none' ? 'none' : filter; // フィルターを直接適用
      group.appendChild(header);
      group.appendChild(image);
      return group;
    }
  </script>


  <style>
    body { background: #222; color: #fff; }
    .tgt { width: 100%; height: 200px; border: 1px dashed #ccc; text-align: center; line-height: 200px; }
    .img { background: center no-repeat; background-size: contain; width: 100%; height: 100%; }
    main { display: flex; flex-wrap: wrap; }
   
    main div {
  margin: 10px;
  display: flex; /* 子要素を横に並べるために追加 */
  flex-direction: column; /* 子要素を縦に並べる指示を削除 */
  align-items: center; /* 要素を中央揃え */
  text-align: center; /* テキストを中央揃え */
    }

    main div img { width: 120px; height: auto; filter: none; }
  </style>



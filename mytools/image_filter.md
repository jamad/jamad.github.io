<link rel="stylesheet" type="text/css" href="../assets/css/styles.css" />

# image filter　（但し、画像を保存しようとした場合、フィルタ前の画像が保存されるようだ？）
* example 

![image](https://github.com/jamad/jamad.github.io/assets/949913/63ff0710-394e-45b5-b83e-c2448f84a4a5)


  <style>
    body { background: #222; color: #fff; }
    .tgt { width: 100%; height: 200px; border: 1px dashed #ccc; text-align: center; line-height: 200px; }
    .img { background: center no-repeat; background-size: contain; width: 100%; height: 100%; }
    
    section { display: flex;flex-wrap: wrap;}

    section div {
      margin: 10px;
      display: flex; /* 子要素を横に並べるために追加 */
      flex-direction: column; /* 子要素を縦に並べる指示を削除 */
      align-items: center; /* 要素を中央揃え */
      text-align: center; /* テキストを中央揃え */
    }
    
    section div img {
      width: 100%; /* 画像を親要素に合わせて調整 */
      max-width: 160px; /* 最大幅を指定 */
      height: auto; /* アスペクト比を保ったまま高さを自動調整 */
      filter: var(--filter); /* 画像に適用されるフィルターを定義 */
    }
  </style>

  <input type="file" accept="image/*" id="fileI" style="display: none">
  <div class="tgt" onclick="document.getElementById('fileI').click()">  <div class="img">Click Here to Display Image</div> </div>

  <section></section>

  <script>
    const img = document.querySelector('.img');
    const section = document.querySelector('section');
    const filters = ["none", "grayscale(100%)", "saturate(200%)", "sepia(100%)", "invert(100%)", "opacity(50%)", "brightness(150%)", "contrast(200%)", "blur(5px)", "hue-rotate(180deg)"];

    function dispI(x) {
      if (x && x.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(event) {
          img.style.backgroundImage = `url(${event.target.result})`;
          section.innerHTML = '';
          filters.forEach(filter => section.appendChild(createContents(event.target.result, filter)));
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



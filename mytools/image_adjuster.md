<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# image adjuster

 <style>
    body { background: #222; color: #fff; }
    .container { width: 100%; }
    .tgt { width: 100%; height: 400px; border: 2px dashed #ccc; text-align: center; line-height: 400px; cursor: pointer; overflow: hidden; }
    .img { background: center no-repeat; background-size: contain; width: 100%; height: 100%; }
    .ctrl { display: flex; flex-direction: column; margin-top: 10px; }
  </style>

  <input type="file" accept="image/*" id="fileInput" style="display: none">
  
  <div class="container">
    <div class="tgt" onclick="document.getElementById('fileInput').click()">
      <div class="img" id="dropArea">Click Here to Display Image</div>
    </div>
    <div class="ctrl">
      <label for="brightness">Brightness</label>
      <input type="range" class="bar bri" id="brightness" min="0" max="200" value="100" step="1">
      
      <label for="hue">Hue</label>
      <input type="range" class="bar hue" id="hue" min="0" max="360" value="0" step="1">
      
      <label for="saturation">Saturation</label>
      <input type="range" class="bar sat" id="saturation" min="0" max="200" value="100" step="1">
    </div>
  </div>

  <script>
    function displayImage(file) {
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(event) {
          const imgElement = document.querySelector('.img');
          imgElement.style.backgroundImage = `url(${event.target.result})`;
        };
        reader.readAsDataURL(file);
      } else { alert('Please select an image file.');}
    }

    const sliders = document.querySelectorAll('.bar');
    const img = document.querySelector('.img');

    sliders.forEach(slider => {
      slider.addEventListener('input', () => {
        const brightness = document.getElementById('brightness').value / 100;
        const hue = document.getElementById('hue').value;
        const saturation = document.getElementById('saturation').value / 100;
        img.style.filter = `brightness(${brightness}) hue-rotate(${hue}deg) saturate(${saturation})`;
      });
    });
    // fileInputのonchangeイベントをJavaScriptで処理する
    document.getElementById('fileInput').addEventListener('change', function(event){displayImage(this.files[0]);});
  </script>

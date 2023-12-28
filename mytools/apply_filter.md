* 画像を開き、'grayscale(100%)'フィルタをApplyし、結果を保存するツール　（PCでは作動。iOSでは不具合？）
* [習作](https://codepen.io/jamad/pen/ZEPGLGo)
* `img { margin-right: 10px; }` /* img要素の右側に隙間を追加 */

---

<style>
  body { background: #222; color: #fff; }
  section { display: flex;}
  img { margin-right: 10px; } 
</style>

<input type="file" accept="image/*" id="fileInput">

<button onclick="saveFiltered()">Save Filtered Image</button>

<section>
  <img id="originalImage" src="https://via.placeholder.com/160"　alt="Placeholder" style="width: 160px;height: 160px;">
  <canvas id="filteredCanvas"></canvas>
</section>

<script>
const fileInput = document.getElementById('fileInput');
const originalImg = document.getElementById('originalImage');
const canvas = document.getElementById('filteredCanvas');
const ctx = canvas.getContext('2d');
const img = new Image();
img.onload = function() { ctx.drawImage(img, 0, 0);};
img.src = 'https://via.placeholder.com/160';

function applyFilter() {
  ctx.filter = 'grayscale(100%)';
  ctx.drawImage(originalImg, 0, 0, originalImg.width, originalImg.height);
}
  
fileInput.addEventListener('change', function(event) {
  const reader = new FileReader();
  reader.readAsDataURL(event.target.files[0]);
  reader.onload = function(e) {
    console.log('画像がロード完了')
    originalImg.src = e.target.result;
    originalImg.style.display = 'block';
    applyFilter();
    };
});

function saveFiltered() {
const downloadLink = document.createElement('a');
downloadLink.href = canvas.toDataURL('image/png');
downloadLink.download = 'filtered_image.png';
downloadLink.click();
}

</script>

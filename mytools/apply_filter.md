* 画像を開き、'grayscale(100%)'フィルタをApplyし、結果を保存するツール

  <style>
  body { background: #222; color: #fff; }
  section { display: flex;flex-wrap: wrap;}　/* 画像を横並びにするため　
</style>

<input type="file" accept="image/*" id="fileInput">
<button onclick="saveFiltered()">Save Filtered Image</button>

<section>
  <img id="originalImage" src="#" style="width: 160px; display: none;">
  <canvas id="filteredCanvas"></canvas>
</section>

<script>
const fileInput = document.getElementById('fileInput');
const originalImg = document.getElementById('originalImage');
const canvas = document.getElementById('filteredCanvas');
const ctx = canvas.getContext('2d');

function applyFilter() {
  const newWidth = originalImg.width;
  const newHeight = originalImg.height;
  canvas.width = newWidth;
  canvas.height = newHeight;
  ctx.filter = 'grayscale(100%)';
  ctx.drawImage(originalImg, 0, 0, newWidth, newHeight);
}
  
fileInput.addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = function(e) {//画像がロード完了された後に実行される
    originalImg.src = e.target.result;
    originalImg.style.display = 'block';
    applyFilter();
    };
  reader.readAsDataURL(file);
});

function saveFiltered() {
const downloadLink = document.createElement('a');
downloadLink.href = canvas.toDataURL('image/png');
downloadLink.download = 'filtered_image.png';
downloadLink.click();
}
</script>

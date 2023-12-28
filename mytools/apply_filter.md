# test for apply filter

<canvas id="filteredCanvas" style="display: none;"></canvas>
<img id="originalImage" src="https://picsum.photos/id/237/300/300.jpg" style="width: 160px;">
<button onclick="applyFilter()">Apply Filter</button>
<button onclick="saveFiltered()">Save Filtered Image</button>

<script>
  function applyFilter() {
    const originalImg = document.getElementById('originalImage');
    const canvas = document.getElementById('filteredCanvas');
    const ctx = canvas.getContext('2d');

    // Canvasのサイズを変更
    const newWidth = originalImg.width / 2;
    const newHeight = originalImg.height / 2;
    canvas.width = newWidth;
    canvas.height = newHeight;

    // フィルタを適用
    ctx.filter = 'grayscale(100%)';

    // フィルタを適用した画像を描画
    ctx.drawImage(originalImg, 0, 0, newWidth, newHeight);

    console.log("画像のリサイズとフィルタの適用が完了しました。");
}




  function saveFiltered() {
    const canvas = document.getElementById('filteredCanvas');
    const filteredImageData = canvas.toDataURL('image/png'); // 画像データを取得
    const downloadLink = document.createElement('a');
    downloadLink.href = filteredImageData;
    downloadLink.download = 'filtered_image.png'; // 保存時のファイル名
    downloadLink.click();
  }
</script>

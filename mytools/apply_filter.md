# test for apply filter

  <style>
    body { background: #222; color: #fff; }
  </style>
  
  <input type="file" accept="image/*" id="fileInput">
  <img id="originalImage" src="#" style="width: 300px; display: none;">
  <button onclick="applyFilter()">Apply Filter</button>
  <button onclick="saveFiltered()">Save Filtered Image</button>
  <canvas id="filteredCanvas"></canvas>

  <script>
    const fileInput = document.getElementById('fileInput');
    const originalImg = document.getElementById('originalImage');
    const canvas = document.getElementById('filteredCanvas');
    const ctx = canvas.getContext('2d');

    fileInput.addEventListener('change', function(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = function(e) {
        originalImg.src = e.target.result;
        originalImg.style.display = 'block';
      };
      reader.readAsDataURL(file);
    });

    function applyFilter() {
      const newWidth = originalImg.width / 2;
      const newHeight = originalImg.height / 2;
      canvas.width = newWidth;
      canvas.height = newHeight;

      ctx.filter = 'grayscale(100%)';
      ctx.drawImage(originalImg, 0, 0, newWidth, newHeight);
    }

    function saveFiltered() {
      const filteredImageData = canvas.toDataURL('image/png');
      const downloadLink = document.createElement('a');
      downloadLink.href = filteredImageData;
      downloadLink.download = 'filtered_image.png';
      downloadLink.click();
    }
  </script>

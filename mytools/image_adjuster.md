<link rel="stylesheet" type="text/css" href="../assets/css/styles.css" />

# image adjuster

 <style>
  body { background: #222; color: #fff; }
  .tgt { width: 100%; height: 400px; border: 1px dashed #ccc; text-align: center; line-height: 400px; }
  .img { background: center no-repeat; background-size: contain; width: 100%; height: 100%; }
  .ctrl { display: flex; flex-direction: column; }
</style>

<input type="file" accept="image/*" id="fileI" style="display: none">
<div class="tgt" onclick="document.getElementById('fileI').click()">  <div class="img">Click Here to Display Image</div> </div>
<div class="ctrl">
  <label for="_bri">Brightness</label>
  <input type="range" class="bar" id="_bri" min="0" max="200" value="100" step="1">
  <label for="hue">Hue</label>
  <input type="range" class="bar" id="hue" min="0" max="360" value="0" step="1">
  <label for="_sat">Saturation</label>
  <input type="range" class="bar" id="_sat" min="0" max="200" value="100" step="1">
</div>

<script>
  const img = document.querySelector('.img');
  
  function dispI(x) {
    if (x && x.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = function(event) {        img.style.backgroundImage = `url(${event.target.result})`;      };
      reader.readAsDataURL(x);
    } else {      alert('Please select an image file.');    }
  }

  document.querySelectorAll('.bar').forEach(slider => {
    slider.addEventListener('input', () => {
      const bri = document.getElementById('_bri').value / 100;
      const hue = document.getElementById('hue').value;
      const sat = document.getElementById('_sat').value / 100;
      img.style.filter = `brightness(${bri}) hue-rotate(${hue}deg) saturate(${sat})`;
    });
  });
  
  document.getElementById('fileI').addEventListener('change', event => {dispI(event.target.files[0]);  });
</script>

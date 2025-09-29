<link rel="stylesheet" type="text/css" href="/assets/css/styles.css">

<img height="160" alt="{FCE24642-BBA5-4C76-B288-096410F19060}" src="https://github.com/user-attachments/assets/c794ccb3-ddaf-449f-9c65-debe0b4931bd" />　[jamad.github.io/graviton/](https://jamad.github.io/graviton/)



todo here !

### note 
* the reason why I use style here is because I cannot read this page in  Dark mode on iOS Safari 


# the following is a quicktest for svg tag

<svg width="100%" height="200">
  <circle cx="0" cy="100" r="20" fill="blue">
    <animate attributeName="cx" from="0" to="100%" dur="5s" repeatCount="indefinite" />
  </circle>
</svg>

* quick clock by javascript
<p id="tm"></p>

<script>
  // 簡易時計
  f=(x)=>String(x).padStart(2,'0');
  g=(d=new Date())=>`${f(d.getHours())}:${f(d.getMinutes())}:${f(d.getSeconds())}`;
  u=()=>document.getElementById('tm').textContent=g();
  setInterval(u,1000);
</script>

---






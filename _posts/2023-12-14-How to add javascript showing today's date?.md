
# HTMLとJavaScriptの例

```html
<!DOCTYPE html>
<html>
<head>
  <title>HTML内のJavaScript</title>
</head>
<body>

<h1>HTML with JavaScript</h1>

<span id="date"></span>
<script>
  window.onload = function() {
    var today = new Date();
    var options = { year: 'numeric', month: 'numeric', day: 'numeric' };
    document.getElementById("date").innerHTML = today.toLocaleDateString('en-US', options);
  }
</script> 

</body>
</html>
```

![image](https://github.com/jamad/jamad.github.io/assets/949913/b3d82ecd-1f0f-48e6-9f27-6807d4d31a96)

```
<span id="date"></span>
<script>
  window.onload = function() {
    var today = new Date();
    var options = { year: 'numeric', month: 'numeric', day: 'numeric' };
    document.getElementById("date").innerHTML = today.toLocaleDateString('en-US', options);
  }
</script> 
```

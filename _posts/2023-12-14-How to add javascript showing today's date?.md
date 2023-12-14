
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

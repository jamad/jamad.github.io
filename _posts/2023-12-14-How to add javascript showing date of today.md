
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

* need to learn more about this
* https://talk.jekyllrb.com/t/how-do-i-embed-javascript-in-jekyll/4374/29
  

<div id="repos">
    <div class="container">
        <!-- Filter controls -->
        <div class="field">
            <p class="control has-icons-left">
                <input class="search input" type="text" placeholder="Search repo names">
                <span class="icon is-left">
                    <i class="fas fa-search" aria-hidden="true"></i>
                </span>
            </p>
        </div>
    </div>
</div>



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

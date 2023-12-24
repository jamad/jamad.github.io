
# 現在の時刻を表示
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/6cd01629-0eeb-495f-99de-02c4de680648)
* https://codepen.io/jamad/pen/JjzoPGB

```html
現在の時間
<p id="time"></p>
```

```javascript
getTime=(now=new Date())=>`${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;
updateTime=()=> document.getElementById('time').textContent=getTime();
updateTime();
setInterval(updateTime, 1000);
```


# HTMLとJavaScriptの例

* [codepenでの例](https://codepen.io/jamad/pen/eYXmOYE)

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

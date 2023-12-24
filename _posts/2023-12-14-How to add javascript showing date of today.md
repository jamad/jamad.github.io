# 現在の日時を表示
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/18f44f87-42b1-4fa3-b91f-71726a1d20ee)
* https://codepen.io/jamad/pen/XWGJWro
```
<span id="datetime"></span>
<script>
dateOptions=Object.fromEntries(['year','month','day','hour','minute','second'].map(key=>[key,'numeric']));
getdate=(today = new Date())=>today.toLocaleDateString('en-US', dateOptions);
const updateDateTime = () => document.getElementById('datetime').innerHTML =`${getdate()}`;
updateDateTime();
setInterval(updateDateTime, 1000);
</script>
```


# 現在の時刻を表示
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/6cd01629-0eeb-495f-99de-02c4de680648)
* https://codepen.io/jamad/pen/JjzoPGB

```html
現在の時間
<p id="time"></p>
<script>
getTime=(now=new Date())=>`${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;
updateTime=()=> document.getElementById('time').textContent=getTime();
updateTime();
setInterval(updateTime, 1000);
</script> 
```


# 現在の日付を表示
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/3e1f707b-83b3-4f6b-85ef-c47c83b4d59b)
* [codepenでの例](https://codepen.io/jamad/pen/eYXmOYE)

```html
<span id="date"></span>
<script>
today= new Date();
options={year:'numeric', month:'numeric',day: 'numeric' };
document.getElementById("date").innerHTML = today.toLocaleDateString('en-US', options);
</script>
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

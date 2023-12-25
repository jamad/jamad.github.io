<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# my works
* https://codepen.io/your-work/
  * [簡易メモ](https://codepen.io/jamad/pen/wvOBJwE?editors=1000)

# practice
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/50f1390a-13fc-4a7d-a750-847e7034cbfa) 001 [https://codepen.io/jamad/pen/yLwBzrQ](https://codepen.io/jamad/pen/yLwBzrQ)

---

# 2023-12-24

<span id="datetime"></span>
<script>
dateOptions=Object.fromEntries(['year','month','day','hour','minute','second'].map(key=>[key,'numeric']));
getdate=(today = new Date())=>today.toLocaleDateString('en-US', dateOptions);
const updateDateTime = () => document.getElementById('datetime').innerHTML =`${getdate()}`;
updateDateTime();
setInterval(updateDateTime, 1000);
</script>

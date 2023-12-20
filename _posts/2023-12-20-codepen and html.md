```
<div class="heart"></div>
```

```
body {
  background: linear-gradient(45deg, #ffe2d3, #a6dee2, #cfc2fc);
}

.heart {
  height: 200px;
  width: 200px;
  background-color: #f49;
  margin: auto;
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  animation-name: beat;
  animation-duration: 1.6s;
  animation-iteration-count: infinite;
}

@keyframes beat {
  0%    {    transform: scale(1) rotate(0deg); }
  50%   {    transform: scale(0.5) rotate(-45deg);}
  100%  {    transform: scale(1) rotate(90deg); }
}

```

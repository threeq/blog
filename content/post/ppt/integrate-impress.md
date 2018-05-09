---
title: Hugo 集成 impress.js 实现播放效果
date: 2018-05-07
lastmod: 2018-05-07
draft: false
keywords: ["Threeq", "博客", "程序员", "架构师"]
categories:
 - 笔记
tags:
 - 笔记
toc: false
comment: true
description: "ppt view demo"

PptView: 
  enable: true
  attrs:
    data-transition-duration: 1000
    data-autoplay: 10
  css:
    - /lib/impress/classic-slides.css
    - /post/ppt-demo/ppt-demo.css
  js:
    - /post/ppt-demo/ppt-demo.js
---


---
data-x: -1000
data-y: -1500
---
# Hugo 中简单 PPT 效果演示 
## 使用 Impress.js 实现

* markdown 支持
* html 支持
* 依赖库
  * [showdown](https://github.com/showdownjs/showdown)
  * impress.js

-----

---
data-rel-x: 1000
data-rel-y: 0
---
# 支持 markdown 样式

* 可以使用常用 markdown 语法
* 例如：*italics* 、 **bold** 、 `code`


-----
# 分页和配置语法

* 由于 markdown 本身没有分页支持，所以这里使用 `-----` 作为分页标志
* 每个页面都可以有自己的配置，配置必须放在页面的最前面放在 **两个 `---`** 之间
* 例如
```
  -----
  ---
  data-rel-x: 1000
  data-rel-y: 0
  ---
  你的内容
```

-----
---
data-rel-x: 300 
data-rel-y: 1100 
data-rotate: 90
---
# html 和 动画支持
## 这是一个 html 元素支持的演示。

<p class="fly-in fly-out">Fly in</p>
<p class="fade-in fade-out" style="transition-delay: 2s">Fade in</p>
<p class="zoom-in zoom-out" style="transition-delay: 4s">And zoom in</p>

*这个有点像 ppt。需要使用 css3 动画库.*
**如果只要 html 解析，请加入配置选项： `html: true`**

-----
---
id: acme
---
# graph 演示
<div id="acme-graph-1">
  <div id="acme-graph-bars">
      <div id="acme-graph-q1" class="acme-graph-bar red" style="height: 183.529px;"></div>
      <div id="acme-graph-q2" class="acme-graph-bar blue" style="height: 200px;"></div>
      <div id="acme-graph-q3" class="acme-graph-bar green" style="height: 0px;"></div>
      <div id="acme-graph-q4" class="acme-graph-bar purple" style="height: 0px;"></div>
  </div>
  <div id="acme-graph-bottom"></div>
</div>
<table border="1">
  <tr><td>Q1</td><td id="acme-q1">234€</td></tr>
  <tr><td>Q2</td><td id="acme-q2">255€</td></tr>
  <tr><td>Q3</td><td><input id="acme-q3" size="5" oninput="acmeDrawGraph();" />€ <small>(insert here)</small></td></tr>
  <tr><td>Q4</td><td><input id="acme-q4" size="5" oninput="acmeDrawGraph();" />€</td></tr>
</table> 

<script src="/post/ppt-demo/ppt-demo.js"></script>
-----

# 2

```
data-rel-x: 800 
data-rel-y: 800
data-rotate: 60
```

-----

---
data-x: 6200
data-y: 4300
data-z: -100
data-rotate-x: -40
data-rotate-y: 10
data-scale: 2
class: step slide markdown step-3d 
---
# This is 3D
<p>
  <span class="have">have</span> <span class="you">you</span> <span class="noticed">noticed</span> <span class="its">it’s</span> 
  <span class="in">in</span> <b>3D<sup>*</sup></b>?
</p>
<span class="footnote">* beat that, prezi ;)</span> 

-----
# 子步骤演示
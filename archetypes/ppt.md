---
title: {{ replace .Name "-" " " | title }}
date: {{ dateFormat "2006-01-02" .Date }}
lastmod: {{ dateFormat "2006-01-02" .Date }}
draft: true
keywords: ["Threeq", "博客", "程序员", "架构师"]
categories:
 - 笔记
tags:
 - 笔记
toc: false
comment: true
description: ""

PptView: 
  enable: true
#  startBtn: 开始演示
  attrs:
    data-transition-duration: 1000
    data-autoplay: 10
  css:
#    - /lib/impress/classic-slides.css
  js:
#    - 
---

---
data-x: -1000
data-y: -1500
---
# Markdown 
## to author Impress.js presentations

* This presentation was written entirely in Markdown
* Added by popular request ---
  * Easy way to make quick, simple yet aesthetic, presentations
  * Authoring without all the clutter of HTML
-----

---
data-rel-x: 1000
data-rel-y: 0
---
# Markdown.js

* Provided by [Markdown.js](https://github.com/evilstreak/markdown-js) 
  in [extras/](https://github.com/henrikingo/impress.js/tree/myfork/extras)
* Jot down your bullet points in *Markdown* & have it automatically converted to HTML
* Note: The Markdown is converted into a presentation client side, in the browser.
  This is unlike existing tools like [Hovercraft](https://github.com/regebro/hovercraft) 
  and [markdown-impress](http://binbinliao.com/markdown-impress/) where you generate 
  a new html file on the command line.
* This combines the ease of --- typing Markdown with the full power of 
  impress.js HTML5+CSS3+JavaScript!

-----
# Styles

* You can use *italics* & **bold**
* ...and `code`

-----
---
data-rel-x: 1100
data-rel-y: 300
data-rotate: 30
---
# 1

```
data-rel-x: 1100
data-rel-y: 300
data-rotate: 30
```

-----
---
data-rel-x: 800 
data-rel-y: 800
data-rotate: 60
---
# 2

```
data-rel-x: 800 
data-rel-y: 800
data-rotate: 60
```

-----
---
html: true
data-rel-x: 300 
data-rel-y: 1100 
data-rotate: 90
---
# Motion effects 101
<p class="fly-in fly-out">Fly in</p>
<p class="fade-in fade-out" style="transition-delay: 2s">Fade in</p>
<p class="zoom-in zoom-out" style="transition-delay: 4s">And zoom in</p>

-----
---
data-x: 6200
data-y: 4300
data-z: -100
data-rotate-x: -40
data-rotate-y: 10
data-scale: 2
---
# This is 3D

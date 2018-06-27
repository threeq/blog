---
title: Python学习 01：学习环境搭建
date: 2018-06-14
lastmod: 2018-06-14
draft: false
keywords: ["Threeq", "博客", "程序员", "架构师", "Python", "python3"]
categories:
 - python
tags:
 - python
toc: true
comment: true
description: "python 是一门使用很广的动态语言，不论是在系统运维、web开发、科学计算、机器学习、图像处理等领域都有 python 的身影。当然这些都不能作为你要学习 python 的理由，学习他的唯一理由就是：你热爱 python。他不是最快的语言，也不是使用最多的语言，但是 python 可以提高你日常处理琐事的效率，并且顺带可以干一些很酷的事情：人生苦短，我用 pytho。"


---

python 是一门使用很广的动态语言，不论是在系统运维、web开发、科学计算、机器学习、图像处理等领域都有 python 的身影。当然这些都不能作为你要学习 python 的理由，学习他的唯一理由就是：你热爱 python。他不是最快的语言，也不是使用最多的语言，但是 python 可以提高你日常处理琐事的效率，并且顺带可以干一些很酷的事情：人生苦短，我用 pytho。

此系列文章主要聚焦在两方面的内容；

> 第一部分：python 基础支持
>
> 第二部分：python 应用实践

由于第一部分我们聚焦在 python 的基础知识的学习上，主要是让大家的属性 python 语法知识上，且能方便记录学习的过程，所以搭建环境我选择最简单的方式。
对于后面在项目实践的时候，会搭建适合项目开发的 python 开发环境。

这里使用 docker 方式搭建我们的学习环境，我们选择 `jupyter/base-notebook` 镜像，它同时兼顾了学习练习和笔记记录的功能，并且可以将学习比价导出，对于我们前期学习 python3 基础知识是最合适的方式，这里对于容器的管理我们使用 `docker-compose`，对于后面有更多需求的时候，也可以很方便的进行扩展或替换成其他版本。当然你也可以选择你喜欢的 docker 镜像版本：[jupyter/docker-stack](https://hub.docker.com/u/jupyter/)。这系列文章也是使用一个在线的类似 Jupyter 工具 [Colaboratory](https://colab.research.google.com/) 写的（后面会介绍）。

<!--more-->

# Docker 安装

*已经有 docker 环境的用户跳过*

## docker 安装

docker 安装可以查看[docker 安装](https://blog.threeq.me/post/articles/noob-learn-sql/1-install-tools/#docker-%E5%AE%89%E8%A3%85)

## docker-compose 安装

请参考官方文档：[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

# 本地 Jupyter


## Dockerfile


```Dockerfile
FROM jupyter/base-notebook
MAINTAINER threeq<threeq@foxmail.com>

```

## docker-compose.yml


```yaml
version: '3'

services:
  notebook:
    build: .
    ports:
      - 8888:8888
    volumes:
      - ./work:/home/jovyan
```

将这两个文件放到同一个目录，使用 `docker-compose up -d` 启动 jupyter 服务器，然后使用 `docker-compose logs` 查看启动是否成功和登录使用的 **token**。看到日日志输入类似

```
Attaching to nooblearnpython_notebook_1
notebook_1  | /usr/local/bin/start-notebook.sh: ignoring /usr/local/bin/start-notebook.d/*
notebook_1  |
notebook_1  | Container must be run with group "root" to update passwd file
notebook_1  | Executing the command: jupyter notebook
notebook_1  | [W 07:23:14.610 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
notebook_1  | [I 07:23:14.686 NotebookApp] JupyterLab beta preview extension loaded from /opt/conda/lib/python3.6/site-packages/jupyterlab
notebook_1  | [I 07:23:14.686 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
notebook_1  | [I 07:23:14.693 NotebookApp] Serving notebooks from local directory: /home/jovyan
notebook_1  | [I 07:23:14.694 NotebookApp] 0 active kernels
notebook_1  | [I 07:23:14.694 NotebookApp] The Jupyter Notebook is running at:
notebook_1  | [I 07:23:14.694 NotebookApp] http://f5a65ccd5cb8:8888/?token=ed3a63c025a0f44ba00a8cb4e39f28cadebc4d8f6679c603
notebook_1  | [I 07:23:14.695 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
notebook_1  | [C 07:23:14.703 NotebookApp]
notebook_1  |
notebook_1  |     Copy/paste this URL into your browser when you connect for the first time,
notebook_1  |     to login with a token:
notebook_1  |         http://f5a65ccd5cb8:8888/?token=ed3a63c025a0f44ba00a8cb4e39f28cadebc4d8f6679c603&token=ed3a63c025a0f44ba00a8cb4e39f28cadebc4d8f6679c603
```

最后一行就是就是访问的地址和 token，打开本地浏览器输入地址：[http://localhost:8888](http://localhost:8888)，会看到登录界面输入最后一行的 **token**，就能进入 jupyter 列表界面

![jupyter 笔记列表](/images/articles/noob-learn-python/01-jupyter-list.jpeg)



## 测试环境正确性

开始我们第一个 python 代码，也是经典的学习入门程序：Hello，World！

* 新建一个学习笔记（点击右上角的 `New` 按钮），在新打开的笔记本页面输入以下代码，按 `Shift+Enter` 执行


```python
print("Hello, World!")
```

输出结果如下

    Hello, World!


# 在线 Jupyter

 对于可以访问 Google 服务的小伙伴，还可以使用 Google 的一个在线服务：[Colaboratory](https://colab.research.google.com/)，Colaboratory 本身是一个数据分析工具，但是这个完全满足我们对于 Python3 学习使用。访问地址：https://colab.research.google.com

这个可以使我们更快速的学习实践，同时将我们的学习笔记存储 google 网盘，只是国内用户访问 google 服务需要使用科学方法。


# 熟悉 Jupyter

## Jupyter 主界面

![jupyter 笔记列表](/images/articles/noob-learn-python/01-jupyter-desc.jpeg)

1. **<1>**: 菜单栏，`Files`: 查看笔记列表；`Running`: 正在打开的笔记；`Clusters`: jupyter 集群信息
2. **<2>**: 笔记列表，所有创建的笔记都在这里
3. **<3>**: `Upload` 上传已有的笔记文件
4. **<4>**: `New` 新建一个笔记，点开下列表可以建立不同类型的笔记本

## Jupyter 笔记界面

![jupyter 笔记列表](/images/articles/noob-learn-python/01-jupyter-note.jpeg)

1. **<1>**: 笔记名称和保存状态，点击 `笔记名称` 可以对笔记名称进行修改 
2. **<2>**: 菜单栏和工具栏，可以做笔记导出、运行等操作
3. **<3>**: 笔记内容区域
4. **<4>**: 笔记块，我们的写的具体内容就在笔记块里面，笔记块有多种类型，我们常用的就是：Code 块和 Markdown 块

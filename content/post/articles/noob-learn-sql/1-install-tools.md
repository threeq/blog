---
title: 小白学 SQL 第一天：环境搭建
date: 2018-04-14
draft: false
categories:
 -  数据库
tags:
 - 数据库
 - SQL
keywords: ["Mysql","SQL","SQL学习","数据库"]
description: "数据库管理系统（DBMS）是 IT 从业者必备工具之一，你能在市面上看到的任何一个软件系统，在后面支持的一定有它的身影。 而这里面关系型数据库管理系统（RDBMS） 目前暂居了绝大部分，操作 RDBMS 的基础就是今天我们要开始学习的 SQL（结构化查询语言），所以我们有必要针对 SQL 进行系统全面的学习。本篇文章是《小白学 SQL》系列的开篇，也是学习的第一天。这个系列的文章是之前的学习笔记整理，同时再加入我自己在使用使用的一些使用经验，属于比较初级的知识整理，适合小白用户（初学者和刚入门）。"
toc: true

---

《小白学 SQL》第一天

本篇文章是《小白学 SQL》系列的开篇，也是学习的第一天。这个系列的文章是之前的学习笔记整理，同时再加入我自己在使用使用的一些使用经验，属于比较初级的知识整理，适合小白用户（初学者和刚入门）。

数据库管理系统（DBMS）是 IT 从业者必备工具之一，你能在市面上看到的任何一个软件系统，在后面支持的一定有它的身影。 而这里面关系型数据库管理系统（RDBMS） 目前暂居了绝大部分，操作 RDBMS 的基础就是今天我们要开始学习的 SQL（结构化查询语言），所以我们有必要针对 SQL 进行系统全面的学习。

作为学习的第一天我们将从搭建环境开始，今天实践涉及到的工具有：

* MySQL
* [Docker](https://www.docker.com/community-edition#/download)
* [ConEmuSetup](https://www.fosshub.com/ConEmu.html/ConEmuSetup.180318.exe)（windows 版本命令行工具，Linux 和 Mac 不需要）
* [Navicat](http://www.navicat.com.cn/download/direct-download?product=navicat_premium_cs_x64.exe&location=1)

<!--more-->

# 工具选择和说明

可能大家有些奇怪，为什么这里会选用 `Docker`，这个和我们 SQL 完全没有关系。这里 `Docker` 确实和我们学习的 SQL 完全没有关系，但就我个人使用来说 ：

一、docker 作为基础环境，在上面安装 MySQL 服务比我们在自己裸机上装 MySQL 方便得多，并且不易且不怕出错；

二、目前整个 IT 行业容器化正在如火如荼的进行，这个是未来不可逆转的趋势，Dcoker 正式这个大军里面的主力军；

三、MySQL 安装跨平台化，使用 Docker 过后你在任何一个系统里面（Windows、Linux、Mac OS）安装 MySQL 操作都是完全一样的

基于以上三点原因，所以这里我选择了 Docker 作为数据库运行基础环境。

软件作用：

| 软件        | 作用说明                                                |
| ----------- | ------------------------------------------------------- |
| Docker      | 提供跨平台的软件运行基础环境                            |
| MySQL       | 最常用的 RDBMS 之一，作为我们学习 SQL 的数据库服务器    |
| Navicat     | 一个被广泛使用的数据库客户端，作为我们主要的 SQL 编辑器 |
| ConEmuSetup | 一个 Window 命令行终端（Linux、Mac 使用自带的足以）     |

# 安装

## Windows 安装 ConEmuSetup  

1. 到 [ConEmuSetup 下载页面](https://www.fosshub.com/ConEmu.html) 现在对应软件版本
2. 然后一路 “Next” 就好

## Docker 安装

Docker 这里我们使用 `Community Edition` 版本，请到这里下载：[下载地址](https://www.docker.com/community-edition#/download)。

1. 对于 Windows 版和 Mac 版，下载下来后双击文件运行，剩下的几乎就是一路 "Next" 点下去就完了，最后双击桌面图标启动 Docker 服务，这里就不在说明了
2. 对于  Linux 版本，由于不同发行版的需求不同，安装步骤略有不同，但是基本也和常用软件安装差不多，并且官方文档也和齐全这里就直接放官方的安装连接地址了（是英文的哟，如果有好的中文教程推荐，请留言我尽快放上来）: [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)  [CentOS](https://docs.docker.com/engine/installation/linux/centos/)  [Fedora](https://docs.docker.com/engine/installation/linux/fedora/)  [Debian](https://docs.docker.com/engine/installation/linux/debian/)

### 加速器配置：Windows、Mac 

对于 Docker 安装完成过后，国内用户还有一步需要操作：指定 docker 加速器（原因不多说）。Windows 和 Mac 系统具体操作如下：

1. 找到  Docker 运行系统托盘图片，右击打开菜单如下

   {{% figure class="center" src="/images/articles/noob-learn-sql/01-docker-prefrences.jpeg" alt="系统菜单" width="256px"%}}

2. 点击 `Preferences` 菜单，打开设置界面如下

   ![](/images/articles/noob-learn-sql/01-docker-prefrences-1.jpeg)

3. 点击 `Daemon` 标签项，再 `Rgistry mirrors` 中输入镜像加速器网址 https://docker.mirrors.ustc.edu.cn。如下图

   ![](/images/articles/noob-learn-sql/01-docker-prefrences-2.jpeg)

对于  Linux 系统配置需要修改相关配置文件，不同系统版本有所不同。

### 加速器配置：Ubuntu 14.04、Debian 7 Wheezy

对于使用 [upstart](http://upstart.ubuntu.com/) 的系统而言，编辑 `/etc/default/docker` 文件，在其中的 `DOCKER_OPTS`中配置加速器地址：

```
DOCKER_OPTS="--registry-mirror=https://docker.mirrors.ustc.edu.cn"
```

重启 Docker 服务：

```
$ sudo service docker restart
```

### 加速器配置：Ubuntu 16.04+、Debian 8+、CentOS 7

对于使用 [systemd](https://www.freedesktop.org/wiki/Software/systemd/) 的系统，请在 `/etc/docker/daemon.json` 中写入如下内容（如果文件不存在请新建该文件）

```
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
```

> 注意，一定要保证该文件符合 json 规范，否则 Docker 将不能启动。

重启 Docker 服务：

```
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

### 检查加速器是否生效

打开终端（命令行工具）输入 `docker info`  命令，如果从结果中看到了如下内容，说明配置成功。

```
Registry Mirrors:
 https://docker.mirrors.ustc.edu.cn/
```

其他可用的加速服务有很多，这里列举几个方便大家查找：

- [Docker 官方提供的中国 registry mirror](https://docs.docker.com/registry/recipes/mirror/#use-case-the-china-registry-mirror) 
- [DaoCloud 加速器](https://www.daocloud.io/mirror#accelerator-doc)
- [阿里云加速器](https://cr.console.aliyun.com/#/accelerator)

##  MySQL 服务安装

在安装完成 Docker 过后，MySQL 服务的安装就很简单了。在你的终端命令行里面输入如下命令启动 MySQL 服务：

```
$ docker run --name sql-learn -e MYSQL_ROOT_PASSWORD=toor -p3306:3306 -d mysql
```

![](/images/articles/noob-learn-sql/01-docker-mysql-install.jpeg)

查看 MySQL 服务运行状态

```
$ docker ps
```

![](/images/articles/noob-learn-sql/01-docker-mysql-install-1.jpeg)

这里不要被命令吓着了，Docker 本身的命令不少，包括以后的所有操作，我们总共用到 docker 命令就4、5个。这里先列出来，大家可以操作一下

```
$ docker run --name sql-learn -e MYSQL_ROOT_PASSWORD=toor -p3306:3306 -d mysql  # 创建一个名为 sql-learn MySQL 容器
$ docker ps  #  查看容器运行状态
$ docker stop sql-learn  # 停止 sql-learn 容器
$ docker rm sql-learn  # 删除 sql-learn 容器，必须先停止
```

## Navicat 安装

安装和 ConEmuSetup 类似

1. 到 [Navicat 下载页面](https://www.fosshub.com/ConEmu.html) 现在对应软件版本。推荐 Navicat Premium
2. 然后一路 “Next” 就好

# 验证环境安装完成

1. 双击桌面 “Navicat” 应用图标，打开 Navicat 软件

   ​	![](/images/articles/noob-learn-sql/01-install-verify-1.jpeg)

2. 点击 “链接” 增加到 `sql-learn` 的数据库链接。输入截图里面的内容，这里密码输入 `toor` ，点击 “Test Connection” 出现绿点没有错误表示成功，如下图

   ![](/images/articles/noob-learn-sql/01-install-verify-2.jpeg)

3.  双击 “左边导航列表” 里的 `sql-learn` 得到如下结果

   ![](/images/articles/noob-learn-sql/01-install-verify-3.jpeg)

4. 创建一个用于我们以后学习使用的数据库。点击 “New Query” 新建一个查询窗口

   ![](/images/articles/noob-learn-sql/01-install-verify-4.jpeg)

   输入一下 SQL 语句

   ```sql
   create database `sql-learn` default charset=utf8mb4;
   ```

   点击执行得到如下结果，表示成功

   ![](/images/articles/noob-learn-sql/01-install-verify-5.jpeg)

支持我们的环境安装和验证全部结束。

# 总结

我们学习一下几点：

1. 如何安装 Docker 服务

2. 如何在 Docker 里面启动 MySQL 服务器

   ```
   docker run --name sql-learn -e MYSQL_ROOT_PASSWORD=toor -p3306:3306 -d mysql # 无 sql-learn 容器时
   或
   docker start sql-learn # 已有 sql-learn 容器时
   ```

3. 我们在使用数据库系统的时候需要一个数据库服务器（这里是 MySQL），还需要一个数据库客户端（这里是 Navicat）

4. 在链接 MySQL 服务器之前需要先启动 MySQL 服务器

5. 在连接一个 MySQL 服务器是需要提供的基本信息有：`服务器 IP`、`服务器端口`、`用户名`、`密码`
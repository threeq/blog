---
title: "Git 代码库分之管理"
date: 2018-04-04
categories:
 - "工具"
tags:
 - "git"
toc: true
---

代码版本库使用git管理，以下是git版本使用规范

## 流程图说明

![git流程](/images/git-branch-flow-1.jpg)

<!--more-->

## 分支使用说明

| 分支名称                       | 名字 | 说明 | 实例 |
| ------------------------------ | ---- | ---- | ---- |
| master  | 线上分支    | 不用于开发，使用tag功能标记版本。只能由beta和hotfix合并，合并同时打上发布版本tag | v1.0.2 |
| beta | 灰度分支组 |  灰度分之只能由test合并master产生，在测试通过后进入灰度阶段产生；灰度通过后合并进入master  | beta/sign |
|test(release) | 测试分支组 | 只能用于测试和修改bug，只能由由master合并进feature产生。对于测试通过的test，使用merge合并方式合并master产生beta分之；合并后的release需要删除 | test/sign; release/active |
| feature | 功能分支组 | 从最新master检出用于开发一个新功能，一旦完成开发，合并master进入下一个test，删除本次feature分支；负责开发中多开发者代码同步使用 | feature/news; feature/vote |
| topic   | 本地开发分支组 | 开发人员基于feature/release/hotfix检出自己本地开发(或修改bug)分支，在开发(或修改bug)中使用rebase合并方式和feature/release/hotfix进行同步。原则上一个feature/release/hotfix分支对应一个topic分支，开发完成的feature/release/hotfix删除对应的topic分支 | topic/feature-news-wlp; topic/release-new-wlp; topic/hotfix-news-wlp |
| hotfix  | 修补分支组 | 对于线上紧急bug修改，产生一个hotfix分支，只能由master上的tag标签签出。修改完成的hotfix合并回master，并且必须删除 | hotfix/v1.0.2 |

> 注意：
> 1. 个人开发分支除特殊情况，不允许提交到远程服务器中。

## 代码提交/合并说明

这个是开发人在日常开发中使用最多的操作。

### 获取代码库

```shell
$ git clone <版本库地址>
$ cd <代码目录>
$ git fetch origin feature/<功能分支>:feature/<功能分支>
```

### 建立自己的本地开发分支

```shell
$ git checkout feature/<功能分支>
$ git checkout -b topic/<功能分支>-<你的标识>
```

### 提交修改

```shell
$ git status
$ git add .
$ git commit -am '修改描述'
```

### 发布你的修改

```shell
$ git fetch origin feature/<功能分支>:feature/<功能分支>
$ git rebase feature/<功能分支>   # 这里可能会产生合并操作
$ git push origin topic/<功能分支>-<你的标识>:feature/<功能分支>
```

## 代码发布说明

发布代码是针对功能发布而定的，发布又分为测试发布和上线发布。对于发布操作，必须是先到测试环境(test)，再从测试环境(test)到灰度环境(beta)，最后从灰度环境(beta)到生产环境(master)，对于线上每次发布都必须有标签记录，可以回退。
原则上从beta到master只会产生 fast-forward 类型操作。**以下所有操作都在自己的开发分支中完成**。

### 发布到测试环境

```shell
# 合并feature分支
$ git fetch origin master:master
$ git fetch origin feature/<功能分支>:feature/<功能分支>
$ git checkout feature/<功能分支>
$ git merge master
~~解决冲突~~
# 生产test分支
$ git checkout -b test/<功能分支>
$ git push origin  test/<功能分支>: test/<功能分支>
# 清理feature分支
$ git push origin :feature/<功能分支>
$ git branch -D feature/<功能分支>
```

### 发布到灰度环境

```shell
# 合并master到测试
$ git fetch origin test/<功能分支>:test/<功能分支>
$ git fetch origin master:master
$ git checkout test/<功能分支>
$ git merge master
~~解决冲突~~
# 生成beta分支
$ git checkout -b beta/<功能分支>
$ git push origin beta/<功能分支>:beta/<功能名称>
# 清理 test
$ git push origin :test/<版本>
$ git branch -D test/<版本>
```

### 发布到生产环境

```shell
# 合并到master
$ git fetch origin beta/<版本>:beta/<版本>
$ git fetch origin master:master
$ git checkout master
$ git merge beta/<版本>
$ git tag -a <发布版本号> -m "发布功能描述"
$ git push origin --tags
$ git push origin master:master
# 清理 beta
$ git push origin :beta/<版本>
$ git branch -D beta/<版本>
```

### 修改生产环境bug

```shell
# 创建补丁版本，进行修改
$ git fetch origin --tag
$ git checkout -b hotfix/<版本号> <版本号>
# 修改完成发布
# 1. 合并到master
$ git fetch origin master:master
$ git checkout master
$ git merge hotfix/<版本号>
$ git tag -a <发布版本号> -m "发布功能描述"
$ git push origin --tag
$ git push origin master:master
# 清理 hotfix
$ git push origin :hotfix/<版本号>
$ git branch -D hotfix/<版本号>
```
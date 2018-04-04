---
title: "让网络更好为我们服务"
date: 2018-04-05
categories:
 - 个人管理
tags:
 - GTD
 - 时间管理
toc: true
---

你每天早上一醒来有没有立即想拿起手机赶紧看一下（facebook、twitter、微信），无论里面有没有信息都要打开一下才安心？并且在上班之前还要想办法挤出时间看一下各大新闻网站，查收邮件在各种邮件信息中找出今天需要处理的事情。并且在工作的时候，一出现一个消息弹框马上点击进去看，害怕自己遗漏哪怕一次消息。

这些在一个信息爆炸的时代是正常的，被称为信息饥渴。其实出现这个情况是由于我们没有很好获取信息方式和管理信息方法。这篇文章就介绍如何更好的利用网络工具来为我们管理信息。
<!--more-->

这里我先把这些网络工具分为：

* 信息产生工具

        github、facebook、twitter、rss博客、linkedin、微信服务号

* 信息收集转换器

        zapier、ifttt、smooch、feedly、pocket、buffer

* 时间/任务/信息管理工具（GTD）

    ```
    Evernote、todoist、kanbanflow、自己博客、bearychat、slack
    ```

![工具连接图](http://p6o5lixut.bkt.clouddn.com/blog/let-the-network-better-serve-you.jpeg)

1. 作为一个有态度的程序员肯定是从我最爱的github开始了，我们在github上面肯定少不了有自己的开源代码，当有人给我们提交一个issue、发起一个pull request等信息时我们

        github --> kanbanflow

2. 我把看书作为一项任务来对待，在我看完一本书的时候自动在 Evernote 里面创建一个书评的待完成的笔记，并在 todolist 中建立一个任务放入到待计划中

        kanbanflow --> Evernote --> kanbanflow

3. 对于facebook、twitter等社交工具中有新信息的时候，全部集中到 slack

        facebook/twitter --> slack

4. 对于各种新闻信息进行快速过滤，对于感兴趣的放入到pocket,同时建立阅读任务；后面在整理pocket的时候需要整理笔记的时候自动在Evernote中建立需要完善的整理笔记和相关todolit任务。

        pocket --> todoist
        pocket --> Evernote --> kanbanflow

5. 对于自己关注的新闻、博客、论坛等信息，订阅rss信息到feedly，如果有信息时自在todolist建立阅读任务；在阅读过程中需要整理笔记的时候自动在Evernote中建立需要完善的整理笔记和相关todolit任务。

        rss/feedly --> kanbanflow
        rss/feedly --> Evernote --> kanbanflow

6. 对于自己博客更新，会自动同步到twitter、facebook等账户中，并且保存到 Evernote

        自己博客 --> facebook --> twitter --> Evernote

7. 在工作中我们会用到 gitlab、jenkins 等工具，我把这些信息全都收集到 bearychat 中

        gitlab/jenkins --> bearychat
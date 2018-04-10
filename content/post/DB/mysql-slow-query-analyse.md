---
title: mysql 查询优化：慢查询分析工具 pt-query-digest
date: 2018-04-05
categories:
 - 数据库
tags:
 - Mysql
 - 数据库
 - 查询优化
 - percona
 - pt-query-digest
toc: true
---

在系统刚上线的时候，经常会出现慢 SQL 的情况，并且有时候系统会在特定的时间点变慢。这个时候的慢 SQL 查询语句往往是大量出现，MySQL 的慢查询日志文件也会比较大。这个时候我们往往需要从哪些查询最多、耗时最长的 sql 开始优化，以提升我们的处理效益。这个时候就需要我们能对慢日志进行统计分析，在上 M ，甚至 几十 M 的日志文件里面使用手工的方式明显是不可能的，这个时候就需要有专门的统计分析工具来帮我们做统计、分析哪些慢查询日志。`percona-toolkit` 就是一个提供统计和分析的工具集，这里重点介绍里面的 `pt-query-digest` 工具。



<!--more-->

# percona-toolkit 安装

`percona-toolkit` 首页 文档 下载地址

### mac 安装

### Linux 安装

### windows 安装

# pt-query-digest 基本使用

在使用 `pt-query-digest` 前需要有 MySQL 慢查询日志文件，这里为了大家方便实验提供了一份 [MySQL 慢查询日实验数据](http://p6o5lixut.bkt.clouddn.com/data/slow-sql-test.sql.zip) 供大家下载测试（[slow-sql-test.sql.zip 点击我下载](http://p6o5lixut.bkt.clouddn.com/data/slow-sql-test.sql.zip)，里面包含2018.04.01～2018.04.04 和 2018.04.06 的日志数据）。



* 查看使用帮助

```
> pt-query-digest --help
```

* 默认分析参数

```
> pt-query-digest slow-sql-test.sql
```

>  总体概要信息：

> ![xxx](/images/slow-sql-anaylse/description.jpeg)
>
> | 信息字段      | 说明                         |
> | ------------- | ---------------------------- |
> | Exec Time     | 执行时间                     |
> | Lock Time     | 锁时间                       |
> | Row sent      | 发送行大小                   |
> | Row examine   | 检查行大小                   |
> | Query size    | 查询大小                     |
> | Rank          | SQL 编号                     |
> | Query ID      | 查询 id                      |
> | Response time | sql 总共执行时间 和 时间比例 |
> | Calls         | sql 执行次数                 |
> | R/Call        | sql 平均每次执行时间         |
> | V/M           |                              |
> | Item          | sql 类型和涉及到的表         |
>
> ----
>
> ------
>
>  单个 SQL 信息：

> ![](/images/slow-sql-anaylse/signle-sql-info.jpeg)
>
> 

​	分析结果说明：



* 分析最近一段时间内的慢查询

```
> pt-query-digest --since=12h  slow-sql-test.sql # 最近 12 小时的慢查询
```

* 分析指定时间段内的慢查询

```
> pt-query-digest slow-sql-test.sql --since '2018-04-01 09:30:00' --until '2018-04-02 10:00:00'
```

* 分析还有指定特征的慢查询 SQL

```
> pt-query-digest --filter '$event->{fingerprint} =~ m/^select/i' slow-sql-test.sql
```

* 分析针对某个用户的慢查询

```
> pt-query-digest --filter '($event->{member} || "") =~ m/^root/i' slow-sql-test.sql
```

* ​

# pt-query-digest进阶使用

有时候我们会遇到针对慢 SQL 进行长期的跟踪分析，这个时候我们就需要将我们的每次的分析结果进行汇总、对比分析。同时对于部分环境我们是不能直接得到慢 SQL 日志的，这个时候我们可以通过抓取 TCP 协议数据或 binlog 进行分析

* 将分析结果保存到数据库

```
> pt-query-digest  --user=root –password=abc123 --review  h=localhost,D=test,t=query_review--create-review-table  slow-sql-test.sql
```

* 通过抓取 TCP 协议数据分析

```
> tcpdump -s 65535 -x -nn -q -tttt -i any -c 1000 port 3306 > mysql.tcp.txt
> pt-query-digest --type tcpdump mysql.tcp.txt> slow_report9.log
```

* 通过 binlog 日志分析

```
> mysqlbinlog mysql-bin.000093 > mysql-bin000093.sql
> pt-query-digest  --type=binlog  mysql-bin000093.sql > slow_report10.log
```



# 单条 SQL 优化基本分析

通过上面的方法就可以找出系统里面所有的慢 SQL 语句了，并且在分析报告里面会排好序，剩下的就是我们针对每条 SQL 语句的分析调优工作了。针对 SQL 的具体优化方式内容很多，建议大家系统的学习，后面我也会写一些我常用的方法。这里说一下单条 SQL 的基础分析方法，好让大家有个开头。

* 查看 SQL 执行计划

```mssql
EXPLAIN
select
        ep_name as '企业名称',
        count(*) as '企业人数',
        FROM_UNIXTIME(ep_created/1000, GET_FORMAT(DATE,'ISO')) as '注册时间'
from uc_member u
left join uc_enterprise e on u.ep_id=e.ep_id
where
ep_domain='yq.vchangyi.com'
and mem_status<3
group by u.ep_id
order by 企业人数 desc;	
```

![](/images/slow-sql-anaylse/sql-exec-explain.jpeg)

对于上面每一列的的意义这里不再详细介绍，有兴趣的同学可以查看 [MySQL 文档](https://dev.mysql.com/doc/refman/5.7/en/execution-plan-information.html)，或者关注我后续的文章，会有专门介绍。

* 查询 SQL 执行信息

查看 MySQL 语句执行信息需要首先开启 `profiling` 选线

```mysql
set profiling = 1;
```

然后执行完 SQL 过后使用 `show profiles;` 语句查看执行 SQL 的记录id

```mysql
select
        ep_name as '企业名称',
        count(*) as '企业人数',
        FROM_UNIXTIME(ep_created/1000, GET_FORMAT(DATE,'ISO')) as '注册时间'
from uc_member u
left join uc_enterprise e on u.ep_id=e.ep_id
where
ep_domain='yq.vchangyi.com'
and mem_status<3
group by u.ep_id
order by 企业人数 desc;

show profiles;
```

![](/images/slow-sql-anaylse/sql-exec-profiles.jpeg)

使用 `show profile` 查看 SQL 的执行信息

```mysql
show profile ALL for query 3;
```

![](/images/slow-sql-anaylse/sql-exec-profile.jpeg)

语法格式：

```mysql
show profile [type] for query <query_id>;
```

如果没有指定 `FOR QUERY` 则显示最近一条查询的详细信息。`type` 是可选的，有以下几个选项：

- ALL 显示所有性能信息
- BLOCK IO 显示块IO操作的次数
- CONTEXT SWITCHES 显示上下文切换次数，不管是主动还是被动
- CPU 显示用户CPU时间、系统CPU时间
- IPC 显示发送和接收的消息数量
- MEMORY [暂未实现]
- PAGE FAULTS 显示页错误数量
- SOURCE 显示源码中的函数名称与位置
- SWAPS 显示SWAP的次数
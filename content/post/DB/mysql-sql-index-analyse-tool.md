---
title: mysql 查询优化：索引优化
date: 2018-04-05
categories:
 - 数据库
tags:
 - Mysql
 - 数据库
 - 查询优化
toc: true
---

我们在产品中使用 MySQL 数据库的时候，肯定会用到索引的，或是在前期建立一些初始索引，或是在后期 SQL 优化的时候根据系统运行状态逐渐增加索引。不论是以什么方式建立的索引，他们都会影响我们对数据库做的操作，并且是对我们所有的数据操作都有影响，包括 增加、删除、修改、查询、统计 操作。这时如果线上有部分索引在系统升级已经失效了，我们怎么知道，怎么及时的排查和删除，需要我们持续的跟踪和分析。今天我就介绍几款针对线上数据库索引的分析工具。

* pt-index-usage
* userstat
* check-unused-keys

<!--more-->

## 1. pt-index-usage

`pt-index-usage` 从日志里面读取查询，并且分析它们是如何使用索引的。它需要 MySQL 的慢查询日志，在实际分析中我们可以讲 MySQL 的慢查询参数设置为 `0` ，这样就可以得到所有的执行 SQL。

`pt-index-uage` 的安装请参考 [[mysql 查询优化：慢查询分析工具 pt-query-digest](https://blog.threeq.me/post/db/mysql-slow-query-analyse/)]

使用：

```
> pt-index-usage [OPTIONS] [FILES]
```

分析 slow.log 的所有查询语句，并打印报告

```
> pt-index-usage /path/to/slow.log --host localhost
```

不打印报告，同时把分析后的结果存入 `percona` 数据库

```
> pt-index-usage slow.log --no-report --save-results-database percona
```

详情参考 [pt-index-uage 官方文档](https://www.percona.com/doc/percona-toolkit/LATEST/pt-index-usage.html) 和 使用手册 [`pt-index-uage --help`]

## 2. userstat

MySQL 设置：

```
mysql> SET GLOBAL userstat=ON;
mysql> SET GLOBAL `thread_statistics`=1;

mysql> SHOW GLOBAL VARIABLES LIKE "userstat";
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| userstat      | ON    |
+---------------+-------+
1 row in set (0.00 sec)
```

查询客户端连接信息

```
mysql> SELECT * FROM INFORMATION_SCHEMA.CLIENT_STATISTICS\G
*************************** 1. row ***************************
                CLIENT: 10.1.12.30
     TOTAL_CONNECTIONS: 20
CONCURRENT_CONNECTIONS: 0
        CONNECTED_TIME: 0
             BUSY_TIME: 93
              CPU_TIME: 48
        BYTES_RECEIVED: 5031
            BYTES_SENT: 276926
  BINLOG_BYTES_WRITTEN: 217
          ROWS_FETCHED: 81
          ROWS_UPDATED: 0
       TABLE_ROWS_READ: 52836023
       SELECT_COMMANDS: 26
       UPDATE_COMMANDS: 1
        OTHER_COMMANDS: 145
   COMMIT_TRANSACTIONS: 1
 ROLLBACK_TRANSACTIONS: 0
    DENIED_CONNECTIONS: 0
      LOST_CONNECTIONS: 0
         ACCESS_DENIED: 0
         EMPTY_QUERIES: 0
 TOTAL_SSL_CONNECTIONS: 0
```

查询索引使用信息：

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INDEX_STATISTICS
   WHERE TABLE_NAME='tables_priv';
+--------------+-----------------------+--------------------+-----------+
| TABLE_SCHEMA | TABLE_NAME            | INDEX_NAME         | ROWS_READ |
+--------------+-----------------------+--------------------+-----------+
| mysql        | tables_priv           | PRIMARY            |         2 |
+--------------+-----------------------+--------------------+-----------+
```

查询表的使用信息：

```
mysql> SELECT * FROM INFORMATION_SCHEMA.TABLE_STATISTICS
   WHERE TABLE_NAME=``tables_priv``;
+--------------+-------------------------------+-----------+--------------+------------------------+
| TABLE_SCHEMA | TABLE_NAME                    | ROWS_READ | ROWS_CHANGED | ROWS_CHANGED_X_INDEXES |
+--------------+-------------------------------+-----------+--------------+------------------------+
| mysql        | tables_priv                   |         2 |            0 |                      0 |
+--------------+-------------------------------+-----------+--------------+------------------------+
```

具体详情请参考文档：[https://www.percona.com/doc/percona-server/5.7/diagnostics/user_stats.html](https://www.percona.com/doc/percona-server/5.7/diagnostics/user_stats.html)

## 3. check-unused-keys

`check-unused-keys` 是 Ryan Lowe 编写的基于 `userstat` 的一个 perl 脚本。能够比较方便输出需要删除的索引。

下载地址：[https://code.google.com/archive/p/check-unused-keys/downloads](https://code.google.com/archive/p/check-unused-keys/downloads) / [备份地址](https://blog.threeq.me/tools/check-unused-keys)

MySQL 设置：

```
mysql> SET GLOBAL userstat=ON;
mysql> SET GLOBAL `thread_statistics`=1;

mysql> SHOW GLOBAL VARIABLES LIKE "userstat";
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| userstat      | ON    |
+---------------+-------+
1 row in set (0.00 sec)
```

语法：

```
> ./check-unused-keys --help
```

![](/images/mysql-index-analyse/check-unused-keys-help.jpeg)

使用：

```
./check-unused-keys --host=127.0.0.1 --username=root --password=toor --port=3306 --create-alter 
```

参考：

[https://www.percona.com/blog/2009/06/26/check-unused-keys-a-tool-to-interact-with-index_statistics/](https://www.percona.com/blog/2009/06/26/check-unused-keys-a-tool-to-interact-with-index_statistics/)

[https://www.percona.com/blog/2008/09/12/googles-user_statistics-v2-port-and-changes/](https://www.percona.com/blog/2008/09/12/googles-user_statistics-v2-port-and-changes/)

[https://code.google.com/archive/p/check-unused-keys/](https://code.google.com/archive/p/check-unused-keys/)

[https://www.percona.com/blog/2012/12/05/quickly-finding-unused-indexes-and-estimating-their-size/](https://www.percona.com/blog/2012/12/05/quickly-finding-unused-indexes-and-estimating-their-size/)

[https://yq.aliyun.com/articles/308518](https://yq.aliyun.com/articles/308518)








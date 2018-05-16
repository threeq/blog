---
title: 小白学 SQL 第九天：数据插入、修改、删除
date: 2018-05-14
lastmod: 2018-05-14
draft: false
keywords: ["Threeq", "博客", "程序员", "架构师", "Mysql","SQL","SQL学习","数据库","create 语句"]
categories:
 - 数据库
tags:
 - 数据库
 - SQL
toc: true
comment: true
description: "数据库管理系统（DBMS）是 IT 从业者必备工具之一，你能在市面上看到的任何一个软件系统，在后面支持的一定有它的身影。 而这里面关系型数据库管理系统（RDBMS） 目前暂居了绝大部分，操作 RDBMS 的基础就是今天我们要开始学习的 SQL（结构化查询语言），所以我们有必要针对 SQL 进行系统全面的学习。同时会对数据库中的一些基础原理和设计工具进行介绍：ER 图、数据类型、范式等。适合小白用户（初学者和刚入门）。"
---

前面七天主要聚焦在数据查询，就是怎么从表里面取出我们想要的数据。但是这些数据是如何录入到数据库的？如果数据错误了需要修改或删除数据怎么操作？我们如何快速的生产测试数据？这些就是这次我们需要讨论的内容。

知识要点

- 插入数据
- 修改数据
- 删除数据

<!--more-->

# 插入数据

插入数据使用 **insert into** 语句，在前面插入数据的时候我们已经使用。

**语法**

```
insert into tbl_name 
[(field1, field2, ...fieldN)]
values
(value1, value2,...valueN)[,...];
```

* 这里的字段可以省略，如果省略就表示依次插入表中的 **所有列**
* 可以依次插入**多行值**，每个 `()` 表示一行数据，每行之间用`,`分隔
* 插入时对于`NOT NULL`(*不能为空*) 的列必须输入
* 如果数据是字符型或日期，必须使用单引号或者双引号，如："value"

看一个我们之前使用过的插入语句：

```
INSERT INTO student(s_id, s_name, s_sex, s_age, s_birthday, s_addr, s_created, s_status) VALUES (1, '王 1', 1, 16, '2007-04-18', '重庆', '2018-04-18 22:29:27', 1);
```

这个语句的意图是向学生表里面加入一条数据，这里是插入表的所有字段，所以也可以简化成下面这样:

```
INSERT INTO student VALUES (1, '王 1', 1, 16, '2007-04-18', '重庆', '2018-04-18 22:29:27', 1);
```



## insert into … select

**insert into … select** 语句是`select`的查询结果加入到某张表中，这个语法是 MySQL 独有的，其他的 RDBMS 的语法略有不同。这个语句常用于数据汇总、存储过程里面的临时表数据插入等地方。也可以使用这个语句快速产生测试数据，下面我们就看如何快速产生测试数据。

**语法**

```sql
insert into tbl_name[(field1, field2,...fieldN)]
<select_clause>
```

* `<select_clause` 是一个完整的`select`语句，和前面讲解的 select 语句完全一样
* `insert` 中的列描述必须和 `select` 中的列描述对应：数量、位置和类型。
  * 列数量必须一致；
  * 列的对应关系是和位置依次对应；
  * 每个对应位置的列数据类型必须一致。

**快速生成学生测试数据**

```
insert into student(`s_name`, `s_sex`, `s_age`, `s_birthday`, `s_addr`, `s_created`, `s_status`)
select `s_name`, `s_sex`, `s_age`, `s_birthday`, `s_addr`, `s_created`, `s_status` from student;
```

不断执行上面这个语句，你的表中数据将会以指数倍增长。这里的 select 子句中的每个返回列，都可以替换成需要的表达式，以满足不同数据需求。

# 修改数据

需改数据使用 update 语句来操作。

**语法**

```sql
update tbl_name set
field1=value1,
field2=value2
[where Clause]
```

* 可以同时更新一个或多个字段
* where 子句中可以指定任何条件
* 可以在一个单独表中同时跟新多条数据
* `value` 可以是一个表达式

## 计算学生的真实年龄

我们发现学生表中的生日数据和年龄数据是没有对应的，现在我们需要：根据学生的生日计算出实际年龄更新到年龄字段

> 分析：根据学生的生日计算出实际年龄更新到年龄字段
>
> 1. 操作类型：**update** （ 更新）
> 2. 到哪里更新数据：**学生**
> 3. 跟新哪些信息：
>    1. 学生年龄 = 根据生日计算学生真实年龄
> 4. 过滤条件：无
>
> > update 学生 set
> >
> > 学生年龄=真实年龄
>
> *真实年龄* 的计算要求根据学生生日计算，只需要使用当前的年份减去生日的年份就可以了：`year(now() - year(s_birthday)` 

根据以上分析可以得到 SQL

```
update student set
s_age=year(now())-year(s_birthday);
```



- [ ] 将年龄小于16岁学生年龄增加 5 岁
- [ ] 根据以上修改的年龄数据，将学生生日年份调整正确

# 删除数据

当我们数据表中的某些数据不再使用时，可以 delete 语句进行删除。

**语法**

```
delete from tbl_name
[where clause]
```

* 如果没有指定 where 子句，将删除表中所有数据
* where 子句可以包含任何条件
* 可以一次删除多条数据

> 在没有指定 where 子句时，相当于清空表操作。MySQL 中清楚表操作还可以使用： ` truncate tbl_name`

## 删除已结业的班级

> 分析：删除已结业的班级
>
> 1. 操作类型：**delete**（删除）
> 2. 删除哪里数据：班级
> 3. 过滤条件：已结业
>
> > delete from 班级
> >
> > where 班级状态=已结业

得到以下 SQL

```
delete from class
where c_status=4;
```

> 这里的 where 子句和查询中的 where 子句一样，可以使用子查询进行更复杂的删除操作。

试试

- [ ] 删除处于异常状态的班级
- [ ] 删除没有学生参与的班级

总计

- 插入数据：insert 结构、insert select 结构
- 修改数据：update 语句
- 删除数据：delete 语句，清空表操作


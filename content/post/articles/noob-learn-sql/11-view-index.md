---
title: 小白学 SQL 第十一天：索引和视图
date: 2018-05-30
lastmod: 2018-05-30
draft: false
keywords: ["Threeq", "博客", "程序员", "架构师", "Mysql","SQL","SQL学习","数据库","视图","索引","SQL 优化"]
categories:
 - 数据库
tags:
 - 数据库
 - SQL
toc: true
comment: true
description: "数据库管理系统（DBMS）是 IT 从业者必备工具之一，你能在市面上看到的任何一个软件系统，在后面支持的一定有它的身影。 而这里面关系型数据库管理系统（RDBMS） 目前暂居了绝大部分，操作 RDBMS 的基础就是今天我们要开始学习的 SQL（结构化查询语言），所以我们有必要针对 SQL 进行系统全面的学习。同时会对数据库中的一些基础原理和设计工具进行介绍：ER 图、数据类型、范式等。适合小白用户（初学者和刚入门）。"
---

已经介绍了 SQL 的查询、定义、插入、修改、删除等操作，接下来将介绍数据库另一个重要的知识点：**索引**，特别是在查询优化的时候，**索引** 将是优化的最重要手段之一。查询本身会随着我们的应用功能的增强，不断的增加复杂度，这时就需要管理复杂查询的手段：*视图* 。

知识要点

- 索引
- MySQL 索引操作语句
- BTREE 和 HASH
- 视图

这里的内容可能有点难，有一定使用经验可能会更容易理解。不过没有关系只要知道索引的基本概念和操作语句就行，大家真的在使用到时再来看或查询相关资料就可以了。

<!--more-->

现代数据库无一不包含 **索引**。首先我们需要理解为什么？就像之前说的，数据库是用来做大量数据管理和查询的系统。在现在这个以数据为中心的时代，任意一个业务系统数据量也是动辄百万了，大部分业务系统都在千万到亿这个级别，现在大家平时接触到的系统在亿这个级别的很多。这么大的数据量存储在磁盘中，怎么能快速的获取我们所需要的数据？总不能每次都取出全部数据吧！（当然这里数据的高效存储也非常重要，不过这个已经超出了这里范围了不做介绍）

# 索引

数据库中的所有数据都会持久化的磁盘中，磁盘读取速度是很慢的，并且数据库里的数据都会比较大，如果我们每次查询都从磁盘里面读入所有数据进行比较过滤，那将会是非常慢的。所以数据库为了更快的检索需要的数据，就需要使用一种高效的数据结构来组织编目原始数据，这就是这里介绍的： **索引**。

大家不要以为索引数据会很小，其实索引也是很大的。如果索引长度是 16字节，表数据量是 1亿，那表的这个索引存储需要的空间至少是15G（因为在存储的时候还需要存储索引结构的其他信息）。计算机的内存资源是很昂贵的，且索引数据也需要永久存储，所以索引结构数据也是存储在磁盘里面。数据库在读取数据时是按照每页读取的，数据库会以页为单位缓存已经读取的索引数据。关于如何估算页数量不在本文内容中，但是这个对于理解如何优化 SQL 会很重要，感兴趣的可以查询相关资料。



## MySQL 索引语法

MySQL 里面索引管理使用 alter 语句，对于创建索引还可以使用 create index 语句。

###  Create Index

create index 语句只是 alter table 语句的另一种语法， 可以完全映射到 alter table 创建索引语句中。并且 create index 不能用于 **主键** 的创建，**主键** 的创建需要使用 alter 语句或在 create table 表结构创建语句中。

```sql
CREATE [UNIQUE|FULLTEXT|SPATIAL] INDEX index_name
    [index_type]
    ON tbl_name (index_col_name,...)
    [index_option]
    [algorithm_option | lock_option] ...

index_col_name:
    col_name [(length)] [ASC | DESC]

index_option:
    KEY_BLOCK_SIZE [=] value
  | index_type
  | WITH PARSER parser_name
  | COMMENT 'string'

index_type:
    USING {BTREE | HASH}

algorithm_option:
    ALGORITHM [=] {DEFAULT|INPLACE|COPY}

lock_option:
    LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}
```

### Alter 语句

使用ALTER 语句添加索引

```sql
Alter TABLE tbl_name ADD [INDEX|UNIQUE|FULLTEXT|SPATIAL] 
index_name(index_col_name,...);
```

使用 ALTER 语句添加主键

```
ALTER TABLE tbl_name ADD PRIMARY KEY (index_col_name,...);
```

删除索引

```
ALTER TABLE tbl_name DROP INDEX index_name;
```

删除主键

```
ALTER TABLE tbl_name DROP PRIMARY KEY;
```

你可以使用 SHOW INDEX 命令来列出表中的相关的索引信息。可以通过添加 \G 来格式化输出信息。

```
SHOW INDEX FROM tbl_name; \G
```

这里这里我把主键和外键也看做是索引，他们只是索引的 2 中特殊类型

> - 索引分类：普通索引（默认）、唯一索引（unique）、全文索引（fulltext）、空间索引（spatial）、主键、外键
> - 普通索引和唯一索引的数据结构类型可以有：BTree 和 Hash
> - 空间索引使用 R-Tree，也叫 R-Tree 索引
> - 主键一个表只能有一个，可以包含多个列，且列的数据(如果是多列，就是组合数据)必须唯一，且列值不能为 NULL
> - 当遇到比较大的字符串字段，可以仅仅使用字段前面部分数据创建索引



## 索引类型

这里面 **主键、外键、普通索引、唯一索引** 比较常见，*全文索引* 和 *空间索引* 在一些特定的业务场景里面会使用到。

针对 **普通索引** 和 **唯一索引** ，底层的存储的数据类型可以有2个选择：一个是 B Tree，一个是 Hash。由于底层的数据结构不同，所以两种类型支持的操作也有所区别。并且不同的存储引擎对索引类型的支持也是不同的。全文索引的数据结构类型的实现依赖于存储引擎，空间索引使用 R-Tree 实现。

| 存储引擎类型 | 索引类型    |
| ------------ | ----------- |
| InnoDB       | BTREE       |
| MyISAM       | BTREE       |
| MEMORY/HEAP  | HASH, BTREE |
| NDB          | HASH, BTREE |



不同存储引擎对于索引类型支持的特性也是不同的。

**InnoDB 存储引擎支持特性**

| 索引分类    | 索引类型 | Null 值 | 多个 NULL值 | IS NULL 扫描方式 | IS NOT NULL 扫描方式 |
| ----------- | -------- | ------- | ----------- | ---------------- | -------------------- |
| Primary key | `BTREE`  | No      | No          | N/A              | N/A                  |
| Unique      | `BTREE`  | Yes     | Yes         | Index            | Index                |
| Key         | `BTREE`  | Yes     | Yes         | Index            | Index                |
| `FULLTEXT`  | N/A      | Yes     | Yes         | Table            | Table                |
| `SPATIAL`   | N/A      | No      | No          | N/A              | N/A                  |

 

**MyISAM 存储引擎支持特性**

| 索引分类    | 索引类型 | Null 值 | 多个 NULL值 | IS NULL 扫描方式 | IS NOT NULL 扫描方式 |
| ----------- | -------- | ------- | ----------- | ---------------- | -------------------- |
| Primary key | `BTREE`  | No      | No          | N/A              | N/A                  |
| Unique      | `BTREE`  | Yes     | Yes         | Index            | Index                |
| Key         | `BTREE`  | Yes     | Yes         | Index            | Index                |
| `FULLTEXT`  | N/A      | Yes     | Yes         | Table            | Table                |
| `SPATIAL`   | N/A      | No      | No          | N/A              | N/A                  |

 

**MEMORY 存储引擎支持特性**

| 索引分类    | 索引类型 | Null 值 | 多个 NULL值 | IS NULL 扫描方式 | IS NOT NULL 扫描方式 |
| ----------- | -------- | ------- | ----------- | ---------------- | -------------------- |
| Primary key | `BTREE`  | No      | No          | N/A              | N/A                  |
| Unique      | `BTREE`  | Yes     | Yes         | Index            | Index                |
| Key         | `BTREE`  | Yes     | Yes         | Index            | Index                |
| Primary key | `HASH`   | No      | No          | N/A              | N/A                  |
| Unique      | `HASH`   | Yes     | Yes         | Index            | Index                |
| Key         | `HASH`   | Yes     | Yes         | Index            | Index                |

 

**NDB 存储引擎支持特性**

| 索引分类    | 索引类型 | Null 值 | 多个 NULL值 | IS NULL 扫描方式   | IS NOT NULL 扫描方式 |
| ----------- | -------- | ------- | ----------- | ------------------ | -------------------- |
| Primary key | `BTREE`  | No      | No          | Index              | Index                |
| Unique      | `BTREE`  | Yes     | Yes         | Index              | Index                |
| Key         | `BTREE`  | Yes     | Yes         | Index              | Index                |
| Primary key | `HASH`   | No      | No          | Table (see note 1) | Table (see note 1)   |
| Unique      | `HASH`   | Yes     | Yes         | Table (see note 1) | Table (see note 1)   |
| Key         | `HASH`   | Yes     | Yes         | Table (see note 1) | Table (see note 1)   |

 

: 注意

: 1. 如果使用 `HASH` ，则可以防止创建隐式有序索引。

说了这么多 BTREE 和 Hash 对于我们平时使用有什么差异。

> * B-Tree 支持的操作有等于、不等于、小于、小于、Between、前缀 like，in
> * Hash 支持支 等于和不等于 2 种操作。特别注意它是不支持 大于、小于之类的区间型条件的，因为 Hash 类型是无序的，并且对于 order by 排序操作不能使用 Hash 索引加快速度
> * like 操作如果不是前缀匹配是不能使用使用索引的。如 `col_name like 'aa%'` 是可以使用索引的，但是 `col_name like '%aa'` 和 `col_name like '%aa%'` 都不能使用索引。

## 索引使用分析

正所谓 **过早优化是万恶之源** 。我们 **不应该在一创建表时就创建索引，应该是在查询真的慢的时候才创建索引** ，因为索引在提高查询速度的时候，也会使 insert、update、delete 语句的操作变慢，并且随着业务功能的迭代，索引也需要跟着优化和修改。这就需要有一定的索引分析手段。

1、索引分析手段

> ① 针对单个 SQL 可以使用 **执行计划** 查看索引使用情况
>
> ② 可以使用 `show status like 'Handler_read%';` 查看 MySQL 索引使用率
>
> ③ 针对数据库中未使用索引分析，可以收集一段时间内数据库执行的所有 SQL 语句，然后使用三方工具分析数据库中哪些索引已经 *失效* 。比如 `pt-index-usage` 等。

2、创建索引时需要注意

> ①主键自动建立唯一索引
>
> ②频繁作为查询条件的字段应该创建索引
>
> ③查询中与其他表关联的字段，外键关系建立索引
>
> ④频繁更新的字段不适合建立索引，因为每次更新不单单是更新了记录还会更新索引
>
> ⑤WHERE条件里用不到的字段不创建索引
>
> ⑥单键/组合索引的选择问题，who?(在高并发下倾向创建组合索引)
>
> ⑦查询中排序的字段，排序的字段若通过索引去访问将大大提高排序速度
>
> ⑧查询中统计或者分组字段

3、哪些情况不要创建索引

> ①表记录太少
>
> ②经常增删改的表
>
> 　　提高了查询速度，同时却会降低更新表的速度，如对表进行INSERT、UPDATE、和DELETE。
>
> 　　因为更新表时，MySQL不仅要保存数据，还要保存一下索引文件。
>
> 　　数据重复且分布平均的表字段，因此应该只为最经常查询和最经常排序的数据建立索引。
>
> ③注意，如果某个数据列包含许多重复的内容，为它建立索引就没有太大的实际效果。

# 视图

## 什么是视图？

在 SQL 中，**视图是基于 SQL 语句的结果集的可视化的表**。可以简单的理解成：*视图就是存储在数据库中并具有名字的 SQL 语句* ，它是管理复杂 SQL 查询的一种方式。

视图包含行和列，就像一个真实的表。视图中的字段就是来自一个或多个数据库中的真实的表中的字段。我们可以向视图添加 SQL 函数、WHERE 以及 JOIN 语句，我们也可以提交数据，就像这些来自于某个单一的表。

视图，一种虚拟的表，允许用户执行以下操作：

- 以用户或者某些类型的用户感觉自然或者直观的方式来组织数据；
- 限制对数据的访问，从而使得用户仅能够看到或者修改（某些情况下）他们需要的数据；
- 从多个表中汇总数据，以产生报表。

注释：数据库的设计和结构不会受到视图中的函数、where 或 join 语句的影响。

## SQL 创建视图

```
CREATE VIEW view_name AS
SELECT column_name(s)[,...]
FROM table_name
WHERE condition
```

注释：视图总是显示最近的数据。每当用户查询视图时，数据库引擎通过使用 SQL 语句来重建数据。

可以从某个查询内部、某个存储过程内部，或者从另一个视图内部来使用视图。通过向视图添加函数、join 等等，我们可以向用户精确地提交我们希望提交的数据。

以之前的学生表为例子，创建一个包含学生名字、学生参与班级名称、根据学生生日计算的年龄视图

```
CREATE VIEW student_view AS
SELECT s.s_name, year(now())-year(s.s_birthday), c.c_name
FROM student s,class c, student_join_class sc
where s.s_id=sc.s_id and c.c_id=sc.c_id
```

我们可以查询上面这个视图：

```
SELECT * FROM student_view
```

: 试试

- [ ] 创建一个包含班级 id、班级名称、班主任、参与人员的视图，视图名称 class_view。（*注意统计函数所使用的字段*）

## SQL 更新视图

视图可以在特定的情况下更新：

- SELECT 子句不能包含任何汇总函数（summary functions）
- SELECT 子句不能包含任何集合函数（set functions）
- SELECT 子句不能包含任何集合运算符（set operators）
- 查询语句中不能有 GROUP BY 或者 HAVING

如果视图满足以上所有的条件，该视图就可以被更新。当然如果需要通过视图使用 insert 语句，那还需要满足其他条件，不过个人不建议这样使用。

您可以使用下面的语法来更新视图：

```
CREATE OR REPLACE VIEW view_name AS
SELECT column_name(s)[,...]
FROM table_name
WHERE condition
```

现在，向 student_view 中加入性别、地址信息：

```
CREATE OR REPLACE VIEW student_view AS
SELECT s.s_name, year(now())-year(s.s_birthday), c.c_name, s.s_sex, s.s_addr
FROM student s,class c, student_join_class sc
where s.s_id=sc.s_id and c.c_id=sc.c_id;
```

查询上面这个视图，看修改结果：

```
SELECT * FROM student_view
```

## SQL 删除视图

您可以通过 DROP VIEW 命令来删除视图。

```
DROP VIEW view_name
```

:试试

- [ ] 向 class_view 中加入参与学生的平均年龄。（需要先删除再创建）

# 总结

- 索引：索引创建、作用、分析索引使用情况
- 视图：视图创建、修改、删除、使用


---
title: 小白学 SQL 第八天：表结构管理
date: 2018-05-10
lastmod: 2018-05-10
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

前面七天全部聚焦在数据查询，就是怎么从表里面取出我们想要的数据。但是这些表是如何建立？建立的时候需要注意哪些信息？如果修改或删除表结构？。这次就一起来讨论表结构的基本管理操作。

知识要点

* 创建表
* 修改表
* 删除表


<!--more-->

# 创建表

创建表所需要基本信息：

* 表名
* 字段名称
* 定义每个字段选项
* 定义表选项

其中 *字段选项* 和 *表选项* 每个数据库系统会有所不同。

**基础语法**

```sql
create [temporary] table table_name (
	column_name column_type [column_options] [,...]
) [table_options];
```

- temporary: 表示当前创建的表示临时表。**临时表只在当前连接可见，当关闭连接时，MySQL会自动删除表并释放所有空间。**
- `table_name`: 表名称
- `column_name`： 列名称
- `data_type`： 列数据类型。[查看数据类型描述](https://blog.threeq.me/post/articles/noob-learn-sql/2-create-table/)
- `column_options`：列定义选项
- `table_options`：表定义选项
- `[, …]`: 表示可以有多个列定义，使用 `,` 分割

要看 MySQL 详细 create table 语法，请参考 [《MySQL 官方手册》](https://dev.mysql.com/doc/refman/5.7/en/create-table.html)。

首先我们来看一下我们前面用到的班级表的创建语句:

```
CREATE TABLE `class` (
  `c_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '班级 id，主键',
  `c_name` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班级名称',
  `c_head_teacher` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班主任名称',
  `c_start_time` date DEFAULT NULL COMMENT '开班日期',
  `c_end_time` date DEFAULT NULL COMMENT '结束日期',
  `c_status` int(11) NOT NULL COMMENT '班级状态【0：报名未开始，1：报名中，2：报名完成，3：已开学，4：已结业】',
  `c_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级信息表';
```

1 列定义分析: `c_id int(11) NOT NULL AUTO_INCREMENT COMMENT '班级 id，组件'`

* `c_id`  列名
* `int(11)` 列类型为整型。[查看其他数据类型描述](https://blog.threeq.me/post/articles/noob-learn-sql/2-create-table/)
* `not null` 定义列不能为空（必须有值）
* `AUTO_INCREMENT` 列是否自动增长。**一个表只能有一个自动增长列列，并且数据类型必须为数值型**
* `COMMENT '班级 id，主键'` 列注释（描述列的作用）

2 主键定义分析： **`PRIMARY KEY (c_id)`** 

* 定义表的主键，可以同时包含多个列，使用 `,` 分隔

3 表选项分析：`ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级信息表'`

* `ENGINE=InnoDB` 定义表的存储引擎
* `DEFAULT CHARSET=utf8mb4` 表文本采用字符集为 utf8mb4。
* `COLLATE=utf8mb4_unicode_ci` 表校对规则 utf8mb4_unicode_ci
* `COMMENT='班级信息表'` 表注释说明

> 当前数据库支持字符集和校对规则可以使用 `SHOW CHARACTER SET;` 查看。
>
> 字符集详细信息请查看 [MySQL 字符集说明文档](https://dev.mysql.com/doc/refman/5.7/en/charset.html)

```
create table learn_test (
  col_1 int not null,
  col_2 varchar(12) default null,
  primary key(col_1)
) engine=InnoDB default charset=utf8 comment='学习测试';
```

使用 `desc learn_test` 查看表结构：

![](/images/articles/noob-learn-sql/08-create-01.jpeg)

# 修改表

修改表的 `alter table` 语句作用很多，里面的语法也比较多，这里只列举常见的用法，详细的使用和语法参考 [《Mysql 官方文档》](https://dev.mysql.com/doc/refman/5.7/en/alter-table.html)。

## 增加列

**语法**

```
ALTER TABLE tbl_name ADD column_name column_type [column_options];
```

*增加 col_3 列，数据类型为 int，其不能为空* :（执行过后可以使用`desc learn_test`  查看最新表结构）

```
alter table learn_test add col_3 int not null;
```

![](/images/articles/noob-learn-sql/08-alter-01.jpeg)

## 删除列

**语法**

```
ALTER TABLE tbl_name  DROP column_name;
```

*删除 col_1 列*

```
alter table learn_test drop col_1;
```

请使用 `desc learn_test` 查看最新表结构。

## 修改列名字和类型

**语法**

```
ALTER TABLE tbl_name CHANGE column_name new_column_name new_column_type [new_column_options];
```

*修改 col_2 为 col_0 ，数据类型 bigint ,默认值 0 且不为空*

```
alter table learn_test change col_2 col_0 bigint not null default 0;
```

请使用 `desc learn_test` 查看最新表结构。

>  如果这里不修改列名可以使用 modify 关键字：`ALTER TABLE tbl_name MODIFY column_name column_type [column_options];`

## 修改表名

**语法**

```
ALTER TABLE tbl_name RENAME TO new_tbl_name;
```

*修改 learn_test 为 learn_temp*

```
alter table learn_test rename to learn_temp;
```

可以使用 `show tables;` 查看修改结果。

## 修改表存储类型

```
ALTER TABLE tbl_name TYPE = MYISAM;
```

其他的表选项语法相似：`alter table table_name option_name=option_value`

## 修改表字符集

```
ALTER TABLE tbl_name CONVERT TO CHARACTER SET charset_name;
```

#  删除表

```
DROP [TEMPORARY] TABLE [IF EXISTS]
    tbl_name [, tbl_name] ...
    [RESTRICT | CASCADE]
```

* `TEMPORARY` 表示删除的是临时表
* `IF EXISTS` 如果表存在就删除，不存无操作。语句永远正确
* `RESTRICT` 确保只有不存在相关视图和 完整性约束的表才能删除
* `CASCADE`  任何相关视图和完整性约束一并被删除

```sql
drop table if exists
learn_test, learn_temp;
```

![](/images/articles/noob-learn-sql/08-drop-01.jpeg)

可以再次执行上面的 sql 和 `drop table learn_test, learn_temp;` 看有什么不同返回信息。

# 总结

* 创建表： create 语句语法、表存储引擎、字符集、列
* 修改表：增加/删除字段、重命名字段、修改字段类型
* 表删除：drop 语法
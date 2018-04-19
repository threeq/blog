---
title: 小白学 SQL 第二天：数据表创建
date: 2018-04-18
lastmod: 2018-04-18
draft: false
keywords: ["Threeq", "博客", "程序员", "架构师", "Mysql","SQL","SQL学习","数据库","ER图"]
categories:
 - 数据库
tags:
 - 数据库
 - SQL
toc: true
comment: true
description: "数据库管理系统（DBMS）是 IT 从业者必备工具之一，你能在市面上看到的任何一个软件系统，在后面支持的一定有它的身影。 而这里面关系型数据库管理系统（RDBMS） 目前暂居了绝大部分，操作 RDBMS 的基础就是今天我们要开始学习的 SQL（结构化查询语言），所以我们有必要针对 SQL 进行系统全面的学习。同时会对数据库中的一些基础原理和设计工具进行介绍：ER 图、数据类型、范式等。适合小白用户（初学者和刚入门）。"
---

《小白学 SQL》第二天

今天我们来学习数据表（table）的建立，涉及到的内容可能大家还不能完全理解，这里主要是为后面的查询语句做些基本准备和数据准备，后面还会专门学习 DDL（数据学习语言），所以没有关系这里大家只要能执行得到正确结果就行。

今天涉及到的内容有：

1. 表创建语句（create）
2. 数据插入语句（insert ）
3. MySQL 基本数据类型
4. E-R图（实体关系图）

<!--more-->

# 启动学习环境

这里假设你的 docker 服务由于某些原因停止了（如：开关机），需要手动启动相关服务。如果你的 docker 服务和 `sql-learn` 已经正常启动，请跳过此章节（[什么？你还没有 docker 和 sql-learn，请看这里](https://blog.threeq.me/post/articles/noob-learn-sql/1-install-tools/)）。这里所有的操作都可以参考第一天的内容，[在这里](https://blog.threeq.me/post/articles/noob-learn-sql/1-install-tools/)。

1. 启动 docker 服务

   >  A、windows 通过桌面图标 或 系统菜单来启动
   >
   > B、Mac 通过 Launchpad 面板来图标启动
   >
   > C、Linux 通过命令行启动，不同版本会有所不同，可以查看第一天学的内容。


2. 启动数据库服务器 (sql-learn 容器)
  
  打开命令行工具输入一下命令，启动 sql-learn 容器

```
docker start sql-learn
```

输入一下命令查看启动状态

```
docker ps
```

结果如下：

![](/images/articles/noob-learn-sql/01-docker-mysql-install-1.jpeg)


3. 启动数据库客户端（Navicat）

打开 Navicat 软件，通过左边的连接收藏栏，双击 `sql-learn` 连接，连接到数据库服务器（图中 <1>）。然后打开 `sql-learn` 数据库，就是双击 `sql-learn` 数据库（图中 <2>）。打开结果如下图：

![](/images/articles/noob-learn-sql/02-open-db.jpeg)

>  **<font color="red">通过以上 3 步，我们就打开了我们的学习环境，对于我们以后的每次学习进来的操作步骤都是一样的，所以这里大家一定要会，如果有什么问题可以给我留言。</font>**

# 创建数据表

## create table (创建表)语句结构

以下是上面 SQL 语句的简单模板说明，具体完整的 `CREATE TABLE` 语句语法请参考 [MySQL 官方文档](https://dev.mysql.com/doc/refman/5.7/en/create-table.html)。我们这里使用的足够了

```
CREATE TABLE <table_name> (
  <column_name> <data_type> [column_options] [COMMENT '<comment>']
  [, ...]
) [table_options]
```

- `table_name`: 表名称
- `column_name`： 列名称
- `data_type`： 列数据类型
- `column_options`：列定义选项
- `comment` ：注释
- `table_options`：表定义选项
- `[, …]`: 表示可以有多个列定义，使用 `,` 分割

## 设计并创建表

这里我们构想一个培训班的业务场景：

> 一个培训班有很多学生
>
> 每个学生可以参加多个培训班

### 班级信息表

![ER 图](/images/articles/noob-learn-sql/02-ER.jpeg)

班级表创建 SQL ：

```sql
CREATE TABLE `class` (
  `c_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '班级 id，组件',
  `c_name` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班级名称',
  `c_head_teacher` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班主任名称',
  `c_start_time` date DEFAULT NULL COMMENT '开班日期',
  `c_end_time` date DEFAULT NULL COMMENT '结束日期',
  `c_status` int(11) NOT NULL COMMENT '班级状态【0：报名未开始，1：报名中，2：报名完成，3：已开学，4：已结业】',
  `c_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级信息表';
```

### 学生信息表



学生表创建 SQL：

```sql
CREATE TABLE `student` (
  `s_id` int(11) NOT NULL AUTO_INCREMENT COMMENT ' 学生 id',
  `s_name` varchar(64) NOT NULL COMMENT '学生名称',
  `s_sex` tinyint(4) DEFAULT NULL COMMENT '学生性别',
  `s_age` int(11) DEFAULT NULL COMMENT '学生年龄',
  `s_birthday` date NOT NULL COMMENT '学生生日',
  `s_addr` varchar(512) DEFAULT NULL COMMENT '学生地址',
  `s_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '加入时间',
  `s_status` int(11) DEFAULT NULL COMMENT '状态（0：禁用，1：可用）',
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表';
```

### 学生班级关联表



学生班级关联表(记录学生参加了那些培训班) SQL：

```sql
CREATE TABLE `student_join_class` (
  `c_id` int(11) NOT NULL COMMENT '班级 id',
  `s_id` int(11) NOT NULL COMMENT '学生表',
  `cs_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '加入时间',
  PRIMARY KEY (`c_id`,`s_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生班级关联表';
```

对于以上 SQL 语句可以在 [这里下载](https://blog.threeq.me/data/sql-learn.sql).

## 数据类型说明

在我们的数据表创建语句里面，有个很重要的概念，也是数据库重要概念之一：数据类型（如：`int(11)、timestamp、date`等）。列的数据类型是描述了列可以接受保持的数据和如何存储数据。每种数据库管理系统的数据类型定义有略微不同，这里我们以 MySQL 数据类型为例说明，其他数据库的请查询相关文档。这里的数据类型大家不用全部记住，只要用到的时候查询参考文档就行。

在 MySQL 中，有三种主要的类型：文本、数字、和日期/时间类型。

### 文本类型（Text）

| 数据类型         | 描述                                                         |
| ---------------- | ------------------------------------------------------------ |
| CHAR(size)       | 保存固定长度的字符串（可包含字母、数字以及特殊字符）。在括号中指定字符串的长度。最多 255 个字符。 |
| VARCHAR(size)    | 保存可变长度的字符串（可包含字母、数字以及特殊字符）。在括号中指定字符串的最大长度。最多 255 个字符。注释：如果值的长度大于 255，则被转换为 TEXT 类型。 |
| TINYTEXT         | 存放最大长度为 255 个字符的字符串。                          |
| TEXT             | 存放最大长度为 65,535 个字符的字符串。                       |
| BLOB             | 用于 BLOBs (Binary Large OBjects)。存放最多 65,535 字节的数据。 |
| MEDIUMTEXT       | 存放最大长度为 16,777,215 个字符的字符串。                   |
| MEDIUMBLOB       | 用于 BLOBs (Binary Large OBjects)。存放最多 16,777,215 字节的数据。 |
| LONGTEXT         | 存放最大长度为 4,294,967,295 个字符的字符串。                |
| LONGBLOB         | 用于 BLOBs (Binary Large OBjects)。存放最多 4,294,967,295 字节的数据。 |
| ENUM(x,y,z,etc.) | 允许你输入可能值的列表。可以在 ENUM 列表中列出最大 65535 个值。如果列表中不存在插入的值，则插入空值。注释：这些值是按照你输入的顺序存储的。可以按照此格式输入可能的值：ENUM('X','Y','Z') |
| SET              | 与 ENUM 类似，SET 最多只能包含 64 个列表项，不过 SET 可存储一个以上的值。 |

### 数字类型（Number）

| 数据类型        | 描述                                                         |
| --------------- | ------------------------------------------------------------ |
| TINYINT(size)   | -128 到 127 常规。0 到 255 无符号*。在括号中规定最大位数。   |
| SMALLINT(size)  | -32768 到 32767 常规。0 到 65535 无符号*。在括号中规定最大位数。 |
| MEDIUMINT(size) | -8388608 到 8388607 普通。0  到 16777215 无符号*。在括号中规定最大位数。 |
| INT(size)       | -2147483648 到 2147483647 常规。0 到 4294967295 无符号*。在括号中规定最大位数。 |
| BIGINT(size)    | -9223372036854775808 到 9223372036854775807 常规。0 到 18446744073709551615 无符号*。在括号中规定最大位数。 |
| FLOAT(size,d)   | 带有浮动小数点的小数字。在括号中规定最大位数。在 d 参数中规定小数点右侧的最大位数。 |
| DOUBLE(size,d)  | 带有浮动小数点的大数字。在括号中规定最大位数。在 d 参数中规定小数点右侧的最大位数。 |
| DECIMAL(size,d) | 作为字符串存储的 DOUBLE 类型，允许固定的小数点。             |

> 这些整数类型拥有额外的选项 UNSIGNED。通常，整数可以是负数或正数。如果添加 UNSIGNED 属性，那么范围将从 0 开始，而不是某个负数。

### 日期/时间类型（Date）

| 数据类型    | 描述                                                         |
| ----------- | ------------------------------------------------------------ |
| DATE()      | 日期。格式：YYYY-MM-DD注释：支持的范围是从 '1000-01-01' 到 '9999-12-31' |
| DATETIME()  | *日期和时间的组合。格式：YYYY-MM-DD HH:MM:SS注释：支持的范围是从 '1000-01-01 00:00:00' 到 '9999-12-31 23:59:59' |
| TIMESTAMP() | *时间戳。TIMESTAMP 值使用 Unix 纪元('1970-01-01 00:00:00' UTC) 至今的描述来存储。格式：YYYY-MM-DD HH:MM:SS注释：支持的范围是从 '1970-01-01 00:00:01' UTC 到 '2038-01-09 03:14:07' UTC |
| TIME()      | 时间。格式：HH:MM:SS 注释：支持的范围是从 '-838:59:59' 到 '838:59:59' |
| YEAR()      | 2 位或 4 位格式的年。注释：4 位格式所允许的值：1901 到 2155。2 位格式所允许的值：70 到 69，表示从 1970 到 2069。 |

> 即便 DATETIME 和 TIMESTAMP 返回相同的格式，它们的工作方式很不同。在 INSERT 或 UPDATE 查询中，TIMESTAMP 自动把自身设置为当前的日期和时间。TIMESTAMP 也接受不同的格式，比如 YYYYMMDDHHMMSS、YYMMDDHHMMSS、YYYYMMDD 或 YYMMDD。

# 录入数据

数据库插入数据使用 `insert` 语句，我们使用到的所有数据插入 sql 到 [这里下载](https://blog.threeq.me/data/insert-data.sql)。下载下来过后将里面所有 SQL 语句拷贝到 Navicat 客户端的查询窗口里面，如下图：

![](/images/articles/noob-learn-sql/02-insert-01.jpeg)

点击执行，会得到一下结果：

![](/images/articles/noob-learn-sql/02-insert-02.jpeg)

这时打开**左边 Tables 里面 `class` 表** 会看到如下图数据已经进去了

![](/images/articles/noob-learn-sql/02-insert-03.jpeg)

里面涉及到的 `insert` 有一下如下两种格式

语法格式一

```sql
INSERT INTO [数据库名.]表名称[(列1,列2,...)] VALUES (值1, 值2,....)
```

实例：

```sql
INSERT INTO student(s_id, s_name, s_sex, s_age, s_birthday, s_addr, s_created, s_status) VALUES (1, '王 1', 1, 16, '2007-04-18', '重庆', '2018-04-18 22:29:27', 1);
```

语法格式二（批量插入）

```
INSERT INTO table_name (列1, 列2,...) 
VALUES 
(值1, 值2,....)
[,...]
```

实例：

```
INSERT INTO `sql-learn`.`student_join_class`(`c_id`, `s_id`, `cs_created`) 
VALUES 
(1, 2, '2018-03-18 10:37:00'),
(1, 3, '2018-02-18 09:41:41'),
(1, 4, '2017-04-03 12:10:00'),
(1, 5, '2018-01-28 14:30:00'),
(1, 10, '2018-04-18 22:26:41');
```

详细语法格式参考 [MySQL 官方文档](https://dev.mysql.com/doc/refman/5.7/en/insert.html)。

# E-R 图（实体关系图）

E-R 图是我个人感觉学习数据库必须掌握的一个技能，它是学习和分析数据库的一个有力工具，能让我们很快的对数据表之间关系形成一个全局观，对我们编写、分析 SQL 也是一个有力的工具。今天先简单讲解一下 E-R 图的基本内容，让大家可以看懂后面出现的 ER 图，后面会有专门的章节详解讲解 E-R 图。

ER图分为实体、属性、关系三个核心部分。实体是长方形体现，而属性则是椭圆形，关系为菱形。

**ER图的实体（entity）**即数据模型中的数据对象，例如人、学生、音乐都可以作为一个数据对象，用长方体来表示，每个实体都有自己的实体成员（entity member）或者说实体对象（entity instance），例如学生实体里包括张三、李四等，实体成员（entity member）/实体实例（entity instance） 不需要出现在ER图中。

**ER图的属性（attribute）**即数据对象所具有的属性，例如学生具有姓名、学号、年级等属性，用椭圆形表示，属性分为唯一属性（ unique attribute）和非唯一属性，唯一属性指的是唯一可用来标识该实体实例或者成员的属性，用下划线表示，一般来讲实体都至少有一个唯一属性。

**ER图的关系（relationship）**用来表现数据对象与数据对象之间的联系，例如学生的实体和成绩表的实体之间有一定的联系，每个学生都有自己的成绩表，这就是一种关系，关系用菱形来表示。

ER图中关联关系有三种：

* 1对1（1:1） ：1对1关系是指对于实体集A与实体集B，A中的每一个实体至多与B中一个实体有关系；反之，在实体集B中的每个实体至多与实体集A中一个实体有关系。
* 1对多（1:N） ：1对多关系是指实体集A与实体集B中至少有N(N>0)个实体有关系；并且实体集B中每一个实体至多与实体集A中一个实体有关系。
* 多对多（M:N） ：多对多关系是指实体集A中的每一个实体与实体集B中至少有M(M>0)个实体有关系，并且实体集B中的每一个实体与实体集A中的至少N（N>0）个实体有关系。

实例讲解：这个是上面创建的`班级`、`学生` ER 图（注意：此图的部分画法不是标准的，不过不影响大家理解，也建议大家平时多多手画 ER 图，不是那么标准也没有关系，只要不影响理解就行）![ER 图](/images/articles/noob-learn-sql/02-ER.jpeg)

* **班级、学生** 是实体。一个学生一个参加多个(**M**)班级，一个班级可以包含多个(**N**)学生。
* **班级名称、学生性别** 是属性。每个实体(**班级或学生**)都可以有多个属性。
* **参加** 是关系，参见关系本身还包含有 *参加时间* 属性。学生加入班级的时候有 *参加时间* 。

*有兴趣的可以自己手动画一下下面的 ER 图：有一个 `班级` 的实体，包含属性：课程名称、课程学分、授课老师。一个班级只授一门课程，但是班级的学生可以多次参加这么课程的考试。*

大家可能已经发现这里和我们实际建立的数据库表有所区别，这里表示的实体只有 2 个，但是我们时间建立的表却有 3 个。这里是我有意为之的，因为我发现很多初学者往往会有一个误区：误认为数据库的每个数据表都会对应 ER 图中的一个实体，其实这个是错误的。

这是由于我们在实际建立数据库表的时候，会将 **多对多（M:N）** 关系拆分成 **1对多（1:N）** 关系，中间会多建立一个 **关联表** （关联表也是物理数据表）。所以这里大家记住： ER图 转换成物理数据表的时候，可能会有所不同，但是他们的关系结构一定是一致的。我们有时还会把一个 **实体** 拆分成多个数据表进行存储，只要到家记住这个误区就行，具体为什么这个不属于这次内容范围，有兴趣的可以自行查找相关文档。

# 总结

* 完成数据表创建和数据导入，知道 `create` 语句和 `insert` 语句基本结构和用户（可以看懂别人写的语句程度）
* 知道数据库基本类型，并且类型是描述列的
* E-R 图基本知识：实体、属性、关系。可以看懂别人给出的 E-R 图，可以自己手绘简单 E-R 图，能够分析简单的数据表 E-R 图


---
title: 小白学 SQL 第六天：统计查询
date: 2018-04-29
lastmod: 2018-04-29
draft: false
keywords: ["Threeq", "博客", "程序员", "架构师", "Mysql","SQL","SQL学习","数据库","select语句"]
categories:
 - 数据库
tags:
 - 数据库
 - SQL
toc: true
comment: true
description: "数据库管理系统（DBMS）是 IT 从业者必备工具之一，你能在市面上看到的任何一个软件系统，在后面支持的一定有它的身影。 而这里面关系型数据库管理系统（RDBMS） 目前暂居了绝大部分，操作 RDBMS 的基础就是今天我们要开始学习的 SQL（结构化查询语言），所以我们有必要针对 SQL 进行系统全面的学习。同时会对数据库中的一些基础原理和设计工具进行介绍：ER 图、数据类型、范式等。适合小白用户（初学者和刚入门）。"

---

今天我们来学习涉及单表查询的最后一种查询方式：统计查询，但让统计查询并不只能用于单表查询的，也可用于多表查询。其实我们前面所有的查询子句都可以用于单表和多表查询，具体多表查询中的使用将在第七天介绍。首先还是看看统计查询里面内容概要，也是今天的知识要点。

知识要点：

* 统计函数
* 分组统计
* 过滤分组统计

<!--more-->



# 统计函数

**SQL聚集函数有 5 个**

| 函数    | 说明             |
| ------- | ---------------- |
| AVG()   | 返回某列的平均值 |
| COUNT() | 返回某列的函数   |
| MIN()   | 返回某列的最小值 |
| MAX()   | 返回某列的最大值 |
| SUM()   | 返回某列值之和   |

> * 对所有执行计算，指定ALL参数或不指定参数（因为ALL是默认行为）；只包含不同的值，指定distinct参数
> * 使用 count(*) 对表中行的数目进行计数，不管表列中包含的是空值（null）还是非空值
> * 使用 count(column) 对特定列中具有值得行进行计数，忽略null值。



## 查询班级总数和设置了开班时间的班级个数



```sql
select count(*), count(c_start_time) 
from class;
```

执行 SQL 得到结果。这里注意 `count(*)` 和 `count(c_start_time)` 的区别

![](/images/articles/noob-learn-sql/06-statistics-01.jpeg)

## 查询班主任的个数



```
select count(distinct c_head_teacher)
from class;
```

得到如下结果

![](/images/articles/noob-learn-sql/06-statistics-02.jpeg)

> 大家注意这里为什么使用 `count(distinct c_head_teacher)` 。大家可以执行下面语句，看两个之前的差别在哪里。
>
> `select count(c_head_teacher) from class;`

## 查询生日在 2008-01-18 这天的学生数量



```
select count(*) from student
where s_birthday='2008-01-18';
```

得到如下结果

![](/images/articles/noob-learn-sql/06-statistics-03.jpeg)

试试

- [ ] 查询所有学生数量、平均年龄、最小年龄、最大年龄、年龄总和

# 分组统计：group 子句

在使用统计查询的时候，常常会遇到对数据进行分类排序的需求，这个时候就需要使用到 **group** 子句，子句格式:

```sql
[GROUP BY {col_name | expr | position} [ASC | DESC], ... [WITH ROLLUP]]
```

 进行分组或分类的条件可以是一个，也可以是多个；既可以是列，也可以是表达式。

> 使用 **group** 子句时，*select* 返回的信息必须是统计信息或分组信息

## 统计不同性别的学生数量和平均年龄，返回性别信息(显示男或女)、数量信息、平均年龄

```sql
select 
case s_sex 
  when 0 then '女'
  when 1 then '男'
end, 
count(*), avg(s_age)
from student
group by s_sex
```

得到如下结果

![](/images/articles/noob-learn-sql/06-statistics-group-01.jpeg)

*试试：去除平均年龄中的小数*

## 统计不同年龄段学生数量，每10岁为一个年龄段，数量最多的在前面，输出年龄段信息和数量

```
select concat((ceil(s_age / 10)-1)*10+1, '~', ceil(s_age / 10)*10, '岁') as seg, count(*)
from student
group by seg
order by count(*) desc
;
```

得到如下结果

![](/images/articles/noob-learn-sql/06-statistics-group-02.jpeg)

试试

- [ ] 查询负责班级最多的班主任和负责班级数量

# 过滤分组统计：having 子句

有时我们会遇到查找满足指定统计条件的数据，这个时候需要使用到 having 子句。having子句类似于where，having支持所有得where操作符，它们得句法是相同的，却别是：**where是过滤行，having是过滤分组**

##  查询学生数量大于1排前三的地区

```sql
select  s_addr, count(*)
from student
group by s_addr
HAVING count(*)>1
order by count(*) desc
limit 0,3
;
```

执行结果

![](/images/articles/noob-learn-sql/06-statistics-having-01.jpeg)

试试

- [ ] 查询负责2个班级的班主任

# 总计

- 统计函数：count、max、min、avg、sum
- 分组统计：group by 子句
- 过滤分组统计：having 子句

至此针对单表的常用查询讲解都完了，这里做一个 SQL 语句结构的整理。

**select子句及其顺序**

| 子句     | 说明               | 是否必须使用             |
| -------- | ------------------ | ------------------------ |
| select   | 要返回的列或表达式 | 是                       |
| from     | 从中检索数据的表   | 仅在从表中选择数据时使用 |
| where    | 行级过滤           | 否                       |
| group by | 分组说明           | 仅在按组计算聚集时使用   |
| having   | 组级过滤           | 否                       |
| order by | 输出排序顺序       | 否                       |
| limit    | 限定结果集大小     | 否                       |

```
SELECT select_expr [, select_expr ...]
[FROM table_references
    [WHERE where_condition]
    [GROUP BY {col_name | expr | position} [ASC | DESC], ... [WITH ROLLUP]]
    [HAVING where_condition]
    [ORDER BY {col_name | expr | position}
      [ASC | DESC], ...]
    [LIMIT {[offset,] row_count | row_count OFFSET offset}]
]
```


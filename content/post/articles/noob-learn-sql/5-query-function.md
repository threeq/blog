---
title: 小白学 SQL 第五天：数据操作函数
date: 2018-04-27
lastmod: 2018-04-27
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



我们之前已经学习很多的 SQL 查询支持，但是这些查询只能原样返回数据库里存储的数据，那如果我们需要对这些数据做一个处理怎么办呢？比如：合并2个字段、返回的学生年龄2倍等。这就是今天要一起学习的内容：数据操作函数。每个 RDBMS 提供提供的函数操作都不一样，这里还是以 MySQL 为例子讲解，其他的 RDBMS 请查阅相关文档。由于数据处理函数比较多，这里没有办法全部覆盖，只会列举我们常用的一些操作函数，我把他们分成 5 类：字符串函数、数值函数、时间函数、统计函数、流程控制函数。想知道更多函数详情请参考 [MySQL 官方文档](https://dev.mysql.com/doc/refman/5.7/en/func-op-summary-ref.html)。

知识要点：

* 计算字段、计算列、虚拟列
* 常用字符串函数
* 常用数值计算、数值函数
* 常用日期时间函数
* 流程控制函数


这里列举的使平时常用的 4 中类型函数分类，另外的统计函数将在下次单独说明。

<!--more-->

在查询里面使用计算表达式或函数表达式的列称为计算列或计算字段。它是一个虚拟列，数据库并不实际存储在表中，计算列的表达式可以使用其他列中的数据来计算其所属列的值。 

# 字符串函数

下面是常用的一些字符处理函数

| 函数                 | 描述               | 实例                                                         |
| -------------------- | ------------------ | ------------------------------------------------------------ |
| concat()             | 拼接字符串         | SELECT concat('Hello', ', ', 'World','!');                   |
| format()             | 格式化数字到字符串 | SELECT format(12332.1,4);                                    |
| length()             | 返回字符串长度     | SELECT length('xxx');                                        |
| lcase()/lower()      | 转换小写           | SELECT lower('ABcDef');                                      |
| ltrim()              | 去掉左边空白字符   | SELECT ltrim('  AB   cD   f   ');                            |
| repeat()             | 重复输出字符串     | SELECT  repeat('A', 3);                                      |
| replace()            | 替换字符串         | SELECT  replace('ABBCD', 'BB', 'W');                         |
| reverse()            | 翻转输出字符串     | SELECT   reverse('abcd');                                    |
| left()               | 返回左边字符串     | SELECT   left('abcdf', 2);                                   |
| right()              | 返回右边字符串     | SELECT   right('abcdf', 2);                                  |
| rtrim()              | 去掉右边空白字符   | SELECT rtrim('  AB   cD   f  ');                             |
| substr()/substring() | 截取子字符串       | SELECT substr('Quadratically',5);<br> SELECT substr('Quadratically',5,6); |
| trim()               | 去掉空白字符       | SELECT trim('  AB   cD   f  ');                              |
| ucase()/upper()      | 转换大写           | SELECT upper('ABcDef');                                      |

还是通过实例分析他们的使用

## 查询班主任信息，输出3遍老师信息

> 分析：查询老师信息，输出3遍老师信息
>
> 1. 操作类型：**select** （查询）
> 2. 到哪里取数据：**班级**
> 3. 得到哪些信息：3 遍班主任信息
> 4. 过滤条件：无
> 5. 排序字段：无
> 6. 取多少数据：所有数据（无 limit）
>
> 我们将这些信息套入到 SELECT 语句结构会得到如下：
>
> > select 班主任 * 3
> >
> > from 班级;
>
> - `班主任 * 3` 由于班主任存储的是字符串类型，重复3次表示为 `repeat(c_head_teacher, 3)`

得到如下 SQL

```sql
select repeat(c_head_teacher, 3)
from class;
```

执行得到如下结果

![](/images/articles/noob-learn-sql/05-function-str-01.jpeg)

试试

- [ ] 查询班级名称长度并将班级名称翻转输出

# 数值计算、数值函数

数值计算操作符

| 操作符   | 描述         | 实例                 |
| -------- | ------------ | -------------------- |
| +        | 加           | select 2+3;          |
| -        | 减 或 取反   | select 2-1, -2;      |
| *        | 乘           | select 2*3;          |
| / 或 div | 除           | select 2/4, 2 div 4; |
| % 或 mod | 取余 或 取模 | select 2%4, 2 mod 4; |

数值计算函数

| 函数               | 描述               | 实例                                                         |
| -------------------- | ------------------ | ------------------------------------------------------------ |
| abs()             | 绝对值         | SELECT abs(-10), abs(9);    |
| ceil()/ceilling() | 上取整 | SELECT ceiling(3.4),  ceil(3.5), ceil(3.6); |
| conv()         | 进制转换 | SELECT conv(10,10 ,2), conv(10,2 ,10);    |
| exp() | 自然数数 `e` 的 n 次方 | SELECT exp(1), exp(0), exp(-1);               |
| floor()       | 下取整 | SELECT floor(3.4),  floor(3.5), floor(3.6); |
| pow()/power() | 指数函数 | SELECT POW(1,3), pow(2,3), pow(4,2); |
| round() | 四舍五入取整 | SELECT round(3.4),  round(3.5), round(3.6); |
| rand() | 随机数 | SELECT rand(), rand()*10;      |
| mod() | 取余/取模 | SELECT mod(25, 7),  25 % 7, mod(25.4, 7),  25.4 % 7; |
| pi() | PI 值 | SELECT pi(), pi()+0.0000000000;      |

## 查询所有学生姓名和年龄，将所有学生的年龄翻倍，且年龄大的在后面

> 分析：查询所有学生信息，将所有学生的年龄翻倍，且年龄大的在后面
>
> 1. 操作类型：**select** （查询）
> 2. 到哪里取数据：**学生**
> 3. 得到哪些信息：姓名、年龄翻倍
> 4. 过滤条件：无
> 5. 排序字段：龄大的在后面
> 6. 取多少数据：所有数据（无 limit）
>
> 我们将这些信息套入到 SELECT 语句结构会得到如下：
>
> > select 姓名,   年龄翻倍
> >
> > from 学生
> >
> > order by 龄大的在后面;
>
> 

得到如下 SQL

```sql
select s_name, s_age * 2
from student
order by s_age * 2 asc;
```

执行得到如下结果

![](/images/articles/noob-learn-sql/05-function-number-01.jpeg)

## 查询学生年龄和姓名，并按照年龄的 1/3 下取整输出

> 分析：查询学生年龄和姓名，并按照年龄的的 1/3 下取整输出
>
> 1. 操作类型：**select** （查询）
> 2. 到哪里取数据：**学生**
> 3. 得到哪些信息：姓名、年龄的 1/3 下取整
> 4. 过滤条件：无
> 5. 排序字段：无
> 6. 取多少数据：所有数据（无 limit）
>
> 我们将这些信息套入到 SELECT 语句结构会得到如下：
>
> > select 姓名,   年龄的 1/3 下取整
> >
> > from 学生
> >
> > order by 龄大的在后面;
>
> *年龄的 1/3 下取整* 先求出年龄的 1/3，再用 下取整函数处理

得到如下 SQL

```
select s_name, floor(s_age/3)
from student;
```

执行得到如下结果

![](/images/articles/noob-learn-sql/05-function-str-02.jpeg)

试试

- [ ] 查询所有10岁的学生姓名和年龄，要求输出2遍姓名和5年后的年龄



# 日期时间函数

| 函数                 | 描述                                                         | 实例                                                         |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| now()                | 当前日期时间                                                 | select now(), CURRENT_TIMESTAMP();                           |
| curtime()            | 当前时间                                                     | select curtime();                                            |
| curdate()            | 当前日期                                                     | select curdate();                                            |
| from_unixtime()      | 从时间戳到日期                                               | select from_unixtime(1);                                     |
| unix_timestamp()     | 返回日期时间戳                                               | select  unix_timestamp(now());                               |
| time()               | 从时间里面获取时间部分                                       | select time(now())                                           |
| date()               | 从时间里面获取日期部分                                       | select now(), date(now());                                   |
| date_format()        | 格式化日期/时间数据<br>`date_format(date, format)`           | select   date_format(now(),'%b %d %Y %h:%i %p'),<br> date_format(now(),'%m-%d-%Y'); |
| adddate()/date_add() | 向日期添加指定的时间间隔<br>`adddate(date, interval num unit)` | select  date_add(now() ,interval 45 DAY), <br>adddate(now() ,interval 45 DAY); |
| subdate()/date_sub() | 向日期减去指定的时间间隔<br>`subdate(date, interval num Type)` | select  date_sub(now() ,interval 45 DAY), <br>subdate(now() ,interval 45 DAY); |
| datediff()           | 返回两个日期之间的天数                                       | SELECT datediff('2018-01-30','2018-04-27');                  |

还有很多的时间获取函数，这里不再列举，在用到的时候查下文件就行 [《MySQL 日期时间函数》](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html)

##  时间 ADD 和 SUB 的 unit 可取值有

| Type 值            |
| ------------------ |
| MICROSECOND        |
| SECOND             |
| MINUTE             |
| HOUR               |
| DAY                |
| WEEK               |
| MONTH              |
| QUARTER            |
| YEAR               |
| SECOND_MICROSECOND |
| MINUTE_MICROSECOND |
| MINUTE_SECOND      |
| HOUR_MICROSECOND   |
| HOUR_SECOND        |
| HOUR_MINUTE        |
| DAY_MICROSECOND    |
| DAY_SECOND         |
| DAY_MINUTE         |
| DAY_HOUR           |
| YEAR_MONTH         |

## 时间 format 可使用的格式有：

| 格式 | 描述                                           |
| ---- | ---------------------------------------------- |
| %a   | 缩写星期名                                     |
| %b   | 缩写月名                                       |
| %c   | 月，数值                                       |
| %D   | 带有英文前缀的月中的天                         |
| %d   | 月的天，数值（00-31）                          |
| %e   | 月的天，数值（0-31）                           |
| %f   | 微秒                                           |
| %H   | 小时（00-23）                                  |
| %h   | 小时（01-12）                                  |
| %I   | 小时（01-12）                                  |
| %i   | 分钟，数值（00-59）                            |
| %j   | 年的天（001-366）                              |
| %k   | 小时（0-23）                                   |
| %l   | 小时（1-12）                                   |
| %M   | 月名                                           |
| %m   | 月，数值（00-12）                              |
| %p   | AM 或 PM                                       |
| %r   | 时间，12-小时（hh:mm:ss AM 或 PM）             |
| %S   | 秒（00-59）                                    |
| %s   | 秒（00-59）                                    |
| %T   | 时间, 24-小时（hh:mm:ss）                      |
| %U   | 周（00-53）星期日是一周的第一天                |
| %u   | 周（00-53）星期一是一周的第一天                |
| %V   | 周（01-53）星期日是一周的第一天，与 %X 使用    |
| %v   | 周（01-53）星期一是一周的第一天，与 %x 使用    |
| %W   | 星期名                                         |
| %w   | 周的天（0=星期日, 6=星期六）                   |
| %X   | 年，其中的星期日是周的第一天，4 位，与 %V 使用 |
| %x   | 年，其中的星期一是周的第一天，4 位，与 %v 使用 |
| %Y   | 年，4 位                                       |
| %y   | 年，2 位                                       |

## 查询学生在哪一年出生，年份早的排在前面

> 分析：查询学生在哪一年出生，年份早的排在前面
>
> 1. 操作类型：**select** （查询）
> 2. 到哪里取数据：**学生**
> 3. 得到哪些信息：在哪一年出生
> 4. 过滤条件：无
> 5. 排序字段：年份早的排在前面
> 6. 取多少数据：所有数据（无 limit）
>
> 我们将这些信息套入到 SELECT 语句结构会得到如下：
>
> > select 在哪一年出生
> >
> > from 学生
> >
> > order by 年份早的排在前面;
>
> **在哪一年出生** 这个信息是在生日字段里面，生日字段是包含了年月日信息，只需要使用 year 函数处理就能得到年了：`year(s_birthday)`

得到 SQL 语句

```sql
select year(s_birthday)
from student
order by year(s_birthday) asc;
```

执行得到如下结果

![](/images/articles/noob-learn-sql/05-function-date-01.jpeg)

试试

- [ ] 大家发现学生表里面有年龄字段和生日字段，上面我们使用了生日计算出生年，现在使用年龄计算出生年，看看会是什么结果，应该是和生日不一样的（这里是故意的，后面在修改数据时候会改过来）
- [ ] 计算班级从开班时间到结束时间持续了多少天

# 流程控制函数

MySQL 流程控制函数有 4 个：`CASE`、`IF()`、`IFNULL` 、`NULLIF` ，我自己平时用的最多的是 `CASE` ，这里只演示 CASE 的使用，其他几个在一个特定的场景下使用，到时候遇到了查下文档吧。

## CASE 语法

`CASE` 语句有2中语法，一种是值判断，一种是条件判断。

## 值判断语法

```
CASE value 
    WHEN [compare_value] THEN result 
    [WHEN [compare_value] THEN result ...] 
    [ELSE result] 
END
```

## 条件判断语法

```
CASE 
    WHEN [condition] THEN result 
    [WHEN [condition] THEN result ...] 
    [ELSE result] 
END
```

## 查询学生性别和姓名，性别输出文中文男和女（0：女，1：男）

```
select s_name,
case c_sex
    when 0 then '女'
    when 1 then '男'
end as '性别'
from student
```



![](/images/articles/noob-learn-sql/05-function-case-01.jpeg)

## 查询学习性别和年龄段，年龄段输出为：1~10的为小，11~15的中，16~20的大



```
select s_name,
case 
    when s_age>=1 and s_age<=10 then '小'
    when s_age>=11 and s_age<=15 then '中'
    when s_age>=16 and s_age<=20 then '大'
end as '年龄段'
from student;
```

![](/images/articles/noob-learn-sql/05-function-case-02.jpeg)

试试

- [ ] 查询学生生日的月份，要求中文数值输出月份(比如：一月、二月、三月)

> 上面最后两个 SQL 没有给出详细的分析过程，对于这个分析过程可以自行按照之前的模式进行，这种分析模式掌握过后，不论多复杂的需求和 SQL 都可以做到游刃有余，所以大家一定要掌握。对于后面简单的 SQL 不再给出详细分析过程，分析过程只针对复杂 SQL 和关键部分，如果大家对于哪个问题和SQL 需要分析过程的，可以在后面留言或联系我。

# 总结

- 计算字段、计算列、虚拟列
- 常用字符串函数
- 常用数值计算、数值函数
- 常用日期时间函数
- 流程控制函数：case 语句的 2 种格式


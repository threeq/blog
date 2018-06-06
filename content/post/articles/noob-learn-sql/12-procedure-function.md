---
title: 小白学 SQL 第十二天：存储过程和函数
date: 2018-06-06
lastmod: 2018-06-06
draft: false
keywords: ["Threeq", "博客", "程序员", "架构师", "Mysql","SQL","SQL学习","数据库","存储过程"]
categories:
 - 数据库
tags:
 - 数据库
 - SQL
toc: true
comment: true
description: "数据库管理系统（DBMS）是 IT 从业者必备工具之一，你能在市面上看到的任何一个软件系统，在后面支持的一定有它的身影。 而这里面关系型数据库管理系统（RDBMS） 目前暂居了绝大部分，操作 RDBMS 的基础就是今天我们要开始学习的 SQL（结构化查询语言），所以我们有必要针对 SQL 进行系统全面的学习。同时会对数据库中的一些基础原理和设计工具进行介绍：ER 图、数据类型、范式等。适合小白用户（初学者和刚入门）。"

---

之前我们已经学习了 SQL 的很多基础知识，最后一起看一下 **存储过程和函数** ，这也是此系列的最后一篇。数据库系统有了存储过程和函数，才真正具备了编程的能力。

知识要点

- 存储过程
- 存储过程和函数的区别

<!--more-->

# 存储过程和函数定义

存储过程和函数是事先经过编译并存储在数据库中的一段SQL语句的集合。调用存储过程和函数可以简化应用开发人员的很多工作，减少数据在数据库和应用服务器之间的传输，对于提高数据处理的效率是有好处的。MySQL的存储过程（stored procedure）和函数（stored function）统称为[stored routines](http://dev.mysql.com/doc/refman/5.0/en/stored-routines.html)。

虽然存储过程和函数可以简化应用开发难度和提升数据处理效率，但是存储过程本身比较复杂，对于应用后期维护和数据库迁移升级并不友好。对于是否应该采用存储过程，可以看文章[Business Logic: To Store or not to Store that is the Question?](http://www.paragoncorporation.com/ArticleDetail.aspx?ArticleID=28)中进行了详细分析和讨论。就我个人来说：在应用业务开发的时候，是很少使用存储过程和函数的，有时是甚至是禁止使用；往往是在在编写数据库升级脚本时使用存储过程和函数。

# 存储过程和函数

创建语法：

```
CREATE
    [DEFINER = { user | CURRENT_USER }]
    PROCEDURE sp_name ([proc_parameter[,...]])
    [characteristic ...] routine_body

CREATE
    [DEFINER = { user | CURRENT_USER }]
    FUNCTION func_name ([func_parameter[,...]])
    RETURNS type
    [characteristic ...] routine_body

proc_parameter:
    [ IN | OUT | INOUT ] param_name type

func_parameter:
    param_name type

type:
    Any valid MySQL data type

characteristic:
    COMMENT 'string'
  | LANGUAGE SQL
  | [NOT] DETERMINISTIC
  | { CONTAINS SQL | NO SQL | READS SQL DATA | MODIFIES SQL DATA }
  | SQL SECURITY { DEFINER | INVOKER }

routine_body:
    Valid SQL routine statement
```

`characteristic` 特征值的部分进行简单的说明：

> `LANGUAGE SQL` 说明下面过程的 BODY 是使用 SQL 语言编写，这条是系统默认的，为今后 MySQL 会支持除 SQL 外的其他语言的存储过程而准备
>
> `DETERMINISTIC` 确定的，即每次输入一样输出也一样的程序
>
> `NOT DETERMINISTIC` 非确定的，默认是非确定的。当前，这个特征值还没有被优化程序使用。
>
> `{ CONTAINS SQL | NO SQL | READS SQL DATA | MODIFIES SQL DATA }` 这些特征值提供子程序使用数据的内在信息，这些特征值目前只是提供给服务器，并没有根据这些特征值来约束过程实际使用数据的情况
>
> > `CONTAINS SQL` 表示子程序不包含读或写数据的语句，没有明确指定时的默认值
> >
> > `NO SQL` 表示子程序不包含 SQL 语句
> >
> > `READS SQL DATA` 表示子程序包含读数据的语句，但不包含写数据的语句
> >
> > `MODIFIES SQL DATA` 表示子程序包含写数据的语句。
>
> `SQL SECURITY { DEFINER | INVOKER }` 可以用来指定子程序该用创建子程序者的许可来执行，还是使用调用者的许可来执行。默认值是 DEFINER
>
> `COMMENT 'string'` 存储过程或者函数的注释信息



详细的 SQL 语法说明，请参考 [《MySQL 官方文档》](https://dev.mysql.com/doc/refman/5.7/en/create-procedure.html) 。

MySQL 的存储过程和函数中允许包含 DDL 语句，也允许在存储过程中执行提交（Commit，即确认之前的修改）或者回滚（Rollback，即放弃之前的修改），但是存储过程和函数中不允许执行 `LOAD DATA INFILE` 语句。此外，存储过程和函数中可以调用其他的过程或者函数

通常我们在执行创建过程和函数之前，都会通过 `DELIMITER $$` 命令将语句的结束符从 `;` 修改成其他符号，这里使用的是 `$$`，这样在过程和函数中的 `;` 就不会被 MySQL 解释成语句的结束而提示错误。在存储过程或者函数创建完毕，通过 `DELIMITER ;` 命令再将结束符改回成 `;`



调用存储过程

```
CALL sp_name([parameter[,...]]);
-- 或
CALL sp_name[()]
```

调用函数

```
select func_name();
```

查看存储过程或者函数的状态

```
SHOW {PROCEDURE | FUNCTION} STATUS [LIKE 'pattern']
```

查看存储过程或者函数的定义

```
SHOW CREATE {PROCEDURE | FUNCTION} sp_name
```

通过查看 `information_schema.Routines` 了解存储过程和函数的信息

删除存储过程或函数

```
DROP {PROCEDURE | FUNCTION} [IF EXISTS] sp_name
```

## 变量的使用

> 存储过程和函数中可以使用变量，变量是不区分大小写的

通过 `DECLARE` 可以定义一个局部变量，该变量的作用范围只能在 `BEGIN…END` 块中，可以用在嵌套的块中。变量的定义必须写在复合语句的开头，并且在任何其他语句的前面。可以一次声明多个相同类型的变量。如果需要，可以使用 `DEFAULT` 赋默认值

定义一个变量的语法如下：

```
DECLARE var_name[,...] type [DEFAULT value]
```

直接赋值使用 SET，可以赋常量或者赋表达式，具体语法如下：

```
SET var_name = expr [, var_name = expr] ...
```

也可以通过查询将结果赋给变量，这要求查询返回的结果必须只有一行，具体语法如下：

```
SELECT col_name[,...] INTO var_name[,...] table_expr
```

## 定义条件和处理

> 条件的定义和处理可以用来定义在处理过程中遇到问题时相应的处理步骤

条件的定义

```
DECLARE condition_name CONDITION FOR condition_value

    condition_value:SQLSTATE [VALUE] sqlstate_value
        | mysql_error_code
```

条件的处理

```
DECLARE handler_type HANDLER FOR condition_value[,...] sp_statement

    handler_type:CONTINUE | EXIT | UNDO

    condition_value:SQLSTATE [VALUE] sqlstate_value
        | condition_name
        | SQLWARNING
        | NOT FOUND
        | SQLEXCEPTION
        | mysql_error_code
```

> `handler_type`：`CONTINUE` 表示继续执行下面的语句，`EXIT` 则表示执行终止
>
> `condition_value` 的值可以是通过 `DECLARE` 定义的 `condition_name`，可以是 `SQLSTATE` 的值或者 `mysql-error-code` 的值或者 `SQLWARNING`、`NOT FOUND`、`SQLEXCEPTION`，这 3 个值是 3 种定义好的错误类别，分别代表不同的含义：
>
> -  `SQLWARNING` 是对所有以 01 开头的 `SQLSTATE` 代码的速记
> -  `NOT FOUND` 是对所有以 02 开头的 `SQLSTATE` 代码的速记
> -  `SQLEXCEPTION` 是对所有没有被 `SQLWARNING` 或 `NOT FOUND` 捕获的 `SQLSTATE` 代码的速记

## 光标的使用

在存储过程和函数中可以使用光标对结果集进行循环的处理。光标的使用包括光标的声明，OPEN， FETCH 和 CLOSE，其语法分别如下：

- 声明光标：

  ```
    DECLARE cursor_name CURSOR FOR select_statement
  ```

- OPEN 光标：

  ```
    OPEN cursor_name
  ```

- FETCH 光标：

  ```
    FETCH cursor_name INTO var_name [, var_name] ...
  ```

- CLOSE 光标：

  ```
    CLOSE cursor_name
  ```

> 注意：变量、条件、处理程序、光标都是通过 `DECLARE` 定义的，它们之间是有先后顺序的要求的。变量和条件必须在最前面声明，然后才能是光标的声明，最后才可以是处理程序的声明

## 流程控制

if 语句

> if 实现条件判断，满足不同的条件执行不同的语句列表，具体语法如下：
>
```
IF search_condition THEN statement_list
[ELSEIF search_condition THEN statement_list] ...
[ELSE statement_list]
END IF
```



CASE 语句

> case 实现比 if 更复杂一些的条件构造，具体语法如下：
>
```
CASE case_value
WHEN when_value THEN statement_list
[WHEN when_value THEN statement_list] ...
[ELSE statement_list]
END CASE
```
or
```
CASE
WHEN search_condition THEN statement_list
[WHEN search_condition THEN statement_list] ...
[ELSE statement_list]
END CASE
```

loop 语句

> LOOP 实现简单的循环，退出循环的条件需要使用其他的语句定义，通常可以使用 LEAVE 语句实现，具体语法如下：
>
```
[begin_label:] LOOP
statement_list
END LOOP [end_label]
```
>
> 如果不在 `statement_list` 中增加退出循环的语句，那么 LOOP 语句可以用来实现简单的死循环

leave 语句

> 用来从标注的流程构造中退出，通常和 BEGIN ... END 或者循环一起使用

iterate 语句

> iterate 语句必须用在循环中，作用是跳过当前循环的剩下的语句，直接进入下一轮循环

repeat 语句

> 有条件的循环控制语句，当满足条件的时候退出循环，具体语法如下：
>
```
[begin_label:] REPEAT
statement_list
UNTIL search_condition
END REPEAT [end_label]
```

while 语句

> WHILE 语句实现的也是有条件的循环控制语句，即当满足条件时执行循环的内容，具体语法如下：
>
```
[begin_label:] WHILE search_condition DO
statement_listEND WHILE [end_label]
```
>
> WHILE 循环和 REPEAT 循环的区别在于：WHILE 是满足条件才执行循环，REPEAT 是满足条件退出循环；WHILE 在首次循环执行之前就判断条件，所以循环最少执行 0 次，而 REPEAT 是在首次执行循环之后才判断条件，所以循环最少执行 1 次

## 事件调度器

> 事件调度器可以将数据库按自定义的时间周期触发某种操作，可以理解为时间触发器

下面是一个最简单的事件调度器，每 5 秒向表中插入数据

```
create event myevent
on schedule
every 5 second
do
insert into tablename values(value1);
```

- 事件名称在 create event 关键字后指定
- 通过 on schedule 子句指定事件在何时执行及执行频次
- 通过 do 子句指定要执行的具体操作或事件

查看事件：`show events;`

查看调度器：`show variables like '%scheduler'` 默认是关闭的

打开调度器：`set global event_scheduler=1;`，事件才能启动

查看后台进程：`show processlist;`

禁用事件：`alter event eventname disable;`

删掉事件：`drop event eventname;`



# 存储过程和函数的比较

大家可以看到存储过程和函数，不论是从功能还是语法上都非常相识，那他们有什么区别呢？存储过程和函数的比较的简要说明参见[Stored procedure vs. function](http://forums.mysql.com/read.php?98,28061,28080#msg-28080)。归纳如下：

- 函数只能通过return语句返回单个值或者表对象。而存储过程不允许执行return，但是可以通过out参数返回多个值。
- 函数是可以嵌入在sql中使用的,可以在select中调用，而存储过程不行。
- 函数限制比较多，比如不能用临时表，只能用表变量等等．而存储过程的限制相对就比较少
- 当存储过程和函数被执行的时候，SQL Manager会到procedure cache中去取相应的查询语句，如果在procedure cache里没有相应的查询语句，SQL Manager就会对存储过程和函数进行编译。
- Procedure cache中保存的是执行计划 (execution plan) ，当编译好之后就执行procedure cache中的execution plan，之后SQL SERVER会根据每个execution plan的实际情况来考虑是否要在cache中保存这个plan，评判的标准一个是这个execution plan可能被使用的频率；其次是生成这个plan的代价，也就是编译的耗时。保存在cache中的plan在下次执行时就不用再编译了。

# 总结



- 存储过程：创建、调用、删除
- 函数：创建、调用、删除
- 存储过程和函数的比较



---

这篇是《小白学 SQL》第一阶段的最后一篇，自此大家应该对 SQL 的基础知识的整体结构的有所认知，同时应该能对问题分析和分解，且能写出对于的 SQL 语句。虽然此系列的 SQL 介绍结束了，但是对于 SQL 的学习和实践才正式开始。由于本人能力有限，不论是在分析、组织和书写方面都有错误，还希望你能指出。希望能得到你的反馈，你的反馈对我很重要，也是我不断前进的动力，望能和你共同进步。

目前正在规划 SQL 介绍的第二阶段，重点聚焦在三方面：

: 一 应用开发中数据库设计优化

: 二 如何写出高效的 SQL

: 三 如何建立有效的索引
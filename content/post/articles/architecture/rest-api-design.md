---
title: 架构师：REST API 设计实践
date: 2019-02-18
categories:
 - 架构
tags:
 - rest
 - restful
 - 设计
 - 架构
toc: true
---



# 简介

REST 这个词是 [Roy Thomas Fielding](http://en.wikipedia.org/wiki/Roy_Fielding) 在他2000年的[博士论文](http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)中提出的，是 Representational State Transfer 的简称，我翻译为“表现层状态转移”。 REST 描述的是一种架构风格，指的是一组架构约束条件和原则，满足这些约束条件和原则的应用程序或设计，就称它为RESTful架构。

## 基本概念

- 资源（Resources） REST是”表现层状态转化”，其实它省略了主语。”表现层”其实指的是”资源”的”表现层”。那么什么是资源呢？就是我们平常上网访问的一张图片、一个文档、一个视频等。这些资源我们通过URI来定位，也就是一个URI表示一个资源。

- 表象（Representational）

  资源是做一个具体的实体信息，他可以有多种的展现方式。而把实体展现出来就是表现层，例如一个txt文本信息，他可以输出成html、json、xml等格式，一个图片他可以jpg、png等方式展现，这个就是表现层的意思。

  URI确定一个资源的实体，但是如何确定它的具体表现形式呢？应该在 HTTP 请求的头信息中用Accept和Content-Type字段指定，这两个字段才是对”表现层”的描述。

- 状态转移（State Transfer）访问一个网站，就代表了客户端和服务器的一个互动过程。在这个过程中，肯定涉及到数据和状态的转移。而HTTP协议是无状态的，那么这些状态肯定保存在服务器端，所以如果客户端想要通知服务器端改变数据和状态的变化，肯定要通过某种方式来通知它。



## Richardson Maturity Model

![](https://ws2.sinaimg.cn/large/006tKfTcly1g0ayi1nf26j30ip0b20ts.jpg)

**有关成熟度的文章**

[Leonard Richardson](https://www.crummy.com)：<https://www.crummy.com/writing/speaking/2008-QCon/>

[Martin Fowler](https://martinfowler.com/)：<https://martinfowler.com/articles/richardsonMaturityModel.html> [（译文）]( https://blog.csdn.net/dm_vincent/article/details/51341037)

<!--more-->

### Level 0：模型的起点

![](https://ws3.sinaimg.cn/large/006tKfTcly1g0ayipe26gj30ei04y75h.jpg)

​     把HTTP这个应用层协议降级为传输层协议用，无任何 web 机制，其实只是远程方法调用（RPC）的一种形式。SOAP 和 XML-RPC 都属于此类。

这个层级主要的表现有：

1. URI 是指定具体行为和操作，完全没有资源的概念 

### Level 1：引入资源

![](https://ws4.sinaimg.cn/large/006tKfTcly1g0ayj7hotcj30ei04ywfs.jpg)

​      在架构中引入资源（Resource）的概念，然而不同的URI只是作为不同的调用入口。

这个层级主要的表现有：

1. 已经引入资源概念 
2. URI 里面包含动词，只是作为操作的入口 
3. 所有请求都是 post 或 get，这里的 post 和 get 没有实质的区别，post 的操作使用 get 请求也能完成 

### Level 2：HTTP 动词

![](https://ws2.sinaimg.cn/large/006tKfTcly1g0ayjkq1fbj30ei04y75o.jpg)

​      此时每一个URI代表一种资源，支持HTTP动词。需要让不同的URI代表不同的资源，同时使用多个HTTP方法操作这些资源，例如使用POST/GET/PUT/DELET分别进行CRUD操作。这时候HTTP头和有效载荷都包含业务逻辑，例如HTTP方法对应CRUD操作，HTTP状态码对应操作结果的状态。我们现在看到的大多数所谓RESTful API做到的也就是这个级别。

这个层级主要的表现有：

1. URI 完全代表资源
2. HTTP 方法对应相应的资源操作，并且准守 HTTP 方法幂等性规范
3. HTTP 状态码对应资源操作结果的状态

### Level 3：超媒体控制

![](https://ws4.sinaimg.cn/large/006tKfTcly1g0ayl5mavfj30f6073wem.jpg)

​      在资源的表达中包含了资源后续可做操作的描述信息。客户端可以根据资源描述信息来发现可以执行的动作。HATEOAS，使用超媒体（hypermedia）作为应用状态引擎

1. 满足所有第三层次 
2. 在资源的表示层中，包含有资源后续可做操作的描述信息 

从上述 REST 成熟度模型中可以看到，使用 HATEOAS(Hypertext As The Engine Of Application State) 的 REST 服务是成熟度最高的，也是推荐的做法。对于不使用 HATEOAS 的 REST 服务，客户端和服务器的实现之间是紧密耦合的。客户端需要根据服务器提供的相关文档来了解所暴露的资源和对应的操作。当服务器发生了变化时，如修改了资源的 URI，客户端也需要进行相应的修改。而使用 HATEOAS 的 REST 服务中，客户端可以通过服务器提供的资源的表达来智能地发现可以执行的操作。当服务器发生了变化时，客户端并不需要做出修改，因为资源的 URI 和其他信息都是动态发现的。

# 设计实践

上面已经了解了 REST 的基本概念和成熟度模型，那我们在具体实践中有哪些需要考虑，并且怎么设计？ 

## 确定目标

1. ​    确定设计的 REST 接口符合的成熟度等级，目前比较常用的是三等级

## 交互协议

1. 传输协议往往是 HTTP 或 HTTPS 
2. 数据参数格式常用：JSON、XML、form data

## 资源（Endpoint）

1. 每个路径代表一个资源，路径里面不能带有动词 
2. 资源的原型：文档(Document)、集合(Collection)、仓库(Store)、控制器(Controller) 
3. 对于单独动作的，把动作转换成资源。具体可以参考 github 的做法 

## 版本

1. 放入 URI 中（常用） 
2. 放入 Context-Type 或 Accept 头部 
3. 放入 自定义 头部。比如：api-version 

## 资源操作 

1. 过滤操作尽量使用 Query参数 
2. 资源操作类型由 HTTP 动词表示 

**常用的HTTP动词有下面五个**

> - GET（SELECT）：从服务器取出资源（一项或多项）。
> - POST（CREATE）：在服务器新建一个资源，或者触发一个动作。
> - PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
> - PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
> - DELETE（DELETE）：从服务器删除资源。

**还有两个不常用的HTTP动词**

> - HEAD：获取资源的元数据。
> - OPTIONS：获取信息，关于资源支持的哪些操作。

**操作（HTTP动词）幂等性**

| 操作（HTTP 动词） | 是否幂等 |
| ----------------- | -------- |
| POST              | 否       |
| GET               | 是       |
| PUT               | 是       |
| PATCH             | 是       |
| DELETE            | 是       |
| HEAD              | 是       |
| OPTIONS           | 是       |

在业务实现中注意逻辑实现的幂等性需求

## 操作状态返回

1. 资源操作状态，使用 HTTP 状态码指示 
2. 并且对于错误操作，会返回错误信息提示 

**常见状态码**

> - 200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。 
> - 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。 
> - 202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务） 
> - 204 NO CONTENT - [DELETE]：用户删除数据成功。 
> - 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。 
> - 401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。 
> - 403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。 
> - 404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。 
> - 406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。 
> - 410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。 
> - 422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。 
> - 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。 

状态码的完全列表参见[这里](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)。



## 资源操作数据返回 

针对不同操作，服务器向用户返回的结果应该符合以下规范。尽量使用 json 格式返回。

> - GET /collection：返回资源对象的列表（数组） 
> - GET /collection/resource：返回单个资源对象 
> - POST /collection：返回新生成的资源对象 
> - PUT /collection/resource：返回完整的资源对象 
> - PATCH /collection/resource：返回完整的资源对象 
> - DELETE /collection/resource：返回一个空文档 



## Hyhermedia API（HATEOAS）

​    对于计划满足**Level 3**的 REST 设计，建议参考 github api 设计  HATEOAS [https://developer.github.com/v3/](https://developer.github.com/v4/) 。github 最新的 API 规范是使用GraphQL  <https://developer.github.com/v4/>




## 其他 

**资源授权**

​    接口授权方式应该使用 `OAuth 2.0 + JWT`  方式。对于简单应用直接使用 JWT 即可。 

**限流**

​    限流触发返回 429 Too many requests，并且在 body 里面附带错误信息。还可以在头部附带限流配置信息，比如Github API 使用的三个相关的头部：

- X-RateLimit-Limit: 用户每个小时允许发送请求的最大值 
- X-RateLimit-Remaining：当前时间窗口剩下的可用请求数目 
- X-RateLimit-Rest: 时间窗口重置的时候，到这个时间点可用的请求数量就会变成 X-RateLimit-Limit 的值 
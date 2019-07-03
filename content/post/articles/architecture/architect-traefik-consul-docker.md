---
title: 架构师：使用 traefik + consul + docker 实现简单可扩展架构
date: 2019-03-08
lastmod: 2019-03-11
draft: false
keywords: [架构,docker,traefik,nginx,微服务,consul,etcd,注册中心,分布式]
description: "在微服务架构的驱动下，我们的服务被拆分得越来越细，同时随着业务的增长服务也会越来越多，这就要求系统有更高的扩展能力，同时尽力保持架构的简洁性，对业务代码最少的侵入性，同时能支持异构系统更好。一种简单高效、高可用、易扩展、支持异构系统的服务架构设计，为微服务提供强有力的网关服务能力。"
categories:
 - 架构
 - 微服务
tags:
 - 架构
 - docker
 - 微服务
toc: true
comment: true

autoCollapseToc: false
postMetaInFooter: false
hiddenFromHomePage: false

contentCopyright: false
reward: false
mathjax: false
mathjaxEnableSingleDollar: false

flowchartDiagrams:
  enable: false
  options: ""

sequenceDiagrams: 
  enable: false
  options: ""
---

# 一种常见的简单架构

在微服务架构的驱动下，我们的服务被拆分得越来越细，同时随着业务的增长服务也会越来越多，这就要求系统有更高的扩展能力，同时尽力保持架构的简洁性，对业务代码最少的侵入性，同时能支持异构系统更好。目前比较常见的一种服务架构如下：

![常见 Web 服务架构](/post/articles/architecture/architect-traefik-consul-docker/normal-web.jpg)

这里首先介绍接入层和 web 层的扩展性方案和实施。

<!--more-->

# 技术选型

首先为了实现扩展性需要满足以下几个要求：

1. 接入层可以自动发现 web 层的 web server
2. 能将请求路由到真确的 web server
3. web server 能自带路由信息
4. 接入层能尽快感知 web 层的 web server 变动
5. 支持异构系统

针对以上需求设计一种简单、可行的架构方案

![](006tKfTcgy1g0xt060j8xj30wc0hoq3a.jpg)

方案的可行性需要两个关键点：

1. web server 启动时能自动注册到注册中心，对于异构系统这个注册系统最好能在基础运行环境中解决，这样对业务框架和和代码就完全透明了
2. 接入网关可以实时监听注册中心变化，并且能将变化用于实时更新自己的状态或配置

> 第一点对于正在进行老系统升级到容器化的团队特别重要。

## 基础运行环境

得益于现在流程的容器化技术，特别是 [Docker](https://docker.com/) 的普及，已经能很方便的基础运行环境中实现容器的注册，同时团队的学习成本较低。

| 常见方案    | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| VM 或物理机 | a）自动注册往往在业务架构实现；b）异构系统支持不好，通常依赖选择的业务框架和协议 |
| Docker      | a）基础环境自动注册；b）团队学习成本低；c）对异构系统支持较好 |
| Kubernetes  | k8s 作为容器云解决方案，有自己一整套的注册发现机制，只是对团队有运维层面上的要求和一定的学习成本 |

为了简单这里选择的方案是 Docker。使用 docker 可以使用 [Registrator](https://gliderlabs.com/registrator/latest/user/backends/) 将容器自动注册到注册中心，它可以支持 `etcd`、`consul` 、`zookeeper` 作为注册中心。

## 注册中心

| 常见方案  | 说明 |
| --------- | ---- |
| etcd      |      |
| zookeeper |      |
| consul    |      |

这里选择 consul 。目前阿里也推出了一个开源的注册中心 [nacos](https://github.com/alibaba/nacos) ，但是这个目前还主要是针对语言框架层面的，并且社区开源的工具还不支持直接将 docker 容器注册到 nacos 中，不过可以持续关注，作为架构工具箱中的备选方案也是不错了。

## 接入层

| 常见方案 | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| F5       | 属于硬件层性能好，但是贵。目前本人还没有机会实践             |
| nginx    | 是现在软件层反向代理使用最广的软件之一，但是由于自身只能读取静态配置文件，所以需要使用其他工具来刷新配置。比如：[confd](https://github.com/kelseyhightower/confd)、[consul-template](https://github.com/hashicorp/consul-template) |
| lvs      | 是现在软件层反向代理使用最广的软件之一，和 nginx 一样需要其他工具来刷新配置文件 |
| traefik  | 软件比较新，本身支持多中后端注册中心，配置比 nginx 和 lvs 更方便 |

这里选择 traefik。

# 工作机制

![](006tKfTcly1g0y5y3iql4j319a0ri0yy.jpg)

`Registrator` 负载监听本地 Docker 服务中的 docker 容器，负责根据容器的启动配置信息将容器注册到`注册中心`，同时在容器停止或销毁时在注册中心销毁相关信息（图中蓝色箭头表示）

`注册中心` 注册中心存储所有注册容器的最新状态，并且提供健康检查

`状态监听器` 负责监听注册中心各个容器的状态变化，并将状态变化实时更新到 `反向代理` 服务中（图中红色箭头表示）

`反向代理` 负责将请求路由、分发到正确的 docker 容器中，并且自身需求进行 docker 容器的健康检查（图中绿色箭头表示）

## traefix + consul 方式实现

由于 traefik 自身已经支持注册中心发现功能，所以`配置刷新`组件不再需要。

![](006tKfTcly1g0z1o9q7knj31940regro.jpg)

## nginx + consul 方式实现

![](006tKfTcly1g0z1r6lst0j31940qwdly.jpg)

## nginx + etcd + confd 方式实现

![](006tKfTcly1g0z1sf0x9bj31960ra44k.jpg)

# 框架搭建

这里给出的配置是 `traefix + consul` 方式。这里测试采用单机 docker 方式部署，所以相应的配置只能用于开发或测试环境，生产环境需要做高可用配置，关于高可用方案后面有具体说明，具体部署图如下：

![](006tKfTcly1g0z0by1f5rj30iu0lgmzr.jpg)

测试机 IP 地址为：192.168.3.26，请替换成自己的真实 IP。

测试代码地址在：[https://github.com/threeq/useful-scripts/tree/master/my-docker/traefik](https://github.com/threeq/useful-scripts/tree/master/my-docker/traefik)

在开始之前新建一个 `traefik` 目录用以存放所需的代码和配置文件，最后的目录结构如下

![](006tKfTcly1g0z6zcq7zoj30dw0ao758.jpg)

## consul 部署

新建 `traefik-consul` 目录用以存放consul 服务相关配置

```bash
mkdir traefik-consul
cd traefik-consul
```

新建`docker-compose.yml`文件，输入以下内容

```yaml
version: "3"
services:
    consul:
        image: consul
        command: consul agent -server -dev -bootstrap -ui -advertise 192.168.3.26 -client=0.0.0.0
        ports:
            - 8400:8400
            - 8500:8500
        environment:
            - SERVICE_TAGS=traefik.enable=false
            - SERVICE_53_TAGS=traefik.enable=false
            - SERVICE_8300_TAGS=traefik.enable=false
            - SERVICE_8500_TAGS=traefik.enable=true
```

> 这里为了简化测试 consul 部署为 dev 模式，在生存环境请将 consul 独立部署为高可用集群模式。

在`traefik-consul`中启动 Consul 服务：`docker-compose up -d`，在浏览器里面访问 consul 服务：http://192.168.3.26:8500

![](006tKfTcly1g0z5rpd7oxj325w0juwgz.jpg)

## Registrator 部署

新建 `consul-registrator` 目录用以存放 registrator 服务相关配置

```bash
mkdir consul-registrator
cd consul-registrator
```

新建`docker-compose.yml`文件，输入以下内容

```yaml
version: "3"
services:
    consul_registrator:
        image: gliderlabs/registrator
        command: -resync=1000 -retry-attempts=-1 -retry-interval=2000 -ip="192.168.3.26" consul://192.168.3.26:8500
        volumes:
            - /var/run/docker.sock:/tmp/docker.sock
```

> 一个 docker 节点只需要部署一个 Registrator 容器。

在`consul-registrator`中启动 Registrator 服务：`docker-compose up -d`，这时在 consul 管理界面可以看到多出了2个Service

![](006tKfTcly1g0z5vdls3cj32620pgq6g.jpg)

## Traefik 部署

新建 `traefik-gateway` 目录用以存放 Traefik 服务相关配置

```bash
mkdir traefik-gateway
cd traefik-gateway
```

新建 Traefik 配置文件 `traefik.toml`

```toml
################################################################
# Consul Catalog configuration backend
################################################################

[entryPoints]
  [entryPoints.http]
  address = ":80"

# Enable web configuration backend
[web]

# Web administration port
#
# Required
#
address = ":8080"

# Enable Consul Catalog configuration backend
[consulCatalog]

# Consul server endpoint
#
# Required
#
endpoint = "127.0.0.1:8500"

# Default domain used.
#
# Optional
#
domain = "localhost"

# Expose Consul catalog services by default in traefik
#
# Optional
#
exposedByDefault = false

# Prefix for Consul catalog tags
#
# Optional
#
prefix = "traefik"

# Default frontEnd Rule for Consul services
#
# The format is a Go Template with:
# - ".ServiceName", ".Domain" and ".Attributes" available
# - "getTag(name, tags, defaultValue)", "hasTag(name, tags)" and "getAttribute(name, tags, defaultValue)" functions are available
# - "getAttribute(...)" function uses prefixed tag names based on "prefix" value
#
# Optional
#
#frontEndRule = "Host:{{.ServiceName}}.{{Domain}}"

```

新建 `Dockerfile` 文件

```dockerfile
FROM traefik:alpine

EXPOSE 8080

COPY traefik.toml /etc/traefik/traefik.toml	
```

新建 `docker-compose.yml`

```yaml
version: "3"
services:
    traefik:
        build: .
        command: -c /dev/null --api --logLevel=DEBUG --consulcatalog.endpoint=192.168.3.26:8500
        ports:
            - "80:80"
            - "8080:8080"
        environment:
            - SERVICE_TAGS=traefik.enable=false
```

在`traefik-gateway`中启动 Traefik 服务：`docker-compose up -d`，这时的 consul 里多出如下服务

![](006tKfTcly1g0z69ndvwoj322q0u0dkh.jpg)

在浏览器里面访问 Traefik 服务：http://192.168.3.26:8080 进入Traefik 管理界面，可以看到如下

![](006tKfTcly1g0z68kw9esj31e40u0gr2.jpg)

> 现在很多系统使用 Nginx 作为服务网关，按照上面的分析使用 Nginx 只需要替换掉 Traefik 即可，经过本人测试完全可行，并且 `Nginx + Consul` 已经用于我司生产环境中。具体 Nginx 的配置可以参考：https://github.com/threeq/useful-scripts/tree/master/my-docker/consul-nginx

到现在为止，从`容器自动注册 Registrator`，到`注册中心 Consul`，再到`服务网关 Traefik` 都已搭建完成，一个简单可扩展的服务架构基本成型，下面进行真实服务测试。

# 测试服务部署

这里为了测试建立 2 个简单的 web 服务，分别使用 golang 语言和 python 语言实现形成异构系统。新建目录 `traefik-example` 作为测试服务工作目录

```
mkdir traefik-example
cd traefik-example
```

## golang 服务

在 `traefik-example` 里面新建 `go` 目录，并进入

```
mkdir go
cd go
```

新建文件 `app.go` ，输入以下代码

```go
package main

import (
	"fmt"
	"log"
	"net/http"
)

func sayhelloName(w http.ResponseWriter, r *http.Request) {
	log.Println("Hello World! I'm Golang!!!")    //这个写入到w的是输出到客户端的
	fmt.Fprintf(w, "Hello World! I'm Golang!!!") //这个写入到w的是输出到客户端的
}

func main() {
	http.HandleFunc("/", sayhelloName) //设置访问的路由
	log.Println("start http server on 9090")
	err := http.ListenAndServe(":9090", nil) //设置监听的端口
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
```

编写 Dockerfile

```dockerfile
FROM golang:alpine

COPY app.go app.go

EXPOSE 9090
```

## python 服务

在 `traefik-example` 里面新建 `python` 目录，并进入

```
mkdir python
cd python
```

新建文件 `app.go` ，输入以下代码

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World! I'm Python!!!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

新建 `requirements.txt`，写入 flask 版本依赖

```txt
flask>=1.0.2
```

编写 Dockerfile

```dockerfile
FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY app.py app.py
```

## 发布测试服务

回到工作目录 `traefik-example` ，新建 `docker-compose.yml` 文件：

```yaml
version: "3"
services:
    web_go:
        build: go
        command: go run app.go
        ports:
            - 9090
        environment:
            - SERVICE_TAGS=traefik.enable=true,traefik.frontend.entryPoints=http,traefik.frontend.rule=Host:go.traefix.example.localhost

    web_python:
        build: python
        command: python app.py
        ports:
            - 9091:5000
        environment:
            - SERVICE_TAGS=traefik.enable=true,traefik.frontend.entryPoints=http,traefik.frontend.rule=Host:python.traefix.example.localhost
```

最后的文件目录结构像这样：

![](006tKfTcly1g0z1ajbizij30bw0c2js7.jpg)

在`traefik-example`目录中启动测试服务容器

```shell
docker-compose up --scale web_go=3
```

在控制台会看到如下日志信息

![](006tKfTcly1g0z6hhkoi9j31hk0io43l.jpg)

在 consul 里面应该可以看到注册的 web_go 服务和 web_python 服务

![](006tKfTcly1g0z6iayolvj31ta0u0n3e.jpg)

在 Traefik 里面应该可以看到 web_go 和 web_python 的路由信息

![](006tKfTcly1g0z6j20tgfj31bi0u07by.jpg)

## 访问测试

在访问之前还需要做最后的配置，可以看到在 Traefik 的路由信息中有 `python.traefix.example.localhost` 和 `go.traefix.example.localhost`，这两个 Host 信息（也就是域名），确保你访问测试的机器能正常连接你的测试机，然后将这两个域名解析地址指向测试机 IP。在我这里是 `192.168.3.26`，修改本机的 `/etc/hosts` 文件添加Host 记录:

```
192.168.3.26    go.traefix.example.localhost
192.168.3.26    python.traefix.example.localhost
```

现在所有配置均已完成，进行访问测试

1、在浏览器中访问 http://python.traefix.example.localhost

![](006tKfTcly1g0z6sga7xlj30om06gt9d.jpg)

2、在浏览器中访问 http://go.traefix.example.localhost

![](006tKfTcly1g0z6stbup1j30ok05swf4.jpg)

以上 2 不正确显示表示已经能正常路由了。下面测试一下负载均衡

3、多次访问 http://go.traefix.example.localhost 后，可以看到访问日志如下说明已经进行负载均衡了，启动的 web_go 3个实例都输出正常请求响应日志。

![](006tKfTcly1g0z6ul3s65j31fc0u0gv6.jpg)

# 思考

1、虽然 `web 层` 已经做到水平扩展，并且已实现高可用，但是 `网关层` 如何做到高可用呢？

> 这里实现了一个简单的高可用方案，在网关层再加入一个网关节点 `node2` ，和 `node1` 一起形成`主从服务`。实现方案上可以使用  `Keepalived + VIP` 的方式，这样在一台服务器挂掉时，可以自动切换到另外一台服务器上。结构图如下：
>
> ![](006tKfTcly1g0y6c3f7a9j317v0u0gw6.jpg)

2、通过上面的架构修改，网关层也已经达到高可用，但是发现所有请求都在单台网关机器上，单台机器能力再强也是有限的，怎么让网关层的机器水平扩展加入多台机器同时服务形成集群？

> 这里可以使用使用 DNS 查询的轮询机制，我们搭建多套`主从结构反向代理服务器`，然后在 DNS 解析配置里面配置多个 `VIP`，这样在客户端进行 DNS 解析时就会轮询返回配置的多个 VIP。结构图如下：
>
>   ![](006tKfTcly1g0y74p0xjyj317v0u0k1n.jpg)

3、注册中心高可用方案？

> 注册中心是整个系统中的核心组件之一，在生产环境中高可用是必须的，不论是 etcd 还是 consul 都有高可用集群方案。

4、解决系统高可用的基本原则是什么？

> 其实解决系统高可用的基本原则就是：**冗余和故障转移**。从上面的结构看不论是是在网关层还是 web 层，解决高可用都是用到了冗余和故障时自动切换，只是由于处在架构的不同层级，所使用的技术解决方案不一样，所以在设计和解决特定问题时，要了解所解决问题处在架构的什么位置，才能给出正确合理的解决方案。

5、除了基本原则外还需要注意什么？

> 在遇到大量请求的时候，为了防止雪崩这里面还需要做**限流、熔断、服务降级**等措施。当然光是这样还是不够的，总不能每次都等到系统挂了，我们才知道出问题了吧！所以这里面就需要在上线前进行严格的**测试**，找出系统瓶颈，上线后对系统进行全面的**监控、预警**等措施。

6、解决系统高并发请求的基础？

> 从上面的架构设计上已经体现了解决高并发请求的基础：**拆流和限流**，在不同的架构位置上拆分和限制时所使用的技术方案不同，当然这个只是从请求流量角度出发。从程序设计实现角度出发就是：**缓存和异步**，这是两个不同的维度，解决不同的问题。

**架构设计，知易行难，实践是最好的捷径。**
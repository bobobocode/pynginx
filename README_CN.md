# PyNginx

Python版的Nginx。

更进一步，它还是一个Python版的[Engine](https://github.com/bobobocode/engine.git)。

事实上，PyNginx是在写Engine的过程中逐步独立出来的一个项目。

开始是从Engine中分离出Driven（现在还处于一个非常原始的阶段），
而后PyNginx又来自于Driven中的调试用嵌入式Web服务器。

所有这些都是围绕Engine项目要实现的一个想法而进行的实验，
本质上是基于一种特定平衡考虑而对多种技术协调使用的尝试。

PyNginx当前更现实的一个意义是为更好地理解Nginx源代码而进行。

## 更好地理解Nginx源代码

阅读Nginx的源代码可以解答关于Web服务的很多深层次的技术疑问。

开发PyNginx的过程就是深入理解Nginx源代码的过程（开发进度会滞后于阅读进度）。
作为Nginx的Python实现，PyNginx代码希望能成为Nginx代码的易读版本。

在版本迭代中，从0.1.0开始，PyNginx将保持可以作为一个（一定范围）可用的Web服务器运行。即运行起来保障支持***examples***目录中展示的使用方法
（你会发现它在开始的阶段更优先支持一些Engine的特性）。

## 什么是和Nginx相同的（或有类比性的）

以下是版本0.1.0要实现的和Nginx对应的目标
（当前0.0.1是要迁移过来Engine(Driven)中相应的代码，尝试转向PyNginx的目标，
目前看这个计划是有效的）：

* 主要用法，特别是配置文件
* 关键设计概念，可以用来阅读理解Nginx的原理

```
a. 核心数据结构ngx_cycle
b. 模块框架机制
c. 基于epoll的事件循环
d. 配置文件解析
```

PyNginx的代码尽量与Nginx的代码形成映射，
甚至尽量保持同样的变量命名（会将ngx\_前缀换成pyngx\_前缀）。
在映射的代码中，需要明确出来不同的地方用前缀py\_命名。

## 需要注意哪些不同

* 在完善到足够高的版本之前，PyNginx使用起来和运行起来无法保障与Nginx一致，
主要是配置文件方面。
* 形成与Nginx的代码映射以达到诠释的效果，并不意味着完全按Nginx的实现方式来写，
很多时候要考虑结合Python作为高级语言的特性。
事实上我在尝试使用函数式编程范式的方法来取得二者的平衡。
* PyNginx当然还被期望于其它意义，但现在讨论这一点为时过早，需要视实验的结果而定。

## 我的联系方式

* <https://github.com/bobobocode>  
* <bobobomail@yeah.net>

欢迎交流 : )

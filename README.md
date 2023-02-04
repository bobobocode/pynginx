# PyNginx

Nginx for Python.

Furthermore, it is a Python version of [Engine](https://github.com/bobobocode/engine.git).

In fact, PyNginx is a project that gradually became independent in the process of programming Engine.

Driven (still in a very primitive stage) is separated from Engine,
And PyNginx comes from the embedded web server for debugging in Driven.

All of these are for the idea of the Engine project,
In essence, it is an attempt to coordinate the use of multiple technologies based on a specific balance consideration.

One of the more realistic meanings of PyNginx is to understand the source code of Nginx better.

## For learning Nginx

Reading the source code of Nginx can answer many deep technical questions about web servers.

The process of developing PyNginx is the process of reading the source code of Nginx.
The developing progress will follow the reading progress and lag behind the reading progress.
In iterative versions, from version 0.1.0, PyNginx will always be able to run as a (certain range) available web server.

Specifically, it is guaranteed to support the usage shown in the ***examples*** directory 
(You will find that it gives priority to supporting some features of Engine at the beginning).

## What is the same (or analogous) to Nginx

The following are the goals of corresponding to Nginx which will be achieved by version 0.1.0:

* Main usage, especially about configuration files
* Key design concepts, which can be used to understand the mechanism of Nginx

```
a. Core data structure ngx_cycle
b. Module framework mechanism
c. Event loop based on epoll
d. Parsing the config file
```

The code of PyNginx is mapped with the code of Nginx as much as possible.
Even try to keep the same variable naming (just replace the ngx prefix with the pyngx prefix).

## Note some differences

* Before it is perfected to a high enough version, PyNginx cannot be guaranteed to be consistent with Nginx in use and operation (on configuration files mainly).
* Forming a code mapping with Nginx to achieve the effect of interpretation does not mean that it is completely written according to the implementation of Nginx.
It is necessary to consider combining the features of Python as a high-level language.
In fact, I am trying to use the functional programming paradigm to achieve a balance between the two.

## Contact with me

* <https://github.com/bobobocode>  
* <bobobomail@yeah.net>

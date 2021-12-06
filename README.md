# 数据科学基础2021 大作业

成员：谭子悦 李佳骏 邱兴驰

方向：司法大数据自动化标注与分析

## 项目总览

## Features

自动化标注系统既可以标注出通用属性，也可以针对部分类别案件标注出特别属性，如：危险驾驶罪，可标注出酒精含量和罚款金额

## 注意事项
*2021-12-6 Update 3*

- Windows 运行脚本前修改权限 `set-executionpolicy remotesigned`
- Windows 启用venv: `./venv/Scripts/activate`(运行前确认是在venv下的terminal)

*2021-12-5 Update 2*
- 所有需要的库都放在了 requirement.txt，开始工作前请做如下操作
> 1.在项目管理中建立新的Virtualenv environment，位置任意，版本用Python3.10

> 2.在pycharm下面的命令行中输入 `pip install -r requirement.txt`

> 3.每次push前先 `pip freeze > requirement.txt`

> 4.一定不要把自己的venv push上来！！！

*2021-12-5 Update 1*

- 开始工作前，请确认编译环境为 `/env/bin/python`中的venv Python 3.10
- 安装 package 时确认装进了虚拟环境（而不是本地环境）
- 请为每一个方法编写 pydoc
- 请将自己负责部分的代码全部写在相应module下，调试时可以从 `src/main.py` 接入

- 对于某一 python 程序而言，其相对根目录为**主函数所在module**的路径（若不属于任何module，则为项目路径），因此在 methods 中处理文件路径时，请使用如下格式：

   ```python
   [Module Name].__path__[0] + '/relative/path/to/your/file'
   """
   - Module Name 为模块名称，使用前需先import, 
   	e.g.: 
   	- from src import Crawling
   	- Crawling.__path__[0]
   	
   - __path__属性为数组
   """
   ```

- 尽量不要选择有系统依赖性的api
- 在本文档中即时更新相应部分的开发笔记 （遇到的困难，或新解决的问题，或大致解决思路）
- 及时commit & push，遇到无法push的时候挂代理（本地监听端口一般为 `127.0.0.1:1087`）
- 可以下载github的GUI客户端
- 想到再补充......

## 开发笔记

### 1. 爬虫部分

// todo

### 2. 自然语言处理部分

// todo
- 完成了一部分jiebaProcessing
  - 完善了函数封装
  - 函数包括文本过滤、和初步分词
  - 初步输出结果进行中
- hanlpProcessing还未进行

### 3. GUI界面部分

// todo
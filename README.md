 # 数据科学基础2021 大作业

成员：谭子悦 李佳骏 邱兴驰

方向：司法大数据自动化标注与分析

## 1 文档

[1. 初期汇报文稿](./docsets/初期汇报文稿.md)

[2. 最终文稿](./docsets/最终文稿.md)

[3. 开发日志](./docsets/开发日志.md)

## 2 使用方法

### 2.1 兼容性

#### 2.1.1 系统：建议使用macOS运行

- 经测试在macOS Monterey 与 macOS Big Sur上均可正常运行。
  - 仅测试了Intel版，未测试ARM版
  - 主要测试机型：
    `MacBook Pro (13-inch, 2020, Four Thunderbolt 3 ports), 2 GHz Quad-Core Intel Core i5, Intel Iris Plus Graphics 1536 MB, macOS Monterey 12.1`

- 在Windows 10中可正常进入GUI界面，但界面比例会出现异常；
  但由于字符编码问题（系统默认编码不是utf-8）IO相关api无法工作，因此不能正常使用。

- 由于WebDriver未提供Linux驱动，自动化爬取模块无法在Linux中运行，其余尚未测试。

#### 2.2.2 Python版本：建议使用 Python 3.9.x 运行

所有的Python版本测试信息均基于macOS Monterey 12.1

- 由于torch兼容性问题，本程序不支持 Python 3.10.x
- Python 3.8.x 可正常运行，但会出现界面比例异常且部分GUI模块显示缺失等问题
- Python 3.9.x 可正常运行，测试环境为 Python 3.9.9

### 2.2 使用步骤

1. 运行前需先安装[支持库](./requirement.txt)：`pip install -r requirement.txt`


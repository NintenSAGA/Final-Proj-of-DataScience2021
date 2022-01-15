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

#### 2.2.3 浏览器：必须安装 Microsoft Edge

本程序自动化爬取部分的Web Driver内核为Microsoft Edge，已预先放于项目文件夹中，

使用前需要先安装最新版Microsoft Edge，否则需要Web Driver的部分无法运行。

### 2.2 启动步骤

1. 运行前需先安装[支持库](./requirement.txt)：`pip install -r requirement.txt`
2. 通过在项目根目录执行 `python main.py`运行本程序

### 2.3 使用说明

本程序包含自动化爬取与自动化批注两个部分

#### 2.3.1 自动化爬取

- 文书源：
  - 经稳定性测试后，文书源仅保留北大法宝一项。
  - 为了获取全部文书信息的访问权限，需在南京大学内网下使用，或预先执行南京大学IP登陆。

- 爬取选项：有两个可选项，其中
  - 爬取url_list指从北大法网获取相应文书的链接，存于本地。
    此步骤需要使用Web Driver。
  - 
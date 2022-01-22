 # 数据科学基础2021 大作业

![Python_version](https://img.shields.io/badge/Python-3.9-white?style=flat&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-macOS_|_Windows-white)
![Platform](https://img.shields.io/badge/Browser-Edge-white)

此项目为南京大学软件学院“数据科学基础2021秋”期末大作业

**主题**：司法大数据自动化标注与分析

**组长**：谭子悦 201250093

**组员**：李佳骏 201250113、邱兴驰201250112

**邮箱**：201250093@smail.nju.edu.cn

**开源链接**：[NintenSAGA/Final-Proj-of-DataScience2021 (github.com)](https://github.com/NintenSAGA/Final-Proj-of-DataScience2021)

**小组分工**：

- **爬虫**： 谭子悦
- **自动化标注**： 李佳骏、谭子悦
- **图形界面**：谭子悦、邱兴驰
- **数据处理与分析**：谭子悦、李佳骏
- **报告撰写**：谭子悦、李佳骏

## 1 文档

### 1.1 开发文档

[1. 初期汇报文稿](./docsets/初期汇报文稿.md)

[2. 开发日志](./docsets/开发日志.md)

### 1.2 研究报告

[研究报告 (上) - 系统概述](./docsets/研究报告(上)-系统概述.md)

[研究报告 (下) - 数据分析报告](./docsets/研究报告(下)-数据分析报告.md)

#### PDF

[研究报告 (上) - 系统概述.pdf](./docsets/研究报告(上)-系统概述.pdf)

[研究报告 (下) - 数据分析报告.pdf](./docsets/研究报告(下)-数据分析报告.pdf)


### 1.3 测试用数据集

[文书纯文本及标注数据（5842份）](./docsets/文书纯文本及标注数据（5842份）.zip)

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

- **文书源**：
  - 经稳定性测试后，文书源仅保留北大法宝一项。
  - 为了获取全部文书信息的访问权限，需在南京大学内网下使用，或预先执行南京大学IP登陆。

- **爬取选项**：有两个可选项，其中

  - 爬取url_list——从北大法网获取相应文书的链接，存于本地。此步骤需要使用Web Driver。
  - 爬取html_list——利用上一步骤取得的链接列表取回相应的html源文件，存于本地。若已勾选前者，则此选项为必选项。
  - 执行完上述步骤后会解析html文件并提取出相应纯文本。

  程序启动时会先行检查本地文件情况与爬取参数，若出现异常则会屏蔽相应的爬取选项。

- **爬取参数**：可以设置年份与文书数量，其中

  - 文书数量上限为15000（但经测试北大法宝最多只能显示2000份）
  - 年份范围为2000～2021，北大法宝默认为降序显示，因此大部分文书可能出于年末     

- 爬取文件将会存在`./src/crawling/results/~refined_text/`中（该文件夹运行一次后才会生成）

#### 2.3.2 自动化批注

- 默认选择文件夹为自动化爬取的[结果文件夹](./src/crawling/results/~refined_text/)，文件类型为txt
- 出于性能考虑，左侧只会预览文书前2000字内容
- 对多名涉案人员或多种罪名的情况无法准确提取
- “自动批注”可在后台快速完成选定文件夹下所有文件的批注
- 批注文件将保存于`文书源/json/`中，格式为json
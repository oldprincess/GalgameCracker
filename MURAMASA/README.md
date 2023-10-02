# MURAMASA

仅供学习交流和个人使用，**请不要将本项目用于违法行为，造成的任何损失与作者本人无关**

## 1 游戏信息

> 来源：[百度百科](https://baike.baidu.com/item/%E8%A3%85%E7%94%B2%E6%81%B6%E9%AC%BC%E6%9D%91%E6%AD%A3/7048475?fromtitle=%E8%A3%85%E7%94%B2%E6%82%AA%E9%AC%BC%E6%9D%91%E6%AD%A3)

中文名：装甲恶鬼村正

原版名称：装甲悪鬼村正

开发商：Nitroplus

发行日期：2009年10月30日

简介：故事发生在一个虚构的国家：大和。这个国家与现实中的日本极为接近，却又有着根本的不同：漫长的战乱之后满目疮痍的国土，高度集权唯我是从的幕府，野心勃勃伺机而动的西方军队，阴影中屏息隐忍的傀儡皇室……硬要说的话，将幕末与战后的日本杂糅啮合，也许就能生出这样一个畸形而脆弱的国家。无数人的野心、复仇、荣耀、欲望在这个动荡的时代下狂野的交错碰撞，强者凭着暴力凌驾征服，而弱者只能无梦地苟活。

## 2 脚本说明

脚本仅包含 [MURAMASA.py](MURAMASA.py) 一个脚本文件，能且仅能破解《装甲悪鬼村正》游戏的.npa文件，能够提取出cg、音频、脚本等。脚本MURAMASA.py参考了 [asmodean](http://asmodean.reverse.net/) 提供的c++破解脚本[exnpa](http://asmodean.reverse.net/pages/exnpa.html)，并将其重写成python，方便跨平台调用。

脚本还额外提供了打包数据成.npa文件的功能，虽然能够正常打包，但测试发现无法成功在游戏中运行，怀疑游戏本体对.npa文件进行了防篡改的处理。

### 2.1 文件和目录说明

本目录的树形结构如下

```
│  demo.py
│  MURAMASA.py
│  README.md
│
└─npa
        cg2.npa
```

|文件名|说明|
|:-:|:-:|
|demo.py|脚本样例|
|MURAMASA.py|脚本|
|README.md|readme文件|
|npa/cg2.npa|用于测试的.npa文件|

### 2.2 测试环境

* 操作系统：Windows11
* 处理器型号：Intel i5-12500H
* 语言环境：python3.11
* 游戏文件：装甲恶鬼村正（翼之梦汉化版）

经过测试，能够正常从cg.npa、cg2.npa中提取出游戏cg，但重新打包的cg文件无法正常在游戏中显示

### 3 使用方式

样例代码见当前目录的demo.py

#### 3.1 解包功能

解包`unpack`函数用于解包.npa文件，输入.npa文件路径in_filePath以及输出目录out_dirPath，需要保证输出目录已存在。样例代码如下，对文件npa/cg2.npa解包，输出至out_cg2目录中。

```python
import os
import MURAMASA

in_filePath = "npa/cg2.npa"
out_dirPath = "out_cg2"

# 创建输出的目录
if not os.path.exists(out_dirPath):
    os.mkdir(out_dirPath)
# 对文件cg2.npa解包，输出至out_cg2目录中
MURAMASA.unpack(in_filePath, out_dirPath)
```

控制台将输出以下信息，提示解包的出来文件名称，最后的finish说明操作完成。

```
[write] cg2\bg\bg031_八幡宮境内_03.jpg
[write] cg2\ev\ev136_戦闘解説ＶＳ首領編３_d.jpg
[write] cg2\ev\ev163_真っ二つの正宗_c.jpg
[write] cg2\ev\ev221_月明かりを浴びて立つ光_a.jpg
[write] cg2\ev\ev221_月明かりを浴びて立つ光_b.jpg
[write] cg2\ev\ev222_茶々丸Ｈ_c.jpg
[write] cg2\ev\ev222_茶々丸Ｈ_d.jpg
[write] cg2\ev\resize\ev212_二世村正戦闘体勢_bm.jpg
[write] cg2\ev\resize\ev221_月明かりを浴びて立つ光_al.jpg
[write] cg2\ev\resize\ev221_月明かりを浴びて立つ光_bl.jpg
[write] cg2\st\3d九〇式竜騎兵_騎突_戦闘.png
[write] cg2\st\3d九〇式竜騎兵_騎突_戦闘2.png
[write] cg2\st\3d九〇式竜騎兵_騎突_戦闘b.png
[write] cg2\sys\telop\tp_銀星号の唄16.png
[write] cg2\sys\telop\tp_銀星号の唄17.png
[log] unpack 'npa/cg2.npa' finish!
```

### 3.2 打包

打包后的.npa文件**无法正确嵌入游戏文件中运行**，待进一步分析。

打包`pack`函数可将一个目录内的文件打包成.npa格式，最简单的调用方式如下，将out_cg2中的文件打包并输出至out_npa/cg2.npa文件中。同样需要校验输出的目录是否存在，若不存在则需要手动创建。

```python
in_dirPath = "out_cg2"
out_filePath = "out_npa/cg2.npa"
if not os.path.exists(os.path.dirname(out_filePath)):
    os.mkdir(os.path.dirname(out_filePath))
MURAMASA.pack(in_dirPath, out_filePath)
```

控制台将输出以下信息，提示打包的项目，最后的finish说明操作完成。

```
[pack] bg
[pack] ev
[pack] st
[pack] sys
[pack] bg\bg031_八幡宮境内_03.jpg
[pack] ev\resize
[pack] ev\ev136_戦闘解説ＶＳ首領編３_d.jpg
[pack] ev\ev163_真っ二つの正宗_c.jpg
[pack] ev\ev221_月明かりを浴びて立つ光_a.jpg
[pack] ev\ev221_月明かりを浴びて立つ光_b.jpg
[pack] ev\ev222_茶々丸Ｈ_c.jpg
[pack] ev\ev222_茶々丸Ｈ_d.jpg
[pack] ev\resize\ev212_二世村正戦闘体勢_bm.jpg
[pack] ev\resize\ev221_月明かりを浴びて立つ光_al.jpg
[pack] ev\resize\ev221_月明かりを浴びて立つ光_bl.jpg
[pack] st\3d九〇式竜騎兵_騎突_戦闘.png
[pack] st\3d九〇式竜騎兵_騎突_戦闘2.png
[pack] st\3d九〇式竜騎兵_騎突_戦闘b.png
[pack] sys\telop
[pack] sys\telop\tp_銀星号の唄16.png
[pack] sys\telop\tp_銀星号の唄17.png
[log] pack 'out_cg2' finish!
```

打包`pack`函数还支持其它的参数形式，参数列表如下

```python
def pack(in_dirPath: str, out_filePath: str, 
         seed1_I: int = 0, seed2_I: int = 0, 
         compress: bool = True):
    ...
```

* in_dirPath和out_filePath标记了输入和输出文件路径
* seed1_I和seed2_I是用于生成加密数据的种子，可以由用户自己传入，不传入则默认为0
* compress标记了是否对文件进行压缩，压缩需要用到zlib库，默认是True

### 3.3 其它

脚本中默认使用gbk字符集，若待解包的文件不是使用gbk编码的或是文件名不想采用gbk编码，可以修改FILE_PATH_ENCODING字段的值来控制编码。即

```python
print(MURAMASA.FILE_PATH_ENCODING)  # gbk
MURAMASA.FILE_PATH_ENCODING = "utf8"  # 重设为utf8编码格式
```

在测试所用的.npa文件中，gbk格式的编码用于记录打包的文件名称，我不知道为什么使用gbk而不是utf8或是日文专用字符集，可能是汉化组进行了修改。
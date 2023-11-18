# python环境配置


| 主要贡献者    | 联系方式                      | 更新时间   | GitHub | 
| :-----------: | ----------------------------- | :--------: | :----: |
| (Main Attributor)<br/>JamesHanZhang | `jameshanzhang@foxmail.com` | 2023-08-15 | [链接](https://github.com/JamesHanZhang)        |

## Anaconda环境配置
### 安装Anaconda
1. 登录[Anaconda官网](https://www.anaconda.com/download)下载安装包；
2. 打开安装包安装，选择默认即可；
3. 在开始菜单中登录Anaconda Prompt，键入`Python -v`，如能显示版本，则表示安装成功；

## 搭建不同的conda environment
除了`base`环境是通用的，各个conda environment是互相独立的。它有如下的优势：

1. **Isolation**：这意味着如果某个环境的包搭建环境，依赖关系出了问题，不影响其他的环境。这可以有效容错，防止因为某个包的安装导致整体conda environment崩溃的情。
2. **Dependency Management**: 不同项目有时候依赖的同一个包的版本不同，这也会影响到项目的质量。独立的依赖管理能有效保证项目不受版本影响。
3. **Sandboxing**: 沙盒模式保证特殊的环境变动不影响其他项目。
### 创建conda environment
```bash
# python要明确所需的版本号
conda create --name <conda_environment_name> python=python_version
# 案例
conda create --name james_environment python=3.11.5
```

### 查看conda environment
```bash
# 查看所有环境，带*号的是目前所处的环境
conda info --envs
```

### 调用conda environment
- **开启环境**
```bash
# 在prompt里激活环境
conda activate <conda_environment_name>
# 案例
conda activate james_environment
```

- **关闭环境**
```bash
# 首先关闭当前环境
conda deactivate
# 然后激活base环境
conda activate
```

### 删除conda environment
- 首先，回到`base`环境（`base`环境作为通用环境不能删除）
```bash
# 首先关闭当前环境
conda deactivate
# 然后激活base环境
conda activate
```
- **选择1**：使用`remove`命令删除环境，根据提示选择`y`
```bash
conda env remove -n <conda_environment_name>
```
- **选择2**：使用`delete`命令删除环境
```bash
# 需要`--name` flag
conda env delete --name <conda_environment_name>
# 也可以使用`-n`flag
conda env delete -n <conda_environment_name>
```

## Anaconda安装Library的两种方式
### 方式1：通过`conda`命令安装
即通过Anaconda的官网路径下载外库的安装包，其依赖关系更准确，不会造成环境崩溃，可以放心大胆地安装在`base`环境里；

#### Anaconda在线通过`conda`安装library
1. 登录[Anaconda官网离线包下载平台](https://anaconda.org/anaconda/repo);
2. 注册并登录账户；
3. 在Anaconda.org的检索栏输入希望下载的library，检索到对应library；
4. 找到`conda install`命令部分，通常有对应的安装语句：
```bash
# 案例
conda install -c plotly plotly
```
5. 以**管理员身份**打开**Anaconda Prompt**，输入`conda install`的命令行；
6. 完成后，输入`conda list`，查看，如果包名在列表内，证明安装成功；

#### Anaconda如何安装离线`conda library`
1. 登录[Anaconda官网离线包下载平台](https://anaconda.org/anaconda/repo)；
2. 注册并登录账户；
3. 在Anaconda.org的检索栏输入希望下载的library，检索到对应library，下载最新版；
4. 安装包文件通常以`.tar.bz2`拓展名结尾，也有其他的情况，拓展名本身并不十分重要；
5. 下载所需安装包到自设路径；
6. 以**管理员身份**打开**Anaconda Prompt**，`cd`到对应路径；
7. 调用安装包安装：
```shell
# 基本格式
conda install library-name.tar.bz2
```
8. 登录Anaconda Prompt，查看安装包列表，看是否安装成功：
```shell
# 查看安装包列表，如所需library名称显示其中，表明已成功安装
conda list
```
#### Anaconda卸载包`conda library`
1. 通过`conda list`确定要卸载的包；
2. 以**管理员身份**打开**Anaconda Prompt**：
```bash
conda uninstall <package name>
```
3. 完成后在命令行输入`conda list`，如果没有该包，证明卸载成功；

### 方式2：通过`pip`命令安装
即通过常规的pip命令进行安装，因非conda官方环境，有一定可能造成环境崩溃。但是好处是能更新到最新的外库，部分library的官网更新是较慢的，可能无法满足构建服务的需要。此时推荐使用独立的`conda environment`来安装环境，以保证整体`base`环境不会崩溃。

#### 通过`pip`在线安装库`library`
以**管理员身份**打开**Anaconda Prompt**：
```bash
# 查询你想安装库的命令，通常格式如下
pip install <package name>
# 案例
pip install pyinstaller
```

#### 离线`pip`安装库
##### 查看系统环境
首先，我们需要知道系统的基本情况
```bash
# python 版本
python --version
```
- **linux环境查看系统**
```bash
uname -m
# `x86_64`: Indicates a 64-bit (x86_64) architecture.
# `i686` or `i386`: Indicates a 32-bit (x86) architecture.
# Other architecture identifiers might also be possible, depending on the system.
uname -s
# `Linux`: inicate the operating system is linux
# `MINGW64_NT-10.0-22621`: indicate the version of windows
cat /etc/os-release
# only available for linux/unix system
# returns all the version info about the operating system
```
- **windows环境查看系统**
```bash
echo %PROCESSOR_ARCHITECTURE%
# `x86` for a 32-bit system or `AMD64` for a 64-bit system
wmic os get osarchitecture
# "64-bit" for a 64-bit system or "32-bit" for a 32-bit system.
```
- **根据系统信息判断应执行的安装包**
	- a filename like `pyinstaller-X.Y.Z-py3-none-X.Y-linux_amd64.whl` would be for Python version X.Y on a 64-bit (x86_64) Linux system.

##### 下载安装包
以**管理员身份**打开**Anaconda Prompt**：
- **下载安装包**（默认下载当前使用平台的安装包）
```bash
# 下载安装包
pip download -d <download path> <package name>
# 案例下载pyinstaller安装包到本地路径，windows下没有标注驱动的话，默认C盘
pip download -d /path/to/download/directory pyinstaller
```
- **根据目标平台下载安装包**：容易产生兼容问题，不推荐
```bash
# `--platform` option is for setting platform target
pip download --platform manylinux1_x86_64 -d "C:\VB Temp Folder\python packages" pyinstaller
pip download pyinstaller -d "C:\VB Temp Folder\python packages" --platform manylinux1_x86_64 --python-version 311 --only-binary=:all: 
# manylinux1_x86_64 是公用的linux安装包版本关键tag
```

**问题**：使用`--platform`进行离线安装包的下载极容易出错，导致兼容性问题。
**最佳的解决方式**，是创建linux虚拟机，并通过虚拟机进行库配置，以保证程序的实用性。

##### 执行安装包
- **在目标环境执行安装包**
```bash
# cd到安装包的路径下
cd <download path>
# 执行安装离线包
pip install <download path> <pacakge-excutable-name.whl>
# 案例，安装pyinstaller安装包，windows下没有标注驱动的话，默认C盘
pip install /path/to/downloaded/pyinstaller-package.whl
```

需要注意的是，不同的包离线安装的目标文件不同。常见的有：
- `.whl`文件
- `.tar.gz`文件

另外，某些库的安装文件很多，需要选择正确的版本。在安装路径下，通过名字判断正确的文件来安装。


#### `pip`卸载库`library`
以**管理员身份**打开**Anaconda Prompt**：
```bash
# 卸载你想卸载的库，通常命令如下
pip uninstall <package name>
# 案例
pip uninstall pyinstaller
```


## 安装常用IDE
### PyCharm的安装及环境配置
1. 登录PyCharm官网安装社区办IDE: [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows);
2. 下载并按照默认安装；
3. 打开`setting`设置，找到`Python Interpreter`，选择`add interpreter`，选择`Add Local Interpreter`；
4. 找到`Conda Environment`，选择`use existing environment`，在路径上选择Anaconda的默认路径/或者选择对应的`conda environment`，例如`C:\ProgramData\anaconda3`或者`james_conda_environment`这样的独立环境；
5. 在`Conda Executable`环境选择：`C:\ProgramData\Anaconda3\condabin\conda.bat`，个人依据安装环境不同进行更改；选择确定OK；
6. 完成环境配置；
### Spyder
1. Anaconda附带编译器；
2. 点击`Anaconda Prompt`，输入`spyder`，回车，即可打开编译器；

### Jupyter Notebook
1. Anaconda附带编译器；
2. 点击`Anaconda Prompt`，输入`jupyter notebook`，回车，即可打开编译器；

## IDE常用调试
### Jupyter Notebook的调试
#### 修改Jupyter Notebook默认工作目录
1. 打开Anaconda Prompt，输入如下命令：
```shell
jupyter notebook --generate-config
```
2. 根据命令返回路径，找到文件`jupyter_notebook_config.py`；如有多个同名文件，选用用户目录下的`.jupyter`文件夹下的文件；
3. 打开该文件，检索`notebook_dir`关键变量；
4. 将`notebook_dir`取消注释，并添加希望设置的默认工作路径；
```python
c.NotebookApp.notebook_dir = 'D:\\CODE-PROJECTS'
```
5. 找到JupyterNotebook快捷方式，右键选择属性，删除【目标】属性中的`%USERPROFILE%`，点击应用，确定；
6. 打开Anaconda Prompt，输入`jupyter notebook`并回车，打开jupyter notebook，确认是否已成功完成目录设置；
#### 修改代码/配置以执行项目主程序
1. 通常项目中包含多个python文件，仅执行主程序的话，无法识别主程序所调用的其他python文件，则会报错，因此要进行一些设置；
```python
import sys
# 将该项目table-data-format-transform-app所在的绝对路径添加到环境变量中
path = "D:\\Projects\\table-data-format-transform-app"
sys.path.append(path)
```
2. 另外，注意如项目本身有相对路径设置，则应将jupyter notebook文件放置在合适的项目路径下，以杜绝对相对路径的影响导致程序执行失败；
```python
# 项目路径
table-data-format-transform-app/
├── main/
	├── __init__.py
	└── jupyter_child.ipynb
├── __init__.py
└── jupyter_mom.ipynb

```

- 如直接在项目路径下：开头可以这么写以通过相对路径识别项目所在路径；
```python
# jupyter_mom.ipynb
import sys
import os
# 将项目路径添加到环境变量
path = sys.path[0]
sys.path.append(path)
```
- 如在项目路径的子目录下：则需要递归到项目路径，才能添加路径到环境变量；
```python
# jupyter_child.ipynb
import sys
import os
# 将项目路径添加到环境变量
path = os.path.dirname(sys.path[0])
sys.path.append(path)
```
### Spyder的调试
#### 如何用Spyder执行项目而非单一脚本
1. 通常项目中包含多个python文件，仅执行主程序的话，无法识别主程序所调用的其他python文件，则会报错，因此要进行一些设置；
2. 通过`main.py`运行一个项目的时候，需要在主程序内的`sys.path`里加入该项目的路径；
```python
import sys
# 将该项目所在的绝对路径添加到环境变量中
path = "D:\\Projects\\table-data-format-transform-app"
sys.path.append(path)
```
3. 如果该项目中运行有调用相对路径，相对路径会自动识别为Spyder的默认安装路径，从而导致程序执行失败；考虑到修改默认路径的繁琐，不推荐使用Spyder运行项目；

## 依赖包配置

### 首先查看各个包的版本号
#### 直接通过`pip`查看
- 每调用一个包，请预先判断该包是内置包，还是外包，如果是外包，可以通过以下命令查看该包的版本号：
```bash
pip show package-name
```

案例：
```bash
pip show requests
```
#### 在anaconda环境查看包的版本号
- 直接查看所有的包
```bash
conda list
```
- Linux bash查看
```bash
conda list | grep package-name
```
- windows查看
```bash
conda list | findstr package-name
```
将 `package-name` 替换为你要查看的包名。这将显示包含指定名称的包的版本信息。
### `requirements.txt`依赖包配置
- `requirements.txt`: 这是一个文本文件，其中每一行都包含一个依赖包的名称和版本号，格式通常为：
```bash
# 可以通过#添加注释
package-name==version
```

例如：
```
requests==2.26.0
Flask==2.0.1
```

- **\=\=**：等于某个版本。
- `>=`：大于等于某个版本。
- `<=`：小于等于某个版本。
- `<`：小于某个版本。
- `>`：大于某个版本。
#### 调用该文件
- 调用配置文件: 进入该配置文件的所在目录，在终端使用命令行直接配置；
- 如果开发者的环境是anaconda，请先通过`conda list`命令查看其已拥有的依赖包，再删减`requirements.txt`里的依赖包的内容，以保证无重复安装的情况；且采用独立虚拟环境安装依赖包；
```bash
# 安装所有依赖包的命令
pip install -r requirements.txt
```
### `Pipfile`依赖包配置
#### 前提：安装`pipenv`包
请先确保已经安装了`pipenv`，如果没有的话，则通过以下命令先安装：
```bash
pip install pipenv
```

#### 使用方法

`Pipfile` 是使用 `Pipenv` 管理项目依赖的一种方式。它通常包含了项目的依赖和开发依赖，并且会指定版本范围而不是精确的版本号。首先在项目的根目录下新建无拓展名的文本文件`Pipfile`，然后在里面新增内容。示例 `Pipfile` 文件：

```bash
[[source]]
# 通过#来写注释, 注意, 注释不能连续多行, 否则报错UnicodeDecodeError
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
# 主要依赖项
requests = "==2.26.0"
Flask = "==2.0.1"

[dev-packages]
# 开发依赖项
pytest = "*"

[requires]
# Python版本需求
# 指定版本则这样写: python_version = "3.11.5"
# 大于等于某个版本这样写: python_version = ">=3.11.5"
python_version = ">=3.11.5"
```

在这个示例中，
- `[[source]]`区块定义从哪里获取软件包，一般是固定的，无需更改。一个软件包源（source）是包含 Python 软件包的仓库或索引，通常是一个 URL。
	- `url` 表示软件包的源的 URL，这里是 Python Package Index（PyPI）的 URL。PyPI 是 Python 的官方软件包索引，包含了大量的 Python 软件包供开发者使用。
	- `verify_ssl` 是一个布尔值，表示是否要验证 SSL 证书。在大多数情况下，你会希望设置为 `true`，以确保通过加密通信下载软件包。
	- `name` 是源的名称，这里是 "pypi"。这个名称在 Pipenv 中没有太多实际作用，但它是源的唯一标识符。
- `[packages]` 区块定义了项目的正常运行时所需的依赖; 
- `[dev-packages]` 区块定义了开发时需要的额外依赖。使用 `pipenv install` 命令可以根据这个文件来安装依赖。
	- `pytest = "*"` 是 `Pipfile` 中对依赖的版本规范的一种写法。在这里，**它表示安装 `pytest` 这个软件包的最新版本**，而不是指定一个具体的版本号。
- `[requires]`用来确定项目运行的python版本号;

#### 安装依赖包
- 在根目录路径的终端内使用 `pipenv install` 命令可以根据 `Pipfile` 安装所有的依赖。
```bash
pipenv install
```

**注意**：`Pipenv` 还会生成一个 `Pipfile.lock` 文件，用于锁定依赖的确切版本，以确保在不同的环境中使用相同的依赖版本。这个文件通常不需要手动编辑，而是由 `Pipenv` 自动生成和管理。

### 注意! 如果是anaconda环境, 需使用独立虚拟环境
在 Anaconda 环境中，通常你可以使用 `conda` 命令来创建虚拟环境并安装依赖项，因为上述依赖通常是为`pip`准备的，所以为了避免影响到anaconda本身环境的依赖关系，需要新建一个独立虚拟环境。

```bash
# 查看所有环境，带*号的是目前所处的环境
conda info --envs

# 新建独立虚拟环境，这里james_environment是自己设定的虚拟环境的名字
conda create --name james_environment

# 详细建立独立虚拟环境
## 明确python版本
python --version
## python要明确所需的版本号
conda create --name <conda_environment_name> python=python_version
## 案例
conda create --name james_environment python=3.11.5

# 调用独立虚拟环境
conda activate james_environment

# 在独立虚拟环境内安装依赖包
pip install -r requirements.txt

# 退出独立虚拟环境，退出当前环境
conda deactivate

# 删除独立虚拟环境
## 需要`--name` flag
conda env delete --name james_environment
## 也可以使用`-n`flag
conda env delete -n james_environment
## 也可以使用`remove`命令
conda env remove -n james_environment
```
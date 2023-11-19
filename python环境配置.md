# python环境配置
#programmingLanguage #python #environment

| 主要贡献者    | 联系方式                      | 更新时间   | GitHub | 
| :-----------: | ----------------------------- | :--------: | :----: |
| (Main Attributor)<br/>JamesHanZhang | `jameshanzhang@foxmail.com` | 2023-11-19 | [链接](https://github.com/JamesHanZhang)        |

## 目录Catalogue
`注意, 在obsidian中直接点击会导致全选该模块, 小心不要误删除`
- [Anaconda环境配置](#Anaconda环境配置)
- [搭建不同的conda-environment](#搭建不同的conda-environment)
- [Anaconda安装Library的两种方式](#Anaconda安装Library的两种方式)
- [直接安装python](#直接安装python)
- [搭建不同的纯python虚拟环境(非anaconda环境)](#搭建不同的纯python虚拟环境(非anaconda环境))
- [纯python环境安装包Library](#纯python环境安装包Library)
- [安装常用IDE](#安装常用IDE)
- [IDE常用调试](#IDE常用调试)

## Anaconda环境配置
### windows环境安装Anaconda
1. 登录[Anaconda官网](https://www.anaconda.com/download)下载安装包；
2. 打开安装包安装，选择默认即可；
3. 在开始菜单中登录Anaconda Prompt，键入`Python -v`，如能显示版本，则表示安装成功；
### linux环境安装Anaconda
1. 通过命令行识别底层g++及gcc指令集：根据以下命令行的反馈，在官网上寻找对应的安装包；
```bash
uname -m
```
2. 普遍的反馈是`x86_64`，意思是amd64系统，在[Anaconda官网](https://www.anaconda.com/download)上可以找到对应的安装包，例如`Anaconda3-2023.09-0-Linux-x86_64.sh`。
3. 下载后可选两种方式
#### 方式1: 手动离线安装
1. 执行安装：在安装过程中，你需要按照提示进行操作，包括同意许可协议、选择安装路径等。
```bash
sudo bash Anaconda3-<version>-Linux-x86_64.sh
```
2. 激活Anaconda:
```bash
source ~/.bashrc # 或 source ~/.bash_profile，根据你的系统刷新bash配置
conda init # 初始化 conda
source ~/.bashrc # 刷新bash配置以使conda配置生效
```
- 或者，如果你使用的是 `zsh` 终端，可能需要运行：
```bash
source ~/.zshrc
conda init zsh
```
3. 如果提示找不到该命令，则说明安装过程中未写入PATH，需要手动添加：
```bash
# 执行如下命令进行手动添加
export PATH="$HOME/anaconda3/bin:$PATH"
# 再次执行conda init来验证添加的情况
conda init
source ~/.bashrc # 刷新bash配置以使conda配置生效
```
- 退出当前终端，再次登录，输入`conda --version`查看版本，如依然不可以，则需要手动添加PATH
```bash
# 输入如下指令打开文档，并在文档编辑器中添加export PATH="$HOME/anaconda3/bin:$PATH"
nano ~/.bashrc
# 或者直接调用如下命令效果一样（注意，只能调用一次，否则会重复添加）
echo 'export PATH="'$HOME'/anaconda3/bin:'$PATH'"' >> ~/.bashrc
```
4. 验证安装：在终端输入`conda --version`来验证终端，如可以正常弹出版本号，则说明安装成功。
5. 安装卸载包`anaconda-clean`，后期如需卸载，比较方便，可以离线下载后安装；
```bash
# 在线安装命令
conda install -c anaconda anaconda-clean
# 离线安装命令，先准备好离线安装包
# 例如这里准备为anaconda-clean-1.1.1-py311h06a4308_0.tar.bz2
conda install anaconda-clean-1.1.1-py311h06a4308_0.tar.bz2
```
6. 可以通过如下命令来更新anaconda（在线）：
```bash
conda update --all
```
7. 如果是离线更新，则需重走一遍安装过程（如安装路径相同，则无需卸载）；

#### 方式2: 直接调用已写完的脚本
- 已写完专门针对linux环境的安装脚本`conda_offline_deploy_cmd.sh`，预先下载安装包及data-clean包，修改脚本内的参数；下载链接：[github地址](https://github.com/JamesHanZhang/linux-scripts-tools/tree/main/linux-env/python-dev-env)
- 保证离线安装包及脚本在同一个目录下，并修改脚本参数：
	- `X86_CONDA_PACKAGE`是`x86_64`暨AMD64的安装包名称；会自动识别；
	- `ARM64_CONDA_PACKAGE`是`aarch64`暨ARM64的安装包名称；会自动识别；
	- `CLEAN_PACKAGE`是`anaconda-clean`包的离线包名称；
- 根据`-h`命令查看如何使用该脚本：
```bash
bash conda_offline_deploy_cmd.sh -h
```
- 直接自动安装
```bash
sudo bash conda_offline_deploy_cmd.sh -i
```

### linux环境卸载anaconda
1. 首先确保已经安装了`anaconda-clean`包，可以通过如下命令进行查看：
```bash
conda list | grep anaconda-clean
```
2. 如果没有的话，需要安装该包:
```bash
# 在线安装命令
conda install -c anaconda anaconda-clean
```
3. 在终端执行命令: `anaconda-clean --yes`
4. 删除安装文件
```bash
# 更替$HOME/anaconda3为安装路径, 通常$HOME/anaconda3是默认路径
sudo rm -rf $HOME/anaconda3
```
5. 删除基本配置
```bash
sudo rm -rf ~/anaconda3
sudo rm -rf ~/opt/anaconda3
```
6. 至此，完成linux环境的anaconda的删除工作；也可以直接通过`conda_offline_deploy_cmd.sh`（[下载地址](https://github.com/JamesHanZhang/linux-scripts-tools/tree/main/linux-env/python-dev-env)）进行卸载；


## 搭建不同的conda-environment
除了`base`环境是通用的，各个conda environment是互相独立的。它有如下的优势：

1. **Isolation**：这意味着如果某个环境的包搭建环境，依赖关系出了问题，不影响其他的环境。这可以有效容错，防止因为某个包的安装导致整体conda environment崩溃的情。
2. **Dependency Management**: 不同项目有时候依赖的同一个包的版本不同，这也会影响到项目的质量。独立的依赖管理能有效保证项目不受版本影响。
3. **Sandboxing**: 沙盒模式保证特殊的环境变动不影响其他项目。
### 创建conda environment
```bash
# 明确python版本
python --version
# python要明确所需的版本号
conda create --name <conda_environment_name> python=python_version
# 案例
conda create --name james_env python=3.11.5
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
pip
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
5. 在**windows系统**以**管理员身份**打开**Anaconda Prompt**，在**Linux系统则直接打开终端**，输入`conda install`的命令行；
6. 完成后，输入`conda list`，查看，如果包名在列表内，证明安装成功；

#### Anaconda如何安装离线`conda library`
1. 登录[Anaconda官网离线包下载平台](https://anaconda.org/anaconda/repo)；
2. 注册并登录账户；
3. 在Anaconda.org的检索栏输入希望下载的library，检索到对应library，下载最新版；
4. 安装包文件通常以`.tar.bz2`拓展名结尾，也有其他的情况，拓展名本身并不十分重要；
5. 下载所需安装包到自设路径；
6. 在**windows系统**以**管理员身份**打开**Anaconda Prompt**，在**Linux系统则直接打开终端**：`cd`到对应路径；
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
2. 在**windows系统**以**管理员身份**打开**Anaconda Prompt**，在**Linux系统则直接打开终端**：
```bash
conda uninstall <package name>
```
3. 完成后在命令行输入`conda list`，如果没有该包，证明卸载成功；

### 方式2：通过`pip`命令安装
即通过常规的pip命令进行安装，因非conda官方环境，有一定可能造成环境崩溃。但是好处是能更新到最新的外库，部分library的官网更新是较慢的，可能无法满足构建服务的需要。此时推荐使用独立的`conda environment`来安装环境，以保证整体`base`环境不会崩溃。

请参考后面的纯python环境安装包的部分：[离线安装包library](#离线安装包library)
注意在windows系统需要以**管理员身份**打开**Anaconda Prompt**进行相关命令行的输入。

## 直接安装纯python
### windows环境安装python
  
在 Windows 上直接安装 Python 通常是一个简单的过程。以下是一些步骤：

1. **下载 Python 安装程序：** 访问 [Python 官方网站](https://www.python.org/downloads/)，在首页中找到最新的稳定版本，并点击 "Downloads" 下载按钮。选择适用于 Windows 的安装程序。
2. **运行安装程序：** 下载完成后，双击下载的安装程序（通常是一个 `.exe` 文件），然后按照安装向导的提示进行操作。
    - 在安装向导的第一个页面，确保勾选 "Add Python 3.x to PATH" 选项，这样你就可以在命令提示符中直接运行 Python。
    - 点击 "Install Now" 开始安装。
3. **等待安装完成：** 安装程序将会下载并安装 Python 到你选择的目录（默认为 `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3x`）。等待安装过程完成。
4. **验证安装：** 打开命令提示符（Command Prompt）或 PowerShell，输入命令来验证 Python 是否成功安装：`python --version`
	- 或者，如果你安装的是 Python 3：`python3 --version`
	- 如果一切正常，你应该看到已安装 Python 的版本号。
5. **运行 Python 解释器：** 输入命令来启动 Python 解释器：`python`
	- 或者，如果你安装的是 Python 3：`python3`
	- 这会进入 Python 解释器的交互模式，表示你已成功安装 Python。

### Linux环境Ubuntu在线安装python
1. 更新软件包列表：`sudo apt update`
2. 安装 Python：`sudo apt install python3`

### Linux环境Ubuntu离线安装python
1. **在有互联网连接的 Ubuntu 系统上下载 Python 安装包及其依赖项：**
```bash
sudo apt update
sudo apt download python3

# 下载 Python 3.11.5 版本的核心库
sudo apt-get download libpython3.11-stdlib

# 下载 Python 3.11.5 版本的开发库
sudo apt-get download libpython3.11-dev

# 下载 Python 3.11.5 版本的命令行工具
sudo apt-get download python3.11
```
上述命令会下载 Python 的安装包以及一些基本的开发库。你可以将这些下载的 `.deb` 文件复制到目标系统。
2. **在目标系统上安装 Python：**
```bash
# 安装python 3.11.5
sudo dpkg -i libpython3.11-stdlib*.deb
sudo dpkg -i libpython3.11-dev*.deb
sudo dpkg -i python3.11*.deb
```
如果有任何缺失的依赖项，你可能需要使用相似的方式手动下载并安装它们。
3. **验证 Python 安装：**
打开终端并运行命令来验证 Python 是否成功安装：`python3 --version`

## 搭建不同的纯python虚拟环境(非anaconda环境)
### `venv`方法
#### 1. 显示所有虚拟环境
- windows显示所有虚拟环境
```bash
# 如为非默认路径
dir \path\to\virtual\environments
# 如为默认路径
dir %USERPROFILE%\Envs
```
- 在 Linux 或 macOS 中显示所有虚拟环境
```bash
# 如为非默认路径
ls -l /path/to/virtual/environments
# 如为默认路径
ls -l ~/.virtualenvs
```
#### 2. 创建虚拟环境
1. **打开终端，并移动到你希望创建虚拟环境的目录**。可以选择默认路径
- windows默认路径:
```bash
# 显示默认路径, 例如这里为C:\Users\james\Envs
echo %USERPROFILE%\Envs
# 移动到默认路径，如尚未建立则需创建该默认路径
cd C:\Users\james\Envs
```
- 在 Linux 或 macOS 中默认路径:
```bash
# 移动到默认路径
cd ~/.virtualenvs
```

2. **运行以下命令创建虚拟环境**：
```bash
# james_env是自己设定的虚拟环境名称
python3 -m venv james_env
```
- 或者，如果你使用的是 Python 2：
```bash
# james_env是自己设定的虚拟环境名称
python -m venv james_env
```
这将在当前目录下创建一个名为 `myenv` 的虚拟环境。

#### 3. 激活虚拟环境
- **在 Linux 或 macOS 中**：
```bash
# cd到james_env的路径，以下为默认路径示例
cd ~/.virtualenvs
# 激活环境
source james_env/bin/activate
```
- **在windows中**：
```bash
# 显示默认路径, 例如这里为C:\Users\james\Envs
echo %USERPROFILE%\Envs
# cd到james_env的路径
cd C:\Users\james\Envs
# 激活james_env的环境
.\james_env\Scripts\activate
```
你的终端提示符前面应该出现虚拟环境的名称，表示你已经进入了该虚拟环境。

可以在虚拟环境中安装依赖项，例如：
```bash
pip install package_name
```

#### 4. 退出虚拟环境
当你完成工作时，可以通过运行以下命令来**退出虚拟环境**：
```bash
deactivate
```

无论你选择使用 `venv` 还是 `virtualenv`，都可以创建独立的 Python 环境，使你能够在不同的项目中管理不同的依赖项和版本。

#### 5. 删除虚拟环境
- **windows删除虚拟环境**
```bash
# 特定路径删除虚拟环境james_env
rmdir /s /q \path\to\virtual\environments\james_env

# 默认路径删除虚拟环境james_env
# 显示默认路径, 例如这里为C:\Users\james\Envs
echo %USERPROFILE%\Envs
## 默认路径删除虚拟环境james_env
rmdir /s /q C:\Users\james\Envs\james_env
```
- 在 Linux 或 macOS 中删除虚拟环境
```bash
# 特定路径删除虚拟环境james_env
rm -rf /path/to/virtual/environments/james_env
# 默认路径删除虚拟环境
rm -rf ~/.virtualenvs/james_env
```
### `virtualenv`方法（略）


## 纯python环境安装包Library
### 在线直接安装包library-使用`pip`命令
```bash
# 直接使用命令即可，将package-name替换成你想安装的包
pip install package-name
```

### 离线安装包library
#### 通过`pip`在线安装库`library`

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
### windows安装IDE
#### PyCharm的安装及环境配置
1. 登录PyCharm官网安装社区办IDE: [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows);
2. 下载并按照默认安装；
3. 打开`setting`设置，找到`Python Interpreter`，选择`add interpreter`，选择`Add Local Interpreter`；
4. 找到`Conda Environment`，选择`use existing environment`，在路径上选择Anaconda的默认路径/或者选择对应的`conda environment`，例如`C:\ProgramData\anaconda3`或者`james_conda_environment`这样的独立环境；
5. 在`Conda Executable`环境选择：`C:\ProgramData\Anaconda3\condabin\conda.bat`，个人依据安装环境不同进行更改；选择确定OK；
6. 完成环境配置；
#### Spyder
1. Anaconda附带编译器；
2. 点击`Anaconda Prompt`，输入`spyder`，回车，即可打开编译器；

#### Jupyter Notebook
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
# 如何在jupyter notebook上使用模块

import sys
import os
# 将项目路径添加到环境变量
path = os.path.dirname(sys.path[0])
sys.path.append(path)

# 添加以上前缀即可
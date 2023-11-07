#! /bin/bash

# 只有通过外部路径的执行, 才可以保证该脚本不被自动打包仅exe内, 可以作为依赖文件放置在外面
# 因为tabulate在打包环境无法被打包，所以手动标注打包 --hidden-import=tabulate
pyinstaller --name=table-data-format-transform-app --onefile --hidden-import=tabulate --icon=rabbit_exe_icon1.ico table_data_format_transform_app.py